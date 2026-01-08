#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import asyncio
import edge_tts
from edge_tts import Communicate
import re

import srt_to_lrc

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
# 每次生成20个文件, 20*5 = 100个topic
file_num = 20

# 单单生成txt, 用于检查, 不生成mp3 (太慢)
dry_run = False
if dry_run:
    start_topic_id = 1
    file_num = 991 # max file num

input_txt = "results/lla_sections_oneline.txt"
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

NUM_WORDS = [
    "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen"
]

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

            # 唯一一处'/@@'情况, 本来就是小bug, / 不应该有的. todo, 在L6里面修正
            line = line.replace("most hated man./@@", "most hated man.@@")
            assert '@@/' not in line, f"line_num={line_num}, line={line}"
            assert '/@@' not in line, f"line_num={line_num}, line={line}"
            # 替换 / 为 or
            line = line.replace(" / ", " or ")
            line = line.replace(" /", " or ")
            line = line.replace("/ ", " or ")
            line = line.replace("/", " or ")
            assert "/" not in line, line

            # 替换 PHRASE<n>
            # line = line.replace("@@PHRASE0@@", f"{BEFORE_PHRASE_BREAK}Phrase one: {NEW_LINE}")
            def repl_phrase(m):
                idx = int(m.group(1))
                # 最多14个phrase, 即 0 ~ 13
                assert 0 <= idx <= 13, f"phrase index out of range: {idx}"
                return f"{BEFORE_PHRASE_BREAK}Phrase {NUM_WORDS[idx]}: {NEW_LINE}"
            line = re.sub(r"@@PHRASE(\d+)@@", repl_phrase, line)
            assert not re.search(r"@@PHRASE\d+@@", line), line

            # 替换 VARIANT
            # 先处理已经带 also 的情况，避免重复
            assert '@@VARIANT@@also' not in line, f"line={line}"
            #line = line.replace("@@VARIANT@@also ", f"{BEFORE_VARIANT_BREAK}Also: {NEW_LINE}")
            # 再处理普通 VARIANT，统一加 also
            line = line.replace("@@VARIANT@@", f"{BEFORE_VARIANT_BREAK}Also: {NEW_LINE}")

            # 替换 DEFINE
            line = line.replace("@@DEFINE@@", f"{BEFORE_DEFINE_BREAK}This means ")

            # 替换 EXAMPLE<n>
            # line = line.replace("@@EXAMPLE0@@", f"{BEFORE_EXAMPLE_BREAK}Example one: {NEW_LINE}")
            def repl_example(m):
                idx = int(m.group(1))
                assert 0 <= idx <= 7, f"example index out of range: {idx}"
                return f"{BEFORE_EXAMPLE_BREAK}Example {NUM_WORDS[idx]}: {NEW_LINE}"
            line = re.sub(r"@@EXAMPLE(\d+)@@", repl_example, line)
            assert not re.search(r"@@EXAMPLE\d+@@", line), line

            # 替换 THESPROPFORM<n>
            #line = line.replace("@@THESPROPFORM0@@", f"{BEFORE_THESPROPFORM_BREAK}You can say: {NEW_LINE}")
            def repl_thespropform(m):
                idx = int(m.group(1))
                assert 0 <= idx <= 10, f"alt index out of range: {idx}"
                # Alt = Alternative expressions (替代表达)
                return f"{BEFORE_THESPROPFORM_BREAK}Alt {NUM_WORDS[idx]}: {NEW_LINE}"
            line = re.sub(r"@@THESPROPFORM(\d+)@@", repl_thespropform, line)
            assert not re.search(r"@@THESPROPFORM\d+@@", line), line

            # 替换 GLOSS
            line = line.replace("@@GLOSS@@", f"{BEFORE_GLOSS_BREAK}Meaning: {NEW_LINE}")

            # todo, 后面修正派生词后用Form (词形变化)

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

'''
examples:
https://github.com/rany2/edge-tts/blob/master/examples/sync_audio_streaming_with_predefined_voice_subtitles.py

https://blog.csdn.net/qq_37292005/article/details/148950758
'''
#async def text_to_mp3(
def text_to_mp3(
    text: str,
    output_mp3: str,
    output_srt: str,
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

    submaker = edge_tts.SubMaker()
    with open(output_mp3, "wb") as file:
        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

    with open(output_srt, "w", encoding="utf-8") as file:
        file.write(submaker.get_srt())
    # await communicate.save(
    #     output_mp3
    # )


def do_the_job():
    # 创建文件夹（已存在不会报错）
    mp3_folder = "lla_tts/mp3"
    txt_folder = "lla_tts/txt"
    os.makedirs(mp3_folder, exist_ok=True)
    os.makedirs(txt_folder, exist_ok=True)
    
    for i in range(file_num):
        print(f"\n")
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
        srt_path     = os.path.join(txt_folder, f"{base}.srt")
        lrc_path     = os.path.join(mp3_folder, f"{base}.lrc")
        mp3_path     = os.path.join(mp3_folder, f"{base}.mp3")

        # 保存
        save_text(raw_txt_path, raw_text)
        save_text(tts_txt_path, tts_text)
        print(f"Raw text saved to: {raw_txt_path}")
        print(f"TTS text saved to: {tts_txt_path}")

        if dry_run:
            continue

        print(f"=== Generating {mp3_path} ===")
        #asyncio.run(
        text_to_mp3(
            text=tts_text,
            output_mp3=mp3_path,
            output_srt=srt_path,
            voice=use_voice,
            rate="-20%", # rate: str = "+0%",
            volume="+0%",
        )
        #)
        srt_to_lrc.srt_to_lrc(srt_path, lrc_path)

        print(f"MP3 saved to: {mp3_path}")

if __name__ == "__main__":
    start_time = time.time()
    do_the_job()
    assert debug_replacement_cnt == 0, f"debug_replacement_cnt = {debug_replacement_cnt}"
    print("Done, takes %.2f s" % (time.time() - start_time))
