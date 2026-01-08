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

最后比较stardict_sections.txt和lls_plus_sections.txt还有46个diff的时候, 手动改了stardict_sections.txt

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
re_phrase_variant = re.compile(
    r'<b>\s*(?:<dtrn>)?\s*([^<]+?)\s*(?:</dtrn>)?\s*</b>',
    re.I
)
re_phrase_gloss = re.compile(
    r'</c>\s*<i>\s*([^<]+?)\s*</i>',
    re.I
)
re_define = re.compile(
    #r"<blockquote><blockquote><c\s+c=\"darkblue\">\s*(.*?)\s*</c>\s*",
    #r'<c\s+c="darkblue">\s*(.*?)\s*</c>(?:\s*<i>.*?</i>)*\s*:',
    r'<blockquote><blockquote><c\s+c="darkblue">\s*(.*?)\s*</c>(?:\s*<i>.*?</i>)*\s*:?',
    re.I
)
re_thespropform = re.compile(
    r'<c\s+c="crimson">\s*<dtrn>\s*(.*?)\s*</dtrn>\s*</c>',
    re.I
)
re_gloss = re.compile(
    r"<blockquote><blockquote><blockquote><i>\s*(.*?)\s*</i>",
    re.I
)
gloss_str = 'the people or things mentioned earlier'
re_subphrase_gloss = re.compile(
    r'<blockquote>(?:\s*<blockquote>){3}.*?<i>\s*<c[^>]*\bc="maroon"[^>]*>[^<]+</c>\s*</i>\s*<i>\s*([^<]+?)\s*</i>',
    re.I
)
re_example = re.compile(
    r'<blockquote>(?:\s*<blockquote>){3}\s*<ex>\s*(.*?)\s*</ex>\s*(?:<i>\s*(.*?)\s*</i>)?',
    re.I
)
# L6里面丢失的部分
re_runon = re.compile(
    #r'<c\s+c="darkgoldenrod">([^<]+)</c>\s*(?:((?:[^<]+|<i>[^<]*</i>|<b>[^<]*</b>|<i>\s*<c[^>]*\bc="maroon"[^>]*>[^<]+</c>\s*</i>)+)\s*)?<c\s+c="green">([^<]+)</c>',
    r'<c\s+c="darkgoldenrod">([^<]+)</c>\s*((?:[^<]+|<i>[^<]*</i>|<b>[^<]*</b>|<i>\s*<c[^>]*\bc="maroon"[^>]*>[^<]+</c>\s*</i>)+)?\s*(?:<c\s+c="green">([^<]+)</c>)?',
    re.I
)
re_runon_label = re.compile(
    r'<i>\s*<c\s+c="maroon">\s*([^<]+?)\s*</c>\s*</i>',
    re.I
)

