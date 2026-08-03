import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, normalize, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const storyboardPath = join(projectRoot, "storyboard.json");
const storyboard = JSON.parse(readFileSync(storyboardPath, "utf8"));

const fail = (message) => {
  throw new Error(`storyboard.json: ${message}`);
};

const finite = (value, label, { positive = false, nonNegative = false } = {}) => {
  if (!Number.isFinite(value)) fail(`${label} must be a finite number`);
  if (positive && value <= 0) fail(`${label} must be greater than 0`);
  if (nonNegative && value < 0) fail(`${label} must be 0 or greater`);
};

const safeId = (value, label) => {
  if (typeof value !== "string" || !/^[A-Za-z][A-Za-z0-9_-]*$/.test(value)) {
    fail(`${label} must start with a letter and contain only letters, numbers, _ or -`);
  }
};

const safeColor = (value, label) => {
  if (typeof value !== "string" || !/^#[0-9A-Fa-f]{6}$/.test(value)) {
    fail(`${label} must be a six-digit hex color`);
  }
};

const assetPath = (path, label, { required = true } = {}) => {
  if (typeof path !== "string" || !path) fail(`${label} must be a non-empty path`);
  const target = resolve(projectRoot, normalize(path));
  if (relative(projectRoot, target).startsWith("..")) fail(`${label} must stay inside the project`);
  if (required && !existsSync(target)) fail(`${label} does not exist: ${path}`);
  return target;
};

const escapeHtml = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("\"", "&quot;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;");

const format = (value) => Number(value.toFixed(3)).toString();
const pointText = (point) => `${format(point.x)},${format(point.y)}`;
const replaceTokens = (template, tokens) => Object.entries(tokens).reduce(
  (output, [token, value]) => output.replaceAll(`{{${token}}}`, String(value)),
  template,
);

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

const estimateNarrationDuration = (text) => {
  const visible = Array.from(String(text)).filter((char) => !/\s/.test(char)).length;
  const punctuation = (String(text).match(/[，。！？；：,.!?;:]/g) || []).length;
  return Math.max(1.8, visible / 4.2 + punctuation * 0.11);
};

const splitCaptionText = (text, maxChars) => {
  const segments = String(text).match(/[^，。！？；：,.!?;:]+[，。！？；：,.!?;:]?/g) || [String(text)];
  const chunks = [];
  for (const rawSegment of segments) {
    const segment = rawSegment.trim();
    if (!segment) continue;
    const chars = Array.from(segment);
    if (chars.length <= maxChars) {
      chunks.push(segment);
      continue;
    }
    for (let index = 0; index < chars.length; index += maxChars) {
      chunks.push(chars.slice(index, index + maxChars).join(""));
    }
  }
  return chunks.filter(Boolean);
};

const captionGroups = (scene, start, duration, maxChars) => {
  const source = Array.isArray(scene.captionChunks) && scene.captionChunks.length > 0
    ? scene.captionChunks.map((chunk) => String(chunk).trim()).filter(Boolean)
    : splitCaptionText(scene.narration, maxChars);
  if (source.length === 0) return [];
  const weights = source.map((chunk) => Math.max(1, Array.from(chunk).filter((char) => !/\s/.test(char)).length));
  const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);
  let cursor = start;
  return source.map((text, index) => {
    const end = index === source.length - 1 ? start + duration : cursor + duration * weights[index] / totalWeight;
    const group = { text, start: cursor, end };
    cursor = end;
    return group;
  });
};

const profileDomainPreset = (aiConfidence) => {
  if (aiConfidence >= 0.72) return "ai-explainer";
  if (aiConfidence >= 0.45) return "hybrid";
  return "general";
};

const boxesOverlap = (a, b) => (
  a.x < b.x + b.width
  && a.x + a.width > b.x
  && a.y < b.y + b.height
  && a.y + a.height > b.y
);

if (storyboard.version !== 2) fail("version must be 2");
if (!storyboard.article || !storyboard.project || !storyboard.hand || !Array.isArray(storyboard.scenes) || storyboard.scenes.length === 0) {
  fail("article, project, hand and at least one scene are required");
}

