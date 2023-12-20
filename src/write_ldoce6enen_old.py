#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil
import time
from collections import Counter

'''
todo, rename to simple_test.py
'''

# list里面有没有重复的
def find_duplicates(strings: list[str]) -> list[str]:
    counter = Counter(strings)
    return [s for s, cnt in counter.items() if cnt > 1]

def check_phrase_sequence_in_heading(path: str):
    phrase_pattern  = re.compile(r'@@PHRASE(\d+)@@')
    atat_pattern = re.compile(r'@@')

    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            # 检查 不允许行首或行尾 @@
            if line.startswith('@@') or line.endswith('@@'):
                assert False, (f"line {line_no}: line cannot start or end with @@")
            
            # 检查PHRASE<n>里面n是从0开始, 递增
            nums = [int(n) for n in phrase_pattern .findall(line)]

            # 必须至少有一个 PHRASE<n>
            if not nums:
                assert False, f"line {line_no}: no PHRASE found"

            # 编号必须从 0 连续递增
            expected = list(range(0, len(nums)))
            assert nums == expected, f"[ERROR] line {line_no}: PHRASE 顺序不对, got={nums}, expected={expected}"
            
            # 检查@@PHRASE<n>@@ 个数是 @@ 个数的一半
            phrase_heads = len(phrase_pattern.findall(line))
            atat_count = len(atat_pattern.findall(line))
            if phrase_heads*2 != atat_count:
                assert False, f"line {line_no}: PHRASE / @@ mismatch, PHRASE={phrase_heads}, @@={atat_count}"    
    
    print("PASS.")

def do_the_job():
    start_time = time.time()
    print("working...")

    print("\nfind_duplicates...")
    with open("lla_plus_headings.txt", "r", encoding="utf-8") as f:
        ordered_headings = [line.rstrip("\n") for line in f]
    print(find_duplicates(ordered_headings))

    print("\ncheck_phrase_sequence_in_heading...")
    check_phrase_sequence_in_heading("lla_plus_headings.txt")

    print("\nSummary:")
    print("Done with the job, totally takes %s s" % (time.time() - start_time))

if __name__ == '__main__':
    do_the_job()
