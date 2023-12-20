#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import time

def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # src
    filename = 'data/LLA.txt'
    #filename = 'data/LLA_BEST.html'
    #filename = 'data/LLA_BURN.html'
    #filename = 'data/LLA_ACROSS.html'

    pattern_test_end = re.compile(r'</>')
    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'

    pattern_target_line = re.compile(r'href="LLA.CSS"')

    pattern_heading = re.compile(r'<span class="SECNR">([^<]*)</span>([^<]*)<zh_cn>')
    # most heading can be found with the pattern_heading, but 'ACROSS, BUT, COMPETITION, KICK, NEVER, NO MATTER WHAT/HOW MUCH ETC, PATTERN' 7 headings only have 1 section and no Chinese, so not ended with <zh_cn>
    # need to search with pattern_heading_alternative
    pattern_heading_alternative = re.compile(r'<span class="SECNR">([^<]*)</span>([^<]*)</span>')

    pattern_phrase = re.compile(r'<span class="EXP"><span class="neutral"> </span>([^<]*)</span>')

    all_keywords = ''
    sec_to_cnt = { } # dict, section (h, phr1, phr2, ...) to cnt (dup headings ?)
    sec_to_keyword = { }

    with open(filename, encoding="utf8") as ifile:
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
            m = pattern_target_line.search(line)
            if not m: continue

            all_keywords += test_name + '\n'

            only_one_heading = 0
            pattern_heading_for_search = pattern_heading
            m = pattern_heading_for_search.findall(line)
            #print(type(m[0])) # m is list, m[0] is a tuple
            #print(m)
            if not m:
                pattern_heading_for_search = pattern_heading_alternative
                only_one_heading = 1
                m = pattern_heading_for_search.findall(line)

            if len(m) == 1:
                only_one_heading = 1

            idx = -1 # the idenx of the itr, start from 0
            prev_heading_start_pos = 0
            cur_heading_start_pos = 0
            prev_heading = ''
            # loop all the headings
            for itr in re.finditer(pattern_heading_for_search, line):
                #print(type(itr))
                #print(itr)

                # build the section key
                section = ''

                # save the start start pos
                prev_heading_start_pos = cur_heading_start_pos
                cur_heading_start_pos = itr.start()

                if prev_heading_start_pos != 0:
                    # each section has at least one phrase, start the section witht the heading str here.
                    section += prev_heading + '@'

                    m_phrase = pattern_phrase.findall(line)
                    phrase_itr_idx = -1
                    # find all the phrase between prev_heading_start_pos and cur_heading_start_pos
                    for phrase_itr in re.finditer(pattern_phrase, line):
                        phrase_itr_idx += 1
                        phrase = m_phrase[phrase_itr_idx].replace("’", "'")
                        #print(m_phrase)
                        #print(phrase)
                        if prev_heading_start_pos < phrase_itr.start() and phrase_itr.start() < cur_heading_start_pos:
                            #heading_to_phrase[prev_heading] = heading_to_phrase.setdefault(prev_heading, '') + phrase + ', '
                            section += phrase + ', '
                    # done with the section build, put it to map
                    sec_to_cnt[section] = sec_to_cnt.setdefault(section, 0) + 1
                    #sec_to_keyword[section] = sec_to_keyword.setdefault(section, '') + test_name + ', '
                    sec_to_keyword[section] = 'X'
                
                # get the heading
                idx += 1
                #print(m[idx][2])
                heading = " ".join(m[idx][1].split())
                
                # save the heading for next itr use.
                prev_heading = heading.replace("’", "'")
            
            # extra step for the last section
            section = ''
            section += prev_heading + '@'
            m_phrase = pattern_phrase.findall(line)
            phrase_itr_idx = -1
            # find all the phrase between prev_heading_start_pos and cur_heading_start_pos
            for phrase_itr in re.finditer(pattern_phrase, line):
                phrase_itr_idx += 1
                phrase = m_phrase[phrase_itr_idx].replace("’", "'")
                #print(m_phrase)
                #print(phrase)
                if only_one_heading == 0 and prev_heading_start_pos < phrase_itr.start() and phrase_itr.start() < cur_heading_start_pos:
                    #heading_to_phrase[prev_heading] = heading_to_phrase.setdefault(prev_heading, '') + phrase + ', '
                    section += phrase + ', '
                elif only_one_heading == 1:
                    # this case there is only one section and adding all the phrase to the section.
                    section += phrase + ', '
            # doen with the last section build, put it to map
            sec_to_cnt[section] = sec_to_cnt.setdefault(section, 0) + 1
            #sec_to_keyword[section] = sec_to_keyword.setdefault(section, '') + test_name + ', '
            sec_to_keyword[section] = 'X'


    with open('lla_866_keywords_LLA20190315.txt', 'w', encoding="utf8") as the_file:
        the_file.write(all_keywords)

    #print(sec_to_cnt)
    sorted_sec_to_cnt = dict(sorted(sec_to_cnt.items()))
    #sorted_sec_to_cnt = dict(sec_to_cnt.items())
    with open('lla_sec_to_cnt_LLA20190315.txt', 'w', encoding="utf8") as the_file:
        for key in sorted_sec_to_cnt:
            str = "%s, %s\n" % (key, sorted_sec_to_cnt[key])
            the_file.write(str)

    sorted_sec_to_keyword = dict(sorted(sec_to_keyword.items()))
    #sorted_sec_to_keyword = dict(sec_to_keyword.items())
    with open('lla_sec_to_keyword_LLA20190315.txt', 'w', encoding="utf8") as the_file:
        for key in sorted_sec_to_keyword:
            str = "%s, %s\n" % (key, sorted_sec_to_keyword[key])
            the_file.write(str)

    print("Summary:")
    print("Done with the job, totally takes %s s" % (time.time() - start_time))
    
if __name__ == '__main__':
    do_the_job()
