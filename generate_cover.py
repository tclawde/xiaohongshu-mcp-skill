#!/usr/bin/env python3
"""标题封面生成器 - 精确换行"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_title_cover(title, output_path="/tmp/title_cover.jpg"):
    """简洁标题封面"""
    width, height = 900, 1600
    img = Image.new('RGB', (width, height), color=(255, 248, 220))
    draw = ImageDraw.Draw(img)
    
    # 横线
    for i in range(140, height-100, 45):
        draw.line([(100, i), (width-50, i)], fill=(240, 235, 220), width=2)
    
    # 左边红线
    draw.line([(90, 110), (90, height-110)], fill=(200, 50, 50), width=5)
    
    # 加载字体
    font = None
    for fp in ["/System/Library/Fonts/PingFang.ttc"]:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 90)
                break
            except:
                pass
    
    if not font:
        font = ImageFont.load_default()
    
    # 精确换行
    lines = []
    current = ""
    margin = 120  # 左右留白
    
    for char in title:
        test_line = current + char
        # 获取实际文字边界
        left, top, right, bottom = font.getbbox(test_line)
        text_width = right - left
        
        if text_width <= width - margin * 2:
            current = test_line
        else:
            if current:
                lines.append(current)
            current = char
    
    if current:
        lines.append(current)
    
    # 绘制
    y = height // 3
    for i, line in enumerate(lines):
        left, top, right, bottom = font.getbbox(line)
        text_width = right - left
        x = (width - text_width) / 2
        draw.text([x, y + i * 105], line, font=font, fill=(0, 0, 0))
    
    img.save(output_path, quality=90)
    print(f"封面: {output_path} ({len(lines)}行)")
    return output_path

if __name__ == "__main__":
    long_title = "美院学生都在用AI工具做作业？我就笑了"
    print(f"测试: {long_title}")
    create_title_cover(long_title)
