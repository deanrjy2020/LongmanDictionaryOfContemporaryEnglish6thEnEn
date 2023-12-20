#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil
import time

def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # src
    filename = '../LongmanDictionaryOfContemporaryEnglish6thEnEn.txt'
    #filename = '../A_capital.html'
    #filename = '../test.txt'

    # delete the dst
    if os.path.exists("../LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt"):
        os.remove("../LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt")

    pattern_test_end = re.compile(r'</>')
    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'
    
    # https://forum.freemdict.com/t/topic/24705/34?u=deanrjy2020
    # https://blog.csdn.net/whatday/article/details/107965291
    # 跳转按钮上单词+右上角数字+词性当中单词+右上角数字缺失的问题, 与Amazon 182MB版mdx保持一致
    pattern_has_part_of_speech = re.compile(r'<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_([^<]*)_([^<]*)"> <i>([^<]*)</i></a>')
    total_n=0
    pattern_no_part_of_speech  = re.compile(r'<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_([^<]*)_([^<]*)"> </a>')
    total_m=0
    # bad double qoute, 替换中文左右双引号
    pattern_double_qoute_l = re.compile(r'“')
    dql = 0
    pattern_double_qoute_r = re.compile(r'”')
    dqr = 0
    # bad single qoute, 替换中文左右单引号
    pattern_single_qoute_l = re.compile(r'‘')
    sql = 0
    pattern_single_qoute_r = re.compile(r'’')
    sqr = 0
    # good double qoute twice, 英文双引号2次, 替换成1次
    pattern_double_qoute_twice = re.compile(r'""')
    dqt = 0
    # goog single qoute twice, 英文单引号2次, 替换成一个双引号
    pattern_single_qoute_twice = re.compile(r"''")
    sqt = 0
    # comma comma dot, 替换成省略号
    pattern_ccd = re.compile(r',,\.')
    ccd = 0
    pattern_hegira_calendar = re.compile(r'ˌ\.\.\. ˈ\.\.\.,\.ˌ\.\. ˈ\.\.\.')
    hc = 0
    # dot comma dot
    pattern_dcd = re.compile(r'\.,\.')
    dcd = 0
    # colon comma dot
    pattern_colon_cd = re.compile(r':,\.')
    colon_cd = 0
    # one case to add a space after far
    pattern_space_suspension_points = re.compile(r'class="expr">how far…')
    space_suspension_points = 0
    pattern_bioprospect = re.compile(r'<span class="neutral"> /</span><span class="amevarpron"><span class="neutral"> \$ </span>ˌ\.\.\.\.\.\. ˈ\.\.\.</span><span class="neutral">/</span>')
    bioprospect = 0
    pattern_self_congratulation = re.compile(r'<span class="neutral"> /</span><span class="amevarpron"><span class="neutral"> \$ </span>ˌ\.\.ˈ\.\.\.\.\.</span><span class="neutral">/</span>')
    self_congratulation = 0
    pattern_self_regulation = re.compile(r'<span class="neutral"> /</span><span class="amevarpron"><span class="neutral"> \$ </span>ˌ\. ˈ\.\.\.\.\.</span><span class="neutral">/</span>')
    self_regulation = 0
    pattern_five_points = re.compile(r'\.\.\.\.\.')
    five_points = 0
    pattern_augustine_st_capillary_action = re.compile(r'<span class="neutral"> /</span><span class="amevarpron"><span class="neutral"> \$ </span>ˌ\.\.\.\. ˈ\.\.</span><span class="neutral">/</span>')
    augustine_st_capillary_action = 0
    pattern_augustine_st_2 = re.compile(r'<span class="neutral"> /</span><span class="amevarpron"><span class="neutral"> \$ </span>ˌ\.\.\.\. ˈ\.\.\.\.</span><span class="neutral">/</span>')
    augustine_st_2 = 0

    pattern_two_words_no_phonetic_symbol = re.compile(r'<span class="neutral"> /</span><span class="amevarpron"><span class="neutral"> \$ </span>([^<]*)</span><span class="neutral">/</span>')
    two_words_no_phonetic_symbol = 0
    two_words_no_phonetic_symbol_search = 0

    pattern_two_words_no_phonetic_symbol_round2 = re.compile(r'<span class="neutral"> /</span><span class="pron"></span><span class="amevarpron"><span class="neutral"> \$ </span>([^<]*)</span><span class="neutral">/</span>')
    two_words_no_phonetic_symbol_round2 = 0
    two_words_no_phonetic_symbol_round2_search = 0

    pattern_soy_sauce = re.compile(r'<span class="amevarpron"><span class="neutral"> \$ </span>ˈ\.\.</span>')
    soy_sauce = 0

    pattern_space_4_dot = re.compile(r' \.\.\.\.')
    space_4_dot = 0

    pattern_only_4_dot = re.compile(r'\.\.\.\.')
    only_4_dot = 0

    # back qoute issue
    pattern_back_qoute = re.compile(r"` ([^<]*)'[str]")
    back_qoute = 0
    
    with open(filename) as ifile:
        for line in ifile:
            # ======================================= read only to get the test_name =======================================
            if state == STATE_TEST_ENDED:
                state = STATE_TEST_STARTED
                test_name = line.strip()
            m = pattern_test_end.search(line)
            if m:
                # no natter what the state is, end everything if we see the test end pattern.
                state = STATE_TEST_ENDED
                test_name = 'init_invalid_name'
            # ======================================= do the modifications =======================================
            # line_has=line and n=0, if not found.
            line_has,n=pattern_has_part_of_speech.subn(r'<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_\1_\2"><span class="hw">\1<sup>\2</sup></span> <i>\3</i></a>', line)
            total_n = total_n + n

            line_no,m=pattern_no_part_of_speech.subn(r'<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_\1_\2"><span class="hw">\1<sup>\2</sup></span> </a>', line_has)
            total_m = total_m + m

            # 1st, bad double
            line1,n = pattern_double_qoute_l.subn(r'"', line_no)
            dql = dql + n
            # 2ne
            line2,n = pattern_double_qoute_r.subn(r'"', line1)
            dqr = dqr + n
            # 3rd, bad single
            #line3 = line2.replace("‘", "'")
            line3,n = pattern_single_qoute_l.subn(r"'", line2)
            sql = sql + n
            # 4th
            #line4 = line3.replace("’", "'")
            line4,n = pattern_single_qoute_r.subn(r"'", line3)
            sqr = sqr + n
            # 5th, good double twice, replaced with one good double: "" -> "
            line5,n = pattern_double_qoute_twice.subn(r'"', line4)
            dqt = dqt + n
            # 6th, good single twice, replace with one good double: '' -> "
            line6,n = pattern_single_qoute_twice.subn(r'"', line5)
            sqt = sqt + n
            # 7th
            line7,n = pattern_ccd.subn(r' …', line6)
            ccd = ccd + n
            # 8th
            line8,n = pattern_hegira_calendar.subn(r'ˈhedʒərə,ˈkæləndə', line7)
            hc = hc + n
            # 9th
            line9,n = pattern_dcd.subn(r'.', line8)
            dcd = dcd + n
            # 10th
            line10,n=pattern_colon_cd.subn(r' …', line9)
            colon_cd = colon_cd + n
            # 11th, only add 1 sapce
            line11,n=pattern_space_suspension_points.subn(r'class="expr">how far …', line10)
            space_suspension_points = space_suspension_points + n
            # 12th, remove
            line12,n=pattern_bioprospect.subn(r'', line11)
            bioprospect = bioprospect + n
            # 13th, remove
            line13,n=pattern_self_congratulation.subn(r'', line12)
            self_congratulation = self_congratulation + n
            # 14th, remove
            line14,n=pattern_self_regulation.subn(r'', line13)
            self_regulation = self_regulation + n
            # 15th
            line15,n=pattern_five_points.subn(r'.', line14)
            five_points = five_points + n
            # 16th
            line16,n=pattern_augustine_st_capillary_action.subn(r'', line15)
            augustine_st_capillary_action = augustine_st_capillary_action + n
            # 17th
            line17,n=pattern_augustine_st_2.subn(r'', line16)
            augustine_st_2 = augustine_st_2 + n

            # 18th
            # check the log
            position = 0
            for m in re.finditer(pattern_two_words_no_phonetic_symbol, line17):
                two_words_no_phonetic_symbol_search = two_words_no_phonetic_symbol_search + 1
                position = m.start()
                #print("round1: " + test_name)
                #print(line17[position:position+200])
            # modify
            line18,n=pattern_two_words_no_phonetic_symbol.subn(r'', line17)
            if n !=0 and test_name == "haulier":
                # this is a WAR since I don't find a solution to exclude this one in the re.
                print("skip the 18th replacement for haulier keyword.")
                assert n == 1
                line18 = line17
            else:
                # count the repalcement.
                two_words_no_phonetic_symbol = two_words_no_phonetic_symbol + n
                # after replaced
                #if position != 0:
                #    print(line18[position:position+50])

            # 19th
            position = 0
            for m in re.finditer(pattern_two_words_no_phonetic_symbol_round2, line18):
                two_words_no_phonetic_symbol_round2_search = two_words_no_phonetic_symbol_round2_search + 1
                position = m.start()
                #print("round2: " + test_name)
                #print(line18[position:position+200])
            # modify
            line19,n=pattern_two_words_no_phonetic_symbol_round2.subn(r'', line18)
            # count the repalcement.
            two_words_no_phonetic_symbol_round2 = two_words_no_phonetic_symbol_round2 + n
            # after replaced
            #if position != 0:
            #    print(line19[position:position+50])

            # 20th
            line20,n=pattern_soy_sauce.subn(r'', line19)
            soy_sauce = soy_sauce + n

            # 21st
            # only replace the 4dot to '…', don't change the space.
            line21,n=pattern_space_4_dot.subn(r' …', line20)
            space_4_dot = space_4_dot + n

            # 22nd
            # For the rest 351 '....' = 243 '[a-z]\.\.\.\.' + 108 '>....'
            # replace the 4dot to '…', and add the space before dot.
            line22,n=pattern_only_4_dot.subn(r' …', line21)
            only_4_dot = only_4_dot + n

            # 23rd
            position = 0
            for m in re.finditer(pattern_back_qoute, line22):
                back_qoute = back_qoute + 1
                position = m.start()
                print(test_name)
                print(line22[position-100:position+100])






            with open('../LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt', 'a') as the_file:
                the_file.write(line22)



    print(back_qoute)

    print("Summary:")
    print("Done with the job, totally takes %s s" % (time.time() - start_time))
    
    print("has_part_of_speech replaced %s times" % total_n)
    print("no_part_of_speech replaced %s times" % total_m)
    assert total_n == 17699
    assert total_m == 314
    """
    has_part_of_speech replaced 17699 times
     no_part_of_speech replaced 314 times

    The same if I search the 2 re ex in the VSC.
  
    in vsc, searching '<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_' hits 18255, why?? 18255-17699-314 = 242 ???

    solved, see parse_ldoce6enen_chwd.py
    """
    
    print("double qoute left=%s" % dql) #21
    print("double qoute right=%s" % dqr) # 21
    assert dql == 21
    assert dqr == 21
    
    print("single qoute left=%s" % sql) #23009
    print("single qoute right=%s" % sqr) #107587
    assert sql == 23009
    assert sqr == 107587

    print("double qoute twice=%s" % dqt) # 96
    print("single qoute twice=%s" % sqt) # 3685
    assert dqt == 96
    assert sqt == 3685

    print("commaCommaDot=%s" % ccd) # 10
    assert ccd == 10
    
    print("hegira_calendar=%s" % hc) # 1
    assert hc == 1

    print("dotCommaDot=%s" % dcd) # 8
    assert dcd == 8

    print("colon_cd=%s" % colon_cd) # 2
    assert colon_cd == 2

    print("space_suspension_points=%s" % space_suspension_points) # 1
    assert space_suspension_points == 1

    print("bioprospect=%s" % bioprospect) # 3
    assert bioprospect == 3
    
    print("self_congratulation=%s" % self_congratulation) # 2
    assert self_congratulation == 2

    print("self_regulation=%s" % self_regulation) # 2
    assert self_regulation == 2

    print("five_points=%s" % five_points) # 6
    assert five_points == 6

    print("augustine_st_capillary_action=%s" % augustine_st_capillary_action) # 2
    assert augustine_st_capillary_action == 2

    print("augustine_st_2=%s" % augustine_st_2) # 1
    assert augustine_st_2 == 1

    # found 94, but replaced 93
    print("two_words_no_phonetic_symbol_search=%s" % two_words_no_phonetic_symbol_search) # 94
    assert two_words_no_phonetic_symbol_search == 94
    print("two_words_no_phonetic_symbol=%s" % two_words_no_phonetic_symbol) # 93
    assert two_words_no_phonetic_symbol == 93

    print("two_words_no_phonetic_symbol_round2_search=%s" % two_words_no_phonetic_symbol_round2_search) #7
    print("two_words_no_phonetic_symbol_round2=%s" % two_words_no_phonetic_symbol_round2) #7
    assert two_words_no_phonetic_symbol_round2_search == 7
    assert two_words_no_phonetic_symbol_round2 == 7

    print("soy_sauce=%s" % soy_sauce) #1
    assert soy_sauce == 1

    print("space_4_dot=%s" % space_4_dot) # 181
    assert space_4_dot == 181
    print("only_4_dot=%s" % only_4_dot) #351
    assert only_4_dot == 351

if __name__ == '__main__':
    do_the_job()
