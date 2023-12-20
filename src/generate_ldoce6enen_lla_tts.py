#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import asyncio
import edge_tts
from edge_tts import Communicate
import re

'''

python -m pip install edge-tts

run: python src/generate_ldoce6enen_lla_tts.py
'''

#================================================
# 每个mp3 5个topic, 固定
topics_per_file = 5
max_topic_id = 4953

# started with 1, 1 ~ 4953 
start_topic_id = 1
# 每次生成10个文件, 10*5 = 50个topic
file_num = 10

# 单单生成txt, 用于检查, 不生成mp3 (太慢)
dry_run = True
if dry_run:
    start_topic_id = 1
    file_num = 991 # max file num

input_txt = "lla_sections.txt"
use_voice = "en-US-AndrewNeural"
#use_voice = "en-US-GuyNeural"
#use_voice = "en-US-BrianNeural"
#use_voice = "en-US-ChristopherNeural"
#use_voice = "en-US-EricNeural"
#use_voice = "en-US-RogerNeural"
#use_voice = "en-US-SteffanNeural"

debug_replacement_cnt = 0

NEW_LINE = '\n'
#BEFORE_PHRASE_BREAK = '<break time="1s"/>'
BEFORE_PHRASE_BREAK = '\n\n'
BEFORE_DEFINE_BREAK = '\n\n'
BEFORE_THESPROPFORM_BREAK = '\n\n'
BEFORE_GLOSS_BREAK = '\n'
BEFORE_VARIANT_BREAK = '\n'
BEFORE_EXAMPLE_BREAK = '\n\n'
END_SECTION_BREAK = '\n\n'

def read_n_lines_from_lla(path: str, start_line: int, n: int) -> str:
    """
    Read n lines starting from start_line (1-based index).
    Return (raw_text, processed_text)
    """
    raw_lines = []
    processed_lines = []

    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            if line_num < start_line:
                continue
            if len(raw_lines) >= n:
                break

            raw_line = line.rstrip('\n')
            raw_lines.append(raw_line)

            line = raw_line

            # 如果是 '@@/', / 不要了.
            global debug_replacement_cnt
            debug_replacement_cnt += line.count("@@VARIANT@@/")
            line = line.replace("@@VARIANT@@/", "@@VARIANT@@")
            # 唯一一处'/@@'情况, 本来就是小bug, / 不应该有的.
            line = line.replace("most hated man./@@", "most hated man.@@")
            assert '@@/' not in line, f"line_num={line_num}, line={line}"
            assert '/@@' not in line, f"line_num={line_num}, line={line}"
            # 替换 / 为 or
            line = line.replace(" / ", " or ")
            line = line.replace(" /", " or ")
            line = line.replace("/ ", " or ")
            line = line.replace("/", " or ")
            assert "/" not in line, line

            # todo, 用简单的
            line = line.replace("@@DEFINE@@", f"{BEFORE_DEFINE_BREAK}This means ")
            # 用which means
            line = line.replace("@@GLOSS@@", f"{BEFORE_GLOSS_BREAK}In other words, {NEW_LINE}")
            # todo, 啰嗦, 换一个短的
            line = line.replace("@@VARIANT@@", f"{BEFORE_VARIANT_BREAK}You can also hear people say: {NEW_LINE}")

            # todo, 用 collocation 1.2... ?
            line = line.replace("@@THESPROPFORM0@@", f"{BEFORE_THESPROPFORM_BREAK}You can also say: {NEW_LINE}")
            line = line.replace("@@THESPROPFORM1@@", f"{BEFORE_THESPROPFORM_BREAK}You may also hear phrases like: {NEW_LINE}")
            line = line.replace("@@THESPROPFORM2@@", f"{BEFORE_THESPROPFORM_BREAK}Another common phrase is: {NEW_LINE}")
            line = line.replace("@@THESPROPFORM3@@", f"{BEFORE_THESPROPFORM_BREAK}People often say: {NEW_LINE}")
            line = line.replace("@@THESPROPFORM4@@", f"{BEFORE_THESPROPFORM_BREAK}Another way to put it is: {NEW_LINE}")
            # 剩下的用一样
            line = re.sub(r"@@THESPROPFORM\d+@@", f"{BEFORE_THESPROPFORM_BREAK}You might also hear: {NEW_LINE}", line)
            # 都处理干净了
            assert not re.search(r"@@THESPROPFORM\d+@@", line), line

            line = line.replace("@@EXAMPLE0@@", f"{BEFORE_EXAMPLE_BREAK}For example: {NEW_LINE}")
            line = line.replace("@@EXAMPLE1@@", f"{BEFORE_EXAMPLE_BREAK}Another example: {NEW_LINE}")
            # 第3个开始直接用 example 3, todo
            line = line.replace("@@EXAMPLE2@@", f"{BEFORE_EXAMPLE_BREAK}And one more example: {NEW_LINE}")
            line = line.replace("@@EXAMPLE3@@", f"{BEFORE_EXAMPLE_BREAK}Here's another example: {NEW_LINE}")
            line = line.replace("@@EXAMPLE4@@", f"{BEFORE_EXAMPLE_BREAK}Example five: {NEW_LINE}")
            line = line.replace("@@EXAMPLE5@@", f"{BEFORE_EXAMPLE_BREAK}Example six: {NEW_LINE}")
            line = line.replace("@@EXAMPLE6@@", f"{BEFORE_EXAMPLE_BREAK}Example seven: {NEW_LINE}")
            line = line.replace("@@EXAMPLE7@@", f"{BEFORE_EXAMPLE_BREAK}Example eight: {NEW_LINE}")
            # 都处理干净了
            assert not re.search(r"@@EXAMPLE\d+@@", line), line

            # todo, 直接用phrase one, two...
            line = line.replace("@@PHRASE0@@", f"{BEFORE_PHRASE_BREAK}Let's start with: {NEW_LINE}")
            line = line.replace("@@PHRASE1@@", f"{BEFORE_PHRASE_BREAK}Let's talk about the next one: {NEW_LINE}")
            line = line.replace("@@PHRASE2@@", f"{BEFORE_PHRASE_BREAK}Let's look at the next one: {NEW_LINE}")
            # 剩下的用一样
            line = re.sub(r"@@PHRASE\d+@@", f"{BEFORE_PHRASE_BREAK}Next, {NEW_LINE}", line)

            # line_num = topic id
            processed_lines.append(f"Topic {line_num}: {line} {END_SECTION_BREAK}")
    
    processed_lines.append("That's all for this set of topics.")
    return (
        "\n".join(raw_lines),
        "\n".join(processed_lines),
        )

