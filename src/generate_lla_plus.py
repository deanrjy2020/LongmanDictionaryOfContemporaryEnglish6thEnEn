#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import re
import shutil
import time
import hashlib
from bs4 import BeautifulSoup, Tag
from copy import copy
from collections import Counter

'''

mdx: https://forum.freemdict.com/t/topic/42061

用soup解析html格式. 得到里面LLA信息
弄到一半...

run: PYTHONUTF8=1 python src/generate_lla_plus.py |& tee lla_plus_log.txt

在lla_section.txt里面做替换(选中大小写和regex):
@@([A-Z0-9]+)@@
\n@@\1@@

book order
BC里面去掉不重要的, 947 diff

两边都换行
比较, 得到2097 diff

改plus这边去match,

76 diff
'''

#不要加\n, 用上面的regex在文本里面替换加上\n
NEW_LINE = "" 
section_map = {}
# 直接从mdx读进来就是LLA book order, key=heading+phrases
section_keys_lla_book_order = []
total_sec_cnt = 0 # adding all the cnt in the sec_to_cnt.
total_phrase_num_in_identical_sections = 0

def hash_text(s):
    return hashlib.sha256(s.encode("utf8")).hexdigest()

def register_section(secheading, all_phrase, sec_value, phrase_cnt, test_name):
    # 里面有全大写的, 影响排序
    if 'to ask someone questions for a newspaper' in secheading or \
        'when you believe or do not believe that' in secheading or \
        'the Internet and places on the Internet' in secheading or \
        'things you do on the Internet' in secheading:
        # 'to ask someone questions for a newspaper, TV programme etc' 里面的TV不改.
        # 'when you believe or do not believe that God'
        # 'the Internet and places on the Internet'
        # 'things you do on the Internet'
        None
    else:
        secheading = secheading.lower()
    # 两个或以上空格 → 一个空格
    secheading = re.sub(r'\s{2,}', ' ', secheading)
    # 和ldoce6一样
    secheading = secheading.replace(" / ", "/")

    # 两个或以上空格 → 一个空格
    all_phrase = re.sub(r'\s{2,}', ' ', all_phrase)    
    all_phrase = all_phrase.replace(" / ", "/")

    # 处理 content问题
    # 两个或以上空格 → 一个空格
    sec_value = re.sub(r'\s{2,}', ' ', sec_value)
    # 和ldoce6一样
    sec_value = sec_value.replace(" / ", "/")
    #sec_value = sec_value.replace("’", "'")


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

# =======================================================
test_name = 'init_invalid_name' # =headword
total_phrase_num = 0
total_section_num = 0

log_info = 0

import re

def assert_no_chinese(s: str):
    assert not re.search(r'[\u4e00-\u9fff]', s), f"String contains Chinese: {s!r}"

def get_en_text(obj) -> str:
    # 浅拷贝，避免破坏原 soup
    copy_obj = copy(obj)
    # 删除中文节点
    for zh in copy_obj.find_all("zh_cn"):
        zh.decompose()
    
    text = copy_obj.get_text(strip=True)
    assert_no_chinese(text)

    return text

