#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil
import time

#from bs4 import BeautifulSoup

def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # src
    # all the inputs below are for testing this script except the last one.
    #filename = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn.txt'
    #filename = 'data/A1.html'
    #filename = 'data/accurate.html'
    #filename = 'data/actress.html'
    #filename = 'data/piggyback.html'
    # real input for running to get the results.
    filename = 'data/LDOCE6_New_0103.txt'
    #filename = 'data/view_new.html'
    #filename = 'data/view.html'

    # delete the dst
    output = 'output.txt'
    if os.path.exists(output):
        os.remove(output)

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

    # the content in the left and right is e.g. '<span' and '</span>'
    # list label start
    pattern_left_1 = [] # use '<span ' to search
    pattern_left_2 = [] # use '<span>' to search
    # list label end
    pattern_right_1 = [] # use '</span ' to search
    pattern_right_2 = [] # use '</span>' to search

    for label in labels:
        """
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
        """
        start_str = '<' + label
        end_str = '</' + label

        #print(start_str)
        #print(end_str)
        start_str_1 = start_str + ' '
        pattern_left_1.append(re.compile(r'%s'%start_str_1))
        start_str_2 = start_str + '>'
        pattern_left_2.append(re.compile(r'%s'%start_str_2))
        end_str_1 = end_str + ' '
        pattern_right_1.append(re.compile(r'%s'%end_str_1))
        end_str_2 = end_str + '>'
        pattern_right_2.append(re.compile(r'%s'%end_str_2))

    #print(len(pattern_right))
    assert len(pattern_left_1) == len(pattern_left_2)
    assert len(pattern_left_1) == len(pattern_right_1)
    assert len(pattern_right_1) == len(pattern_right_2)
    assert len(labels) == len(pattern_right_1)

    # manually add one more.
    #pattern_left_1.append(re.compile(r'<'))
    #pattern_right.append(re.compile(r'>'))

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
            for i in range(len(pattern_right_1)):
                # e.g. ('<span ' + '<span>') and '</span>', they need to have the same size.
                m_s_1 = pattern_left_1[i].findall(line)
                m_s_2 = pattern_left_2[i].findall(line)
                m_e_1 = pattern_right_1[i].findall(line)
                m_e_2 = pattern_right_2[i].findall(line)
                #if (len(m_s_1) + len(m_s_2)) != len(m_e):
                if (len(m_s_1) + len(m_s_2)) > (len(m_e_1) + len(m_e_2)):
                    print(test_name)
                    output_msg = "error: label (left1 %s (num=%s), left2 %s (num=%s)) and (right1 %s (num=%s), right2 %s (num=%s)) not match" % (pattern_left_1[i], len(m_s_1), pattern_left_2[i], len(m_s_2), pattern_right_1[i], len(m_e_1), pattern_right_2[i], len(m_e_2))
                    print(output_msg)
                    #with open(output, 'a', encoding="utf8") as the_file:
                    #    the_file.write(test_name)
                    #    the_file.write(test_name)

            #with open('data/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt', 'a', encoding="utf8") as the_file:
            #    the_file.write(line)



    print("Summary:")
    print("Done with the job, totally takes %s s" % (time.time() - start_time))
    

if __name__ == '__main__':
    do_the_job()