const { project, hand, narration } = storyboard;
const { canvas, transition, timing, captions } = project;
safeId(project.id, "project.id");
const visualStyle = project.visualStyle || "dense-whiteboard";
if (visualStyle !== "dense-whiteboard") fail("project.visualStyle must remain dense-whiteboard");
const validDomainPresets = new Set(["auto", "general", "hybrid", "ai-explainer"]);
const requestedDomainPreset = project.domainPreset || "general";
if (!validDomainPresets.has(requestedDomainPreset)) fail("project.domainPreset is invalid");
const contentProfile = storyboard.contentProfile ?? null;
if (requestedDomainPreset === "auto" && !contentProfile) fail("contentProfile is required when project.domainPreset is auto");
if (contentProfile) {
  if (!["general", "ai", "mixed"].includes(contentProfile.domain)) fail("contentProfile.domain is invalid");
  finite(contentProfile.aiConfidence, "contentProfile.aiConfidence", { nonNegative: true });
  if (contentProfile.aiConfidence > 1) fail("contentProfile.aiConfidence must be between 0 and 1");
  if (!["general", "hybrid", "ai-explainer"].includes(contentProfile.resolvedDomainPreset)) fail("contentProfile.resolvedDomainPreset is invalid");
  const expectedPreset = profileDomainPreset(contentProfile.aiConfidence);
  if (contentProfile.resolvedDomainPreset !== expectedPreset) {
    fail(`contentProfile.resolvedDomainPreset must be ${expectedPreset} for aiConfidence ${contentProfile.aiConfidence}`);
  }
  if (!Array.isArray(contentProfile.topics)) fail("contentProfile.topics must be an array");
  contentProfile.topics.forEach((topic, index) => {
    if (typeof topic !== "string" || !topic.trim()) fail(`contentProfile.topics[${index}] must be a non-empty string`);
  });
  if (!["beginner", "intermediate", "advanced"].includes(contentProfile.technicalDepth)) fail("contentProfile.technicalDepth is invalid");
  if (typeof contentProfile.audience !== "string" || !contentProfile.audience.trim()) fail("contentProfile.audience is required");
  if (!["concept", "workflow", "comparison", "tutorial", "opinion", "news", "case-study", "mixed"].includes(contentProfile.articleType)) fail("contentProfile.articleType is invalid");
  if (!Array.isArray(contentProfile.signals) || contentProfile.signals.length < 1 || contentProfile.signals.length > 8) fail("contentProfile.signals must contain 1-8 items");
  contentProfile.signals.forEach((signal, index) => {
    if (typeof signal !== "string" || !signal.trim()) fail(`contentProfile.signals[${index}] must be a non-empty string`);
  });
  if (typeof contentProfile.reason !== "string" || !contentProfile.reason.trim()) fail("contentProfile.reason is required");
}
const resolvedDomainPreset = requestedDomainPreset === "auto"
  ? contentProfile.resolvedDomainPreset
  : requestedDomainPreset;
const aiVisualMode = resolvedDomainPreset === "ai-explainer" || resolvedDomainPreset === "hybrid";
finite(canvas.width, "project.canvas.width", { positive: true });
finite(canvas.height, "project.canvas.height", { positive: true });
if (![24, 30, 60].includes(canvas.fps)) fail("project.canvas.fps must be 24, 30 or 60");
if (transition.type !== "crossfade") fail("project.transition.type currently supports only crossfade");
finite(transition.duration, "project.transition.duration", { positive: true });
for (const key of ["narrationLead", "tailHold", "minSceneDuration", "revealStart", "revealEndBefore", "moduleGap", "maxRevealDuration"]) {
  finite(timing[key], `project.timing.${key}`, { positive: key !== "revealStart" && key !== "moduleGap", nonNegative: key === "revealStart" || key === "moduleGap" });
}
if (timing.tailHold < transition.duration) fail("project.timing.tailHold must be at least the transition duration");
if (!captions || typeof captions.enabled !== "boolean") fail("project.captions.enabled is required");
if (!Number.isInteger(captions.maxChars) || captions.maxChars < 4 || captions.maxChars > 24) fail("project.captions.maxChars must be an integer from 4 to 24");
finite(captions.safeBottom, "project.captions.safeBottom", { positive: true });
if (captions.safeBottom >= canvas.height / 2) fail("project.captions.safeBottom must be less than half the canvas height");
if (typeof captions.fontFamily !== "string" || !captions.fontFamily.trim()) fail("project.captions.fontFamily is required");
finite(captions.fontSize, "project.captions.fontSize", { positive: true });
safeColor(captions.textColor, "project.captions.textColor");
safeColor(captions.outlineColor, "project.captions.outlineColor");
finite(captions.outlineWidth, "project.captions.outlineWidth", { nonNegative: true });
if (typeof captions.background !== "string" || !captions.background.trim()) fail("project.captions.background is required");
assetPath(storyboard.article.source, "article.source");
assetPath(hand.asset, "hand.asset");
finite(hand.displayWidth, "hand.displayWidth", { positive: true });
finite(hand.displayHeight, "hand.displayHeight", { positive: true });
finite(hand.penTip.x, "hand.penTip.x", { nonNegative: true });
finite(hand.penTip.y, "hand.penTip.y", { nonNegative: true });
finite(hand.exit.duration, "hand.exit.duration", { positive: true });
finite(hand.exit.pen.x, "hand.exit.pen.x");
finite(hand.exit.pen.y, "hand.exit.pen.y");
finite(narration.volume, "narration.volume", { nonNegative: true });
if (narration.volume > 1) fail("narration.volume must be between 0 and 1");

const diagnostics = storyboard.diagnostics || {};
safeColor(diagnostics.pathColor || "#EF4444", "diagnostics.pathColor");
safeColor(diagnostics.labelColor || "#171717", "diagnostics.labelColor");
const validDirections = new Set(["down", "up", "right", "left"]);
const validVisualPatterns = new Set(["general", "pipeline", "architecture", "comparison", "loop", "cause-effect", "timeline", "hub-spoke", "metric-dashboard"]);
const validAiVisualKeys = new Set([
  "model-core", "token-chunks", "embedding-space", "vector-store", "retrieval", "rag-pipeline",
  "agent-loop", "tool-call", "memory", "training", "inference", "context-window",
  "hallucination-risk", "api-exchange", "fine-tuning", "multimodal", "evaluation",
  "cost-latency", "guardrail", "generic-node",
]);
const validTechComponentTypes = new Set(["prompt-box", "code-card", "api-exchange", "metric-badge", "data-chip", "risk-callout", "model-badge", "tool-badge"]);
const techAccentDefaults = {
  "prompt-box": "#3B9C95",
  "code-card": "#8B5CF6",
  "api-exchange": "#8B5CF6",
  "metric-badge": "#F6C453",
  "data-chip": "#3B9C95",
  "risk-callout": "#EF4444",
  "model-badge": "#8B5CF6",
  "tool-badge": "#F6C453",
};
const seenSceneIds = new Set();
let rootCursor = 0;

