import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const raw = process.argv.slice(2);
const skipVoice = raw.includes("--skip-voice");
const skipCheck = raw.includes("--skip-check");
const forceVoice = raw.includes("--force-voice");
const renderArgs = raw.filter((value) => !["--skip-voice", "--skip-check", "--force-voice"].includes(value));

const run = (program, args) => {
  const result = spawnSync(program, args, { cwd: projectRoot, stdio: "inherit" });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
};

if (!skipVoice) run(process.execPath, ["scripts/generate-voiceovers.mjs", ...(forceVoice ? ["--force"] : [])]);
run(process.execPath, ["scripts/build-article-video.mjs"]);
if (!skipCheck) run("npx", ["--yes", "hyperframes@0.7.64", "check"]);
run(process.execPath, ["scripts/render-article-video.mjs", ...renderArgs]);
