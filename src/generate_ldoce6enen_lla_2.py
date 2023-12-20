#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import re
import shutil
import time
import hashlib
from bs4 import BeautifulSoup, Tag

'''
解析里面LDOCE6里面的LLA
866个keyword, 每个keyword有若干个section, 整本LLA一共有4953个section
    每个section里面有
        一个标题heading
        若干个phrase
            每个phrase里面有解释和例子.
用soup解析html格式. 得到LDOCE6 里面LLA信息

run: PYTHONUTF8=1 python src/generate_ldoce6enen_lla_2.py |& tee lla_log.txt
Parsing...

Summary:
total section number = 32630
identical section number = 4953
by average, each section has been seen 6.59 times in the mdx.

total phrase num in identical sections = 22068
by average, each section has phrase num = 22068 / 4953 = 4.46
Done with the job, totally takes 520.12 s

'''

ALLOWED_REGISTERLABS = {
    "American",
    "American formal",
    "American informal",
    "American spoken",
    "American spoken informal",
    "American written",
    "American, especially spoken",
    "British",
    "British formal",
    "British informal",
    "British informal spoken",
    "British spoken",
    "especially American",
    "especially American informal",
    "especially American, informal",
    "especially American, spoken",
    "especially British",
    "especially British, formal",
    "especially British, informal",
    "especially British, spoken",
    "especially British, written",
    "especially spoken",
    "especially spoken, informal",
    "especially written",
    "formal",
    "formal or written",
    "formal spoken",
    "formal written",
    "formal, especially written",
    "formal, informal",
    "informal",
    "informal spoken",
    "spoken",
    "spoken formal",
    "spoken informal",
    "technical",
    "trademark",
    "usually",
    "written",
    "written abbreviation",
}

ALLOWED_PHRASE_HAS_EMPTY_EXAMPLE = {
    # 有个空行example, 下面每个都和LLA书本确认过, 不是缺少example, 而是多出空行
    "agitate", "VJ/veejay", "be interested in", "tears", "what's the damage", "cure", "thunderous", "sorrow", "be ten a penny",
    # 下面的不检查了, 默认和上面一样
    "player", "whinger", "idle", "happen to", "the past"
}

ALLOWED_PHRASE_NO_EXAMPLE = {
    # 下面的都在字典里确认过, 没有example, 但是没有在LLA书本里确认过.
    "mailing list", "off licence", "chemist", "pharmacy", "hardware store", "comprehensive school", "sixth form college"
}

ALLOWED_ALSO = {
    "also", "usually", "plural", "abbreviation", "past tense and past participle", "or"
}

SECTION_NUM = 4953
PHRASE_NUM = 22068

# 不要用\n, 出问题, 在sublime里面自己替换.
NEW_LINE = ""

section_map = {}
total_identical_sec_cnt = 0
total_sec_cnt = 0 # adding all the cnt in the sec_to_cnt.
total_phrase_num_in_identical_sections = 0

def hash_text(s):
    return hashlib.sha256(s.encode("utf8")).hexdigest()

def register_section(secheading, all_phrase, sec_value, phrase_cnt, test_name):
    global total_sec_cnt
    global total_phrase_num_in_identical_sections
    total_sec_cnt += 1

    # WAR
    if secheading == f"what you say when something is not important":
        # 把/两边的空格去掉, 用于和lla plus生成的section比对, 有一样的key
        all_phrase = all_phrase.replace("it's no big deal / it's not a big deal", "it's no big deal/it's not a big deal")

    sec_key = secheading + all_phrase
    
    # WAR
    # e/E 开头的单词里面的LLA的heading conflict
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

