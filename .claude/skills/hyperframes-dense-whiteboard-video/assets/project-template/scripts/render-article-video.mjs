import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const run = (program, args) => {
  const result = spawnSync(program, args, { cwd: projectRoot, stdio: "inherit" });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
};

run(process.execPath, ["scripts/build-article-video.mjs"]);
const manifestPath = join(projectRoot, "build-manifest.json");
if (!existsSync(manifestPath)) throw new Error("build-manifest.json was not generated");
const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
const forwarded = process.argv.slice(2);
const hasFpsOverride = forwarded.some((value) => value === "--fps" || value.startsWith("--fps="));
const args = ["--yes", "hyperframes@0.7.64", "render"];
if (!hasFpsOverride) args.push("--fps", String(manifest.fps));
args.push(...forwarded);
run("npx", args);
