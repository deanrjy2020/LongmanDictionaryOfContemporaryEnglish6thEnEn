#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil
import time

#from bs4 import BeautifulSoup

def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # src
    filename = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn.txt'
    #filename = 'data/A1.html'
    #filename = 'data/accurate.html'
    #filename = 'data/actress.html'
    #filename = 'data/mark.html'
    #filename = 'data/piggyback.html'
    #filename = 'data/singe.html'
    #filename = 'data/tell.html'
    #filename = 'data/view.html'

    # delete the dst
    output = 'output.txt'
    if os.path.exists(output):
        os.remove(output)

    pattern_test_end = re.compile(r'</>')
    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'

    pattern_thes = re.compile(r'<span class="popheader popthes">THESAURUS')
    pattern_lla = re.compile(r'Longman Language Activator')
    pattern_thesbox = re.compile(r'class="thesbox"')

    # this will find the LLA headings, tab thes headings and the thesbox headings, need to refine.
    pattern_all_headings = re.compile(r'<span class="secheading">([^<]*)</span><span class="exponent">')
    # dict, heading to cnt
    heading_to_cnt = { }
    largest_cnt = 0
    total_cnt = 0

    # dict, heading to word
    heading_to_word = { }

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
            # if the content doesn't have 'Longman Language Activator' string, skip
            itr_lla = re.finditer(pattern_lla, line)
            if all(False for _ in itr_lla):
                continue
            
            # find all the heading itrs
            itr_heading = re.finditer(pattern_all_headings, line)
            itr_heading_num = sum(1 for _ in itr_heading)
            
            # find all the headings
            m = pattern_all_headings.findall(line)
            # heading itrs and all_headings should have the same size.
            assert itr_heading_num == len(m)
            #print(itr_heading_num)

            # for each heading
            idx = -1
            # need to do the finditer again? Why we can't use the itr_heading here?
            for itr in re.finditer(pattern_all_headings, line):
                # for each heading, before puting into the dict, we need to check something.
                idx = idx + 1 # current idx, starts from 0
                #print("idx=%s, type m=%s " % (idx, type(m)))
                heading_str = m[idx]
                
                # 1, don't need empty heading
                if not heading_str:
                    continue

                start = itr.start() + 25 # why 25? see the re in pattern_all_headings above
                end = start + len(heading_str)
                heading_str_from_itr = line[start:end]

                assert heading_str == heading_str_from_itr
                #print("heading_str         =%s" % heading_str)

                # find the closest thes string before this heading
                closest_thes_start = 0 # could be 0 if there is no thes (only has lla)
                for thes in re.finditer(pattern_thes, line):
                    if thes.start() < itr.start():
                        closest_thes_start = thes.start()

                # find the closest lla string before this heading
                closest_lla_start = 0 # could be 0 if the heading is in thesaurus tab before lla
                # search again?
                for lla in re.finditer(pattern_lla, line):
                    #print(line[lla.start():lla.start()+26])
                    if lla.start() < itr.start():
                        closest_lla_start = lla.start()
                
                # find the closest box string before this heading
                closest_thesbox_start = 0 # could be 0 if there is no box
                for box in re.finditer(pattern_thesbox, line):
                    #print(line[box.start():box.start()+26])
                    if box.start() < itr.start():
                        closest_thesbox_start = box.start()

                # if (box < lla < heading) and (thes < lla < heading), this is a valid heading,
                # otherwise, it is a heading of thesaurus tab or a heading of thesaurus box.
                if closest_thesbox_start < closest_lla_start and closest_thes_start < closest_lla_start:
                    # dean todo, fix me
                    #key = heading_str.lower().strip()
                    key = heading_str
                    # put into the heading_to_cnt dict
                    heading_to_cnt[key] = heading_to_cnt.setdefault(key, 0) + 1
                    if heading_to_cnt[key] > largest_cnt:
                        largest_cnt = heading_to_cnt[key]
                    
                    # put into the heading_to_word dict
                    heading_to_word[key] = heading_to_word.setdefault(key, '') + test_name + ', '

            #with open('data/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt', 'a', encoding="utf8") as the_file:
            #    the_file.write(line)

    print("Summary:")
    assert len(heading_to_cnt) == len(heading_to_word)
    sorted_heading_to_cnt = dict(sorted(heading_to_cnt.items()))
    #print(heading_to_cnt)
    for key in sorted_heading_to_cnt:
        total_cnt = total_cnt + sorted_heading_to_cnt[key]
        content = "\'%s\', %s, %s\n" % (key, sorted_heading_to_cnt[key], heading_to_word[key])
        #content = "%s\n" % (key)
        with open(output, 'a', encoding="utf8") as the_file:
            the_file.write(content)

    print("total heading_to_cnt: %s" % len(heading_to_cnt))
    print("largest cnt %s" % largest_cnt)
    print("total cnt %s" % total_cnt)

    print("Done with the job, totally takes %s s" % (time.time() - start_time))
    

if __name__ == '__main__':
    do_the_job()
