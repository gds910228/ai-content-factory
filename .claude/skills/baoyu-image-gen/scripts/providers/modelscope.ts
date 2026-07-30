import type { CliArgs } from "../types";

const DEFAULT_MODEL = "Tongyi-MAI/Z-Image-Turbo";
const POLL_MAX_ATTEMPTS = 60;
const POLL_INTERVAL_MS = 5000;
const TIMEOUT_MS = 300_000;

export function getDefaultModel(): string {
  return process.env.MODELSCOPE_IMAGE_MODEL || DEFAULT_MODEL;
}

function getApiKey(): string | null {
  return process.env.MODELSCOPE_API_KEY || process.env.DASHSCOPE_API_KEY || null;
}

function getBaseUrl(): string {
  return (
    process.env.MODELSCOPE_BASE_URL || "https://api-inference.modelscope.cn/"
  ).replace(/\/+$/, "");
}

type AspectRatio = [number, number];

const ASPECT_RATIOS: Record<string, AspectRatio> = {
  "1:1": [1024, 1024],
  "16:9": [1344, 768],
  "9:16": [768, 1344],
  "4:3": [1152, 864],
  "3:4": [864, 1152],
  "3:2": [1216, 832],
  "2:3": [832, 1216],
  "21:9": [1536, 640],
};

function resolveSize(args: CliArgs): string | null {
  if (args.size) return args.size;
  if (!args.aspectRatio) return null;
  const ratio = ASPECT_RATIOS[args.aspectRatio];
  if (ratio) return `${ratio[0]}x${ratio[1]}`;
  const parts = args.aspectRatio.split(":");
  if (parts.length === 2) {
    const w = parseFloat(parts[0]!);
    const h = parseFloat(parts[1]!);
    if (w > 0 && h > 0) {
      const base = 1024;
      const scale = base / Math.sqrt(w * h);
      return `${Math.round(w * scale)}x${Math.round(h * scale)}`;
    }
  }
  return null;
}

async function submitTask(
  prompt: string,
  model: string,
  size: string | null,
  apiKey: string,
  baseUrl: string
): Promise<string> {
  const bodyObj: Record<string, unknown> = {
    model,
    prompt,
  };
  if (size) {
    bodyObj.size = size;
  }

  const res = await fetch(`${baseUrl}/v1/images/generations`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      "X-ModelScope-Async-Mode": "true",
    },
    body: JSON.stringify(bodyObj),
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`ModelScope API error (${res.status}): ${errText}`);
  }

  const data = (await res.json()) as { task_id?: string };
  if (!data.task_id) {
    throw new Error(`ModelScope API returned no task_id: ${JSON.stringify(data)}`);
  }
  return data.task_id;
}

async function pollForResult(
  taskId: string,
  apiKey: string,
  baseUrl: string
): Promise<Uint8Array> {
  const startTime = Date.now();

  for (let attempt = 0; attempt < POLL_MAX_ATTEMPTS; attempt++) {
    if (Date.now() - startTime > TIMEOUT_MS) {
      throw new Error(`ModelScope image generation timeout after ${TIMEOUT_MS / 1000} seconds`);
    }

    const res = await fetch(`${baseUrl}/v1/tasks/${taskId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "X-ModelScope-Task-Type": "image_generation",
      },
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`ModelScope poll error (${res.status}): ${errText}`);
    }

    const data = (await res.json()) as {
      task_status?: string;
      output_images?: string[];
      results?: { url?: string }[];
      error?: string;
    };

    const status = data.task_status;
    console.error(`ModelScope task ${taskId}: ${status} (${attempt + 1}/${POLL_MAX_ATTEMPTS})`);

    if (status === "SUCCEED") {
      let imageUrl: string | undefined;

      if (data.output_images && data.output_images.length > 0) {
        imageUrl = data.output_images[0];
      } else if (data.results && data.results.length > 0 && data.results[0]?.url) {
        imageUrl = data.results[0].url;
      }

      if (!imageUrl) {
        throw new Error(`ModelScope task succeeded but no image URL found: ${JSON.stringify(data)}`);
      }

      console.error(`Downloading image from ModelScope: ${imageUrl}`);
      const imgRes = await fetch(imageUrl);
      if (!imgRes.ok) {
        throw new Error(`Failed to download image from ${imageUrl}: ${imgRes.status}`);
      }
      const buffer = await imgRes.arrayBuffer();
      return new Uint8Array(buffer);
    }

    if (status === "FAILED") {
      throw new Error(`ModelScope task failed: ${data.error || "Unknown error"}`);
    }

    // Still pending (PENDING, RUNNING, QUEUED, etc.) — wait and retry
    await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));
  }

  throw new Error(`ModelScope polling exhausted after ${POLL_MAX_ATTEMPTS} attempts`);
}

export async function generateImage(
  prompt: string,
  model: string,
  args: CliArgs
): Promise<Uint8Array> {
  const apiKey = getApiKey();
  if (!apiKey) {
    throw new Error("MODELSCOPE_API_KEY is required (falls back to DASHSCOPE_API_KEY)");
  }

  const baseUrl = getBaseUrl();
  const size = resolveSize(args);

  console.error(`ModelScope: submitting task (model=${model}, size=${size || "default"})`);
  const taskId = await submitTask(prompt, model, size, apiKey, baseUrl);
  console.error(`ModelScope: task submitted, id=${taskId}`);

  return await pollForResult(taskId, apiKey, baseUrl);
}
