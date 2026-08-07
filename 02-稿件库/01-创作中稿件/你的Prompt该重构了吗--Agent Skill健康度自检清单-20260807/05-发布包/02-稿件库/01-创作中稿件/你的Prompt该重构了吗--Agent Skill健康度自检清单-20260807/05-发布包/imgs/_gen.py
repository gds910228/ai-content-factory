#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ModelScope text-to-image generation wrapper (OpenAI-compatible endpoint).

Why this exists: a previous session blew up with HTTP 400 because the LLM was
made to emit ~4MB of base64 inline, exhausting the output-token budget. The fix
is structural: the LLM only writes prompt files + <img>/markdown links; this
local script owns the API call, the base64/url handling, and the file write.

Usage:
    python _gen.py --prompt-file prompts/01-...md --out imgs/01-...png \
                   --model wanx2.1-t2i-plus --size 1280*720

The prompt file may start with a YAML frontmatter block (--- ... ---); it is
stripped and the remaining body is sent verbatim as the prompt. The script
prints ONE compact JSON line to stdout: {"ok": true, "path": "...", ...}.
It NEVER prints image bytes or base64.
"""
import argparse
import base64
import json
import os
import sys
import time
import re

import requests

API_BASE = "https://api-inference.modelscope.cn/v1"
API_KEY = os.environ.get("MODELSCOPE_API_KEY", "").strip()
TIMEOUT = 180  # per HTTP call
POLL_INTERVAL = 3  # seconds between async task polls
POLL_MAX = 120  # max polls (~6 min)


def die(msg, **extra):
    print(json.dumps({"ok": False, "error": msg, **extra}, ensure_ascii=False))
    sys.exit(1)


def strip_frontmatter(text):
    """Remove a leading YAML frontmatter block (--- ... ---) if present."""
    if text.lstrip().startswith("---"):
        m = re.match(r"^\s*---\s*\n.*?\n---\s*\n", text, re.DOTALL)
        if m:
            return text[m.end():]
    return text


def read_prompt(prompt_file, prompt_inline):
    if prompt_inline:
        return prompt_inline.strip()
    if not prompt_file or not os.path.isfile(prompt_file):
        die("prompt file not found", path=prompt_file)
    with open(prompt_file, "r", encoding="utf-8") as f:
        raw = f.read()
    body = strip_frontmatter(raw).strip()
    if not body:
        die("prompt body is empty after stripping frontmatter", path=prompt_file)
    return body


def headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def submit_generation(prompt, model, size, n):
    """POST to /images/generations. Returns parsed JSON (sync result or task)."""
    body = {
        "model": model,
        "prompt": prompt,
        "n": n,
        "size": size,
        "response_format": "url",
    }
    try:
        r = requests.post(
            f"{API_BASE}/images/generations",
            headers=headers(),
            data=json.dumps(body).encode("utf-8"),
            timeout=TIMEOUT,
        )
    except requests.RequestException as e:
        die(f"network error on submit: {e}")
    if r.status_code != 200:
        die(
            f"submit HTTP {r.status_code}",
            body=r.text[:1000],
        )
    try:
        return r.json()
    except ValueError:
        die("submit response not JSON", body=r.text[:1000])


def extract_task_id(resp):
    """Detect an async task handle in various ModelScope response shapes."""
    if not isinstance(resp, dict):
        return None
    # OpenAI-compatible async wrappers sometimes nest under output
    for key in ("task_id", "taskId"):
        if resp.get(key):
            return resp[key]
    out = resp.get("output") or {}
    if isinstance(out, dict):
        for key in ("task_id", "taskId"):
            if out.get(key):
                return out[key]
    return None


def poll_task(task_id):
    url = f"{API_BASE}/tasks/{task_id}"
    for _ in range(POLL_MAX):
        try:
            r = requests.get(url, headers=headers(), timeout=TIMEOUT)
        except requests.RequestException as e:
            die(f"network error polling task: {e}")
        if r.status_code != 200:
            die(f"poll HTTP {r.status_code}", body=r.text[:1000])
        try:
            data = r.json()
        except ValueError:
            die("poll response not JSON", body=r.text[:1000])
        status = (
            data.get("status")
            or (data.get("output") or {}).get("task_status")
            or ""
        )
        status = str(status).upper()
        if status in ("SUCCEEDED", "SUCCESS"):
            return data
        if status in ("FAILED", "ERROR", "UNKNOWN"):
            die(f"task {status}", response=str(data)[:1000])
        time.sleep(POLL_INTERVAL)
    die("task timed out", task_id=task_id)


def collect_image_urls(resp):
    """Pull image url(s) or b64 from a sync response or completed task."""
    urls = []
    if not isinstance(resp, dict):
        return urls
    # OpenAI shape: data: [{"url": ...}] or [{"b64_json": ...}]
    data = resp.get("data")
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            if item.get("url"):
                urls.append(("url", item["url"]))
            elif item.get("b64_json"):
                urls.append(("b64", item["b64_json"]))
    # DashScope shape: output.results: [{"url": ...}]
    out = resp.get("output") or {}
    if isinstance(out, dict):
        results = out.get("results")
        if isinstance(results, list):
            for item in results:
                if isinstance(item, dict) and item.get("url"):
                    urls.append(("url", item["url"]))
    return urls


def save_image(kind, payload, out_path):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    if kind == "url":
        try:
            r = requests.get(payload, timeout=TIMEOUT)
        except requests.RequestException as e:
            die(f"image download failed: {e}")
        if r.status_code != 200:
            die(f"image download HTTP {r.status_code}")
        with open(out_path, "wb") as f:
            f.write(r.content)
        return len(r.content)
    elif kind == "b64":
        raw = base64.b64decode(payload)
        with open(out_path, "wb") as f:
            f.write(raw)
        return len(raw)
    die(f"unknown image kind: {kind}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file")
    ap.add_argument("--prompt")
    ap.add_argument("--model", default="wanx2.1-t2i-plus")
    ap.add_argument("--size", default="1024*1024")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--out", required=True)
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()

    if not API_KEY:
        die("MODELSCOPE_API_KEY env var not set")

    prompt = read_prompt(args.prompt_file, args.prompt)
    if args.debug:
        print(
            json.dumps(
                {"_debug": "prompt", "len": len(prompt), "head": prompt[:200]},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )

    resp = submit_generation(prompt, args.model, args.size, args.n)
    if args.debug:
        print(
            json.dumps({"_debug": "submit_resp", "keys": list(resp.keys())}, ensure_ascii=False),
            file=sys.stderr,
        )

    task_id = extract_task_id(resp)
    if task_id and not collect_image_urls(resp):
        if args.debug:
            print(json.dumps({"_debug": "async", "task_id": task_id}, ensure_ascii=False), file=sys.stderr)
        resp = poll_task(task_id)

    urls = collect_image_urls(resp)
    if not urls:
        die("no image url/b64 in response", response=str(resp)[:1000])

    saved = []
    for i, (kind, payload) in enumerate(urls):
        path = args.out
        if len(urls) > 1:
            base, ext = os.path.splitext(args.out)
            path = f"{base}_{i}{ext or '.png'}"
        size = save_image(kind, payload, path)
        saved.append({"path": path, "bytes": size})

    print(
        json.dumps(
            {
                "ok": True,
                "model": args.model,
                "size": args.size,
                "images": saved,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
