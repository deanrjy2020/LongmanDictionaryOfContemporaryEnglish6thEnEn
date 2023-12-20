#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil

def do_the_job():
    print("Parsing...")
    filename = '../LongmanDictionaryOfContemporaryEnglish6thEnEn.txt'
    #filename = 'test.txt'

    pattern_collobox = re.compile(r'class="collobox"')
    pattern_regbox = re.compile(r'class="f2nbox"')
    pattern_grambox = re.compile(r'class="grambox"')
    pattern_spokenbox = re.compile(r'class="spokensect"')
    pattern_thesbox = re.compile(r'class="thesbox"')
    pattern_usagebox = re.compile(r'class="usagebox"')

    pattern_test_end = re.compile(r'</>')

    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'
    usage_keys = 'usage_keys: '
    usage_key_num = 0
    spoken_keys = 'spoken_keys: '
    spoken_key_num = 0

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
                mm = pattern_usagebox.findall(line)
                for i in mm:
                    usage_keys = usage_keys + "/" + test_name.strip()
                    usage_key_num = usage_key_num + 1
                mm = pattern_spokenbox.findall(line)
                for i in mm:
                    spoken_keys = spoken_keys + "/" + test_name.strip()
                    spoken_key_num = spoken_key_num + 1

                m = pattern_collobox.search(line)
                if not m: continue

                m = pattern_regbox.search(line)
                if not m: continue

                m = pattern_grambox.search(line)
                if not m: continue

                m = pattern_spokenbox.search(line)
                if not m: continue

                m = pattern_thesbox.search(line)
                if not m: continue
                print(test_name.strip())
                    
    print(usage_keys)
    print(usage_key_num)
    
    print(spoken_keys)
    print(spoken_key_num)

    print("Done with the job.")


if __name__ == '__main__':
    do_the_job()
