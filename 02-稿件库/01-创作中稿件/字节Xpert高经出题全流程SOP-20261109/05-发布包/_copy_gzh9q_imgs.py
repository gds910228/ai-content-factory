# -*- coding: utf-8 -*-
"""按 9期宣传文 配图清单收录 9 张图到 imgs/（gzh9q-* 命名）"""
import shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'D:\Program Files\Obsidian\repository\ArcherArticle\02-稿件库\01-创作中稿件'
PUB  = ROOT + r'\字节Xpert高经出题全流程SOP-20261109\05-发布包'
DST  = PUB + r'\imgs'

pairs = [
    (PUB + r'\朋友圈配图\01-平台通知-9期开启10期或暂缓.png',      DST + r'\gzh9q-01-tongzhi.png'),
    (PUB + r'\小红书配图\05-免费额度.png',                        DST + r'\gzh9q-02-mianfei-edu.png'),
    (PUB + r'\imgs\交付交易信息\9-68.png',                        DST + r'\gzh9q-03-68-dangtian.png'),
    (PUB + r'\imgs\交付交易信息\7-1的交付答疑和自测达标结果.png',  DST + r'\gzh9q-04-zice-dabiao.png'),
    (PUB + r'\imgs\交付交易信息\6-299.png',                       DST + r'\gzh9q-05-299-danan.png'),
    (PUB + r'\imgs\交付交易信息\8-1的其他行业提示词咨询.png',       DST + r'\gzh9q-06-fugou.png'),
    (PUB + r'\小红书配图\02-完整地图-每关一句话.png',               DST + r'\gzh9q-07-ditu.png'),
    (PUB + r'\小红书配图\07-适合谁劝退谁.png',                     DST + r'\gzh9q-08-quantui.png'),
    (ROOT + r'\我在字节Xpert接任务收获和实操心得-20261106\05-发布包\imgs\08-邀请码.png', DST + r'\gzh9q-09-yaoqingma.png'),
]
for s, d in pairs:
    assert os.path.exists(s), '源图缺失: ' + s
    shutil.copy2(s, d)

print('imgs/ 目录 gzh9q-* 现状：')
for f in sorted(os.listdir(DST)):
    if f.startswith('gzh9q'):
        print(f'  {os.path.getsize(DST + chr(92) + f)//1024:>5}KB  {f}')