html_path = "stardict.html"
debug = 0

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

                if debug and word.lower() != 'above':
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
    # 如果不在runon里面, 就是在phrase和subphrase里面
    in_runon = 0
    #propform_idx_in_runon = 0

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

        '''
        case 1, phrase+音标+词性, 只要第一个
        <blockquote><blockquote>▷<b> <dtrn> about</dtrn></b> /əˈbaʊt/<c c="green"> [preposition]</c> </blockquote></blockquote>
        case 2, phrase + variant + variant + register + 音标 + 词性, 要前3个.
        <blockquote><blockquote>▷<b> <dtrn> focus on</dtrn></b> <i> also</i><b> centre on</b><i><c c="maroon"> British</c></i> <b> /center on</b><i><c c="maroon"> American</c></i> /ˈfəʊkəs ɒn, ˈsentər ɒn/<c c="green"> [verb phrase]</c></blockquote></blockquote>
        case 3, phrase + 音标 + 词性 + gloss, 要phrase和gloss
        <blockquote><blockquote>▷<b> <dtrn> 5-year-old/10-year-old etc</dtrn></b> /ˈfaɪv jɪər ˌəʊld/<c c="green"> [adjective only before noun]</c><i> aged 5/10/35 etc</i></blockquote></blockquote>
        '''

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
            # 不在runon里面
            in_runon = 0

            # case 2, 可能还有VARIANT, 再找一遍.
            m2 = re_phrase_variant.findall(line)
            assert len(m2) >= 1
            if len(m2) > 1:
                for item_idx, item in enumerate(m2):
                    print(item_idx)
                    if item_idx == 0:
                        assert item == phrase, f"item={item}, phrase={phrase}"
                        # 不要在这里处理phrase, 在上面找到后马上处理define
                    else:
                        variant = item

                        # 把可能的/开头去掉
                        if variant[0] == '/':
                            variant = variant[1:]

                        tmp = f"{NEW_LINE}@@VARIANT@@{variant}"
                        print(tmp)
                        seccontent += tmp
            else:    
                # case 3, 可能还有 gloss
                # 用这个也可能找到case 2里面的also, 所以做了case 2就不做这个了.
                m3 = re_phrase_gloss.search(line)
                if m3:
                    gloss = (m3.group(1))
                    tmp = f"{NEW_LINE}@@GLOSS@@{gloss}"
                    print(tmp)
                    seccontent += tmp
            continue

        '''
        # phrase的define, subphrase的define 和runon的define一样的, 都用这个找.
        case 1, regular_def
        <blockquote><blockquote><blockquote><blockquote><c c="darkblue"> to say yes to an offer, an invitation, or a chance to do something</c>: </blockquote></blockquote></blockquote></blockquote>
        case 2,
        <blockquote><blockquote><blockquote><blockquote><c c="darkblue"> to be brave enough to do something unpleasant or difficult that other people are afraid to do</c><i><c c="maroon"> spoken</c></i>: </blockquote></blockquote></blockquote></blockquote>
        case 3 ,runon_def
        <blockquote><blockquote><blockquote><blockquote><c c="darkblue"> when you officially accept something, such as a job offer</c>:</blockquote></blockquote></blockquote></blockquote>
        case 4, runon_def
        <blockquote><blockquote><blockquote><blockquote><c c="darkblue"> when you add a number</c></blockquote></blockquote></blockquote></blockquote>
        case 5        
        <blockquote><blockquote><blockquote><blockquote><c c="darkblue"> if you talk or write<c> on the subject of</c>  someone or something, you talk or write about them</c>: </blockquote></blockquote></blockquote></blockquote>
        case 5 去掉<c>...</c> 
        <blockquote><blockquote><blockquote><blockquote><c c="darkblue"> if you talk or write on the subject of  someone or something, you talk or write about them</c>: </blockquote></blockquote></blockquote></blockquote>
        '''
        m = re_define.search(line)
        if m:
            define1 = (m.group(1))

            if '<c>' in define1:
                assert ("<c>" in line) == ("</c>" in line), f"line={line}, define1={define1}"
                # 确定两个都在了, 再去掉, 只去一个出错, </c> 只替换 <c>的个数
                # 可能有<c c=xxx> YYY </c>, </c>个数可能多很多
                c1=line.count("<c>")
                c2=line.count("</c>")
                #assert c1+1 == c2 and c2 >= 2, f"c1={c1}, c2={c2}, line]={line}"
                assert c1 <= c2
                line1 = line.replace("<c>", "").replace("</c>", "", c1)
                # <c>...</c> 会影响抓到的结果, 去掉后在抓一遍
                m = re_define.search(line1)
                assert m, f"line = {line}, line1={line1}"
                define = m.group(1)
            else:
                define = define1
            
            assert ("<i> " in define) == ("</i>" in define), f"line={line}, define1={define}"
            define = define.replace("<i> ", "(=", 1).replace("</i>", ")", 1)

            if in_runon:
                tmp = f"{NEW_LINE}@@RUNON_DEFINE@@{define}"
            else:
                tmp = f"{NEW_LINE}@@DEFINE@@{define}"
            print(tmp)
            seccontent += tmp

            continue

        '''
        case 1, subphrase
        <blockquote><blockquote><blockquote><c c="crimson"><dtrn>purely accidental</dtrn></c></blockquote></blockquote></blockquote>
        case 2, subphrase + variant
        <blockquote><blockquote><blockquote><c c="crimson"><dtrn>completely by accident</dtrn></c><i> also</i><c c="crimson"><dtrn>  quite by accident</dtrn></c></blockquote></blockquote></blockquote>
        '''
        #m = re_thespropform.search(line)
        m = re_thespropform.findall(line)
        if m:
            # 去掉多余空白
            arr = [item.strip() for item in m]
            thespropform = arr[0]

            # thespropform/runon_propform 有自己的example
            example_idx = 0

            if in_runon:
                # todo, 不用idx
                tmp = f"{NEW_LINE}@@RUNON_EXAS_PROPFORM@@{thespropform}"
                print(tmp)
                seccontent += tmp
            else:
                tmp = f"{NEW_LINE}@@THESPROPFORM{subphrase_idx_in_phrase}@@{thespropform}"
                subphrase_idx_in_phrase += 1
                print(tmp)
                seccontent += tmp

                if len(arr) == 2:
                    # variant
                    variant = arr[1]

                    # 把可能的/开头去掉
                    if variant[0] == '/':
                        variant = variant[1:]
                        
                    tmp = f"{NEW_LINE}@@VARIANT@@{variant}"
                    print(tmp)
                    seccontent += tmp

            continue
        
        '''
        gloss:
        case 1, subphrase的 register + gloss, 要gloss
        <blockquote><blockquote><blockquote><blockquote><i><c c="maroon"> British</c></i><i> a pile up involving a large number of cars</i></blockquote></blockquote></blockquote></blockquote>
        case 2, subphrase_gloss, 要gloss
        <blockquote><blockquote><blockquote><blockquote><i> used when you are talking about a subject and want to say more about it</i></blockquote></blockquote></blockquote></blockquote>
        case 3, subphrase register1, 不要
        <blockquote><blockquote><blockquote><blockquote><i><c c="maroon"> especially British</c></i></blockquote></blockquote></blockquote></blockquote>
        case 3, subphrase register2, 不要
        <blockquote><blockquote><blockquote><blockquote><i><c c="maroon"> formal</c></i></blockquote></blockquote></blockquote></blockquote>
        case 4, runon_phrase的subphrase的gloss, 要gloss
        <blockquote><blockquote><blockquote><i> general acceptance</i></blockquote></blockquote></blockquote>
        case 5, subphrase的 logss + register, 要gloss
        <blockquote><blockquote><blockquote><blockquote><i> use this to tell someone that you will not help them</i><i><c c="maroon"> spoken</c></i></blockquote></blockquote></blockquote></blockquote>
        
        case 6, 只有这一行特别, 单独处理, subphrase 'the above'的gloss
        <blockquote><blockquote><blockquote><blockquote><c c="green"> [singular noun]</c><i> the people or things mentioned earlier</i></blockquote></blockquote></blockquote></blockquote>

        case 10, 在phrase里面
        case 11, 在example里面
        '''

        if gloss_str in line:
            tmp = f"{NEW_LINE}@@GLOSS@@{gloss_str}"
            print(tmp)
            seccontent += tmp
            continue
        m = re_gloss.search(line)
        if m:
            # 上面的case 1 ~ 5都抓到了, 只有1,2,4,5要
            gloss = (m.group(1))

            if line.startswith('<blockquote><blockquote><blockquote><blockquote><i><c c="maroon">'):
                # case 1,3
                mm = re_subphrase_gloss.search(line)
                if mm:
                    # case 1, subphrase的gloss
                    gloss = (mm.group(1))
                    tmp = f"{NEW_LINE}@@GLOSS@@{gloss}"
                    print(tmp)
                    seccontent += tmp
                else:
                    # case 3
                    None
            elif line.startswith('<blockquote><blockquote><blockquote><blockquote><i>'):
                # case 2, 5
                tmp = f"{NEW_LINE}@@GLOSS@@{gloss}"
                print(tmp)
                seccontent += tmp
            else:
                # case 4
                assert line.startswith('<blockquote><blockquote><blockquote><i>')
                tmp = f"{NEW_LINE}@@RUNON_EXAS_GLOSS@@{gloss}"
                print(tmp)
                seccontent += tmp

            continue

        '''
        case 1, example
        <blockquote><blockquote><blockquote><blockquote><ex>▪ Le Shuttle competes with an ever-rising number of ferries for the busy Channel crossing.</ex></blockquote></blockquote></blockquote></blockquote>
        case 2, example + gloss
        <blockquote><blockquote><blockquote><blockquote><ex>▪ the rising rate of smoking among teenagers</ex><i> when problems increase and become more serious</i></blockquote></blockquote></blockquote></blockquote>
        '''
        m = re_example.search(line)
        if m:
            example = (m.group(1))
            if len(example) == 1:
                # 大概有20处空的, 不管, 空行, 不是example缺失
                assert example == "▪"
            else:
                assert example.startswith(f"▪ "), f"word={word!r}, example={example!r}"
                example = example[2:]

                # 都在, 或者都不在, <i>后有空格
                assert ("<i> " in example) == ("</i>" in example), f"example={example}"
                if '</i>' in example:
                    example = example.replace("</i>", ")").replace("<i> ","(=")

                # phrase/subphrase 的example和runon的example都会在这里, 要区分一下.
                if in_runon:
                    tmp = f"{NEW_LINE}@@RUNON_EXAMPLE{example_idx}@@{example}"
                else:
                    tmp = f"{NEW_LINE}@@EXAMPLE{example_idx}@@{example}"
                print(tmp)
                seccontent += tmp

                example_idx += 1
            
            # 可能还有gloss
            gloss = m.group(2)
            if gloss:
                tmp = f"{NEW_LINE}@@GLOSS@@{gloss}"
                print(tmp)
                seccontent += tmp
            continue

        m = re_runon.search(line)
        if m:
            '''
            case 1, runon + 音标pron + 词性gram, 都要
            <blockquote><blockquote><blockquote> <c c="darkgoldenrod">overhead</c> /ˈəʊvəʳhed/<c c="green"> [adjective only before noun]</c></blockquote></blockquote></blockquote>
            case 2, runon + 词性gram, 都要
            <blockquote><blockquote><blockquote> <c c="darkgoldenrod">upstairs</c><c c="green"> [adjective only before noun]</c></blockquote></blockquote></blockquote>
            case 3, runon + 词性gram + label, 都要
            <blockquote><blockquote><blockquote> <c c="darkgoldenrod">acceptance</c><c c="green"> [uncountable noun]</c><i><c c="maroon"> formal</c></i></blockquote></blockquote></blockquote>
            case 4 = case1, runon + 音标pron + 词性gram, 都要
            <blockquote><blockquote><blockquote> <c c="darkgoldenrod">resignation</c> /ˌrezɪgˈneɪʃ<i>ə</i>n/<c c="green"> [uncountable noun]</c></blockquote></blockquote></blockquote>
            case 5, runon + variant + label + 词性gram, 都要
            <blockquote><blockquote><blockquote> <c c="darkgoldenrod">organizer</c> <i> also</i><b> organiser</b><i><c c="maroon"> British</c></i><c c="green"> [countable noun]</c></blockquote></blockquote></blockquote>
            case 5.1, 一样的顺序, 里面的格式一点不一样
            <blockquote><blockquote><blockquote> <c c="darkgoldenrod">beggar</c><i> also</i><c c="darkgoldenrod">  panhandler</c><i><c c="maroon"> American</c></i><c c="green"> [countable noun]</c></blockquote></blockquote></blockquote>
            case 6, runon + 音标pron + 词性gram + label
            <blockquote><blockquote><blockquote> <c c="darkgoldenrod">indignation</c> /ˌɪndɪgˈneɪʃ<i>ə</i>n/<c c="green"> [uncountable noun]</c><i><c c="maroon"> formal</c></i>:</blockquote></blockquote></blockquote>
            case 7, runon + 音标pron + label, 都要
            <blockquote><blockquote><blockquote> <c c="darkgoldenrod">my treat</c> /ˌmaɪ ˈtriːt/<i><c c="maroon"> spoken</c></i></blockquote></blockquote></blockquote>
            
            
            <blockquote><blockquote><blockquote> <c c="darkgoldenrod">scepticism</c> <i> also</i><b> skepticism</b><i><c c="maroon"> American</c></i> /ˈskeptɪsɪz<i>ə</i>m, ˈskeptəsɪz<i>ə</i>m/<c c="green"> [uncountable noun]</c></blockquote></blockquote></blockquote>
            
            '''
            runon_phrase = m.group(1)
            runon_pron = m.group(2)
            runon_gram = m.group(3)

            # phrase, 必须有
            assert runon_phrase
            # runon_phrase 有自己的example
            example_idx = 0
            in_runon = 1

            # debug
            if runon_phrase in ('beggar', 'organizer'):
                None
            
            if runon_gram != None:
                assert runon_gram.startswith(" [") and runon_gram.endswith("]"), \
                    f"runon_gram={runon_gram}"
                runon_gram = runon_gram[2:-1]

            # reset case id
            runon_case_id = 0
            mm = re_runon_label.search(line)
            if mm:
                # case 3, 5, 6
                assert len(mm.groups()) == 1
                runon_label = mm.group(1).strip()
                if 'also</i>' in line:
                    # case 5
                    runon_case_id = 5
                    # 这里用的findall, mmm是两个元素的arr
                    # mmm[0]里面是匹配到的runon
                    # mmm[1]才是variant在里面
                    # mmm[1] 有两个group, 哪个非空用哪个
                    mmm = re.findall(
                        r'(?:<b>\s*([^<]+)\s*</b>|<c\s+c="darkgoldenrod">\s*([^<]+)\s*</c>)',
                        line
                    )
                    assert mmm
                    runon_variant = mmm[1][0] or mmm[1][1]
                else:
                    # case 3, 6
                    if runon_pron == None:
                        runon_case_id = 3
                    else:
                        if runon_gram == None:
                            runon_case_id = 7
                        else:
                            runon_case_id = 6
            else:
                if runon_pron == None:
                    # case 2
                    runon_case_id = 2
                else:
                    # case 1/4
                    runon_case_id = 1

            # 根据case id, 打印顺序
            assert runon_case_id != 0
            if runon_case_id == 1:
                # case 1 和 4 一样
                # runon + pron + gram
                tmp = f"{NEW_LINE}@@RUNON_PHRASE@@{runon_phrase}"
                print(tmp)
                seccontent += tmp
                
                assert ("<i>" in runon_pron) == ("</i>" in runon_pron)
                runon_pron = runon_pron.replace("</i>", "").replace("<i>","")
                tmp = f"{NEW_LINE}@@runon_pron@@{runon_pron}"
                print(tmp)
                seccontent += tmp
                
                tmp = f"{NEW_LINE}@@RUNON_GRAM@@{runon_gram}"
                print(tmp)
                seccontent += tmp

            elif runon_case_id == 2:
                # runon + gram
                tmp = f"{NEW_LINE}@@RUNON_PHRASE@@{runon_phrase}"
                print(tmp)
                seccontent += tmp
                
                tmp = f"{NEW_LINE}@@RUNON_GRAM@@{runon_gram}"
                print(tmp)
                seccontent += tmp
            elif runon_case_id == 3:
                # runon + gram + label
                tmp = f"{NEW_LINE}@@RUNON_PHRASE@@{runon_phrase}"
                print(tmp)
                seccontent += tmp
                
                tmp = f"{NEW_LINE}@@RUNON_GRAM@@{runon_gram}"
                print(tmp)
                seccontent += tmp

                tmp = f"{NEW_LINE}@@RUNON_LABEL@@{runon_label}"
                print(tmp)
                seccontent += tmp
            elif runon_case_id == 5:
                #runon + variant + label + 词性gram
                tmp = f"{NEW_LINE}@@RUNON_PHRASE@@{runon_phrase}"
                print(tmp)
                seccontent += tmp

                tmp = f"{NEW_LINE}@@RUNON_VARIANT@@{runon_variant}"
                print(tmp)
                seccontent += tmp

                tmp = f"{NEW_LINE}@@RUNON_LABEL@@{runon_label}"
                print(tmp)
                seccontent += tmp

                # bugfix, 没有的话重新抓
                if runon_gram == None:
                    m4 = re.search(r'<c\s+c="green">\s*\[([^\]]+)\]\s*</c>', line)
                    runon_gram = m4.group(1)
                    assert runon_gram
                tmp = f"{NEW_LINE}@@RUNON_GRAM@@{runon_gram}"
                print(tmp)
                seccontent += tmp
            elif runon_case_id == 6:
                # runon + pron + gram + label
                tmp = f"{NEW_LINE}@@RUNON_PHRASE@@{runon_phrase}"
                print(tmp)
                seccontent += tmp
                
                assert ("<i>" in runon_pron) == ("</i>" in runon_pron)
                runon_pron = runon_pron.replace("</i>", "").replace("<i>","")
                tmp = f"{NEW_LINE}@@runon_pron@@{runon_pron}"
                print(tmp)
                seccontent += tmp

                tmp = f"{NEW_LINE}@@RUNON_GRAM@@{runon_gram}"
                print(tmp)
                seccontent += tmp

                tmp = f"{NEW_LINE}@@RUNON_LABEL@@{runon_label}"
                print(tmp)
                seccontent += tmp
            elif runon_case_id == 7:
                # runon + pron + label
                tmp = f"{NEW_LINE}@@RUNON_PHRASE@@{runon_phrase}"
                print(tmp)
                seccontent += tmp
                
                assert ("<i>" in runon_pron) == ("</i>" in runon_pron)
                runon_pron = runon_pron.replace("</i>", "").replace("<i>","")
                tmp = f"{NEW_LINE}@@runon_pron@@{runon_pron}"
                print(tmp)
                seccontent += tmp

                tmp = f"{NEW_LINE}@@RUNON_LABEL@@{runon_label}"
                print(tmp)
                seccontent += tmp
            else:
                assert False, f"runon_case_id={runon_case_id}"


            # 处理pron, 可能runon里面没有pron
            # if runon_mix:
            #     # 都在或者都不在, 去掉.
            #     assert ("<i>" in runon_mix) == ("</i>" in runon_mix)
            #     runon_mix = runon_mix.replace("</i>", "").replace("<i>","")
            #     tmp = f"{NEW_LINE}@@runon_mix@@{runon_mix}"
            #     print(tmp)
            #     seccontent += tmp



            # 处理 label, 可能没有
            
            


    
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
    with open("results/lla_plus_headings.txt", "r", encoding="utf-8") as f:
        section_keys_lla_book_order = [line.rstrip("\n") for line in f]
    if not debug:
        assert len(section_keys_lla_book_order) == SECTION_NUM, \
            f"len(section_keys_lla_book_order)={len(section_keys_lla_book_order)}"

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
    if debug:
        parse_star_dict_format()

    parse_html()

    print("Done, totally takes %.2f s" % (time.time() - start_time))
