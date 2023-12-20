#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil
import time

"""
检查txt里面没一行的空格只有单个出现, 如果多个出现打印error信息, 同时把行内容输出到两个文本, 用于比较.
PASS
"""

def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # src
    debug = 0
    if debug:
        filename = 'data/burn.html'
    else:
        filename = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt'

    pattern_test_end = re.compile(r'</>')
    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'

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
            rstrip_line = line.rstrip('\n')
            new_line = ' '.join(rstrip_line.split())
            if new_line != rstrip_line:
                line_file = 'line.txt'
                new_line_file = 'new_line.txt'
                print("Error: the %s headword has issue, see the %s and %s" % (test_name, line_file, new_line_file))
                with open(line_file, 'w', encoding="utf8") as the_file:
                    the_file.write(rstrip_line)
                with open(new_line_file, 'w', encoding="utf8") as the_file:
                    the_file.write(new_line)
                break

    print("Summary:")
    print("Done with the job, totally takes %s s" % (time.time() - start_time))
    

if __name__ == '__main__':
    do_the_job()
