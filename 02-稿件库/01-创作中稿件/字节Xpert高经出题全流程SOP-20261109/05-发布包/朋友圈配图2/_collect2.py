# -*- coding: utf-8 -*-
"""9期截止冲刺朋友圈：9图按发布顺序收录到 朋友圈配图2/（01 通知卡已渲染，02-09 拷贝）"""
import shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'D:\Program Files\Obsidian\repository\ArcherArticle\02-稿件库\01-创作中稿件'
PUB  = ROOT + r'\字节Xpert高经出题全流程SOP-20261109\05-发布包'
DST  = PUB + r'\朋友圈配图2'

pairs = [
    (PUB + r'\imgs\交付交易信息\10-68.png',                                DST + r'\02-成交-第10单68新行业.png'),
    (PUB + r'\imgs\交付交易信息\12-进群直接找付费学习参与陪跑.png',          DST + r'\03-自主进群-直接找陪跑.png'),
    (PUB + r'\imgs\交付交易信息\11-10的补差价不白嫖问题.png',                DST + r'\04-升级-补差价231升299.png'),
    (PUB + r'\imgs\交付交易信息\13-299-追求高效付费陪跑还乐意加钱.png',       DST + r'\05-成交-299高效客户.png'),
    (PUB + r'\朋友圈配图\07-战绩-一次通过6题.png',                          DST + r'\06-战绩-一次通过6题.png'),
    (PUB + r'\朋友圈配图\08-10道关完整地图.png',                            DST + r'\07-10道关完整地图.png'),
    (PUB + r'\小红书配图\05-免费额度.png',                                  DST + r'\08-免费额度.png'),
    (PUB + r'\朋友圈配图\09-群二维码.png',                                  DST + r'\09-群二维码.png'),
]
for s, d in pairs:
    assert os.path.exists(s), '源图缺失: ' + s
    shutil.copy2(s, d)

print('朋友圈配图2/ 目录现状：')
for f in sorted(os.listdir(DST)):
    p = DST + '\\' + f
    print(f'  {os.path.getsize(p)//1024:>5}KB  {f}')
