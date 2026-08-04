import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r'D:\Program Files\Obsidian\repository\ArcherArticle\02-稿件库\02-已发布稿件归档\你越强调AI越不听话--Prompt工程里的恶性循环-20260730'
files = [
    (base + r'\01-访谈记录.md', '访谈记录'),
    (base + r'\05-发布包\长文发布包.md', '长文发布包'),
]
for path, name in files:
    print('\n' + '='*25 + ' ' + name + ' ' + '='*25)
    try:
        with open(path, encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print('READ ERROR:', e)
