#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
#import shutil
# for md5
import hashlib
import time

def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # src
    filename = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn.txt'
    #filename = '../A_capital.html'
    #filename = '../test.txt'

    # verify the md5 of the input file.
    md5 = hashlib.md5(open(filename,'rb').read()).hexdigest()
    assert md5 == '59381ae02ff570208b9e9dd1ceda31a2'

    # delete the dst
    output = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt'
    if os.path.exists(output):
        os.remove(output)

    pattern_test_end = re.compile(r'</>')
    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name' # =word head

    pattern_above = re.compile(r'a number or amount that is approximately right')
    pattern_above_n = 0

    pattern_across = re.compile(r'someone who officially tries to prove that someone is guilty')
    pattern_across_n = 0

    pattern_ambitious = re.compile(r'remaining or continuing forever')
    pattern_ambitious_n = 0

    pattern_another = re.compile(r'to try to make someone less angry')
    pattern_another_n = 0

    pattern_appear = re.compile(r'any one of the people in a group or in the world')
    pattern_appear_n = 0

    pattern_because = re.compile(r'dressed, arranged, decorated etc in a beautiful way')
    pattern_because_n = 0

    pattern_between = re.compile(r'to do something better than before')
    pattern_between_n = 0

    pattern_both = re.compile(r'money that is borrowed')
    pattern_both_n = 0

    pattern_but = re.compile(r'<span class="secheading">busy</span><span class="exponent">')
    pattern_but_n = 0

    pattern_cancel = re.compile(r'when you are not allowed or do not have the power to do something')
    pattern_cancel_n = 0

    pattern_check = re.compile(r'someone who cheats')
    pattern_check_n = 0

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
            # ======================================= do the modifications =================================================
            ## LLA above keyword heading fix. 'a number or amount that is approximately right' -> 'in a higher position than something' 6 times (above above over overhang overhead upstairs).
            if any(test_name == c for c in ["above", "over", "overhang", "overhead", "upstairs"]):
                line1,n = pattern_above.subn(r'in a higher position than something', line)
                pattern_above_n += n
            else:
                line1 = line
            # txt = fa85cfbebd2f2d4f773e96895b86e474

            ## LLA across keyword heading fix. 'someone who officially tries to prove that someone is guilty' -> 'across' 7 times (across over through trans- cut cross crossing).
            if any(test_name == c for c in ["across", "over", "through", "trans-", "cut", "cross", "crossing"]):
                line2,n = pattern_across.subn(r'across', line1)
                pattern_across_n += n
            else:
                line2 = line1
            # txt = 322fb1c0afc0960e48e0006d4a4e840d

            ## LLA ambitious keyword heading fix. 'remaining or continuing forever' -> 'determined to be successful in your life or job' 8 times (ambitious ambitiously ambitiousness ambition go-getter go-getting competitive competitively).
            if any(test_name == c for c in ["ambitious", "ambitiously", "ambitiousness", "ambition", "go-getter", "go-getting", "competitive", "competitively"]):
                line3,n = pattern_ambitious.subn(r'determined to be successful in your life or job', line2)
                pattern_ambitious_n += n
            else:
                line3 = line2
            # txt = bdb4f05d63e72a3c69a26e43f0893f76

            ## LLA another keyword heading fix. 'to try to make someone less angry' -> 'one more of the same kind' 6 times (another one more extra spare additional).
            if any(test_name == c for c in ["another", "one", "more", "extra", "spare", "additional"]):
                line4,n = pattern_another.subn(r'one more of the same kind', line3)
                pattern_another_n += n
            else:
                line4 = line3
            # txt = 1534d26300d4df2c076ae1e052d4ff53

            ## LLA appear keyword heading fix. 'any one of the people in a group or in the world' -> 'to start to be seen' 7 times (appear visible view emerge loom reappear reappearance).
            if any(test_name == c for c in ["appear", "visible", "view", "emerge", "loom", "reappear", "reappearance"]):
                line5,n = pattern_appear.subn(r'to start to be seen', line4)
                pattern_appear_n += n
            else:
                line5 = line4
            # txt = cd1cfb3e43d6b3d5044db339fe84cb82

            ## LLA because keyword heading fix. 'dressed, arranged, decorated etc in a beautiful way' -> 'what you say when you are giving the reason for something' 9 times (because 'due to' 'owing to' thanks result reason out account seeing).
            if any(test_name == c for c in ["because", "due to", "owing to", "thanks", "result", "reason", "out", "account", "seeing"]):
                line6,n = pattern_because.subn(r'what you say when you are giving the reason for something', line5)
                pattern_because_n += n
            else:
                line6 = line5
            # txt = 4ddd8f32e3146e6fb321e32d001c519c

            ## LLA between keyword heading fix. 'to do something better than before' -> 'between two or more people or things' (between among middle sandwich).
            if any(test_name == c for c in ["between", "among", "middle", "sandwich"]):
                line7,n = pattern_between.subn(r'between two or more people or things', line6)
                pattern_between_n += n
            else:
                line7 = line6
            # txt = 1803f119b5b2d9aed1b55c0ac657f77c

            ## LLA both keyword heading fix. 'money that is borrowed' -> 'what you say to talk about two people or things' 10 times (both two pair each 'one another' either neither neither mutual share).
            if any(test_name == c for c in ["both", "two", "pair", "each", "one another", "either", "neither", "mutual", "share"]):
                line8,n = pattern_both.subn(r'what you say to talk about two people or things', line7)
                pattern_both_n += n
            else:
                line8 = line7
            # txt = 39a26d9d451469f1e1fc3079ed9da472

            ## LLA but keyword heading fix. 'busy' -> 'but' 17 times (but, but, however, nevertheless, nonetheless, hand, still, all, same, yet, whereas, while, though, though, even, only, except).
            if any(test_name == c for c in ["but", "however", "nevertheless", "nonetheless", "hand", "still", "all", "same", "yet", "whereas", "while", "though", "even", "only", "except"]):
                line9,n = pattern_but.subn(r'<span class="secheading">but</span><span class="exponent">', line8)
                pattern_but_n += n
            else:
                line9 = line8
            # txt = ba8282ebd61b1d40c270f178f0dd39ef

            ## LLA cancel keyword heading fix. 'when you are not allowed or do not have the power to do something' -> 'to decide that a planned event will not now happen' 4 times (cancel call scrub shelve).
            if any(test_name == c for c in ["cancel", "call", "scrub", "shelve"]):
                line10,n = pattern_cancel.subn(r'to decide that a planned event will not now happen', line9)
                pattern_cancel_n += n
            else:
                line10 = line9
            # txt = c739756db7be497da034fa29f504aae1

            ## LLA check keyword heading fix. 'someone who cheats' -> 'to make sure that something is true or correct' 12 times (check check sure sureness certain double-check verifiable verification verify confirm ascertain ascertainable)
            if any(test_name == c for c in ["check", "sure", "sureness", "certain", "double-check", "verifiable", "verification", "verify", "confirm", "ascertain", "ascertainable"]):
                line11,n = pattern_check.subn(r'to make sure that something is true or correct', line10)
                pattern_check_n += n
            else:
                line11 = line10
            # txt = 4c877648f9a562d067d834be283e73b1


            with open(output, 'a', encoding="utf8") as the_file:
                the_file.write(line11)


    print("\nSummary:")
    
    # 1
    assert pattern_above_n == 6
    assert pattern_across_n == 7
    assert pattern_ambitious_n == 8
    assert pattern_another_n == 6
    assert pattern_appear_n == 7
    assert pattern_because_n == 9
    assert pattern_between_n == 4
    assert pattern_both_n == 10
    assert pattern_but_n == 17
    assert pattern_cancel_n == 4
    # 11
    assert pattern_check_n == 12

    print("%s md5: %s" % (output, hashlib.md5(open(output,'rb').read()).hexdigest()))

    print("Done with the job, totally takes %s s" % (time.time() - start_time))


def generate_change_log():
    print("\nChange log:")

    pattern_chagne_log = re.compile(r'## ')
    log_id = 1

    # read current file and parse the change log.
    with open('src/write_ldoce6enen_bugfix.py', encoding="utf8") as ifile:
        for line in ifile:
            m = pattern_chagne_log.search(line)
            for itr in re.finditer(pattern_chagne_log, line):
                change_log = line[itr.start():].strip()
                print("%s. %s" % (log_id, change_log))
                log_id += 1


if __name__ == '__main__':
    do_the_job()
    generate_change_log()
