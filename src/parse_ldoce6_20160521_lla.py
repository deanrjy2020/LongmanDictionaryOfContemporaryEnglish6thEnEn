#!/usr/bin/env python2
import sys
import os
import re
import shutil

def do_the_job():
    print("Parsing...")
    filename = 'LDOCE6_2.txt'
    #filename = 'test.txt'

    pattern_freq_hi = re.compile(r'Core vocabulary: High-frequency')
    pattern_freq_mi = re.compile(r'Core vocabulary: Medium-frequency')
    pattern_freq_lo = re.compile(r'Core vocabulary: Lower-frequency')
    pattern_lla = re.compile(r'type="activator" oid="')
    pattern_test_end = re.compile(r'</>')

    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name'
    all_words = { } # word to word, basically a set
    key2oid = { } # key to oid list
    oid2word = { } # oid to word list
    """
    use python2 to run this, decoding the src error with python3.
    data structure
    dict:
        key - keywords
        value - set
            #bool is_hi
            #bool is_mi
            # is_lo #may have dup
            #bool has_lla
            list lla_ids
    """

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
                all_words[test_name] = test_name
                
                #print(test_name)
            elif state == STATE_TEST_STARTED:
                m = pattern_lla.search(line)
                if not m: continue
                
                #keywords_no_dup = keywords_no_dup + test_name
                #print(type(m))
                #print(m.start())
                """
                # use the findall to see if the number (with dup) is correct.
                m = pattern_lla.findall(line)
                print(type(m))
                for i in m:
                    keywords_dup = keywords_dup + test_name
                """
                # to search the LLA starting string,
                # each word could have more than one pos, each pos could have their own LLA.
                # which means each word could have multiple LLA (=multiple oid)
                lla_oids = []
                for m in re.finditer(pattern_lla, line):
                    #print(m)
                    #keywords_dup = keywords_dup + test_name
                    lla_oid_start = m.end()
                    lla_oid_end = line.find('"', m.end())
                    lla_oid = line[lla_oid_start:lla_oid_end]
                    
                    lla_oids.append(lla_oid)
                    #print(lla_oids)
                    
                    if lla_oid in oid2word:
                        oid2word[lla_oid].append(test_name)
                    else:
                        oid2word[lla_oid] = [test_name]
                    
                key2oid[test_name] = lla_oids
                #print(key2oid)
                #print(oid2word)
                #print("XXXXXXXXXXXX")

    # 52748, the same as shown in Eudic
    with open('all_words.txt', 'w') as the_file:
        for k, v in all_words.items():
            the_file.write(k + "\n")

    # 40748
    with open('words_without_lla.txt', 'w') as the_file:
        for k, v in all_words.items():
            if k not in key2oid:
                the_file.write(k + "\n")

    # 12000, 12000 + 40748 = 52748
    with open('lla_key_no_dup.txt', 'w') as the_file:
        for k, v in key2oid.items():
            the_file.write(k + "\n")

    # 13199, the same value when searching "type="activator" oid="" in the database.
    with open('lla_key_dup.txt', 'w') as the_file:
        for k, v in key2oid.items():
            for i in v:
                the_file.write(k + "\n")

    # 4461, there is dup here, use the excel to remove dup = 3875
    with open('lla_key_with_exclusive_oid.txt', 'w') as the_file:
        for k, v in oid2word.items():
            if len(v) == 1:
                the_file.write(v[0] + "\n")


    print("Done with the job.")


if __name__ == '__main__':
    do_the_job()
