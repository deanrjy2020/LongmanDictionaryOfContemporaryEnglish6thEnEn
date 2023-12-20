#!/usr/bin/env python2
import sys
import os
import re
import shutil

def do_the_job():
    print("Parsing...")
    filename = '../LongmanDictionaryOfContemporaryEnglish6thEnEn.txt'
    #filename = '../LDOCE6/LDOCE6.txt'

    #out = 'out'
    #os.makedirs(out, exist_ok=True)

    pattern_nofile = re.compile(r'no-sound')
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
                test_name = line.strip()
                
                #print(test_name)
            elif state == STATE_TEST_STARTED:
                m = pattern_nofile.findall(line)
                for i in m:
                    print(test_name)

    print("Done with the job.")


if __name__ == '__main__':
    do_the_job()
