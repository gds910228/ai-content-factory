import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const [command, ...forwarded] = process.argv.slice(2);
const allowed = new Set(["check", "preview", "publish"]);
if (!allowed.has(command)) throw new Error(`Expected one of: ${Array.from(allowed).join(", ")}`);

const run = (program, args) => {
  const result = spawnSync(program, args, { cwd: projectRoot, stdio: "inherit" });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
};

run(process.execPath, ["scripts/build-article-video.mjs"]);
run("npx", ["--yes", "hyperframes@0.7.64", command, ...forwarded]);