const preparedScenes = storyboard.scenes.map((scene, sceneIndex) => {
  safeId(scene.id, `scenes[${sceneIndex}].id`);
  if (seenSceneIds.has(scene.id)) fail(`duplicate scene id: ${scene.id}`);
  seenSceneIds.add(scene.id);
  if (typeof scene.narration !== "string" || !scene.narration.trim()) fail(`${scene.id}.narration is required`);
  assetPath(scene.sourceImage, `${scene.id}.sourceImage`);
  const visualPattern = scene.visualPattern || "general";
  if (!validVisualPatterns.has(visualPattern)) fail(`${scene.id}.visualPattern is invalid`);
  const rawAiConcepts = scene.aiConcepts ?? [];
  if (!Array.isArray(rawAiConcepts)) fail(`${scene.id}.aiConcepts must be an array`);
  const rawTechComponents = scene.techComponents ?? [];
  if (!Array.isArray(rawTechComponents)) fail(`${scene.id}.techComponents must be an array`);
  if (rawTechComponents.length > 6) fail(`${scene.id}.techComponents supports at most 6 items`);
  if (!Array.isArray(scene.modules) || scene.modules.length === 0) fail(`${scene.id}.modules must not be empty`);
  if (!Array.isArray(scene.annotations)) fail(`${scene.id}.annotations must be an array`);
  if (scene.modules.length < 6 || scene.modules.length > 9) {
    console.warn(`[quality] ${scene.id} has ${scene.modules.length} modules; dense mode recommends 6-9`);
  }
  if (scene.annotations.length < 3 || scene.annotations.length > 5) {
    console.warn(`[quality] ${scene.id} has ${scene.annotations.length} annotations; dense mode recommends 3-5`);
  }
  if (aiVisualMode && rawAiConcepts.length > 0 && visualPattern === "general") {
    console.warn(`[quality] ${scene.id} contains AI concepts but uses the general visual pattern`);
  }

  const audioRelative = `assets/audio/${scene.id}.wav`;
  const audioAbsolute = assetPath(audioRelative, `${scene.id}.audio`, { required: false });
  const probedDuration = existsSync(audioAbsolute) ? probeDuration(audioAbsolute) : null;
  const audioReady = Number.isFinite(probedDuration) && probedDuration > 0;
  const audioDuration = probedDuration || estimateNarrationDuration(scene.narration);
  const sceneDuration = Math.max(timing.minSceneDuration, timing.narrationLead + audioDuration + timing.tailHold);
  const start = sceneIndex === 0 ? 0 : rootCursor - transition.duration;
  rootCursor = start + sceneDuration;

  const minimumRevealSpan = scene.modules.length * 0.35 + Math.max(0, scene.modules.length - 1) * timing.moduleGap;
  const hardRevealEnd = sceneDuration - timing.revealEndBefore - hand.exit.duration;
  if (timing.revealStart + minimumRevealSpan > hardRevealEnd) fail(`${scene.id} has too many modules for its scene duration`);
  const narrationRevealEnd = timing.narrationLead + audioDuration - 0.1;
  const revealEnd = Math.min(
    hardRevealEnd,
    timing.revealStart + timing.maxRevealDuration,
    Math.max(timing.revealStart + minimumRevealSpan, narrationRevealEnd),
  );
  const gapTotal = Math.max(0, scene.modules.length - 1) * timing.moduleGap;
  const durationPool = revealEnd - timing.revealStart - gapTotal;
  const totalWeight = scene.modules.reduce((sum, module) => sum + (module.reveal?.weight ?? 1), 0);
  let moduleCursor = timing.revealStart;
  const seenModuleIds = new Set();

  const modules = scene.modules.map((module, moduleIndex) => {
    safeId(module.id, `${scene.id}.modules[${moduleIndex}].id`);
    if (seenModuleIds.has(module.id)) fail(`${scene.id} has duplicate module id: ${module.id}`);
    seenModuleIds.add(module.id);
    const role = module.role || "visual";
    if (!["visual", "card"].includes(role)) fail(`${scene.id}.${module.id}.role is invalid`);
    safeColor(module.diagnosticColor || "#0EA5E9", `${scene.id}.${module.id}.diagnosticColor`);
    const box = module.box;
    for (const key of ["x", "y"]) finite(box[key], `${scene.id}.${module.id}.box.${key}`, { nonNegative: true });
    for (const key of ["width", "height"]) finite(box[key], `${scene.id}.${module.id}.box.${key}`, { positive: true });
    if (box.x + box.width > canvas.width || box.y + box.height > canvas.height) fail(`${scene.id}.${module.id} box exceeds the canvas`);
    const clipPolygon = module.clipPolygon ?? null;
    if (clipPolygon !== null) {
      if (!Array.isArray(clipPolygon) || clipPolygon.length < 3) fail(`${scene.id}.${module.id}.clipPolygon must contain at least 3 points`);
      clipPolygon.forEach((point, pointIndex) => {
        finite(point.x, `${scene.id}.${module.id}.clipPolygon[${pointIndex}].x`);
        finite(point.y, `${scene.id}.${module.id}.clipPolygon[${pointIndex}].y`);
        if (point.x < 0 || point.x > 1 || point.y < 0 || point.y > 1) {
          fail(`${scene.id}.${module.id}.clipPolygon[${pointIndex}] must use normalized coordinates from 0 to 1`);
        }
      });
    }
    const extraRevealBoxes = module.extraRevealBoxes ?? [];
    if (!Array.isArray(extraRevealBoxes)) fail(`${scene.id}.${module.id}.extraRevealBoxes must be an array`);
    extraRevealBoxes.forEach((extraBox, extraIndex) => {
      for (const key of ["x", "y"]) finite(extraBox[key], `${scene.id}.${module.id}.extraRevealBoxes[${extraIndex}].${key}`, { nonNegative: true });
      for (const key of ["width", "height"]) finite(extraBox[key], `${scene.id}.${module.id}.extraRevealBoxes[${extraIndex}].${key}`, { positive: true });
      if (extraBox.x + extraBox.width > canvas.width || extraBox.y + extraBox.height > canvas.height) {
        fail(`${scene.id}.${module.id}.extraRevealBoxes[${extraIndex}] exceeds the canvas`);
      }
    });
    const reveal = module.reveal || {};
    if (!validDirections.has(reveal.direction)) fail(`${scene.id}.${module.id}.reveal.direction is invalid`);
    const edgePosition = reveal.edgePosition ?? 0.5;
    const weight = reveal.weight ?? 1;
    finite(edgePosition, `${scene.id}.${module.id}.reveal.edgePosition`);
    finite(weight, `${scene.id}.${module.id}.reveal.weight`, { positive: true });
    if (edgePosition < 0 || edgePosition > 1) fail(`${scene.id}.${module.id}.edgePosition must be between 0 and 1`);
    const duration = durationPool * weight / totalWeight;
    const moduleStart = moduleCursor;
    const end = moduleStart + duration;
    moduleCursor = end + timing.moduleGap;

    let startPoint;
    let endPoint;
    if (reveal.direction === "down" || reveal.direction === "up") {
      const x = box.x + box.width * edgePosition;
      startPoint = { x, y: reveal.direction === "down" ? box.y : box.y + box.height };
      endPoint = { x, y: reveal.direction === "down" ? box.y + box.height : box.y };
    } else {
      const y = box.y + box.height * edgePosition;
      startPoint = { x: reveal.direction === "right" ? box.x : box.x + box.width, y };
      endPoint = { x: reveal.direction === "right" ? box.x + box.width : box.x, y };
    }

    return {
      ...module,
      role,
      label: module.label || module.id,
      diagnosticColor: module.diagnosticColor || "#0EA5E9",
      clipPolygon,
      revealBoxes: [box, ...extraRevealBoxes],
      reveal: { ...reveal, edgePosition, weight, start: moduleStart, duration },
      startPoint,
      endPoint,
      end,
    };
  });

  const lastModuleEnd = modules.at(-1).end;
  const exitStart = lastModuleEnd + 0.08;
  if (exitStart + hand.exit.duration > sceneDuration) fail(`${scene.id} hand exit exceeds the scene duration`);

  const moduleById = new Map(modules.map((module) => [module.id, module]));
  const seenConceptKeys = new Set();
  const aiConcepts = rawAiConcepts.map((concept, conceptIndex) => {
    if (!concept || typeof concept !== "object") fail(`${scene.id}.aiConcepts[${conceptIndex}] must be an object`);
    if (typeof concept.key !== "string" || !/^[a-z][a-z0-9-]*$/.test(concept.key)) fail(`${scene.id}.aiConcepts[${conceptIndex}].key is invalid`);
    if (!validAiVisualKeys.has(concept.key)) fail(`${scene.id}.${concept.key} is not in the AI visual dictionary; use generic-node for unknown concepts`);
    if (seenConceptKeys.has(concept.key)) fail(`${scene.id} has duplicate AI concept key: ${concept.key}`);
    seenConceptKeys.add(concept.key);
    if (typeof concept.label !== "string" || !concept.label.trim()) fail(`${scene.id}.${concept.key}.label is required`);
    if (!moduleById.has(concept.moduleId)) fail(`${scene.id}.${concept.key}.moduleId references an unknown module`);
    return { key: concept.key, label: concept.label, moduleId: concept.moduleId };
  });
  const seenAnnotationIds = new Set();
  const annotations = scene.annotations.map((annotation, annotationIndex) => {
    safeId(annotation.id, `${scene.id}.annotations[${annotationIndex}].id`);
    if (seenAnnotationIds.has(annotation.id)) fail(`${scene.id} has duplicate annotation id: ${annotation.id}`);
    seenAnnotationIds.add(annotation.id);
    if (typeof annotation.text !== "string" || !annotation.text.trim()) fail(`${scene.id}.${annotation.id}.text is required`);
    if (!["title", "label", "callout"].includes(annotation.variant)) fail(`${scene.id}.${annotation.id}.variant is invalid`);
    const box = annotation.box;
    for (const key of ["x", "y"]) finite(box[key], `${scene.id}.${annotation.id}.box.${key}`, { nonNegative: true });
    for (const key of ["width", "height"]) finite(box[key], `${scene.id}.${annotation.id}.box.${key}`, { positive: true });
    if (box.x + box.width > canvas.width || box.y + box.height > canvas.height) fail(`${scene.id}.${annotation.id} box exceeds the canvas`);
    if (box.y + box.height > canvas.height - captions.safeBottom) fail(`${scene.id}.${annotation.id} enters the caption safe area`);
    const relatedModule = moduleById.get(annotation.revealAfter);
    if (!relatedModule) fail(`${scene.id}.${annotation.id}.revealAfter references an unknown module`);
    const placement = annotation.placement || "free";
    if (!["free", "inside"].includes(placement)) fail(`${scene.id}.${annotation.id}.placement is invalid`);
    if (placement === "inside") {
      const parentBox = relatedModule.box;
      const contained = box.x >= parentBox.x
        && box.y >= parentBox.y
        && box.x + box.width <= parentBox.x + parentBox.width
        && box.y + box.height <= parentBox.y + parentBox.height;
      if (!contained) fail(`${scene.id}.${annotation.id} must stay inside module ${relatedModule.id}`);
    }
    const accentColor = annotation.accentColor || "#3B9C95";
    safeColor(accentColor, `${scene.id}.${annotation.id}.accentColor`);
    return { ...annotation, placement, accentColor, start: Math.min(sceneDuration - 0.2, relatedModule.end + 0.06) };
  });
  for (const module of modules.filter((item) => item.role === "card")) {
    const hasInsideTitle = annotations.some((annotation) =>
      annotation.revealAfter === module.id && annotation.placement === "inside",
    );
    if (!hasInsideTitle) fail(`${scene.id}.${module.id} is a card but has no inside annotation`);
  }

  const seenTechComponentIds = new Set();
  const techComponents = rawTechComponents.map((component, componentIndex) => {
    if (!component || typeof component !== "object") fail(`${scene.id}.techComponents[${componentIndex}] must be an object`);
    safeId(component.id, `${scene.id}.techComponents[${componentIndex}].id`);
    if (seenTechComponentIds.has(component.id)) fail(`${scene.id} has duplicate tech component id: ${component.id}`);
    seenTechComponentIds.add(component.id);
    if (!validTechComponentTypes.has(component.type)) fail(`${scene.id}.${component.id}.type is invalid`);
    if (typeof component.title !== "string" || !component.title.trim()) fail(`${scene.id}.${component.id}.title is required`);
    const body = component.body == null ? "" : String(component.body).trim();
    const lines = component.lines ?? [];
    if (!Array.isArray(lines) || lines.length > 8) fail(`${scene.id}.${component.id}.lines must contain at most 8 items`);
    lines.forEach((line, lineIndex) => {
      if (typeof line !== "string" || !line.trim()) fail(`${scene.id}.${component.id}.lines[${lineIndex}] must be a non-empty string`);
    });
    if (component.type === "code-card" && lines.length === 0) fail(`${scene.id}.${component.id} code-card requires lines`);
    const box = component.box;
    if (!box || typeof box !== "object") fail(`${scene.id}.${component.id}.box is required`);
    for (const key of ["x", "y"]) finite(box[key], `${scene.id}.${component.id}.box.${key}`, { nonNegative: true });
    for (const key of ["width", "height"]) finite(box[key], `${scene.id}.${component.id}.box.${key}`, { positive: true });
    if (box.x + box.width > canvas.width || box.y + box.height > canvas.height) fail(`${scene.id}.${component.id} box exceeds the canvas`);
    if (box.y + box.height > canvas.height - captions.safeBottom) fail(`${scene.id}.${component.id} enters the caption safe area`);
    const relatedModule = moduleById.get(component.revealAfter);
    if (!relatedModule) fail(`${scene.id}.${component.id}.revealAfter references an unknown module`);
    const accentColor = component.accentColor || techAccentDefaults[component.type];
    safeColor(accentColor, `${scene.id}.${component.id}.accentColor`);
    return {
      ...component,
      body,
      lines: lines.map((line) => line.trim()),
      accentColor,
      start: Math.min(sceneDuration - 0.2, relatedModule.end + 0.06),
    };
  });
  for (let leftIndex = 0; leftIndex < techComponents.length; leftIndex += 1) {
    for (let rightIndex = leftIndex + 1; rightIndex < techComponents.length; rightIndex += 1) {
      if (boxesOverlap(techComponents[leftIndex].box, techComponents[rightIndex].box)) {
        fail(`${scene.id}.${techComponents[leftIndex].id} overlaps tech component ${techComponents[rightIndex].id}`);
      }
    }
  }
  for (const component of techComponents) {
    const overlappingAnnotation = annotations.find((annotation) => boxesOverlap(component.box, annotation.box));
    if (overlappingAnnotation) fail(`${scene.id}.${component.id} overlaps annotation ${overlappingAnnotation.id}`);
  }

  const sceneCaptions = captions.enabled
    ? captionGroups(scene, timing.narrationLead, audioDuration, captions.maxChars)
    : [];
  for (const [captionIndex, group] of sceneCaptions.entries()) {
    if (!(group.start >= 0 && group.end > group.start && group.end <= sceneDuration)) {
      fail(`${scene.id}.caption[${captionIndex}] has invalid timing`);
    }
    if (captionIndex > 0 && group.start < sceneCaptions[captionIndex - 1].end) {
      fail(`${scene.id}.caption[${captionIndex}] overlaps the previous group`);
    }
  }

  return {
    ...scene,
    visualPattern,
    aiConcepts,
    start,
    duration: sceneDuration,
    audio: {
      path: audioRelative,
      exists: audioReady,
      duration: audioDuration,
      source: audioReady ? "file" : "estimate",
      start: start + timing.narrationLead,
    },
    modules,
    annotations,
    techComponents,
    captions: sceneCaptions,
    exitStart,
  };
});