def save_text(path: str, text: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

async def text_to_mp3(
    text: str,
    output_mp3: str,
    voice: str,
    rate: str,
    volume: str
):
    """
    Convert text to speech using Edge TTS and save as mp3.
    """
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume,
    )
    await communicate.save(output_mp3)


def do_the_job():
    # 创建文件夹（已存在不会报错）
    mp3_folder = "lla_tts/mp3"
    txt_folder = "lla_tts/txt"
    os.makedirs(mp3_folder, exist_ok=True)
    os.makedirs(txt_folder, exist_ok=True)
    
    for i in range(file_num):
        start = start_topic_id + i * topics_per_file
        end = start + topics_per_file - 1
        if end >= max_topic_id:
            end = max_topic_id

        raw_text, tts_text = read_n_lines_from_lla(
            input_txt,
            start_line=start,
            n=topics_per_file,
        )

        if not raw_text:
            print(f"No text for topics {start}-{end}, stop.")
            break

        base = f"{start}-{end}"
        # 文件路径
        raw_txt_path = os.path.join(txt_folder, f"{base}_lla.txt")
        tts_txt_path = os.path.join(txt_folder, f"{base}_tts.txt")
        mp3_path     = os.path.join(mp3_folder, f"{base}.mp3")

        # 保存
        save_text(raw_txt_path, raw_text)
        save_text(tts_txt_path, tts_text)
        print(f"Raw text saved to: {raw_txt_path}")
        print(f"TTS text saved to: {tts_txt_path}")

        if dry_run:
            continue

        print(f"\n=== Generating {mp3_path} ===")
        asyncio.run(
            text_to_mp3(
                text=tts_text,
                output_mp3=mp3_path,
                voice=use_voice,
                rate="-20%", # rate: str = "+0%",
                volume="+0%",
            )
        )
        print(f"MP3 saved to: {mp3_path}")

if __name__ == "__main__":
    start_time = time.time()
    do_the_job()
    print(f"replacement cnt = {debug_replacement_cnt}")
    print("Done, takes %.2f s" % (time.time() - start_time))
