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
    pattern_section = re.compile(r'<span class="ACTIVATOR"><span class="Section">')
    pattern_test_end = re.compile(r'</>')

    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'
    section_num = 0
    one_sec_key = 0

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

                m = pattern_section.search(line)
                if not m: print("error, this keyword has no section!!!!")

                m = pattern_section.findall(line)
                section_num = section_num + len(m)

                if len(m) == 1:
                    print(test_name.strip())
                
    print("section_num=" + str(section_num))
    print("Done with the job.")


if __name__ == '__main__':
    do_the_job()
