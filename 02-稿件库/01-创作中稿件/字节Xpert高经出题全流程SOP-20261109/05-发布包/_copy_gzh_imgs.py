# -*- coding: utf-8 -*-
"""拷贝公众号长文所需 6 张配图到 imgs/（简化命名，供 gzh-design 嵌图脚本使用）"""
import shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')
root = r'D:\Program Files\Obsidian\repository\ArcherArticle\02-稿件库\01-创作中稿件'
pairs = [
    (root + r'\字节Xpert高经出题全流程SOP-20261109\assets\01-注册-01-注册登录页（使用我的邀请链接）.png', 'imgs/gzh-01-zhuce.png'),
    (root + r'\字节Xpert高经出题全流程SOP-20261109\assets\05-首轮-01-跑完后的工作目录.png', 'imgs/gzh-02-mulu.png'),
    (root + r'\国庆出题战报时薪5000-20261107\05-发布包\imgs\03-机评水分数据.png', 'imgs/gzh-03-jiping.png'),
    (root + r'\我在字节Xpert接任务收获和实操心得-20261106\05-发布包\imgs\06-质检流程.png', 'imgs/gzh-04-zhijian.png'),
    (root + r'\字节Xpert高经出题全流程SOP-20261109\assets\11-结算-01-FDE分流群通知.png', 'imgs/gzh-05-fde.png'),
    (root + r'\我在字节Xpert接任务收获和实操心得-20261106\05-发布包\imgs\08-邀请码.png', 'imgs/gzh-06-yqm.png'),
]
os.makedirs('imgs', exist_ok=True)
for s, d in pairs:
    assert os.path.exists(s), '源图缺失: ' + s
    shutil.copy2(s, d)
print('\n'.join(f'{os.path.getsize(d)//1024}KB  {d}' for s, d in pairs))