def parse_section(section):
    assert section.get("class") == ["Section"]

    kids = section.find_all("span", recursive=False)

    # 第1个孩子, sk_title, 一定是空的.
    assert kids[0].get("class") == ["sk_title"], f"test_name={test_name}"
    sk_title = kids[0].get_text(strip=True)
    assert not sk_title
    
    # 第2个孩子, SECDEF
    assert kids[1].get("class") == ["SECDEF"], f"test_name={test_name}"
    # 浅拷贝，避免破坏原 soup
    secdef = copy(kids[1])
    # 删除中文节点
    for zh in secdef.find_all("zh_cn"):
        zh.decompose()
    # 确认SECDEF只有一个孩子
    secdef_children = secdef.find_all("span", recursive=False)
    assert len(secdef_children) == 1
    secdef_children[0].get("class") == ["SECNR"]
    # 删除 SECNR
    for secnr in secdef.find_all("span", class_="SECNR"):
        secnr.decompose()
    # 取剩余文本
    secheading = secdef.get_text(strip=True)
    assert_no_chinese(secheading)
    assert secheading[0].isalpha(), f"test_name={test_name}, text={secheading}"
    print(f"secheading={secheading}")
    
    one_sec_all_phrase = ""
    one_sec_all_phrase_cnt = 0
    seccontent = ""

    # 剩下的孩子, 第3个开始
    for idx, kid in enumerate(kids[2:]):
        # ACTIVATOR 处理过了, 不管
        # 其他2个, 检查过了, 没用
        if kid.get("class") == ["ACTIVATOR"] or \
            kid.get("class") == ["word_table"] or \
            kid.get("class") == ["Hint"] or \
            kid.get("class") == ["addtion"]:
            continue

        
        global total_phrase_num
        total_phrase_num += 1
        print(f"total_phrase_num={total_phrase_num}")
        example_idx = 0
        subphrase_idx_in_phrase = 0

        # Exponent对应section里面的一个phrase 块
        assert kid.get("class") == ["Exponent"], \
            f"test_name={test_name}, Section child {idx} not Exponent: {kid.get('class')}"
        phrase_block_children = kid.find_all("span", recursive=False)
        for phrase_block_idx, phrase_block_child in enumerate(phrase_block_children):
            if phrase_block_child.get("class") == ["EXP"]:
                # phrase 开始
                assert phrase_block_idx == 0

                # # 浅拷贝，避免破坏原 soup
                # copy_exp = copy(phrase_block_child)
                # # 删除中文节点
                # for zh in copy_exp.find_all("zh_cn"):
                #     zh.decompose()
                
                phrase = phrase_block_child.get_text(strip=True)
                assert_no_chinese(phrase)

                # one_sec_all_phrase_cnt 就是phrase idx in cur section
                tmp = f"{NEW_LINE}@@PHRASE{one_sec_all_phrase_cnt}@@{phrase}"
                print(tmp)
                seccontent += tmp

                one_sec_all_phrase += tmp
                one_sec_all_phrase_cnt += 1

                example_idx = 0
                subphrase_idx_in_phrase = 0

            elif phrase_block_child.get("class") == ["PRON"]:
                # 音标, 没用
                None
            elif phrase_block_child.get("class") == ["LABEL"]:
                None
            elif phrase_block_child.get("class") == ["GRAM"]:
                # 动词, 名词等词性, 没用
                None
            elif phrase_block_child.get("class") == ["DEF"]:
                # phrase 的define
                define = get_en_text(phrase_block_child)

                tmp = f"{NEW_LINE}@@DEFINE@@{define}"
                print(tmp)
                seccontent += tmp

                example_idx = 0

            elif phrase_block_child.get("class") == ["Exas"]:
                # 所有的例子
                example_children = phrase_block_child.find_all("span", recursive=False)
                for example_child_idx, example_child in enumerate(example_children):
                    # 这个example可以是phrase的exam, 也可以是subphrase的exam, 就是按顺序下来.
                    if example_child.get("class") == ["EXAMPLE"]:
                        example = get_en_text(example_child)
                        #example = example_child.get_text(strip=True)

                        # 空的话跳过
                        if not example:
                            continue

                        tmp = f"{NEW_LINE}@@EXAMPLE{example_idx}@@{example}"
                        print(tmp)
                        seccontent += tmp

                        example_idx += 1
                        
                    elif example_child.get("class") == ["PROPFORM"]:
                        THESPROPFORM = get_en_text(example_child)
                        #THESPROPFORM = example_child.get_text(strip=True)

                        tmp = f"{NEW_LINE}@@THESPROPFORM{subphrase_idx_in_phrase}@@{THESPROPFORM}"
                        print(tmp)
                        seccontent += tmp

                        example_idx = 0
                        subphrase_idx_in_phrase += 1

                    elif example_child.get("class") == ["LABEL"]:
                        #没用
                        None
                    elif example_child.get("class") == ["GRAM"]:
                        #没用
                        None
                    elif example_child.get("class") == ["GLOSS"]:
                        # 可以是subphrase的gloss, 或者其他的?
                        gloss = get_en_text(example_child)
                        #gloss = example_child.get_text(strip=True)

                        tmp = f"{NEW_LINE}@@GLOSS@@{gloss}"
                        print(tmp)
                        seccontent += tmp

                        example_idx = 0

                    else:
                        assert False, f"test_name={test_name}, class = {example_child.get("class")}"
            elif phrase_block_child.get("class") == ["Variant"]:
                variant_children = phrase_block_child.find_all("span", recursive=False)
                varitype = None
                for variant_child_idx, variant_child in enumerate(variant_children):
                    if variant_child.get("class") == ["VARITYPE"]:
                        varitype = get_en_text(variant_child)

                    elif variant_child.get("class") == ["GRAM"]:
                        None
                        #内容无用
                    elif variant_child.get("class") == ["VAR"]:
                        variant = get_en_text(variant_child)
                        #variant = variant_child.get_text(strip=True)

                        if varitype:
                            tmp = f"{NEW_LINE}@@VARIANT@@{varitype} {variant}"
                            varitype = None
                        else:
                            tmp = f"{NEW_LINE}@@VARIANT@@{variant}"
                        
                        print(tmp)
                        seccontent += tmp

                        example_idx = 0

                    else:
                        assert variant_child.get("class") == ["LABEL"]
                        # label 无用
            elif phrase_block_child.get("class") == ["GLOSS"]:
                gloss_children = phrase_block_child.find_all("span", recursive=False)
                if len(gloss_children) == 0:
                    gloss = get_en_text(phrase_block_child)
                elif len(gloss_children) == 1:
                    gloss = get_en_text(gloss_children[0])
                    #gloss = gloss_children[0].get_text(strip=True)                    
                else:
                    assert False
                
                tmp = f"{NEW_LINE}@@GLOSS@@{gloss}"
                print(tmp)
                seccontent += tmp

                example_idx = 0
            elif phrase_block_child.get("class") == ["PROPFORM"]:
                propform_children = phrase_block_child.find_all("span", recursive=False)
                prop = ""
                if len(propform_children) == 0:
                    # 没有孩子直接用自己去get
                    prop = get_en_text(phrase_block_child)
                else:
                    assert len(propform_children) == 1
                    prop = get_en_text(propform_children[0])
                    #prop = propform_children[0].get_text(strip=True)

                tmp = f"{NEW_LINE}@@THESPROPFORM{subphrase_idx_in_phrase}@@{prop}"
                print(tmp)
                seccontent += tmp

                example_idx = 0
                subphrase_idx_in_phrase += 1

            elif phrase_block_child.get("class") == ["RunOn"]:
                continue
                # LDOCE6里面可能没有这个部分, todo
                runon_children = phrase_block_child.find_all("span", recursive=False)
                for runon_child_idx, runon_child in enumerate(runon_children):
                    if runon_child.get("class") == ["SPELLING"]:
                        spelling = get_en_text(runon_child)
                        #spelling = runon_child.get_text(strip=True)

                        tmp = f"{NEW_LINE}@@RUNONSPELL@@{spelling}"
                        print(tmp)
                        seccontent += tmp

                        example_idx = 0
                        
                    elif runon_child.get("class") == ["RUNONDEF"]:
                        runondef = get_en_text(runon_child)
                        #runondef = runon_child.get_text(strip=True)

                        tmp = f"{NEW_LINE}@@RUNONDEF@@{runondef}"
                        print(tmp)
                        seccontent += tmp

                        example_idx = 0

                    elif runon_child.get("class") == ["Variant"]:
                        Variant = get_en_text(runon_child)
                        #Variant = runon_child.get_text(strip=True)

                        tmp = f"{NEW_LINE}@@RUNONVARI@@{Variant}"
                        print(tmp)
                        seccontent += tmp

                        example_idx = 0

                    elif runon_child.get("class") == ["PRON"]:
                        # 音标没用
                        None
                    elif runon_child.get("class") == ["PROPFORM"]:
                        PROPFORM = get_en_text(runon_child)
                        #PROPFORM = runon_child.get_text(strip=True)

                        tmp = f"{NEW_LINE}@@RUNONPROPFORM@@{PROPFORM}"
                        print(tmp)
                        seccontent += tmp

                        example_idx = 0

                    elif runon_child.get("class") == ["GRAM"]:
                        # 词性, 没用
                        None
                    elif runon_child.get("class") == ["LABEL"]:
                        # 没用
                        None
                    elif runon_child.get("class") == ["Exas"]:
                        exams_children = runon_child.find_all("span", recursive=False)
                        #assert len(exams_children) == 1, f"len(exams_children)={len(exams_children)}"
                        for exams_child_idx, exams_child in enumerate(exams_children):
                            if exams_child.get("class") == ["EXAMPLE"]:
                                exa = get_en_text(exams_child)
                                #exa = exams_child.get_text(strip=True)

                                tmp = f"{NEW_LINE}@@RUNON_EXAS_EXA{example_idx}@@{exa}"
                                print(tmp)
                                seccontent += tmp

                                example_idx += 1
                                
                            elif exams_child.get("class") == ["PROPFORM"]:
                                propform = get_en_text(exams_child)
                                #propform = exams_child.get_text(strip=True)

                                tmp = f"{NEW_LINE}@@RUNON_EXAS_PROPFORM@@{propform}"
                                print(tmp)
                                seccontent += tmp

                                example_idx = 0

                            elif exams_child.get("class") == ["GLOSS"]:
                                gloss = get_en_text(exams_child)
                                #gloss = exams_child.get_text(strip=True)

                                tmp = f"{NEW_LINE}@@RUNON_EXAS_GLOSS@@{gloss}"
                                print(tmp)
                                seccontent += tmp

                                example_idx = 0

                            elif exams_child.get("class") == ["LABEL"]:
                                # 没用
                                None
                            else:
                                assert False
                    else:
                        assert False, f"class = {runon_child.get("class")}"
                
            elif phrase_block_child.get("class") == ["addtion"]:
                assert False
            elif phrase_block_child.get("class") == ["Hint"]:
                # 不要了
                None
            elif phrase_block_child.get("class") == ["ACTIVATOR"]:
                # 不完整的, 忽略
                None
            else:
                assert False, f"test_name={test_name}, class={phrase_block_child.get("class")}"
    
    # 得到一个section了
    register_section(secheading, one_sec_all_phrase, seccontent, one_sec_all_phrase_cnt, test_name)


