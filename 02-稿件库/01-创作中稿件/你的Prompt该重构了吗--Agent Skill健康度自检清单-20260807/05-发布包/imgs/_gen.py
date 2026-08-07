#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ModelScope text-to-image generation wrapper.

Why this exists: a previous session blew up with HTTP 400 because the LLM was
made to emit ~4MB of base64 inline, exhausting the output-token budget. The fix
is structural - the LLM only writes prompt files + markdown links; this local
script owns the API call, the url/base64 handling, and the file write. The LLM
never sees image bytes.

Backend: ModelScope API-Inference, OpenAI-compatible image endpoint.
  POST https://api-inference.modelscope.cn/v1/images/generations
  Auth: Bearer $MODELSCOPE_API_KEY
  Model: Qwen/Qwen-Image (flagship T2I; strong prompt adherence, bilingual)
  size format: "WxH" (lowercase x), e.g. "1280x720", "960x1280", "1024x1024"
  Async submit -> task_id -> poll /v1/tasks/{id} until SUCCEED -> output_images[]

Usage:
    python _gen.py --prompt-file prompts/01-...md --out imgs/01-...png \
                   --model Qwen/Qwen-Image --size 1280x720

The prompt file may start with a YAML frontmatter block (--- ... ---); it is
stripped and the remaining body is sent verbatim as the prompt. Prints ONE
compact JSON line to stdout: {"ok": true, "images": [{"path","bytes"}]}.
Status/progress goes to stderr. NEVER prints image bytes or base64.
"""
import argparse
import json
import os
import sys
import time
import random
import re

import requests

API_BASE = "https://api-inference.modelscope.cn/v1"
API_KEY = os.environ.get("MODELSCOPE_API_KEY", "").strip()
TIMEOUT = 180
POLL_INTERVAL = 4
POLL_MAX = 150  # ~10 min ceiling


def say(msg):
    print(msg, file=sys.stderr, flush=True)


def die(msg, **extra):
    print(json.dumps({"ok": False, "error": msg, **extra}, ensure_ascii=False))
    sys.exit(1)


def strip_frontmatter(text):
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
        die("prompt body empty after frontmatter", path=prompt_file)
    return body


def auth_headers():
    return {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def submit(prompt, model, size, steps, guidance, negative, seed):
    payload = {"model": model, "prompt": prompt, "size": size}
    if steps is not None:
        payload["steps"] = steps
    if guidance is not None:
        payload["guidance"] = guidance
    if negative:
        payload["negative_prompt"] = negative
    payload["seed"] = seed if seed is not None else random.randint(0, 2**31 - 1)

    headers = auth_headers()
    headers["X-ModelScope-Async-Mode"] = "true"
    headers["X-ModelScope-Task-Type"] = "text-to-image-generation"

    say(f"submit model={model} size={size} seed={payload['seed']}")
    try:
        r = requests.post(
            f"{API_BASE}/images/generations",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            timeout=TIMEOUT,
        )
    except requests.RequestException as e:
        die(f"network error on submit: {e}")

    if r.status_code == 400:
        say("400 with full params; retrying minimal payload {model, prompt, size}")
        minimal = {"model": model, "prompt": prompt, "size": size}
        try:
            r = requests.post(
                f"{API_BASE}/images/generations",
                data=json.dumps(minimal, ensure_ascii=False).encode("utf-8"),
                headers=headers,
                timeout=TIMEOUT,
            )
        except requests.RequestException as e:
            die(f"network error on minimal submit: {e}")

    if r.status_code != 200:
        die(f"submit HTTP {r.status_code}", body=r.text[:1200])
    try:
        return r.json()
    except ValueError:
        die("submit response not JSON", body=r.text[:1200])


def poll(task_id):
    url = f"{API_BASE}/tasks/{task_id}"
    headers = auth_headers()
    headers["X-ModelScope-Task-Type"] = "image_generation"
    for i in range(POLL_MAX):
        try:
            r = requests.get(url, headers=headers, timeout=TIMEOUT)
        except requests.RequestException as e:
            die(f"network error polling: {e}")
        if r.status_code != 200:
            die(f"poll HTTP {r.status_code}", body=r.text[:1200])
        try:
            data = r.json()
        except ValueError:
            die("poll response not JSON", body=r.text[:1200])
        status = str(data.get("task_status") or data.get("status") or "").upper()
        if i % 3 == 0 or status in ("SUCCEED", "SUCCEEDED", "FAILED", "ERROR"):
            say(f"poll [{i}] status={status or '?'}")
        if status in ("SUCCEED", "SUCCEEDED"):
            return data
        if status in ("FAILED", "ERROR", "UNKNOWN"):
            die(f"task {status}", response=str(data)[:1200])
        time.sleep(POLL_INTERVAL)
    die("task timed out", task_id=task_id)


def collect_urls(resp):
    """Pull image url(s) from sync or completed-async responses."""
    urls = []
    if not isinstance(resp, dict):
        return urls
    imgs = resp.get("images")
    if isinstance(imgs, list):
        for it in imgs:
            if isinstance(it, dict) and it.get("url"):
                urls.append(it["url"])
            elif isinstance(it, str):
                urls.append(it)
    data = resp.get("data")
    if isinstance(data, list):
        for it in data:
            if isinstance(it, dict):
                if it.get("url"):
                    urls.append(it["url"])
                elif it.get("b64_json"):
                    urls.append(("b64", it["b64_json"]))
    out = resp.get("output") or {}
    if isinstance(out, dict):
        oi = out.get("output_images") or out.get("results")
        if isinstance(oi, list):
            for it in oi:
                if isinstance(it, str):
                    urls.append(it)
                elif isinstance(it, dict) and it.get("url"):
                    urls.append(it["url"])
    return urls


def download(url, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    r = requests.get(url, timeout=TIMEOUT)
    if r.status_code != 200:
        die(f"download HTTP {r.status_code}")
    with open(path, "wb") as f:
        f.write(r.content)
    return len(r.content)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file")
    ap.add_argument("--prompt")
    ap.add_argument("--model", default="Qwen/Qwen-Image")
    ap.add_argument("--size", default="1328x1328")
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--guidance", type=float, default=None)
    ap.add_argument("--negative", default="")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    if not API_KEY:
        die("MODELSCOPE_API_KEY env var not set")

    prompt = read_prompt(args.prompt_file, args.prompt)
    resp = submit(prompt, args.model, args.size, args.steps, args.guidance, args.negative, args.seed)

    task_id = resp.get("task_id") if isinstance(resp, dict) else None
    if task_id and not collect_urls(resp):
        say(f"async task_id={task_id}, polling...")
        resp = poll(task_id)

    urls = collect_urls(resp)
    # b64 tuples leak in via collect_urls; filter
    clean = [u for u in urls if isinstance(u, str)]
    if not clean:
        die("no image url in response", response=str(resp)[:1200])

    saved = []
    for i, url in enumerate(clean):
        path = args.out
        if len(clean) > 1:
            base, ext = os.path.splitext(args.out)
            path = f"{base}_{i}{ext or '.png'}"
        n = download(url, path)
        saved.append({"path": path, "bytes": n})
        say(f"saved {path} ({n} bytes)")

    print(json.dumps({"ok": True, "model": args.model, "size": args.size, "images": saved}, ensure_ascii=False))


if __name__ == "__main__":
    main()