def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # 两个独立的
    debug = 0
    log_info = 0
    if debug:
        # 初始数据
        input_txt = 'data/bar.html'
    else:
        input_txt = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt'

    # verify the md5 of the input file.
    md5 = hashlib.md5(open(input_txt,'rb').read()).hexdigest()
    if not debug:
        # bugfix.py生成的 txt, v20240202
        #assert md5 == '98f0174a1e2318aeb4b1402848e58a75'
        None

    POS_HEAD = 'POSITION_HEAD'
    POS_BODY = 'POSITION_BODY'
    POS_TAIL = 'POSITION_TAIL'
    line_position = POS_TAIL
    test_name = 'init_invalid_name' # =headword

    with open(input_txt, encoding="utf8") as ifile:
        for line in ifile:
            # Get the info that where is the line_position.
            if line_position == POS_TAIL:
                # was tail, re-started with head.
                line_position = POS_HEAD
                test_name = line.rstrip('\n')
            elif line_position == POS_HEAD:
                # was head, now it is body
                line_position = POS_BODY
            elif line_position == POS_BODY:
                # was body, now it is tail
                line_position = POS_TAIL
                # 最后一行没有 \n
                assert line.rstrip('\n') == '</>', f"test_name={test_name}"
                test_name = 'init_invalid_name'
            # ======================================= do the modifications =======================================       
            # debug 按字母跑, 而不是每次都从头开始
            # c = test_name[0]
            # if c not in {'e', 'E'}:
            #     continue

            # if the content doesn't have 'Longman Language Activator' string, skip
            if line_position != POS_BODY or 'Longman Language Activator' not in line:
                continue
            # 特殊的单词, 忽略
            if line_position == POS_BODY and test_name == 'faq-about 33de5e2430c248afb78dd34e20f35466':
                continue

            soup = BeautifulSoup(line, "lxml")
            
            # 找到 LLA header
            lla_headers = soup.find_all(
                "span",
                class_="popheader popthes",
                string="Longman Language Activator"
            )
            assert len(lla_headers) >= 1, f"test_name={test_name}"

            for lla_idx, lla_header in enumerate(lla_headers):
                if debug: print(f"lla_idx={lla_idx}")
                assert lla_header, f"test_name={test_name}, lla_idx={lla_idx}, lla_header is none"

                # LLA 的内容在同一个 entry 里
                lla_entry = lla_header.find_parent("span", class_="entry")
                spans = lla_entry.find_all("span", recursive=False)
                assert len(spans) >= 2, f"test_name={test_name}, lla_idx={lla_idx}"

                # 1️⃣ 第一个 span：LLA header
                first = spans[0]
                assert first.get("class") == ["popheader", "popthes"], f"test_name={test_name}, lla_idx={lla_idx}"
                assert first.get_text(strip=True) == "Longman Language Activator", f"test_name={test_name}, lla_idx={lla_idx}"
                
                # 剩下的都是section
                sections = spans[1:]
                assert len(sections) >= 1, f"test_name={test_name}, lla_idx={lla_idx}"
                for sec_idx, sec in enumerate(sections):
                    if debug: print(f"sec_idx={sec_idx}")
                    assert isinstance(sec, Tag), f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"

                    classes = sec.get("class", [])
                    if sec_idx == len(sections) - 1:
                        # 最后一个 section
                        assert classes == ["section", "last"], f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                    else:
                        assert classes == ["section"], f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                    
                    # 解析每个 section 内部结构
                    sec_spans = sec.find_all("span", recursive=False)
                    assert len(sec_spans) >= 2, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"

                    # 第一个 span：secheading
                    secheading_span = sec_spans[0]
                    assert secheading_span.get("class") == ["secheading"], f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                    secheading = secheading_span.get_text(strip=True)
                    assert secheading, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, empty string"
                    if log_info: print(secheading)

                    # 剩下的 span: exponent = phrase
                    one_sec_all_phrase = ""
                    one_sec_all_phrase_cnt = 0
                    seccontent = ""

                    exponents = sec_spans[1:]
                    for exp_idx, exp in enumerate(exponents):
                        if debug: print(f"exp_idx={exp_idx}")
                        assert exp.get("class") == ["exponent"], f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, exp_idx={exp_idx}, {exp.get('class')}"

                        # exponent 内部结构
                        exp_children = exp.find_all(recursive=False)
                        # exponent里面第一个是expandable
                        expandable_span = exp_children[0]
                        assert expandable_span.name == "span", f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                        assert expandable_span.get("class") == ["expandable"], f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                        
                        # expandable两个孩子
                        expandable_children = expandable_span.find_all("span", recursive=False)
                        assert len(expandable_children) == 2, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                        arrow, display = expandable_children
                        # 第一个孩子就是个箭头图标
                        assert arrow.get("class") == ["arrow"], f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                        # 第二个孩子就是phrase
                        assert display.get("class") == ["exp", "display"], f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                        phrase = display.get_text(strip=True)
                        assert phrase, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, empty phrase"
                        
                        tmp = f"{NEW_LINE}@@PHRASE{exp_idx}@@{phrase}"
                        if log_info: print(tmp)
                        seccontent += tmp

                        one_sec_all_phrase += tmp
                        one_sec_all_phrase_cnt += 1
                        # subphrase = thespropform
                        subphrase_idx_in_phrase = 0

                        # exponent里面第二个是content
                        content = exp_children[1]
                        assert content.name == "div", f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                        assert content.get("class") == ["content"], f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"

                        # content里面:
                        content_spans = content.find_all("span", recursive=False)
                        # 可能就只有一个def
                        if len(content_spans) == 0:
                            assert phrase == "not know"
                            continue
                        assert len(content_spans) >= 1, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"

                        # abandon.lla0.sec0.leave没有def
                        def_cnt = 0
                        # todo, 可能一个就够了, 只有exampele++, 其他都清0?
                        example_cnt_in_cur_phrase = 0
                        # phrase 里面的subphrase=thespropform的example都是独立的.
                        example_idx_in_cur_subphrase = 0

                        for s in content_spans:
                            cls = s.get("class")
                            #assert cls in (["registerlab"], ["variant"], ["def"], ["neutral"], ["example"], ["thespropform"], ["gloss"]), f"test_name={test_name}, cls={cls}"  
                            if cls == ["def"]:
                                # 当前 phrase 或者 thespropform 的定义
                                def_cnt += 1
                                define=s.get_text(strip=True)
                                assert define, "empty string"
                                assert define[0].isalnum() or define[0] in {'-', '$'}, \
                                    f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, define={define!r}"

                                tmp = f"{NEW_LINE}@@DEFINE@@{define}"
                                if log_info: print(tmp)
                                seccontent += tmp

                                # reset example id
                                example_idx_in_cur_subphrase = 0

                            elif cls == ["example"]:
                                # phrase的例子, 或者是phrase词组的例子
                                example_cnt_in_cur_phrase += 1
  
                                example = s.get_text(strip=True)
                                assert example[0] == "·", f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                                example = example[1:].lstrip()

                                if not example:
                                    # 有个空行example, 小bug
                                    assert phrase in ALLOWED_PHRASE_HAS_EMPTY_EXAMPLE, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                                    continue
                                assert example, "empty string"
                                # '`'其实是符号bug, 应该是单引号'
                                assert example[0].isalnum() or example[0] in {'£', '$', '.', '"', "'", '`', '('}, \
                                    f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, example={example!r}"
                                
                                tmp = f"{NEW_LINE}@@EXAMPLE{example_idx_in_cur_subphrase}@@{example}"
                                example_idx_in_cur_subphrase += 1
                                if log_info: print(tmp)
                                seccontent += tmp

                                # 验证                              
                                example_children = s.find_all("span", recursive=False)
                                len(example_children) >= 1 and len(example_children) <= 2
                                example_children[0].get("class") == ["neutral"]
                                if len(example_children) == 2:
                                    # 少数有gloss, 即这个例子的等价解释: xxx(=yyy)
                                    example_children[1].get("class") == ["gloss"]
                                    assert "(=" in example and ")" in example, \
                                        f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"

                            elif cls == ["registerlab"]:
                                # 不重要
                                registerlab = s.get_text(strip=True)

                                if not registerlab:
                                    # 目前只发现这个的registerlab是空的
                                    assert phrase in {"outplay", "set"}, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                                    continue
                                assert registerlab, "empty string"
                                assert registerlab[0].isalpha(), f"registerlab={registerlab!r}"               
                                assert registerlab in ALLOWED_REGISTERLABS, f"registerlab={registerlab!r}"

                                # reset example id
                                example_idx_in_cur_subphrase = 0

                            elif cls == ["variant"]:
                                variant = ""
                                variant_children = s.find_all("span", recursive=False)
                                
                                # 只关心2种class, 忽略其他的.
                                for variant_child in variant_children:
                                    variant_child_cls = variant_child.get("class")
                                    if variant_child_cls == ["varitype"]:
                                        also = variant_child.get_text(strip=True)
                                        assert also in ALLOWED_ALSO, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, also={also}"
                                        variant += f"{also} "
                                    elif variant_child_cls == ["lexvar"]:
                                        variant += variant_child.get_text(strip=True)
                                assert variant, "empty string"
                                # 这个bug被fix了.
                                assert not variant.startswith(f"/")
                                
                                tmp = f"{NEW_LINE}@@VARIANT@@{variant}"
                                if log_info: print(tmp)
                                seccontent += tmp

                                # reset example id
                                example_idx_in_cur_subphrase = 0

                            elif cls == ["thespropform"]:
                                # phrase词组
                                thespropform = s.get_text(strip=True)
                                if thespropform[0] == ":":
                                    thespropform = thespropform[1:].lstrip()

                                if not thespropform:
                                    # 目前只发现这个的 thespropform 是空的
                                    assert phrase == "record-breaking", f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}"
                                    continue
                                assert thespropform, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, empty string"
                                assert thespropform[0].isalnum() or thespropform[0] in {'$', '£', '(', '+'}, \
                                    f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, thespropform={thespropform!r}"
                                
                                tmp = f"{NEW_LINE}@@THESPROPFORM{subphrase_idx_in_phrase}@@{thespropform}"
                                if log_info: print(tmp)
                                seccontent += tmp

                                # reset example id
                                example_idx_in_cur_subphrase = 0
                                subphrase_idx_in_phrase += 1

                            elif cls == ["gloss"]:
                                # phrase词组的等价解释
                                gloss = s.get_text(strip=True)
                                assert gloss, "empty string"
                                assert gloss[0] == "(" and gloss[1] == "=" and gloss[-1] == ")", \
                                    f"gloss={gloss!r}"
                                gloss = gloss[2:-1] # 去掉前面的(=, 和后面的)

                                tmp  =f"{NEW_LINE}@@GLOSS@@{gloss}"
                                if log_info: print(tmp)
                                seccontent += tmp

                                # 这个gloss不是example的gloss (在example里面)
                                # reset example id
                                example_idx_in_cur_subphrase = 0

                            elif cls == ["neutral"]:
                                # 标点符号, 不重要
                                neutral = s.get_text(strip=True)
                                assert neutral in {":", ""}, f"neutral={neutral}"

                            else:
                                assert False, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, exp_idx={exp_idx}, cls={cls}"

                        #assert def_cnt == 1, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, exp_idx={exp_idx}"
                        if secheading == "types of film" or phrase in ALLOWED_PHRASE_NO_EXAMPLE:
                            assert example_cnt_in_cur_phrase == 0
                        else:
                            assert example_cnt_in_cur_phrase >= 1, f"test_name={test_name}, lla_idx={lla_idx}, sec_idx={sec_idx}, exp_idx={exp_idx}"
                    
                    # 得到一个section了
                    register_section(secheading, one_sec_all_phrase, seccontent, one_sec_all_phrase_cnt, test_name)

    # 得到LLA书本顺序, 先跑lla_plus.py生成, 或者到results里面找.
    with open("lla_plus_headings.txt", "r", encoding="utf-8") as f:
        section_keys_lla_book_order = [line.rstrip("\n") for line in f]
    if not debug:
        assert len(section_keys_lla_book_order) == SECTION_NUM

    global section_map
    
    # 单单保存key, 字母顺序
    with open("lla_headings_alpha_order.txt", "w", encoding="utf8") as ofile:
        for sec_key in sorted(section_map.keys()):
            line = sec_key
            # entry = section_map[sec_key]
            # sechead = entry["sec_heading"]
            # seccontent = entry["content"]

            # line = f"{sechead}{seccontent}"

            ofile.write(line)
            ofile.write("\n")

    # 单单保存key, 书本顺序
    output_file = 'lla_headings.txt'
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
                print(f"[ERROR] sec_key not found: {sec_key!r}")
                #assert False
                continue
            
            # 写入文件
            #entry = section_map[sec_key]
            #sechead = entry["sec_heading"]
            #seccontent = entry["content"]
      
            line = f"{sec_key}"
      
            ofile.write(line)
            ofile.write("\n")

    # 保存全部sections, 书本顺序
    output_file = 'lla_sections.txt'
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
                print(f"[ERROR] sec_key not found: {sec_key!r}")
                #assert False
                continue
            
            # 写入文件
            entry = section_map[sec_key]
            sechead = entry["sec_heading"]
            seccontent = entry["content"]
            
            line = f"{sechead}{seccontent}"

            ofile.write(line)
            ofile.write("\n")

            # 用过就删
            del section_map[sec_key]
    # 最后断言 section_map 已经为空, todo, 加上
    assert not section_map, f"[ERROR] Some sec_keys were not written: {list(section_map.keys())}"

    print("\nSummary:")
    print(f"total section number = {total_sec_cnt}")
    print(f"identical section number = {total_identical_sec_cnt}")
    print(f"by average, each section has been seen %.2f times in the mdx." % (float(total_sec_cnt)/total_identical_sec_cnt))

    print(f"\ntotal phrase num in identical sections = {total_phrase_num_in_identical_sections}")
    print(f"by average, each section has phrase num = {total_phrase_num_in_identical_sections} / {total_identical_sec_cnt} = %.2f" % \
          (float(total_phrase_num_in_identical_sections)/total_identical_sec_cnt))

    print("Done with the job, totally takes %.2f s" % (time.time() - start_time))

if __name__ == '__main__':
    do_the_job()
