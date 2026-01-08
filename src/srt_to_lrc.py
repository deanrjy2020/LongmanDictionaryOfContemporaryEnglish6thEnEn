#!/usr/bin/env python
# encoding: utf-8
'''
@Author  : 草木零
@Software: PyCharm
@File    : SrtToLrc.py
@Time    : 2025/6/27 11:19
@desc	 : 将srt文件转换成lrc文件，srt文件格式如下：
1
00:00:05,240 --> 00:00:08,520
Hello. This is Six Minute
你好。 这是

2
00:00:08,520 --> 00:00:09,840
English from BBC
来自 BBC
'''

import re
import os

def srt_to_lrc(srt_path, lrc_path):
    """将SRT文件转换为LRC格式"""
    try:
        # 读取SRT文件内容
        with open(srt_path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 '{srt_path}'")
        return
    except Exception as e:
        print(f"错误：读取文件时出错 - {e}")
        return

    # 分割SRT文件中的每个字幕块，以字幕块中间的空行为分隔符
    srt_blocks = re.split(r'\n\s*\n', srt_content.strip()) #['1\n00:00:05,240 --> 00:00:08,520\nHello. This is Six Minute\n你好。 这是', ...]

    lrc_lines = []

    for block in srt_blocks:
        if not block.strip():
            continue

        # 分割字幕块为序号、时间和文本
        lines = block.strip().split('\n')

        # 提取时间行（通常是第二行）
        if len(lines) < 2:
            continue

        time_line = lines[1]
        text_lines = lines[2:]

        # 提取开始时间和结束时间
        time_match = re.search(r'(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)', time_line)
        if not time_match:
            continue

        start_time = time_match.group(1)
        # end_time = time_match.group(2)  # LRC格式通常只需要开始时间

        # 转换SRT时间格式（00:00:00,000）为LRC时间格式（[mm:ss.xx]）
        # 解析小时、分钟、秒和毫秒
        h, m, s_ms = start_time.split(':')
        s, ms = s_ms.split(',')

        # 计算总分钟和秒
        total_minutes = int(h) * 60 + int(m)
        seconds = float(s) + float(ms) / 1000

        # 格式化为LRC时间标签
        #06.3f 是格式化指令。f：将数值格式化为浮点数。.3：保留 3 位小数（例如 15.3 → 15.300）。6：总宽度为 6 位（包括小数点和小数部分）。0：用 0 填充空位。
        lrc_time = f"[{total_minutes:02d}:{seconds:06.3f}]"

        # 合并文本行
        text = ' '.join(text_lines).strip()

        # 添加到LRC行列表
        if text:
            lrc_lines.append(f"{lrc_time}{text}")

    #print(lrc_lines)

    # 构建LRC文件路径（保持原文件名，只改后缀）
    # base_name, _ = os.path.splitext(srt_path)
    # lrc_path = f"{base_name}.lrc"

    try:
        # 写入LRC文件
        with open(lrc_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lrc_lines))
        print(f"转换成功！LRC文件已保存至: {lrc_path}")
    except Exception as e:
        print(f"错误：写入LRC文件时出错 - {e}")


# 批量重命名
if __name__ == "__main__":

    # debug用，单个文件示例，修改为你的SRT文件路径
    # srt_path = './Our love of pets_我们对宠物的爱.srt'
    # srt_to_lrc(srt_path)

    srt_to_lrc("lla_tts/mp3/1-5.srt", "lla_tts/mp3/1-5.lrc")
    # 需重命名的文件所在的文件夹路径
    # dir_path = r'D:\Files\英语mp3\六分钟英语'
    # # path有多少个文件，就会循环多少次
    # for file in os.listdir(dir_path):  # 返回包含文件名的列表
    #     srt_path = os.path.join(dir_path, file)
    #     # print(srt_path)
    #     srt_to_lrc(srt_path)

    # # 删除原来的srt文件
    # for file in os.listdir(dir_path):  # 返回包含文件名的列表
    #     srt_path = os.path.join(dir_path, file)
    #     name, suffix = os.path.splitext(file)
    #     print(name, suffix)
    #     if suffix == '.srt':
    #         os.remove(srt_path)

