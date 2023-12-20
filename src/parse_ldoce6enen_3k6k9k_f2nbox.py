#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil

def do_the_job():
    print("Parsing...")
    filename = '../LongmanDictionaryOfContemporaryEnglish6thEnEn.txt'

    pattern_freq_h = re.compile(r'<span class="level tooltip"> ●●●</span>')
    pattern_freq_m = re.compile(r'<span class="level tooltip"> ●●○</span>')
    pattern_freq_l = re.compile(r'<span class="level tooltip"> ●○○</span>')
    pattern_f2nbox = re.compile(r'class="f2nbox"')
    pattern_test_end = re.compile(r'</>')

    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'
    results_3k = ''
    results_6k = ''
    results_9k = ''
    results_9k_out = ''

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
                m = pattern_f2nbox.findall(line)
                if not m: continue
                
                #m = pattern_freq.search(line)
                # use the findall to see if the number (with dup) is correct.
                m_h = pattern_freq_h.findall(line)
                #print(type(m))
                for i in m_h:
                    results_3k = results_3k + test_name
                m_m = pattern_freq_m.findall(line)
                for i in m_m:
                    results_6k = results_6k + test_name
                m_l = pattern_freq_l.findall(line)
                for i in m_l:
                    results_9k = results_9k + test_name

                if m_h: continue
                if m_m: continue
                if m_l: continue

                # the collo box is not in the 9k
                results_9k_out = results_9k_out + "/" + test_name.strip()
                #print(test_name)
                

    with open('3k_with_f2nbox_EnEn.txt', 'w') as the_file:
        the_file.write(results_3k)
    with open('6k_with_f2nbox_EnEn.txt', 'w') as the_file:
        the_file.write(results_6k)
    with open('9k_with_f2nbox_EnEn.txt', 'w') as the_file:
        the_file.write(results_9k)
    with open('9k_out_with_f2nbox_EnEn.txt', 'w') as the_file:
        the_file.write(results_9k_out)
    print("Done with the job.")


if __name__ == '__main__':
    do_the_job()
