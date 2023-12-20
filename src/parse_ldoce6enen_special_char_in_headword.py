#!/usr/bin/env python3
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
    filename = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt'
    #filename = 'data/A1.html'

    output_file = 'special_char_in_headword.txt'
    # delete the dst
    if os.path.exists(output_file):
        os.remove(output_file)

    pattern_test_end = re.compile(r'</>')
    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'

    # the following chars are considered as normal char.
    # hypen/minus -
    # single qoute '
    # space
    # , . ! ? ( ) / : $ * & + 0-9 a-z A-Z
    pattern_special_char = re.compile(r'[^-,!?()/:$*&+\'\.0-9a-zA-Z\s]') # 230 results

    headword_to_cnt = { }

    with open(filename, encoding="utf8") as ifile:
        for line in ifile:
            # ======================================= read only to get the test_name =======================================
            if state == STATE_TEST_ENDED:
                state = STATE_TEST_STARTED
                test_name = line.strip()
                
                headword_to_cnt[test_name] = headword_to_cnt.setdefault(test_name, 0) + 1

                if pattern_special_char.search(test_name):
                    """
                    if running this py program in git bash, it can't print some special char
                    save to file is okay.
                    """
                    #print(test_name)
                    with open(output_file, 'a', encoding="utf8") as the_file:
                        the_file.write(line) # test_name with the '\n'

            if pattern_test_end.search(line):
                # no natter what the state is, end everything if we see the test end pattern.
                state = STATE_TEST_ENDED
                test_name = 'init_invalid_name'

    print("Summary:")

    output = 'dup_headword.txt'
    with open(output, 'w', encoding="utf8") as the_file:
        the_file.write("started:")
        for key in headword_to_cnt:
            if (headword_to_cnt[key] != 1):
                content = "%s, %s\n" % (key, headword_to_cnt[key])
                the_file.write(content)

    print("Done with the job, totally takes %s s" % (time.time() - start_time))
    

if __name__ == '__main__':
    do_the_job()