def parse_activator(activ_span):
    """
    activ_span: <span class="ACTIVATOR">
    """
    assert activ_span.name == "span"
    assert activ_span.get("class") == ["ACTIVATOR"]

    children = activ_span.find_all("span", recursive=False)
    assert len(children) == 1
    assert children[0].get("class") == ["Section"]

    global total_section_num
    total_section_num += 1
    print(f"\ntotal_section_num={total_section_num}")

    parse_section(children[0])


def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # 两个独立的
    debug = 0
    log_info = 0
    if debug:
        # 初始数据
        filename = 'data/bar.html'
    else:
        filename = 'data/LLA_plus.txt'

    '''
    py解析的是txt, 不会直接用mdx, double check一下txt对应的mdx的md5
    '''
    mdx_md5 = hashlib.md5(open('data/LLA_plus.mdx','rb').read()).hexdigest()
    assert mdx_md5 == 'c9cc2265e2914e33fcb18c66508e3b5a'

    # verify the md5 of the input file.
    md5 = hashlib.md5(open(filename,'rb').read()).hexdigest()
    if not debug:
        '''
        todo, 手动改了:
        ’ -> '
        
        ‘ -> '
        
        to ask someone questions for a newspaper, tv programme etc@@PHRASE0@@interview@@PHRASE1@@interview
        -> 
        to ask someone questions for a newspaper, TV programme etc@@PHRASE0@@interview@@PHRASE1@@interview

        ways of beginning a letter@@PHRASE0@@Dear Sir/Sirs/Sir or Madam@@PHRASE1@@Dear Mr Wiggins/Ms Harper@@PHRASE2@@Dear Jim/Sarah etc@@PHRASE3@@Hi
        -> Hi / Hey

        'anexperiment' -> 'an experiment'

        add keyword的 2. to add more to an amount or cost 下面的add phrase的中文结构修正:
        <zh_cn>增加；添加<zh_cn>
        ->
        <zh_cn>增加；添加</zh_cn>

        better then all others里面一个空的PROPFORM span删掉.
        '''
        #assert md5 == '68406aca5bccd72b352ff18737c66483'
        None

    POS_HEAD = 'POSITION_HEAD'
    POS_BODY = 'POSITION_BODY'
    POS_TAIL = 'POSITION_TAIL'
    line_position = POS_TAIL

    global test_name
    with open(filename, encoding="utf8") as ifile:
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

            # 这个要删掉, bug.
            # if test_name == '30 metres / 100 feet etc high' or \
            #     test_name == '40 metres / 100 feet etc deep':
            #     continue

            # if the content doesn't have 'Longman Language Activator' string, skip
            if line_position != POS_BODY:
                continue
            # 特殊的单词, 忽略
            # if line_position == POS_BODY and test_name == 'faq-about 33de5e2430c248afb78dd34e20f35466':
            #     continue

            soup = BeautifulSoup(line, "lxml")
            
            concept_spans = soup.find_all("span", class_="Concept")
            if len(concept_spans) == 0:
                continue
            assert len(concept_spans) == 1, \
                f"test_name={test_name}, len(concept_spans) = {len(concept_spans)}"

            ppp = concept_spans[0].parent
            acts_spans = ppp.find_all("span", recursive=False)
            for idx, act_span in enumerate(acts_spans):
                if act_span.get("class") == ["ACTIVATOR"]:
                    parse_activator(act_span)

    # 单单保存heading到文件.
    with open("lla_plus_headings.txt", "w", encoding="utf-8") as f:
        for s in section_keys_lla_book_order:
            f.write(s + "\n")

    # 按书本顺序, 保存全部sections
    output_file = 'lla_plus_sections.txt'
    # 如果只写heading的话, 和上面的一样, 用于比对顺序一致.
    only_write_key = False
    global section_map
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
                assert False, f"[ERROR] has_seen_someone_who_hates_you = {has_seen_someone_who_hates_you}, sec_key not found: {sec_key!r}"

            # 写入文件
            entry = section_map[sec_key]
            sechead = entry["sec_heading"]
            seccontent = entry["content"]
            
            if only_write_key:
                line = f"{sec_key}"
            else:
                line = f"{sechead}{seccontent}"
            
            ofile.write(line)
            ofile.write("\n")

            # 用过就删
            del section_map[sec_key]
    # 最后断言 section_map 已经为空
    assert not section_map, f"[ERROR] Some sec_keys were not written: {list(section_map.keys())}"


    print("\nSummary:")
    assert total_section_num == 4953 and total_sec_cnt == 4953 and len(section_map) == 0
    assert  total_phrase_num == 22068 and total_phrase_num_in_identical_sections == 22068
    print(f"identical section number = {total_sec_cnt}")
    print(f"total phrase num in identical sections = {total_phrase_num_in_identical_sections}")
    print(f"by average, each section has phrase num = {total_phrase_num_in_identical_sections} / {total_sec_cnt} = %.2f" % \
            (float(total_phrase_num_in_identical_sections)/total_sec_cnt))

    print("Done with the job, totally takes %.2f s" % (time.time() - start_time))

if __name__ == '__main__':
    do_the_job()
