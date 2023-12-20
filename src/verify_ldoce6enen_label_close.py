#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil
import time

"""
Results:

faq-about 33de5e2430c248afb78dd34e20f35466
error: label re.compile('<li>') (num=0) and re.compile('</li>') (num=10) not match
faq-about 33de5e2430c248afb78dd34e20f35466
error: label re.compile('<b>') (num=1) and re.compile('</b>') (num=53) not match
faq-about 33de5e2430c248afb78dd34e20f35466
error: label re.compile('<th') (num=6) and re.compile('</th>') (num=4) not match

"""

def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # src
    filename = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt'

    pattern_test_end = re.compile(r'</>')
    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'

    labels = { } # label to label map, = set.
    pattern_label = re.compile(r'</([^<]*)>')

    # go thru the file and find all the labels: </XXX>
    with open(filename, encoding="utf8") as ifile:
        for line in ifile:
            for m in re.finditer(pattern_label, line):
                label_end = line.find('>', m.start())
                label = line[m.start()+2:label_end]
                #print(label)
                if label != '':
                    labels[label] = label

    print("done with the pass 1: ")
    print(labels)

    # list label start
    pattern_left = []
    # list label end
    pattern_right = []

    for label in labels:
        if label == 'i' or label == 'li' or label == 'b':
            # don't use '<i' and '</i>' to search, as the '<img' will interfere with it.
            # use '<i>' and </i> to search
            #
            # for '<li', '<link' will interfere with it.
            # for '<b', '<br' will interfere with it.
            start_str = '<' + label + '>'
            end_str = '</' + label + '>'
        else:
            start_str = '<' + label
            end_str = '</' + label + '>'
        #print(start_str)
        #print(end_str)
        pattern_left.append(re.compile(r'%s'%start_str))
        pattern_right.append(re.compile(r'%s'%end_str))

    #print(len(pattern_right))
    assert len(pattern_left) == len(pattern_right)
    assert len(labels) == len(pattern_right)

    # manually add one more.
    pattern_left.append(re.compile(r'<'))
    pattern_right.append(re.compile(r'>'))

    # go thru the file again to see if the left and right matches.
    with open(filename, encoding="utf8") as ifile:
        for line in ifile:
            # ======================================= read only to get the test_name =======================================
            if state == STATE_TEST_ENDED:
                state = STATE_TEST_STARTED
                test_name = line.strip()
            m = pattern_test_end.search(line)
            if m:
                # no natter what the state is, end everything if we see the test end pattern.
                state = STATE_TEST_ENDED
                test_name = 'init_invalid_name'
            # ======================================= do the modifications =======================================
            # for each line, need to check for all the labels.
            for i in range(len(pattern_right)):
                # e.g. '<span' and '</span>' , they need to have the same size.
                m_s = pattern_left[i].findall(line)
                m_e = pattern_right[i].findall(line)
                #print("s_num=%s, e_num=%s, label: %s, %s" % (len(m_s), len(m_e), pattern_left[i], pattern_right[i]))
                if len(m_s) != len(m_e):
                    print(test_name)
                    print("error: label %s (num=%s) and %s (num=%s) not match" % (pattern_left[i], len(m_s), pattern_right[i], len(m_e)))

            #with open('data/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt', 'a', encoding="utf8") as the_file:
            #    the_file.write(line)



    print("Summary:")
    print("Done with the job, totally takes %s s" % (time.time() - start_time))
    

if __name__ == '__main__':
    do_the_job()