if (requestedDomainPreset === "auto" && aiVisualMode && contentProfile.topics.length === 0) {
  fail("contentProfile.topics must not be empty for an automatically detected AI or hybrid article");
}
if (aiVisualMode && !preparedScenes.some((scene) => scene.aiConcepts.length > 0)) {
  fail("AI or hybrid mode requires at least one scene.aiConcepts mapping");
}
if (aiVisualMode && !preparedScenes.some((scene) => scene.visualPattern !== "general")) {
  fail("AI or hybrid mode requires at least one domain-specific visualPattern");
}

const rootDuration = preparedScenes.at(-1).start + preparedScenes.at(-1).duration;
const indexTemplate = readFileSync(join(projectRoot, "templates/index.template.html"), "utf8");
const sceneTemplate = readFileSync(join(projectRoot, "templates/whiteboard-scene.template.html"), "utf8");
mkdirSync(join(projectRoot, "compositions"), { recursive: true });

const sceneClips = preparedScenes.map((scene, index) =>
  `      <div id="clip-${scene.id}" class="clip scene-clip" data-composition-id="${scene.id}" data-composition-src="compositions/${scene.id}.html" data-start="${format(scene.start)}" data-duration="${format(scene.duration)}" data-track-index="${index % 2}" style="position:absolute;inset:0;z-index:${index + 1}"></div>`,
).join("\n");

