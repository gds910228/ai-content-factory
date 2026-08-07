#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ModelScope text-to-image batch generation wrapper.

WHY THIS EXISTS
---------------
A previous session blew up with HTTP 400 because the LLM was made to emit ~4MB
of base64 inline, exhausting the output-token budget. The fix is structural:
the LLM only writes prompt files + markdown links; THIS local script owns the
API call, the url/base64 handling, and the file write. The LLM never sees image
bytes or base64.

ENCODING NOTE (Windows + git-bash)
----------------------------------
Passing Chinese paths through bash argv mangles them before Python sees them
(os.path.isfile returns False on a path that looks correct). So this script is
invoked with a Chinese-free --jobs path; all Chinese paths live INSIDE the jobs
JSON, which Python decodes as proper UTF-8 and feeds to the Windows wide file
API. That round-trip is correct.

BACKEND
-------
ModelScope API-Inference (OpenAI-compatible image endpoint):
  POST https://api-inference.modelscope.cn/v1/images/generations
  Auth: Bearer $MODELSCOPE_API_KEY
  Model: Qwen/Qwen-Image
  size: "WxH" (lowercase x), e.g. "1280x720", "960x1280", "1328x1328"
  Async submit (X-ModelScope-Async-Mode: true) -> task_id
  -> poll GET /v1/tasks/{task_id} until task_status == SUCCEED
  -> output_images[] (list of URLs) -> download -> PIL save as PNG

JOBS FILE FORMAT (JSON)
-----------------------
A single object {"workers": 4, "jobs": [ ... ]}  OR a bare list [ ... ].
Each job:
  {
    "id": "01",
    "prompt_file": "D:/.../imgs/prompts/01-...md",   # absolute, Chinese OK
    "out":        "D:/.../imgs/01-...png",            # absolute, Chinese OK
    "model":      "Qwen/Qwen-Image",                  # optional
    "size":       "1280x720",                         # optional
    "steps":      30,                                  # optional
    "guidance":   4.0,                                 # optional
    "negative":   "...",                               # optional
    "seed":       12345,                               # optional
    "retry":      1                                    # optional, default 1
  }
prompt_file may start with a YAML frontmatter block; it is stripped and the
remaining body is sent verbatim as the prompt.

OUTPUT
------
Prints ONE JSON line to stdout summarizing every job:
  {"ok": true, "workers": 4, "results": [{"id","ok","path","bytes","error"}]}
