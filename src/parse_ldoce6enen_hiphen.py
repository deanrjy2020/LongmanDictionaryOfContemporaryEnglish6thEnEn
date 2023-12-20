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

    pattern1                = re.compile(r'—')
    match1 = 0
    pattern2               = re.compile(r'<span>—')
    match2 = 0
    diff = 0
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
                continue

            if state == STATE_TEST_ENDED:
                state = STATE_TEST_STARTED
                test_name = line

            elif state == STATE_TEST_STARTED:
                #print(line)
                # replace1=line and n=0, if not found.
                m1=pattern1.findall(line)
                #print(len(m1))
                for i in m1:
                    match1 = match1 + 1

                m2=pattern2.findall(line)
                for i in m2:
                    match2 = match2 + 1

                if len(m1) != len(m2):
                    diff = diff + 1
                    print(test_name)
                    
                #with open('../LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt', 'a') as the_file:
                #    the_file.write(test_name + replace2)


    print(match1)
    print(match2)
    print(diff)
    print("Done with the job, totally takes %s s" % (time.time() - start_time))
    """
    has_part_of_speech replaced 17699 times
     no_part_of_speech replaced 314 times

    The same if I search the 2 re ex in the VSC.
  
    in vsc, searching '<a href="entry://#6504937708254a64972bf4d4ccdfcc9d_LDOCE6_' hits 18255, why?? 18255-17699-314 = 242 ???
    """

if __name__ == '__main__':
    do_the_job()
