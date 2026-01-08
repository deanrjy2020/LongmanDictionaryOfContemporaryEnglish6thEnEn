#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen import MutagenError
from difflib import SequenceMatcher

'''
pip install mutagen

python src/mp3_stat.py

'''
#=============================================================
# 检测mp3和lrc大致匹配

time_pattern = re.compile(r"\[(\d+):(\d+)(?:\.(\d+))?\]")
def parse_lrc_times(lrc_path):
    times = []
    with open(lrc_path, "r", encoding="utf-8") as f:
        for line in f:
            m = time_pattern.search(line)
            if m:
                mm, ss, ms = m.groups()
                t = int(mm) * 60 + int(ss) + (int(ms) / 100 if ms else 0)
                times.append(t)
    return times


def rough_match(mp3_path, lrc_path):
    #两个文件里的时间长度大致一致
    mp3_len = MP3(mp3_path).info.length
    times = parse_lrc_times(lrc_path)

    if not times:
        return False, f"LRC has no timestamps, {mp3_path}"

    lrc_len = times[-1]
    ratio = abs(mp3_len - lrc_len) / mp3_len

    if ratio > 0.1:  # 超过 10%
        return False, f"Duration mismatch ({mp3_len:.1f}s vs {lrc_len:.1f}s), {mp3_path}"

    return True, "Duration roughly matches"

#=============================================================
# 检测lrc内容和tts一致

def validate_lrc_tts(mp3_path: str):
    # ---------- 校验 mp3 文件名 ----------
    base = os.path.basename(mp3_path)
    m = re.fullmatch(r"(\d+)-(\d+)\.mp3", base)
    assert m, f"Invalid mp3 filename format: {base}"

    abc, _ = m.groups()

    # ---------- 构造 lrc 路径 ----------
    lrc_path = mp3_path[:-4] + ".lrc"
    assert os.path.exists(lrc_path), f"LRC file not found: {lrc_path}"

    # 得到tts 路径
    lrc_dir = os.path.dirname(lrc_path)
    parent_dir = os.path.dirname(lrc_dir)
    grand_parent = os.path.dirname(parent_dir)
    tts_path = os.path.join(grand_parent, "txt", f"{abc}-{_}_tts.txt")
    assert os.path.exists(tts_path), f"TTS not found: {tts_path}"

    # ---------- 工具函数: 去掉时间戳 ----------
    def strip_timestamp(line: str) -> str:
        # 去掉最前面的 [....]
        return re.sub(r"^\[[^\]]+\]", "", line).strip()

    # ---------- 读取 lrc ----------
    with open(lrc_path, "r", encoding="utf-8") as f:
        lrc_lines = [line.rstrip("\n") for line in f if line.strip()]
    assert len(lrc_lines) >= 3, "LRC file must have at least 3 non-empty lines"
    
    lrc_text = [strip_timestamp(line) for line in lrc_lines]
    
    # ---------- 第一行 ----------
    first = lrc_text[0]
    expected_prefix = f"Topic {abc}:"
    assert first.startswith(expected_prefix), (
        f"First line invalid.\n"
        f"Expected prefix: '{expected_prefix}'\n"
        f"Actual: '{first}'"
    )
    
    # ---------- 第二行 ----------
    second = lrc_text[1]
    assert second == "Phrase one:", (
        f"Second line invalid.\n"
        f"Expected: 'Phrase one:'\n"
        f"Actual: '{second}'"
    )
    
    # ---------- 最后一行 ----------
    last = lrc_text[-1]
    assert last == "That's all for this set of topics.", (
        f"Last line invalid.\n"
        f"Expected: \"That's all for this set of topics.\"\n"
        f"Actual: '{last}'"
    )

    # 合成lrc到一个string, 里面的空格全部不要
    # 1791lrc里面的`(在句子中间)又没有消失, 也不要了,
    lrc_content = ''.join(line.replace(' ', '').replace('`','').rstrip('\n') for line in lrc_text)

    # ---------- 读取 tts, 放到一个str, , 里面的空格全部不要
    with open(tts_path, "r", encoding="utf-8") as f:
        # 2541tts里面的`(句子开头)应该是', 但是生成的lrc会消失, 比较的时候不要
        tts_content = ''.join(line.replace(' ', '').replace('`','').rstrip('\n') for line in f)


    if lrc_content != tts_content:
        with open('lrc_error.txt', 'w', encoding='utf-8') as f:
            f.write(lrc_content)
        with open('tts_error.txt', 'w', encoding='utf-8') as f:
            f.write(tts_content)
        assert False, f"file {base}"
      
    return True

#=============================================================
# mp3 统计信息

def format_time(seconds: float) -> str:
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def scan_mp3_dir(root_dir: str):
    total_seconds = 0.0
    mp3_count = 0
    failed_files = []
    rough_compared_cnt = 0

    assert os.path.isdir(root_dir), f"Not a directory: {root_dir}"
    for root, _, files in os.walk(root_dir):
        for name in files:
            if not name.lower().endswith(".mp3"):
                continue

            #print(f"working on {name}")

            # 检测mp3和lrc大致匹配
            mp3_path = os.path.join(root, name)
            mp3 = Path(mp3_path)
            lrc_path = mp3.with_suffix(".lrc")
            ret, msg = rough_match(mp3_path, lrc_path)
            if ret == False:
                print(msg)
            rough_compared_cnt += 1

            # 检测lrc内容和tts里面一致
            validate_lrc_tts(mp3_path)
            
            try:
                audio = MP3(mp3_path)
                duration = audio.info.length  # seconds (float)

                total_seconds += duration
                mp3_count += 1

            except MutagenError as e:
                failed_files.append((mp3_path, str(e)))
            except Exception as e:
                failed_files.append((mp3_path, str(e)))

    avg_seconds = total_seconds / mp3_count if mp3_count > 0 else 0

    return {
        "count": mp3_count,
        "total_seconds": total_seconds,
        "avg_seconds": avg_seconds,
        "failed": failed_files,
        "rough_compared_cnt": rough_compared_cnt
    }


if __name__ == "__main__":
    start_time = time.time()

    target_dir = r"D:\renjiayuan1314\Comm\LLA_TTS\mp3"
    result = scan_mp3_dir(target_dir)

    print("MP3 count          :", result["count"])
    print("Total duration     :", format_time(result["total_seconds"]))
    print("Average            :", format_time(result["avg_seconds"]))
    print("rough_compared_cnt :", result["rough_compared_cnt"])

    if result["failed"]:
        print("\nFailed files:")
        for path, err in result["failed"]:
            print(" -", path)

    print("Done with the job, totally takes %.2f s" % (time.time() - start_time))