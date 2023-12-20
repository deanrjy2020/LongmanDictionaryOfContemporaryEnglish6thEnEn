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
    debug = 0
    if debug:
        #filename = 'data/Longman Language Activator EnEn_ACROSS.html'
        filename = 'data/Longman Language Activator EnEn_BURN.html'
    else:
        filename = 'data/Longman Language Activator EnEn.txt'

    pattern_test_end = re.compile(r'</>')
    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'

    pattern_target_line = re.compile(r'<span style="color: white; background-color:#A9A9A9">')

    pattern_heading = re.compile(r'<a name="index-([^<]*)"></a><b>([^<]*)</b>([^<]*)</div>')
    pattern_phrase = re.compile(r'■<b><trn>([^<]*)</trn>')
    pattern_example = re.compile(r'<ex><font color=gray>([^<]*)</font>')

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

            m = pattern_heading.findall(line)
            heading_idx = -1 # the index of the heading_itr, start from 0
            # loop all the headings
            for heading_itr in re.finditer(pattern_heading, line):
                heading_idx += 1
                heading_str = m[heading_idx][2].strip().replace("’", "'")

                # build the section key  
                section = heading_str.lower() + '@'
                if debug: print(section)

                # for all the phrase
                m_phrase = pattern_phrase.findall(line)
                phrase_itr_idx = -1
                for phrase_itr in re.finditer(pattern_phrase, line):
                    phrase_itr_idx += 1
                    phrase_str = m_phrase[phrase_itr_idx].replace("’", "'")
                    
                    # the phrase must be after the valid lla heading
                    if phrase_itr.start() < heading_itr.start():
                        continue

                    # find the closest heading before this phrase
                    phrase_closest_heading_itr = iter([]) # must exists.
                    for closest_heading_itr in re.finditer(pattern_heading, line):
                        if closest_heading_itr.start() < phrase_itr.start():
                            phrase_closest_heading_itr = closest_heading_itr
                        else:
                            break
                    if debug: print('\tphrase_closest_heading_itr=%s' % phrase_closest_heading_itr)
                    if phrase_closest_heading_itr.start() != heading_itr.start():
                        # done with the cur section.
                        break

                    # Now it is a good phrase, add it to the section
                    section += phrase_str + '|'
                    if debug: print('\tsection=%s' % section)

                # add the first example in this section (after heading)
                first_example_str = ''
                m_example = pattern_example.findall(line)
                example_itr_idx = -1
                for example_itr in re.finditer(pattern_example, line):
                    example_itr_idx += 1
                    if heading_itr.start() < example_itr.start():
                        first_example_str = m_example[example_itr_idx]
                        break
                # only the 'types of film' heading, which is the second section of 'film' keyword,
                # has no example.
                if heading_str == 'types of film':
                    assert first_example_str == ''
                section += '#' + first_example_str.replace("’", "'") \
                                                  .replace("‘","'") \
                                                  .replace('"',"'") \
                                                  .strip()

                # done with the section build, put it to map
                sec_to_cnt[section] = sec_to_cnt.setdefault(section, 0) + 1
                sec_to_keyword[section] = sec_to_keyword.setdefault(section, '') + test_name + ', '

    assert len(sec_to_cnt) == len(sec_to_keyword)

    with open('lla_866_keywords_LLAenen20130622.txt', 'w', encoding="utf8") as the_file:
        the_file.write(all_keywords)

    if debug:
        sorted_sec_to_cnt = dict(sec_to_cnt.items())
    else:
        sorted_sec_to_cnt = dict(sorted(sec_to_cnt.items()))
    
    with open('lla_sec_info_LLAenen20130622.txt', 'w', encoding="utf8") as the_file:
        for key in sorted_sec_to_cnt:
            #str = "%s, %s, %s\n" % (key, sorted_sec_to_cnt[key], sec_to_keyword[key])
            str = "%s\n" % (key)
            the_file.write(str)

    print("Summary:")
    print("Done with the job, totally takes %s s" % (time.time() - start_time))
    
if __name__ == '__main__':
    do_the_job()
