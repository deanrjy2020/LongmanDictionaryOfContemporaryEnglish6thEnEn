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
    
    # https://forum.freemdict.com/t/topic/24705/34?u=deanrjy2020
    # https://blog.csdn.net/whatday/article/details/107965291
    pattern_has_part_of_speech = re.compile(r'<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_([^<]*)_([^<]*)"> <i>([^<]*)</i></a>')
    list_re=''
    pattern_no_part_of_speech  = re.compile(r'<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_([^<]*)_([^<]*)"> </a>')
    pattern_all                = re.compile(r'<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_')
    list_normal=''

    pattern_deriv              = re.compile(r'<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_([^<]*)_([^<]*)"><span class="deriv">')

    pattern_test_end = re.compile(r'</>')

    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'

    with open(filename) as ifile:
        for line in ifile:
            m = pattern_test_end.search(line)
            if m:
                # no natter what the state is, end everything if we see the test end pattern.
                state = STATE_TEST_ENDED
                test_name = 'init_invalid_name'
                with open('../LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt', 'a') as the_file:
                    the_file.write(line)
                continue

            if state == STATE_TEST_ENDED:
                state = STATE_TEST_STARTED
                test_name = line

            elif state == STATE_TEST_STARTED:
                #print(line)
                # replace1=line and n=0, if not found.
                mm=pattern_has_part_of_speech.findall(line)
                for i in mm:
                    list_re = list_re + test_name

                mm=pattern_no_part_of_speech.findall(line)
                for i in mm:
                    list_re = list_re + test_name

                mm=pattern_all.findall(line)
                for i in mm:
                    list_normal = list_normal + test_name


                
                #with open('../LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt', 'a') as the_file:
                #    the_file.write(test_name + replace2)

    #print("has_part_of_speech replaced %s times" % total_n)
    #print(" no_part_of_speech replaced %s times" % total_m)
    with open('list_re.txt', 'w') as the_file:
        the_file.write(list_re)
    with open('list_normal.txt', 'w') as the_file:
        the_file.write(list_normal)
    print("Done with the job, totally takes %s s" % (time.time() - start_time))
    """
    has_part_of_speech replaced 17699 times
     no_part_of_speech replaced 314 times

    The same if I search the 2 re ex in the VSC.
  
    in vsc, searching '<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_' hits 18255, why?? 18255-17699-314 = 242 ???
    """

if __name__ == '__main__':
    do_the_job()
