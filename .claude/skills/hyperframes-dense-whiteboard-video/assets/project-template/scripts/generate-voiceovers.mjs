import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, unlinkSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { tmpdir } from "node:os";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const storyboard = JSON.parse(readFileSync(join(projectRoot, "storyboard.json"), "utf8"));
const args = process.argv.slice(2);
const force = args.includes("--force");
const valueAfter = (flag, fallback) => {
  const index = args.indexOf(flag);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
};
const voice = valueAfter("--voice", storyboard.narration?.voice || "Tingting");
const rate = Number(valueAfter("--rate", storyboard.narration?.rate || 241));

if (storyboard.narration?.provider !== "macos-say") {
  throw new Error("The current pipeline supports narration.provider=macos-say. Add another provider explicitly before using it.");
}
if (!Number.isFinite(rate) || rate <= 0) throw new Error("Narration rate must be a positive number");

const audioDir = join(projectRoot, "assets", "audio");
mkdirSync(audioDir, { recursive: true });
const tempDir = mkdtempSync(join(tmpdir(), "article-whiteboard-tts-"));
const cachePath = join(audioDir, ".voice-cache.json");
const previousCache = existsSync(cachePath)
  ? JSON.parse(readFileSync(cachePath, "utf8"))
  : { version: 1, scenes: {} };
const nextCache = { version: 1, scenes: {} };

const voiceSignature = (scene) => createHash("sha256").update(JSON.stringify({
  provider: storyboard.narration.provider,
  voice,
  rate,
  text: scene.narration,
})).digest("hex");

const run = (command, commandArgs) => {
  const result = spawnSync(command, commandArgs, { cwd: projectRoot, stdio: "inherit" });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(`${command} exited with status ${result.status}`);
};

const probeDuration = (path) => {
  const result = spawnSync("ffprobe", [
    "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    path,
  ], { encoding: "utf8" });
  if (result.status !== 0) return null;
  const duration = Number.parseFloat(result.stdout.trim());
  return Number.isFinite(duration) && duration > 0 ? duration : null;
};

try {
  for (const scene of storyboard.scenes) {
    const output = join(audioDir, `${scene.id}.wav`);
    const signature = voiceSignature(scene);
    nextCache.scenes[scene.id] = signature;
    if (existsSync(output) && previousCache.scenes?.[scene.id] === signature && !force) {
      console.log(`Skip cached voiceover: ${scene.id}`);
      continue;
    }
    const aiff = join(tempDir, `${scene.id}.aiff`);
    console.log(`Generate voiceover: ${scene.id} (${voice}, rate ${rate})`);
    run("say", ["-v", voice, "-r", String(rate), "-o", aiff, scene.narration]);
    run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-i", aiff, "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", output]);
    const duration = probeDuration(output);
    if (!duration) {
      unlinkSync(output);
      throw new Error("macOS say produced empty audio. Run this command with permission to access the system speech service.");
    }
    console.log(`Voiceover ready: ${scene.id} (${duration.toFixed(2)}s)`);
  }
} finally {
  rmSync(tempDir, { recursive: true, force: true });
}

writeFileSync(cachePath, JSON.stringify(nextCache, null, 2) + "\n");

console.log(`Voiceovers ready in ${audioDir}`);
