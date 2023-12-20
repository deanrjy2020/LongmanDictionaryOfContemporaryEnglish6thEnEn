#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import re
import shutil
import struct
import os
import time
import hashlib
import struct
from bs4 import BeautifulSoup, Tag
import json

'''

stardict from: https://forum.freemdict.com/t/topic/42061/29

- 解析stardict的dict和idx两个文件, 得到mtml文本
- 解析html文本的到LLA
    <k>	                词头, keyword
    <dtrn>	            音标, 词性, 下一行定义c="darkblue">
    <ex>	            例句
    c=crimson <dtrn>    搭配, collocation
    <i>                 搭配的定义
    c="darkgoldenrod">  变体延伸, 词性
    <kref>	            相关词
    <c ...>	颜色/样式，可忽略
    <blockquote>	结构层级，可忽略

run: PYTHONUTF8=1 python src/generate_stardict_lla.py |& tee stardict_log.txt

'''

tar_path = "data/stardict-Longman_Language_Activator_2nd_Ed-2.4.2.tar.7z"
dict_path = "data/Longman Language Activator 2nd Ed.dict"
idx_path  = "data/Longman_Language_Activator_2nd_Ed.idx"

html_path = "stardict.html"

output_path = "stardict.txt"

debug = False

def parse_star_dict():
    tar_md5 = hashlib.md5(open(tar_path,'rb').read()).hexdigest()
    assert tar_md5 == '558ed9b3b70a928d593711d80f41ccb8'
    dict_md5 = hashlib.md5(open(dict_path,'rb').read()).hexdigest()
    assert dict_md5 == '06d7dcfb1401484ef758932a89377a97'
    idx_md5 = hashlib.md5(open(idx_path,'rb').read()).hexdigest()
    assert idx_md5 == '08d1c08c839c41911b33824649999e0f'

    dict_file = open(dict_path, "rb")
    idx_file = open(idx_path, "rb")

    def read_cstring(f):
        s = bytearray()
        while True:
            c = f.read(1)
            if c == b"":                 # EOF
                if s:
                    return s.decode("utf-8", errors="ignore")
                else:
                    raise EOFError
            if c == b"\x00":
                return s.decode("utf-8", errors="ignore")
            s.extend(c)


    # 文件大小（用于安全检查）
    idx_file.seek(0, os.SEEK_END)
    idx_size = idx_file.tell()
    idx_file.seek(0)

    dict_file.seek(0, os.SEEK_END)
    dict_size = dict_file.tell()
    dict_file.seek(0)


    entry_count = 0

    with open(html_path, "w", encoding="utf-8") as f:
        while idx_file.tell() < idx_size:
            try:
                word = read_cstring(idx_file)

                buf = idx_file.read(8)
                if len(buf) < 8:
                    break

                offset, size = struct.unpack(">II", buf)

                if offset + size > dict_size:
                    print("BAD ENTRY:", word, offset, size)
                    break

                dict_file.seek(offset)
                data = dict_file.read(size)

                text = data.decode("utf-8", errors="ignore")

                if debug and word.lower() != 'best':
                    continue

                f.write(f"===== {word} =====\n")
                f.write(text)
                f.write("\n\n")
                # print(f"===== {word} =====\n")
                # print(text)
                # print()

                entry_count += 1

            except EOFError:
                break
            except Exception as e:
                print("ERROR at idx pos", idx_file.tell(), ":", e)
                break

    print("Read entries from stardict:", entry_count)
    if not debug: assert entry_count == 19263

    dict_file.close()
    idx_file.close()

# def classify_dtrn(tag):
#     """
#     return: "heading" | "phrase" | "def"
#     """

#     # dtrn 在 <b> 里面 → 通常是词形 (best)
#     if tag.parent and tag.parent.name == "b":
#         return "phrase"

#     # 向上找同级是否有 <b>1.</b> 这样的编号
#     parent = tag.parent
#     if parent:
#         for b in parent.find_all("b", recursive=False):
#             if b.get_text(strip=True).rstrip(".").isdigit():
#                 return "heading"

#     # 其他情况才是真正 definition
#     return "def"

def classify_node(node):
    """
    return: heading | form | def | other
    """

    # ---------- heading ----------
    # <b>1.</b> + blue dtrn
    if node.name == "dtrn":
        # 是否在蓝色 c 标签里
        c_parent = node.find_parent("c")
        if c_parent and c_parent.get("c") == "blue":
            # 同层是否有 <b>1.</b>
            blk = node.find_parent("blockquote")
            if blk:
                for b in blk.find_all("b", recursive=False):
                    t = b.get_text(strip=True).rstrip(".")
                    if t.isdigit():
                        return "heading"

    # ---------- form ----------
    # ▷ <b><dtrn> best</dtrn></b> /best/ [adj]
    if node.name == "dtrn":
        if node.parent and node.parent.name == "b":
            blk = node.find_parent("blockquote")
            if blk and "▷" in blk.get_text():
                return "form"

    # ---------- definition ----------
    # <c c="darkblue"> text :
    if node.name == "c" and node.get("c") == "darkblue":
        text = node.get_text(strip=True)
        if text:
            return "def"

    return "other"

def parse_entry_keep_order(word, html):
    soup = BeautifulSoup(html, "html.parser")

    headword = soup.find("k")
    headword = headword.get_text(strip=True)
    # todo, add later.
    #assert word == headword

    seq = []

    for node in soup.descendants:
        if not hasattr(node, "name"):
            continue

        if node.name == "dtrn":
            text = node.get_text(" ", strip=True)
            if not text:
                continue
            
            typ = classify_node(node)

            if typ == "heading":
                seq.append(("heading", text))
            elif typ == "def":
                seq.append(("def", text))
            elif typ == "phrase":
                seq.append(("phrase", text))
            
            # if text:
            #     seq.append(("def", text))

        elif node.name == "ex":
            text = node.get_text(" ", strip=True)
            if text:
                seq.append(("ex", text))

        # elif node.name == "kref":
        #     text = node.get_text(" ", strip=True)
        #     if text:
        #         seq.append(("ref", text))

    return headword, seq


def parse_html():
    entries = []

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"^===== (.+?) =====$", content, flags=re.M)

    for i in range(1, len(blocks), 2):
        word = blocks[i].strip()
        html = blocks[i + 1]

        entry = parse_entry_keep_order(word, html)
        entries.append(entry)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print("Parsed entries:", len(entries))
    if not debug: assert len(entries) == 19263

if __name__ == '__main__':
    start_time = time.time()
    
    #do_the_job()
    parse_star_dict()
    parse_html()

    print("Done, totally takes %.2f s" % (time.time() - start_time))
