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
import html

# 自己的全局变量/函数
import utils

'''

stardict from: https://forum.freemdict.com/t/topic/42061/29

- 解析stardict的dict和idx两个文件, 得到html文本
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

# line_idx==1时用这个找word
re_word = re.compile(
    r"<k>\s*(.*?)\s*</k>",
    re.I
)

re_heading = re.compile(
    r"<b>\s*(\d+)\.\s*</b>.*?<c\s+c=\"blue\">\s*<dtrn>\s*(.*?)\s*</dtrn>",
    re.I
)
re_phrase = re.compile(
    r"▷.*?<b>\s*<dtrn>\s*(.*?)\s*</dtrn>\s*</b>",
    re.I
)
re_variant = re.compile(
    r'<b>\s*(?:<dtrn>)?\s*([^<]+?)\s*(?:</dtrn>)?\s*</b>',
    re.I
)
re_define = re.compile(
    r"<c\s+c=\"darkblue\">\s*(.*?)\s*</c>\s*:",
    re.I
)
re_thespropform = re.compile(
    r'<c\s+c="crimson">\s*<dtrn>\s*(.*?)\s*</dtrn>\s*</c>',
    re.I
)
re_gloss = re.compile(
    r"<blockquote><blockquote><blockquote><blockquote><i>\s*(.*?)\s*</i>",
    re.I
)
re_example = re.compile(
    r"<blockquote><blockquote><blockquote><blockquote><ex>\s*(.*?)\s*</ex>",
    re.I
)

html_path = "stardict.html"
debug = False

SECTION_NUM = 4953
NEW_LINE = ""

section_map = {}
# 直接从mdx读进来就是LLA book order, key=heading+phrases
section_keys_lla_book_order = []
total_sec_cnt = 0 # adding all the cnt in the sec_to_cnt.
total_phrase_num_in_identical_sections = 0

def parse_star_dict_format():
    tar_path = "data/stardict-Longman_Language_Activator_2nd_Ed-2.4.2.tar.7z"
    dict_path = "data/Longman Language Activator 2nd Ed.dict"
    idx_path  = "data/Longman_Language_Activator_2nd_Ed.idx"

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
                '''
                ma&apos;am   → ma'am
                don&apos;t   → don't
                &amp;        → &
                &quot;       → "
                &#8217;      → ’
                '''
                text = html.unescape(text)
                word = html.unescape(word)

                if debug and word.lower() != 'about':
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
    if not debug: assert entry_count == 19263, f"entry_count={entry_count}"

    dict_file.close()
    idx_file.close()

def hash_text(s):
    return hashlib.sha256(s.encode("utf8")).hexdigest()

def register_section(secheading, all_phrase, sec_value, phrase_cnt, test_name):
    secheading = secheading.replace("’", "'")
    all_phrase = all_phrase.replace("’", "'")
    sec_value = sec_value.replace("’", "'")
    
    secheading = secheading.replace("‘", "'")
    all_phrase = all_phrase.replace("‘", "'")
    sec_value = sec_value.replace("‘", "'")

    # 两个或以上空格 → 一个空格
    secheading = re.sub(r'\s{2,}', ' ', secheading)
    all_phrase = re.sub(r'\s{2,}', ' ', all_phrase)
    sec_value = re.sub(r'\s{2,}', ' ', sec_value)

    # /两边不要空格, 和ldoce6一样
    secheading = secheading.replace(" / ", "/")
    all_phrase = all_phrase.replace(" / ", "/")
    sec_value = sec_value.replace(" / ", "/")

    # 处理heading
    if 'to ask someone questions for a newspaper' in secheading or \
        'when you believe or do not believe that' in secheading or \
        'the Internet and places on the Internet' in secheading or \
        'things you do on the Internet' in secheading:
        # 这几个不用变小写:
        # 'to ask someone questions for a newspaper, TV programme etc' 里面的TV不改.
        # 'when you believe or do not believe that God'
        # 'the Internet and places on the Internet'
        # 'things you do on the Internet'
        None
    else:
        # 里面有全大写的, 影响排序, 变小写
        secheading = secheading.lower()

    # lla plus 的格式问题, 导致'/Hey'没有被捕获到, 这里加上.
    if 'ways of beginning a letter' == secheading:
        all_phrase += '/Hey'

    # # phrase里面少了一个空格, 影响key, 其他地方也有, 但是不管了. plus mdx里面有大量这样的情况
    if 'to do a test on something in order to check it or find out about it' == secheading:
        all_phrase = all_phrase.replace("anexperiment", "an experiment")


    global total_sec_cnt
    global total_phrase_num_in_identical_sections
    total_sec_cnt += 1

    sec_key = secheading + all_phrase
    section_keys_lla_book_order.append(sec_key)
    # WAR
    if secheading == f"someone who hates you and wants to harm you" and \
        sec_value.startswith(f"{NEW_LINE}@@PHRASE0@@enemy{NEW_LINE}@@EXAMPLE0@@The detective wanted"):
        # LLA书本的 enemy 主题下有这个, hate主题下也有, secheading一样, phrase 一样, 内容不一样.
        sec_key += " 2"

    val_hash = hash_text(sec_value)
    if sec_key not in section_map:
        # 第一次看到这个 section
        total_phrase_num_in_identical_sections += phrase_cnt
        section_map[sec_key] = {
            "sec_heading": secheading,
            "content": sec_value,
            "content_hash": val_hash,
            "count": 1,
            "words": [test_name],
        }
    else:
        entry = section_map[sec_key]

        # 核心断言：内容必须完全一致
        assert entry["content_hash"] == val_hash, (
            f"section content mismatch\n"
            f"heading={sec_key!r}\n"
            f"existing content={entry['content']}\n"
            f"test_name={', '.join(entry['words'])}\n"
            f"new content={sec_value}\n"
            f"new test_name={test_name!r}"
        )

        # 加进去
        entry["count"] += 1
        entry["words"].append(test_name)

        # section不能重复出现在一个单词里
        len(set(entry["words"])) == len(entry["words"])


def parse_entry(word, text):
    '''
    一个entry对应stardict里面的一个单词的内容, 如果是866个keyword之一, 那就有一个或者多个section
    否则没有section提取到.
    '''
    is_keyword_entry = False

    secheading = ""
    one_sec_all_phrase = ""
    one_sec_all_phrase_cnt = 0
    seccontent = ""

    example_idx = 0
    subphrase_idx_in_phrase = 0

    lines = text.splitlines()
    for line_idx, line in enumerate(lines):
        is_last = (line_idx == len(lines) - 1)
        line = line.strip()

        if not line:
            assert line_idx != 1
            continue
    
        # 必定是word
        if line_idx == 1:
            m = re_word.search(line)
            assert m
            # 找到就行, 不用纠结相等了, 有些不一样
            # if word == "a likely story":
            #     None
            # else:
            #     assert m.group(1) == word, f"m.group(1)={m.group(1)}, word={word}"
            continue

        if '<blockquote><c c="darkblue"><b><c>INDEX:</c></b></c></blockquote>' == line:
            is_keyword_entry = True

        # 还没看到keyword标志, 后面不用做了.
        if not is_keyword_entry:
            continue

        m = re_heading.search(line)
        if m:
            # 找一个新的heading, 把前面的加到map里面
            if secheading:
                register_section(secheading, one_sec_all_phrase, seccontent, one_sec_all_phrase_cnt, word)
                # reset
                secheading = ""
                one_sec_all_phrase = ""
                one_sec_all_phrase_cnt = 0
                seccontent = ""

            secheading = (m.group(2))
            print(f"\n{secheading}")

            continue

        m = re_phrase.search(line)
        if m:
            phrase = (m.group(1))
            tmp = f"{NEW_LINE}@@PHRASE{one_sec_all_phrase_cnt}@@{phrase}"
            print(tmp)
            seccontent += tmp

            one_sec_all_phrase += tmp
            one_sec_all_phrase_cnt += 1

            # phrase 有自己的example
            example_idx = 0
            # phrase 有自己的subphrase
            subphrase_idx_in_phrase = 0

            # 可能还有VARIANT, 再找一遍.
            more = re_variant.findall(line)
            assert len(more) >= 1
            for item_idx, item in enumerate(more):
                print(item_idx)
                if item_idx == 0:
                    assert item == phrase, f"item={item}, phrase={phrase}"
                    # 不要在这里处理phrase, 在上面找到后马上处理define
                else:
                    variant = item
                    next, 把可能的/开头去掉
                    tmp = f"{NEW_LINE}@@VARIANT@@{variant}"
                    print(tmp)
                    seccontent += tmp

                
            continue

        m = re_define.search(line)
        if m:
            define1 = (m.group(1))

            # 只有define里面可能出现 <c>...</c>, 去掉
            define = define1.replace("<c>", "").replace("</c>", "")
            tmp = f"{NEW_LINE}@@DEFINE@@{define}"
            print(tmp)
            seccontent += tmp

            continue

        m = re_thespropform.search(line)
        if m:
            thespropform = (m.group(1))
            tmp = f"{NEW_LINE}@@THESPROPFORM{subphrase_idx_in_phrase}@@{thespropform}"
            print(tmp)
            seccontent += tmp

            # thespropform 有自己的example
            example_idx = 0
            subphrase_idx_in_phrase += 1
            continue

        m = re_gloss.search(line)
        if m:
            gloss = (m.group(1))
            tmp = f"{NEW_LINE}@@GLOSS@@{gloss}"
            print(tmp)
            seccontent += tmp
            continue

        m = re_example.search(line)
        if m:
            example = (m.group(1))
            if len(example) == 1:
                # 大概有20处空的, 不管, 空行, 不是example缺失
                assert example == "▪"
            else:
                assert example.startswith(f"▪ "), f"word={word!r}, example={example!r}"
                example = example[2:]
                tmp = f"{NEW_LINE}@@EXAMPLE{example_idx}@@{example}"
                print(tmp)
                seccontent += tmp

                example_idx += 1
            continue
    
    # add the last section.
    if secheading:
        register_section(secheading, one_sec_all_phrase, seccontent, one_sec_all_phrase_cnt, word)
                
def parse_html():
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"^===== (.+?) =====$", content, flags=re.M)
    for i in range(1, len(blocks), 2):
        word = blocks[i].strip()
        html = blocks[i + 1]

        parse_entry(word, html)

    # 得到LLA书本顺序, 先跑lla_plus.py生成, 或者到results里面找.
    with open("lla_plus_headings.txt", "r", encoding="utf-8") as f:
        section_keys_lla_book_order = [line.rstrip("\n") for line in f]
    if not debug:
        assert len(section_keys_lla_book_order) == SECTION_NUM

    # 单单保存key, 字母顺序
    # with open("stardict_map_debug.txt", "w", encoding="utf8") as ofile:
    #     for sec_key in sorted(section_map.keys()):
    #         line = sec_key
    #         # entry = section_map[sec_key]
    #         # sechead = entry["sec_heading"]
    #         # seccontent = entry["content"]

    #         # line = f"{sechead}{seccontent}"

    #         ofile.write(line)
    #         ofile.write("\n")

    # 单单保存key, 书本顺序
    output_file = 'stardict_headings.txt'
    total_identical_sec_cnt = len(section_map)
    if not debug:
        assert len(section_map) == SECTION_NUM
    has_seen_someone_who_hates_you = False
    with open(output_file, "w", encoding="utf8") as ofile:
        for sec_key in section_keys_lla_book_order:
            # 只有这个conflict, 特别对待
            if sec_key == f"someone who hates you and wants to harm you{NEW_LINE}@@PHRASE0@@enemy":
                if has_seen_someone_who_hates_you:
                    sec_key += " 2"
                else:
                    has_seen_someone_who_hates_you = True

            if sec_key not in section_map:
                if debug:
                    continue
                else:
                    print(f"[ERROR] sec_key not found: {sec_key!r}")
                    assert False
      
            line = f"{sec_key}"

            ofile.write(line)
            ofile.write("\n")


    # 按书本顺序, 保存全部sections
    output_file = 'stardict_sections.txt'
    # 如果只写heading的话, 和上面的一样, debug用, 用于和上面对比顺序.
    only_write_key = False
    #global section_map
    if not debug:
        assert len(section_map) == len(section_keys_lla_book_order)
    has_seen_someone_who_hates_you = False
    with open(output_file, "w", encoding="utf8") as ofile:
        for sec_key in section_keys_lla_book_order:
            # 只有这个conflict, 特别对待
            if sec_key == f"someone who hates you and wants to harm you{NEW_LINE}@@PHRASE0@@enemy":
                if has_seen_someone_who_hates_you:
                    sec_key += " 2"
                else:
                    has_seen_someone_who_hates_you = True

            if sec_key not in section_map:
                if debug:
                    continue
                else:
                    assert False, f"[ERROR] has_seen_someone_who_hates_you = {has_seen_someone_who_hates_you}, sec_key not found: {sec_key!r}"

            # 写入文件
            entry = section_map[sec_key]
            sechead = entry["sec_heading"]
            seccontent = entry["content"]
            
            if only_write_key:
                line = f"{sec_key}"
            else:
                line = f"{sechead}{seccontent}"
                # 多行用于比较方便, 只有在保存整个section的时候可能用. 上面的单单key没必要
                if not utils.one_line_per_section:
                    # 用正则匹配 @@...@@, 就是加一个\n
                    line = re.sub(r'(@@.*?@@)', r'\n\1', line)
            
            ofile.write(line)
            ofile.write("\n")

            # 用过就删
            del section_map[sec_key]
    # 最后断言 section_map 已经为空
    assert not section_map, f"[ERROR] Some sec_keys were not written: {list(section_map.keys())}"


if __name__ == '__main__':
    start_time = time.time()

    # 不用每次重新parse
    parse_star_dict_format()

    parse_html()

    print("Done, totally takes %.2f s" % (time.time() - start_time))
