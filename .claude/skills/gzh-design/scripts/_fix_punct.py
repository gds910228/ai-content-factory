import re, sys

path = sys.argv[1]
with open(path, encoding='utf-8') as f:
    html = f.read()

# CJK: ideographs + CJK symbols/punctuation + fullwidth forms + curly quotes
cjk = r'[一-鿿　-〿＀-￯“”‘’]'

# half -> full
pairs = [(',', '，'), (':', '：'), ('?', '？'), ('!', '！'), (';', '；'), ('.', '。')]
out = html
for hw, fw in pairs:
    if hw == '.':
        # only preceded by CJK (avoid decimals like 1.5, file.png)
        out = re.sub(rf'(?<={cjk})\.', fw, out)
    else:
        # preceded by CJK OR followed by CJK
        out = re.sub(rf'(?<={cjk}){re.escape(hw)}', fw, out)
        out = re.sub(rf'{re.escape(hw)}(?={cjk})', fw, out)

with open(path, 'w', encoding='utf-8') as f:
    f.write(out)

# count changes
diff = sum(1 for a, b in zip(html, out) if a != b)
print(f"done, char-level diffs (approx): {diff}")
