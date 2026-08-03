import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
root = r'D:\Program Files\Obsidian\repository\ArcherArticle\01-选题库'
want = []
for base, dirs, files in os.walk(root):
    for f in files:
        if f.startswith('2026-07-30') or 'Prompt Engineering' in f:
            want.append(os.path.join(base, f))
want.sort()
for t in want:
    print('='*20, os.path.basename(t), '='*20)
    with open(t, encoding='utf-8') as fh:
        print(fh.read())
    print('\n\n')