const audioClips = preparedScenes.filter((scene) => scene.audio.exists).map((scene) =>
  `      <audio id="audio-${scene.id}" class="clip" data-start="${format(scene.audio.start)}" data-duration="${format(scene.audio.duration)}" data-track-index="10" data-volume="${format(narration.volume)}" src="${escapeHtml(scene.audio.path)}"></audio>`,
).join("\n");

const transitionTimeline = preparedScenes.slice(1).map((scene) =>
  `      tl.from("#clip-${scene.id}", { opacity: 0, duration: ${format(transition.duration)}, ease: "sine.inOut" }, ${format(scene.start)});`,
).join("\n");

const indexHtml = replaceTokens(indexTemplate, {
  WIDTH: format(canvas.width),
  HEIGHT: format(canvas.height),
  DURATION: format(rootDuration),
  SCENE_CLIPS: sceneClips,
  AUDIO_CLIPS: audioClips,
  TRANSITION_TIMELINE: transitionTimeline,
});
writeFileSync(join(projectRoot, "index.html"), indexHtml);

for (const scene of preparedScenes) {
  const idPrefix = scene.id;
  const initialClipPath = {
    down: "inset(0% 0% 100% 0%)",
    up: "inset(100% 0% 0% 0%)",
    right: "inset(0% 100% 0% 0%)",
    left: "inset(0% 0% 0% 100%)",
  };
  const moduleWindows = scene.modules.flatMap((module) => module.revealBoxes.map((box, boxIndex) => {
    const staticShape = boxIndex === 0 && module.clipPolygon
      ? `polygon(${module.clipPolygon.map((point) => `${format(point.x * 100)}% ${format(point.y * 100)}%`).join(", ")})`
      : "inset(0%)";
    return `      <div class="module-window" style="left:${format(box.x)}px; top:${format(box.y)}px; width:${format(box.width)}px; height:${format(box.height)}px; clip-path:${staticShape}"><div id="${idPrefix}-paint-${module.id}-${boxIndex}" class="module-paint reveal-${module.reveal.direction}" style="clip-path:${initialClipPath[module.reveal.direction]}; background-image:url(&quot;${escapeHtml(scene.sourceImage)}&quot;); background-position:-${format(box.x)}px -${format(box.y)}px"></div></div>`;
  })).join("\n");
  const currentLabels = scene.modules.map((module) =>
    `      <div id="${idPrefix}-label-${module.id}" class="current-module">${escapeHtml(module.label)}</div>`,
  ).join("\n");
  const moduleBoxes = scene.modules.flatMap((module) => module.revealBoxes.map((box, boxIndex) =>
    `      <div class="module-box" style="--diagnostic-color:${module.diagnosticColor}; left:${format(box.x)}px; top:${format(box.y)}px; width:${format(box.width)}px; height:${format(box.height)}px"><span class="module-label">${escapeHtml(module.label)}${boxIndex > 0 ? ` · 连线 ${boxIndex}` : ""}</span></div>`,
  )).join("\n");
  const annotationMarkup = scene.annotations.map((annotation) => {
    const { box } = annotation;
    return `      <div id="${idPrefix}-annotation-${annotation.id}" class="knowledge-annotation annotation-${annotation.variant} placement-${annotation.placement}" style="--accent-color:${annotation.accentColor}; left:${format(box.x)}px; top:${format(box.y)}px; width:${format(box.width)}px; height:${format(box.height)}px"><span>${escapeHtml(annotation.text)}</span></div>`;
  }).join("\n");
  const techComponentMarkup = scene.techComponents.map((component) => {
    const { box } = component;
    const body = component.body ? `<div class="tech-component-body">${escapeHtml(component.body)}</div>` : "";
    const lines = component.lines.length > 0
      ? `<div class="tech-component-lines">${component.lines.map((line) => `<span>${escapeHtml(line)}</span>`).join("")}</div>`
      : "";
    return `      <div id="${idPrefix}-tech-${component.id}" class="tech-component tech-${component.type}" style="--accent-color:${component.accentColor}; left:${format(box.x)}px; top:${format(box.y)}px; width:${format(box.width)}px; height:${format(box.height)}px"><div class="tech-component-title">${escapeHtml(component.title)}</div>${body}${lines}</div>`;
  }).join("\n");
  const captionMarkup = scene.captions.map((group, index) =>
    `      <div id="${idPrefix}-caption-${index}" class="caption-group"><span>${escapeHtml(group.text)}</span></div>`,
  ).join("\n");
  const motionPathPoints = scene.modules.flatMap((module) => [module.startPoint, module.endPoint]).map(pointText).join(" ");
  const handRigSelector = `#${idPrefix}-hand-rig`;
  const timelineLines = [];
  const first = scene.modules[0];
  timelineLines.push(`      const firstStart = handPosition(${format(first.startPoint.x)}, ${format(first.startPoint.y)});`);
  timelineLines.push(`      tl.set("${handRigSelector}", { ...firstStart }, ${format(Math.max(0, first.reveal.start - 0.16))});`);
  timelineLines.push(`      tl.to("${handRigSelector}", { opacity: 1, duration: 0.16, ease: "power2.out" }, ${format(Math.max(0, first.reveal.start - 0.16))});`);
  scene.modules.forEach((module, index) => {
    const startVar = `module${index}Start`;
    const endVar = `module${index}End`;
    timelineLines.push(`      const ${startVar} = handPosition(${format(module.startPoint.x)}, ${format(module.startPoint.y)});`);
    timelineLines.push(`      const ${endVar} = handPosition(${format(module.endPoint.x)}, ${format(module.endPoint.y)});`);
    if (index > 0) {
      const prior = scene.modules[index - 1];
      const travelDuration = module.reveal.start - prior.end;
      timelineLines.push(`      tl.to("${handRigSelector}", { ...${startVar}, duration: ${format(travelDuration)}, ease: "power1.inOut" }, ${format(prior.end)});`);
    }
    const paintSelectors = module.revealBoxes.map((_, boxIndex) => `#${idPrefix}-paint-${module.id}-${boxIndex}`).join(", ");
    timelineLines.push(`      tl.to("${paintSelectors}", { clipPath: "inset(0% 0% 0% 0%)", duration: ${format(module.reveal.duration)}, ease: "none" }, ${format(module.reveal.start)});`);
    timelineLines.push(`      tl.to("${handRigSelector}", { ...${endVar}, duration: ${format(module.reveal.duration)}, ease: "none" }, ${format(module.reveal.start)});`);
    timelineLines.push(`      tl.to("#${idPrefix}-label-${module.id}", { opacity: 1, duration: 0.01 }, ${format(module.reveal.start)});`);
    timelineLines.push(`      tl.to("#${idPrefix}-label-${module.id}", { opacity: 0, duration: 0.01 }, ${format(module.end)});`);
  });
  const finalImageReveal = Math.min(scene.exitStart, scene.modules.at(-1).end + 0.02);
  timelineLines.push(`      tl.set("#${idPrefix}-image", { visibility: "visible", opacity: 1 }, ${format(finalImageReveal)});`);
  timelineLines.push(`      const exit = handPosition(${format(hand.exit.pen.x)}, ${format(hand.exit.pen.y)});`);
  timelineLines.push(`      tl.to("${handRigSelector}", { ...exit, opacity: 0, duration: ${format(hand.exit.duration)}, ease: "power1.in" }, ${format(scene.exitStart)});`);
  scene.annotations.forEach((annotation, index) => {
    const selector = `#${idPrefix}-annotation-${annotation.id}`;
    const ease = ["power3.out", "back.out(1.3)", "sine.out"][index % 3];
    timelineLines.push(`      tl.set("${selector}", { visibility: "visible" }, ${format(annotation.start)});`);
    timelineLines.push(`      tl.from("${selector}", { opacity: 0, y: 10, scale: 0.96, duration: 0.24, ease: "${ease}", immediateRender: false }, ${format(annotation.start)});`);
  });
  scene.techComponents.forEach((component, index) => {
    const selector = `#${idPrefix}-tech-${component.id}`;
    const ease = ["power3.out", "back.out(1.18)", "sine.out"][index % 3];
    timelineLines.push(`      tl.set("${selector}", { visibility: "visible" }, ${format(component.start)});`);
    timelineLines.push(`      tl.from("${selector}", { opacity: 0, y: 8, scale: 0.97, duration: 0.24, ease: "${ease}", immediateRender: false }, ${format(component.start)});`);
  });
  scene.captions.forEach((group, index) => {
    const selector = `#${idPrefix}-caption-${index}`;
    const exitDuration = Math.min(0.12, Math.max(0.06, (group.end - group.start) * 0.2));
    timelineLines.push(`      tl.set("${selector}", { visibility: "visible", opacity: 1 }, ${format(group.start)});`);
    timelineLines.push(`      tl.from("${selector}", { opacity: 0, y: 8, duration: 0.12, ease: "power2.out", immediateRender: false }, ${format(group.start)});`);
    timelineLines.push(`      tl.to("${selector}", { opacity: 0, scale: 0.97, duration: ${format(exitDuration)}, ease: "power2.in" }, ${format(group.end - exitDuration)});`);
    timelineLines.push(`      tl.set("${selector}", { opacity: 0, visibility: "hidden" }, ${format(group.end)});`);
  });

  const sceneHtml = replaceTokens(sceneTemplate, {
    COMPOSITION_ID: scene.id,
    SCENE_ROOT_ID: `${idPrefix}-root`,
    SCENE_IMAGE_ID: `${idPrefix}-image`,
    HAND_RIG_ID: `${idPrefix}-hand-rig`,
    HAND_MARKER_ID: `${idPrefix}-hand-marker`,
    WIDTH: format(canvas.width),
    HEIGHT: format(canvas.height),
    DURATION: format(scene.duration),
    DEBUG_DEFAULT: String(diagnostics.defaultEnabled ?? false),
    SOURCE_IMAGE: escapeHtml(scene.sourceImage),
    SOURCE_IMAGE_ALT: escapeHtml(scene.sourceImageAlt || scene.title || "白板线稿场景"),
    HAND_ASSET: escapeHtml(hand.asset),
    HAND_WIDTH: format(hand.displayWidth),
    HAND_HEIGHT: format(hand.displayHeight),
    PEN_TIP_X: format(hand.penTip.x),
    PEN_TIP_Y: format(hand.penTip.y),
    PATH_COLOR: escapeHtml(diagnostics.pathColor || "#EF4444"),
    LABEL_COLOR: escapeHtml(diagnostics.labelColor || "#171717"),
    CAPTION_SAFE_BOTTOM: format(captions.safeBottom),
    CAPTION_FONT_FAMILY: escapeHtml(captions.fontFamily),
    CAPTION_FONT_SIZE: format(captions.fontSize),
    CAPTION_TEXT_COLOR: escapeHtml(captions.textColor),
    CAPTION_OUTLINE_COLOR: escapeHtml(captions.outlineColor),
    CAPTION_OUTLINE_WIDTH: format(captions.outlineWidth),
    CAPTION_BACKGROUND: escapeHtml(captions.background),
    MODULE_WINDOW_MARKUP: moduleWindows,
    ANNOTATION_MARKUP: annotationMarkup,
    TECH_COMPONENT_MARKUP: techComponentMarkup,
    CAPTION_MARKUP: captionMarkup,
    CURRENT_LABELS: currentLabels,
    MODULE_BOXES: moduleBoxes,
    MOTION_PATH_POINTS: motionPathPoints,
    TIMELINE_SCRIPT: timelineLines.join("\n"),
  });
  writeFileSync(join(projectRoot, "compositions", `${scene.id}.html`), sceneHtml);
}

