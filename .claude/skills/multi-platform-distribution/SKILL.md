---
name: multi-platform-distribution
description: >
  One-click multi-platform content distribution. Adapts a finalized article draft (04-定稿.md)
  into platform-specific publishing packages for WeChat Official Account (长文), Xiaohongshu/RED
  (图文笔记), and Douyin/Video Account (短视频口播). Reads the draft, personal writing style
  report, and account info from the vault, then generates complete publishing packages
  (titles + content + image suggestions + hashtags + publishing time) for each platform.
  Saves output to 05-发布包/ directory inside the article folder.
  Use when: (1) A finalized draft needs multi-platform distribution
  (2) User says '多平台分发', '发布包', '适配多平台', '一键分发', '生成发布包', 'multi-platform'
  (3) User provides a finalized draft and asks for platform adaptations
  (4) User says '生成长文发布包', '生成图文发布包', '生成短视频文案' for a specific platform
  Prerequisites: Working directory must be Obsidian vault root. Finalized draft must exist.
---

# Multi-Platform Distribution

## Overview

Convert a finalized article draft into ready-to-publish content packages for multiple platforms. Each package includes platform-optimized titles, formatted content, image/cover suggestions, hashtags, and publishing time recommendations.

## Prerequisites

Before executing, verify these files exist. If any is missing, stop and ask the user.

| File | Vault Path | Purpose |
|------|-----------|---------|
| Finalized draft | `02-稿件库/01-创作中稿件/{article-folder}/04-定稿.md` | Source content to adapt |
| Writing style report | `00-模板库/我的个人写作风格分析报告.md` | Personal style constraints |
| Account info | `00-模板库/自媒体账号基础信息.md` | Audience, positioning, platform info |

## Workflow

### 1. Identify the draft

Determine the source draft from one of:
- User explicitly provides the path (e.g., `@02-稿件库/.../04-定稿.md`)
- Current note context (`<current_note>` tag)
- User describes the article topic → search `02-稿件库/01-创作中稿件/` for matching folder containing `04-定稿.md`

If ambiguous, ask the user to confirm.

### 2. Read all context files

Read all three prerequisite files. The style report is the **authoritative style standard** — all adaptations must conform to it.

### 3. Determine target platforms

Default: generate all three platforms. If user specifies a subset, only generate those.

| Platform | Output File | Reference File |
|----------|-------------|----------------|
| WeChat (长文) | `05-发布包/长文发布包.md` | `references/platform-longform.md` |
| Xiaohongshu (图文) | `05-发布包/图文发布包.md` | `references/platform-image-text.md` |
| Short Video (短视频) | `05-发布包/短视频口播文案.md` | `references/platform-short-video.md` |

### 4. Create output directory

Ensure this directory structure exists inside the article folder:
```
{article-folder}/
├── 05-发布包/
│   └── 配图素材/
```

### 5. Adapt for each platform

For each target platform:

1. Read the corresponding reference file from `references/` in this skill
2. Apply the platform-specific adaptation rules to the draft content
3. Generate the complete publishing package following the output format defined in the reference file
4. Write the output file

**Adaptation principles (apply to all platforms):**
- 100% preserve core viewpoints,干货 content, personal voice, and tone
- No fabricated content — all facts/data/cases come from the original draft
- Maintain personal catchphrases: "那种感觉怎么说呢？", "说实话", "兄弟们", "我的做法是"
- Keep the "踩坑过来人" persona — authentic, relatable, expert-but-approachable
- Adapt structure and format only, never the substance

### 6. Confirm output

After generation, report:
- Which platforms were generated
- Output file paths (as wikilinks for vault navigation)
- List the generated titles for each platform
- Note any content that required significant adaptation decisions

## Platform-Specific Notes

### WeChat (长文)
- Target account: 「AI启蒙学习」(AI tech content)
- Paragraph length: 3-5 lines
- Ending must include 「在看」引导 + 星标关注引导
- Cover image: 900×383px

### Xiaohongshu (图文)
- Paragraph length: 1-2 lines
- Heavy emoji usage (but thematic, not random)
- Core concepts in 【】brackets
- Cover image: 1242×1660px (3:4 portrait)
- 10 hashtags: 5 high-traffic + 3 mid-long-tail + 2 personal IP
- Include carousel image plan (6-8 slides)

### Short Video (短视频)
- ~4 characters/second oral speed
- 60s ≈ 240 chars, 90s ≈ 360 chars, 120s ≈ 480 chars
- Every sentence ≤ 15 characters
- Must annotate: pauses, emphasis, emotion, camera changes
- Cover image: 1080×1920px (9:16 portrait)
- Default duration: 60 seconds unless user specifies otherwise

## Resources

### references/

- **platform-longform.md** — WeChat long-form adaptation rules (role, requirements, output format)
- **platform-image-text.md** — Xiaohongshu image-text adaptation rules (role, requirements, output format)
- **platform-short-video.md** — Short video oral script adaptation rules (role, requirements, output format)

Read the relevant reference file before adapting for each platform. Each contains the full role prompt, adaptation requirements, and output format template.
