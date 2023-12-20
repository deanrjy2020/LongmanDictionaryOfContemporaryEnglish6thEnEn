#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil
import time

'''
单单用regex去得到LDOCE6里LLA的信息.

run: python src/generate_ldoce6enen_lla.py
Parsing...
Summary:
total section number = 32630
identical section number = 4953
by average, each section has been seen 6.59 times in the mdx.

total phrase num in identical sections = 22068
by average, each section has phrase num = 22068 / 4953 = 4.46
Done with the job, totally takes 269.99 s
'''

def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # src
    debug = 0
    if debug:
        filename = 'data/burn.html'
        #filename = 'data/diary.html'
        #filename = 'data/dinner.html'
        #filename = 'data/newborn.html'
        #filename = 'data/novel.html'
    else:
        filename = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt'

    pattern_test_end = re.compile(r'</>')
    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'

    pattern_thes = re.compile(r'<span class="popheader popthes">THESAURUS')
    pattern_lla = re.compile(r'Longman Language Activator')
    pattern_thesbox = re.compile(r'class="thesbox"')
    pattern_grambox = re.compile(r'class="grambox"')

    '''
    这个pattern会找到3种headings: 
        LLA headings, 要找的目标, 例子, bar里面有LLA, 里面有两个section
        tab thes headings, 在tab 'THESAURUS' 点开, 在LLA前还会有普通的THESAURUS, 例子, bar单词LLA前面有普通section
            普通的section可能没有标题heading.
        thesbox headings, 
    '''
    pattern_all_headings = re.compile(r'<span class="secheading">([^<]*)</span><span class="exponent">')
    # this will find the LLA phrase, tab thes phrase, and the thesbox phrase, need to refine.
    pattern_phrase = re.compile(r'<span class="exp display">([^<]*)</span>')
    pattern_example = re.compile(r'<span class="example"><span class="neutral">([^<]*)</span>([^<]*)</span>')

    sec_to_keyword = { } # Where (wordhead) is this section.
    sec_to_cnt = { } # how many times this section is seen in the entire ldoce6.
    total_sec_cnt = 0 # adding all the cnt in the sec_to_cnt.
    sec_to_phrase_num = { } # how many phrases in this section.

    with open(filename, encoding="utf8") as ifile:
        for line in ifile:
            # ======================================= read only to get the test_name =======================================
            if state == STATE_TEST_ENDED:
                state = STATE_TEST_STARTED
                test_name = line.strip()
            if pattern_test_end.search(line):
                # no natter what the state is, end everything if we see the test end pattern.
                state = STATE_TEST_ENDED
                test_name = 'init_invalid_name'
            # ======================================= do the modifications =======================================
            # if the content doesn't have 'Longman Language Activator' string, skip
            if not pattern_lla.search(line):
                continue

            # for all the headings, 3 types
            for heading_itr in re.finditer(pattern_all_headings, line):
                # for each heading, before puting into the dict, we need to check something.
                heading_str = heading_itr.groups()[0].strip().lower()
                
                # 1, don't need empty heading
                if not heading_str:
                    continue

                # find the closest thes string before this heading
                closest_thes_start = 0 # could be 0 if there is no thes (only has lla)
                for thes in re.finditer(pattern_thes, line):
                    if thes.start() < heading_itr.start():
                        closest_thes_start = thes.start()

                # find the closest lla string before this heading
                closest_lla_start = 0 # could be 0 if the heading is in thesaurus tab before lla
                for lla in re.finditer(pattern_lla, line):
                    if lla.start() < heading_itr.start():
                        closest_lla_start = lla.start()
                
                # find the closest box string before this heading
                closest_thesbox_start = 0 # could be 0 if there is no box
                for box in re.finditer(pattern_thesbox, line):
                    if box.start() < heading_itr.start():
                        closest_thesbox_start = box.start()

                # if (box < lla < heading) and (thes < lla < heading), this is a valid LLA heading,
                # otherwise, it is a heading of thesaurus tab or a heading of thesaurus box.
                if closest_thesbox_start > closest_lla_start or closest_thes_start > closest_lla_start:
                    continue

                # start to build section for current heading/section
                valid_lla_heading_str = heading_str
                valid_lla_heading_itr = heading_itr
                section = valid_lla_heading_str + '@'
                if debug: print('\nvalid_lla_heading_str=%s, valid_lla_heading_itr=%s, groups=%s' % \
                                (valid_lla_heading_str, valid_lla_heading_itr, valid_lla_heading_itr.groups()))

                # for both the thes phrase and LLA phrase
                phrase_cnt = 0
                for phrase_itr in re.finditer(pattern_phrase, line):
                    # the phrase must be after the valid lla heading
                    if phrase_itr.start() < valid_lla_heading_itr.start():
                        continue

                    phrase_str = phrase_itr.groups()[0].strip()
                    if debug: print('\tphrase_str=%s' % phrase_str)
                    
                    # find the closest heading (3 types: thes, lla, thesbox) before this phrase
                    phrase_closest_3_types_heading_itr = iter([]) # must exists.
                    for three_types_heading_itr in re.finditer(pattern_all_headings, line):
                        if three_types_heading_itr.start() < phrase_itr.start():
                            phrase_closest_3_types_heading_itr = three_types_heading_itr
                        else:
                            break
                    if debug: print('\tphrase_closest_3_types_heading_itr=%s' % phrase_closest_3_types_heading_itr)
                    if phrase_closest_3_types_heading_itr.start() != valid_lla_heading_itr.start():
                        # done with the cur section.
                        break
                    
                    # corner case 1, this phrase could be in the thes without heading, after the valid lla heading. See the novel entry.
                    # find the closest thes string before this phrase
                    phrase_closest_thes_start = 0 # could be 0 if there is no thes (only has lla)
                    for thes in re.finditer(pattern_thes, line):
                        if thes.start() < phrase_itr.start():
                            phrase_closest_thes_start = thes.start()
                        else:
                            break
                    if valid_lla_heading_itr.start() < phrase_closest_thes_start:
                        break

                    # corner case 2, this phrase could be in the thesbox without heading, after the valid lla heading. See the diary entry.
                    # find the closest thesbox string before this phrase
                    phrase_closest_thesbox_start = 0 # could be 0 if there is no thesbox
                    for thesbox in re.finditer(pattern_thesbox, line):
                        if thesbox.start() < phrase_itr.start():
                            phrase_closest_thesbox_start = thesbox.start()
                        else:
                            break
                    if valid_lla_heading_itr.start() < phrase_closest_thesbox_start:
                        break
                    
                    # corner case 3, this phrase could be in the grammarbox, after the valid lla heading. See the dinner entry.
                    # find the closest grammar string before this phrase
                    phrase_closest_grambox_start = 0 # could be 0 if there is no grambox
                    for grambox in re.finditer(pattern_grambox, line):
                        if grambox.start() < phrase_itr.start():
                            phrase_closest_grambox_start = grambox.start()
                        else:
                            break
                    if valid_lla_heading_itr.start() < phrase_closest_grambox_start:
                        break

                    # Now it is a good phrase, add it to the section
                    section += phrase_str + '|'
                    phrase_cnt += 1
                    if debug: print('\tsection=%s' % section)

                # add the first example in this section (after heading)
                # only the 'types of film' heading, which is the second section of 'film' keyword,
                # has no example, use the empty instead.
                first_example_str = ''
                if valid_lla_heading_str != 'types of film':
                    for example_itr in re.finditer(pattern_example, line):
                        if valid_lla_heading_itr.start() < example_itr.start():
                            first_example_str = example_itr.groups()[1]
                            break
                section += '#' + first_example_str.replace("’", "'") \
                                                  .replace('"', "'") \
                                                  .replace("''", "'") \
                                                  .strip()


                # done with the section build, put it to map
                sec_to_cnt[section] = sec_to_cnt.setdefault(section, 0) + 1
                sec_to_keyword[section] = sec_to_keyword.setdefault(section, '') + test_name + ', '
                sec_to_phrase_num[section] = phrase_cnt


    print("Summary:")
    assert len(sec_to_cnt) == len(sec_to_keyword)
    assert len(sec_to_cnt) == len(sec_to_phrase_num)

    if debug == 1:
        sorted_sec_to_cnt = dict((sec_to_cnt.items()))
    else:
        sorted_sec_to_cnt = dict(sorted(sec_to_cnt.items()))

    output = 'section_details.txt'
    with open(output, 'w', encoding="utf8") as the_file:
        for key in sorted_sec_to_cnt:
            total_sec_cnt += sorted_sec_to_cnt[key]
            #content = "%s, has %s phrase, has seen %s times in (%s) headwords.\n" % (key, sec_to_phrase_num[key], sec_to_cnt[key], sec_to_keyword[key])
            content = "%s\n" % (key)
            the_file.write(content)

    total_phrase_num_in_identical_sections = 0
    for key in sec_to_phrase_num:
        total_phrase_num_in_identical_sections += sec_to_phrase_num[key]

    print("total section number = %s" % total_sec_cnt)
    print("identical section number = %s" % len(sec_to_cnt))
    print("by average, each section has been seen %.2f times in the mdx.\n" % (float(total_sec_cnt)/len(sec_to_cnt)))

    print("total phrase num in identical sections = %s" % total_phrase_num_in_identical_sections)
    print("by average, each section has phrase num = %s / %s = %.2f" % \
          (total_phrase_num_in_identical_sections, len(sec_to_cnt), float(total_phrase_num_in_identical_sections)/len(sec_to_cnt)))

    print("Done with the job, totally takes %.2f s" % (time.time() - start_time))

if __name__ == '__main__':
    do_the_job()
