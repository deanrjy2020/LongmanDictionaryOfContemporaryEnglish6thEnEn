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
    filename = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn.txt'

    pattern_freq_h = re.compile(r'<span class="level tooltip"> ●●●</span>')
    pattern_freq_m = re.compile(r'<span class="level tooltip"> ●●○</span>')
    pattern_freq_l = re.compile(r'<span class="level tooltip"> ●○○</span>')
    pattern_test_end = re.compile(r'</>')

    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'
    results_3k = ''
    file_3k = '3k.txt'
    results_6k = ''
    file_6k = '6k.txt'
    results_9k = ''
    file_9k = '9k.txt'
    results_9k_out = ''
    file_9k_out = '9k_out.txt'

    file_3k_entry = '3k_entry.txt'
    file_6k_entry = '6k_entry.txt'
    file_9k_entry = '9k_entry.txt'
    file_9k_out_entry = '9k_out_entry.txt'

    # delete the dst
    if os.path.exists(file_3k_entry):
        os.remove(file_3k_entry)
    if os.path.exists(file_6k_entry):
        os.remove(file_6k_entry)
    if os.path.exists(file_9k_entry):
        os.remove(file_9k_entry)
    if os.path.exists(file_9k_out_entry):
        os.remove(file_9k_out_entry)


    with open(filename, encoding="utf8") as ifile:
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
                # search to see if it is 3k
                m = pattern_freq_h.search(line)
                #m_h = pattern_freq_h.findall(line)
                #print(type(m))
                if m:
                    results_3k = results_3k + test_name
                    with open(file_3k_entry, 'a', encoding="utf8") as the_file:
                        the_file.write(test_name + line + '</>\n')
                    continue
                # not 3k, search to see if it is 6k
                m = pattern_freq_m.search(line)
                if m:
                    with open(file_6k_entry, 'a', encoding="utf8") as the_file:
                        the_file.write(test_name + line + '</>\n')
                    results_6k = results_6k + test_name
                    continue
                # not 6k, search to see if it is 9k
                m = pattern_freq_l.search(line)
                if m:
                    with open(file_9k_entry, 'a', encoding="utf8") as the_file:
                        the_file.write(test_name + line + '</>\n')
                    results_9k = results_9k + test_name
                    continue

                # not 9k, the result.
                results_9k_out = results_9k_out + test_name
                with open(file_9k_out_entry, 'a', encoding="utf8") as the_file:
                    the_file.write(test_name + line + '</>\n')


    with open(file_3k, 'w', encoding="utf8") as the_file:
        the_file.write(results_3k)
    with open(file_6k, 'w', encoding="utf8") as the_file:
        the_file.write(results_6k)
    with open(file_9k, 'w', encoding="utf8") as the_file:
        the_file.write(results_9k)
    with open(file_9k_out, 'w', encoding="utf8") as the_file:
        the_file.write(results_9k_out)

    print("Done with the job, totally takes %s s" % (time.time() - start_time))

if __name__ == '__main__':
    do_the_job()
