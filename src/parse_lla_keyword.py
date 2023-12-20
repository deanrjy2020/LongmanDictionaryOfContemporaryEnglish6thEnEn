#!/usr/bin/env python2
import sys
import os
import re
import shutil

def do_the_job():
    print("Parsing...")
    filename = 'LLA.txt'
    #filename = 'test.txt'

    pattern_keyword = re.compile(r'href="LLA.CSS"')
    pattern_test_end = re.compile(r'</>')

    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'
    all_keys = ''

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
                
                
                #print(test_name)
            elif state == STATE_TEST_STARTED:
                m = pattern_keyword.search(line)
                if not m: continue
                
                all_keys = all_keys + test_name

    with open('lla_866_keywords.txt', 'w') as the_file:
        the_file.write(all_keys)

    print("Done with the job.")


if __name__ == '__main__':
    do_the_job()