Progress goes to stderr. NEVER prints image bytes or base64.
"""
import argparse
import json
import os
import sys
import time
import random
import re
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from PIL import Image
from io import BytesIO

API_BASE = "https://api-inference.modelscope.cn/v1"
API_KEY = os.environ.get("MODELSCOPE_API_KEY", "").strip()
TIMEOUT = 180
POLL_INTERVAL = 4
POLL_MAX = 150


def say(msg):
    print(msg, file=sys.stderr, flush=True)


def strip_frontmatter(text):
    if text.lstrip().startswith("---"):
        m = re.match(r"^\s*---\s*\n.*?\n---\s*\n", text, re.DOTALL)
        if m:
            return text[m.end():]
    return text


def read_prompt(prompt_file):
    if not prompt_file or not os.path.isfile(prompt_file):
        raise RuntimeError(f"prompt file not found: {prompt_file}")
    with open(prompt_file, "r", encoding="utf-8") as f:
        raw = f.read()
    body = strip_frontmatter(raw).strip()
    if not body:
        raise RuntimeError(f"prompt body empty: {prompt_file}")
    return body


def auth_headers():
    return {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def submit(prompt, model, size, steps, guidance, negative, seed):
    payload = {"model": model, "prompt": prompt, "size": size, "seed": seed}
    if steps is not None:
        payload["steps"] = steps
    if guidance is not None:
        payload["guidance"] = guidance
    if negative:
        payload["negative_prompt"] = negative

    headers = auth_headers()
    headers["X-ModelScope-Async-Mode"] = "true"
    headers["X-ModelScope-Task-Type"] = "text-to-image-generation"

    r = requests.post(
        f"{API_BASE}/images/generations",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        timeout=TIMEOUT,
    )
    if r.status_code == 400:
        # retry with minimal payload (some params rejected by certain models)
        minimal = {"model": model, "prompt": prompt, "size": size, "seed": seed}
        r = requests.post(
            f"{API_BASE}/images/generations",
            data=json.dumps(minimal, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            timeout=TIMEOUT,
        )
    if r.status_code != 200:
        raise RuntimeError(f"submit HTTP {r.status_code}: {r.text[:600]}")
    return r.json()


def poll(task_id):
    url = f"{API_BASE}/tasks/{task_id}"
    headers = auth_headers()
    headers["X-ModelScope-Task-Type"] = "image_generation"
    for i in range(POLL_MAX):
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        if r.status_code != 200:
            raise RuntimeError(f"poll HTTP {r.status_code}: {r.text[:600]}")
        data = r.json()
        status = str(data.get("task_status") or data.get("status") or "").upper()
        if status in ("SUCCEED", "SUCCEEDED"):
            return data
        if status in ("FAILED", "ERROR", "UNKNOWN"):
            raise RuntimeError(f"task {status}: {str(data)[:600]}")
        time.sleep(POLL_INTERVAL)
    raise RuntimeError(f"task timed out: {task_id}")


def collect_urls(resp):
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
            if isinstance(it, dict) and it.get("url"):
                urls.append(it["url"])
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


def save_as_png(url, out_path):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    r = requests.get(url, timeout=TIMEOUT)
    if r.status_code != 200:
        raise RuntimeError(f"download HTTP {r.status_code}")
    img = Image.open(BytesIO(r.content))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    elif img.mode != "RGB":
        img = img.convert("RGB")
    img.save(out_path, "PNG")
    return os.path.getsize(out_path)


def run_job(job):
    jid = job.get("id", "?")
    prompt_file = job.get("prompt_file")
    out = job.get("out")
    model = job.get("model", "Qwen/Qwen-Image")
    size = job.get("size", "1328x1328")
    steps = job.get("steps")
    guidance = job.get("guidance")
    negative = job.get("negative", "")
    seed = job.get("seed")
    retries = int(job.get("retry", 1))

    if not out:
        return {"id": jid, "ok": False, "error": "missing out"}

    last_err = None
    for attempt in range(retries + 1):
        try:
            if seed is None:
                use_seed = random.randint(0, 2**31 - 1)
            else:
                use_seed = seed
            prompt = read_prompt(prompt_file) if prompt_file else job.get("prompt", "")
            if not prompt:
                raise RuntimeError("no prompt (need prompt_file or prompt)")
            resp = submit(prompt, model, size, steps, guidance, negative, use_seed)
            task_id = resp.get("task_id") if isinstance(resp, dict) else None
            if task_id and not collect_urls(resp):
                resp = poll(task_id)
            urls = collect_urls(resp)
            if not urls:
                raise RuntimeError(f"no image url: {str(resp)[:400]}")
            n = save_as_png(urls[0], out)
            say(f"[{jid}] OK -> {out} ({n} bytes) attempt={attempt}")
            return {"id": jid, "ok": True, "path": out, "bytes": n, "seed": use_seed}
        except Exception as e:
            last_err = str(e)
            say(f"[{jid}] attempt={attempt} FAIL: {last_err}")
            if attempt < retries:
                time.sleep(3)
    return {"id": jid, "ok": False, "error": last_err}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", required=True, help="path to jobs JSON (Chinese-free path)")
    ap.add_argument("--workers", type=int, default=None)
    args = ap.parse_args()

    if not API_KEY:
        print(json.dumps({"ok": False, "error": "MODELSCOPE_API_KEY env var not set"}))
        sys.exit(1)

    with open(args.jobs, "r", encoding="utf-8") as f:
        spec = json.load(f)
    if isinstance(spec, list):
        jobs = spec
        workers = args.workers or 4
    else:
        jobs = spec.get("jobs", [])
        workers = args.workers or spec.get("workers", 4)

    say(f"running {len(jobs)} jobs with {workers} workers")
    results = [None] * len(jobs)

    def _index_run(idx):
        return idx, run_job(jobs[idx])

    with ThreadPoolExecutor(max_workers=min(workers, max(1, len(jobs)))) as ex:
        futs = {ex.submit(_index_run, i): i for i in range(len(jobs))}
        for fut in as_completed(futs):
            idx, res = fut.result()
            results[idx] = res

    ok = sum(1 for r in results if r and r.get("ok"))
    say(f"done: {ok}/{len(jobs)} succeeded")
    print(json.dumps({"ok": ok == len(jobs), "workers": workers, "results": results}, ensure_ascii=False))


if __name__ == "__main__":
    main()