const manifest = {
  version: 2,
  projectId: project.id,
  title: project.title,
  sourceArticle: storyboard.article.source,
  visualStyle,
  requestedDomainPreset,
  resolvedDomainPreset,
  contentProfile,
  width: canvas.width,
  height: canvas.height,
  fps: canvas.fps,
  durationSeconds: Number(rootDuration.toFixed(3)),
  transition,
  scenes: preparedScenes.map((scene) => ({
    id: scene.id,
    title: scene.title,
    visualPattern: scene.visualPattern,
    aiConcepts: scene.aiConcepts,
    start: Number(scene.start.toFixed(3)),
    duration: Number(scene.duration.toFixed(3)),
    narration: scene.narration,
    audio: {
      path: scene.audio.path,
      exists: scene.audio.exists,
      source: scene.audio.source,
      start: Number(scene.audio.start.toFixed(3)),
      duration: Number(scene.audio.duration.toFixed(3)),
    },
    modules: scene.modules.map((module) => ({
      id: module.id,
      start: Number(module.reveal.start.toFixed(3)),
      duration: Number(module.reveal.duration.toFixed(3)),
    })),
    annotations: scene.annotations.map((annotation) => ({
      id: annotation.id,
      text: annotation.text,
      revealAfter: annotation.revealAfter,
      start: Number(annotation.start.toFixed(3)),
    })),
    techComponents: scene.techComponents.map((component) => ({
      id: component.id,
      type: component.type,
      title: component.title,
      revealAfter: component.revealAfter,
      start: Number(component.start.toFixed(3)),
    })),
    captions: scene.captions.map((group) => ({
      text: group.text,
      start: Number(group.start.toFixed(3)),
      end: Number(group.end.toFixed(3)),
    })),
  })),
};
writeFileSync(join(projectRoot, "build-manifest.json"), JSON.stringify(manifest, null, 2) + "\n");

const audioStatus = preparedScenes.every((scene) => scene.audio.exists) ? "audio ready" : "audio estimated; run npm run voice";
console.log(`Built ${preparedScenes.length} scenes, ${format(rootDuration)}s at ${canvas.fps}fps (${audioStatus})`);
