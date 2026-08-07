import json, os, shutil, sys
# path to the DOUBLED subtree to remove (Chinese, from JSON so no argv mangling)
doubled = "D:/Program Files/Obsidian/repository/ArcherArticle/02-稿件库/01-创作中稿件/你的Prompt该重构了吗--Agent Skill健康度自检清单-20260807/05-发布包/02-稿件库"
if os.path.isdir(doubled):
    shutil.rmtree(doubled)
    print("removed doubled tree")
else:
    print("doubled tree not present (already gone?)")
# ensure correct single dirs exist
for d in [
    "D:/Program Files/Obsidian/repository/ArcherArticle/02-稿件库/01-创作中稿件/你的Prompt该重构了吗--Agent Skill健康度自检清单-20260807/05-发布包/imgs",
    "D:/Program Files/Obsidian/repository/ArcherArticle/02-稿件库/01-创作中稿件/你的Prompt该重构了吗--Agent Skill健康度自检清单-20260807/05-发布包/imgs/prompts",
]:
    os.makedirs(d, exist_ok=True)
    print("ensured dir:", d, "exists=", os.path.isdir(d))
# sanity: article still present
art = "D:/Program Files/Obsidian/repository/ArcherArticle/02-稿件库/01-创作中稿件/你的Prompt该重构了吗--Agent Skill健康度自检清单-20260807/05-发布包/长文发布包.md"
print("article intact:", os.path.isfile(art), "size=", os.path.getsize(art) if os.path.isfile(art) else 0)
