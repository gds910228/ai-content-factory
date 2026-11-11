# -*- coding: utf-8 -*-
"""按朋友圈9图发布顺序收录所需配图到 朋友圈配图/ 目录"""
import shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'D:\Program Files\Obsidian\repository\ArcherArticle\02-稿件库\01-创作中稿件'
PUB = ROOT + r'\字节Xpert高经出题全流程SOP-20261109\05-发布包'
DST = PUB + r'\朋友圈配图'

# 1) 通知卡 00- 改名为 01-（统一序号）
old, new = DST + r'\00-平台通知-9期开启10期或暂缓.png', DST + r'\01-平台通知-9期开启10期或暂缓.png'
if os.path.exists(old):
    os.rename(old, new)

pairs = [
    (PUB + r'\imgs\交付交易信息\9-68.png',                             DST + r'\02-成交-9期当天68单.png'),
    (PUB + r'\imgs\交付交易信息\7-1的交付答疑和自测达标结果.png',        DST + r'\03-客户自测达标结果.png'),
    (PUB + r'\imgs\交付交易信息\6-299.png',                            DST + r'\04-成交-299陪跑第二单.png'),
    (PUB + r'\imgs\交付交易信息\3-68.png',                             DST + r'\05-成交-九期新人68单.png'),
    (PUB + r'\imgs\交付交易信息\8-1的其他行业提示词咨询.png',            DST + r'\06-复购-其他行业咨询.png'),
    (ROOT + r'\国庆出题战报时薪5000-20261107\05-发布包\imgs\02-媳妇一次通过6题.png', DST + r'\07-战绩-一次通过6题.png'),
    (PUB + r'\小红书配图\02-完整地图-每关一句话.png',                    DST + r'\08-10道关完整地图.png'),
]
for s, d in pairs:
    assert os.path.exists(s), '源图缺失: ' + s
    shutil.copy2(s, d)

print('朋友圈配图 目录现状：')
for f in sorted(os.listdir(DST)):
    p = DST + '\\' + f
    print(f'  {os.path.getsize(p)//1024:>5}KB  {f}')
print('\n待补：09-群二维码（自备后放入本目录即可）')
