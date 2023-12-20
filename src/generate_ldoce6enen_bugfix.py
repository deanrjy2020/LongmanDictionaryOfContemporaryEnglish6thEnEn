#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
# for md5
import hashlib
import time

def do_the_job():
    start_time = time.time()
    print("Parsing...")

    # src
    debug = 0
    if debug:
        filename = 'data/ago.html'
    else:
        filename = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn.txt'

    # verify the md5 of the input file.
    md5 = hashlib.md5(open(filename,'rb').read()).hexdigest()
    if not debug:
        assert md5 == '59381ae02ff570208b9e9dd1ceda31a2'

    # delete the dst
    output = 'data/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt'
    if os.path.exists(output):
        os.remove(output)

    pattern_test_end = re.compile(r'</>')
    STATE_TEST_STARTED = 'STATE_TEST_STARTED'
    STATE_TEST_ENDED = 'STATE_TEST_ENDED'
    state = STATE_TEST_ENDED
    test_name = 'init_invalid_name' # =headword
    line_is_test_name = False

    # 1
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
    # 11
    pattern_check = re.compile(r'someone who cheats')
    pattern_check_n = 0
    pattern_competition = re.compile(r'someone who likes competing')
    pattern_competition_n = 0
    pattern_completely = re.compile(r'<span class="secheading">a complaint</span><span class="exponent">')
    pattern_completely_n = 0
    pattern_dead = re.compile(r'<span class="secheading">darkness</span><span class="exponent">')
    pattern_dead_n = 0
    pattern_depend = re.compile(r'looking or smelling delicious')
    pattern_depend_n = 0
    pattern_doubt = re.compile(r'<span class="secheading">not caring about something</span><span class="exponent">')
    pattern_doubt_n = 0
    pattern_eachother = re.compile(r'happening during the time that something else happens')
    pattern_eachother_n = 0
    pattern_equipment = re.compile(r'not having equal rights')
    pattern_equipment_n = 0
    pattern_especially_ever = re.compile(r'<span class="secheading">unable to escape</span><span class="exponent">')
    pattern_especially_n = 0
    pattern_ever_n = 0
    # 21
    pattern_fairlyquite = re.compile(r'when a situation or decision is fair')
    pattern_fairlyquite_n = 0
    pattern_fedup = re.compile(r'someone who is liked more than other people')
    pattern_fedup_n = 0
    pattern_finally = re.compile(r'<span class="secheading">types of film</span><span class="exponent">')
    pattern_finally_n = 0
    pattern_flow = re.compile(r'with lots of hills or mountains')
    pattern_flow_n = 0
    pattern_inorderto_insist = re.compile(r'when a law court decides that someone is innocent')
    pattern_inorderto_n = 0
    pattern_insist_n = 0
    pattern_instructions = re.compile(r'using instinct rather than knowledge')
    pattern_instructions_n = 0
    pattern_kick = re.compile(r'when you are forced to stay somewhere')
    pattern_kick_n = 0
    pattern_maybe = re.compile(r'material for making clothes, curtains etc')
    pattern_maybe_n = 0
    pattern_never = re.compile(r'to make someone feel nervous')
    pattern_never_n = 0
    # 31
    pattern_nomatter = re.compile(r'to shake your head as a way of saying no')
    pattern_nomatter_n = 0
    pattern_once = re.compile(r'old-fashioned in a pleasant way')
    pattern_once_n = 0
    pattern_partly = re.compile(r'<span class="secheading">to be a part of something</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c\.toggle\(this\)" class="expandable"><span class="arrow">►</span> <span class="exp display">partly')
    pattern_partly_n = 0
    pattern_passgopast = re.compile(r'the people at a party')
    pattern_passgopast_n = 0
    pattern_pattern = re.compile(r'<span class="secheading">on one occasion in the past</span><span class="exponent">')
    pattern_pattern_n = 0
    pattern_pointat = re.compile(r'a person or group of people you play against')
    pattern_pointat_n = 0
    pattern_pour = re.compile(r'to make something possible')
    pattern_pour_n = 0
    pattern_publicservices = re.compile(r'when a lot of people can see you or know about what is happening')
    pattern_publicservices_n = 0
    pattern_realize = re.compile(r'when pictures, films etc do not make things seem real')
    pattern_realize_n = 0
    pattern_rubbishgarbage = re.compile(r'to move over a surface while pressing against it')
    pattern_rubbishgarbage_n = 0
    # 41
    pattern_rumour = re.compile(r'rules of acceptable behaviour')
    pattern_rumour_n = 0
    pattern_since = re.compile(r'not having a lot of decoration or things added')
    pattern_since_n = 0
    pattern_sotherefore = re.compile(r'what you say to tell someone that you are sorry')
    pattern_sotherefore_n = 0
    pattern_special_speed = re.compile(r'not able to speak')
    pattern_special_n = 0
    pattern_speed_n = 0
    pattern_system = re.compile(r'to try to make someone feel sorry for you')
    pattern_system_n = 0
    pattern_thirsty = re.compile((r'what you say when you think something is true, but you are not sure'))
    pattern_thirsty_n = 0
    pattern_tool = re.compile(r'to use the toilet')
    pattern_tool_n = 0
    pattern_until = re.compile(r'when things are spread around in a messy way')
    pattern_until_n = 0
    pattern_working = re.compile(r'to not work hard enough')
    pattern_working_n = 0
    # adding 10 missing sections. (don't insert to the last section)
    section_common_post = '<span class="section' # regular sec or last sec
    # 51
    AFairlyLongTime_content = '''<span class="section"><span class="secheading">a fairly long time</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">a while</span></span><div class="content"><span class="variant"> <span class="varitype">also</span><span class="neutral"> </span><span class="lexvar">some time</span><span class="neutral"> </span></span><span class="neutral"> </span><span class="registerlab">formal</span><span class="def"> a fairly long time</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>He was furious, and it took him a while to calm down.</span><span class="example"><span class="neutral">· </span>It may be some time before the company starts to make a profit.</span><span class="thespropform">for a while/for some time</span><span class="example"><span class="neutral">· </span>We hadn't seen him for a while, and he'd completely changed.</span><span class="example"><span class="neutral">· </span>I've known Paul for some time, and I'm sure he wouldn't have said that.</span><span class="thespropform">after a while/after some time</span><span class="example"><span class="neutral">· </span>After a while, I realized what he meant.</span><span class="example"><span class="neutral">· </span>Not a single vehicle passed, but after some time they heard the roar of planes taking off at the airfield.</span><span class="thespropform">quite a while/quite some time</span><span class="example"><span class="neutral">· </span>When she left school, it was quite a while before she found a job.</span><span class="example"><span class="neutral">· </span>I stayed in the Stage Coach Inn, but it's been quite some time ago.</span><span class="thespropform">a while since/some time since</span><span class="example"><span class="neutral">· </span>It's been a while since we last heard from Jo.</span><span class="example"><span class="neutral">· </span>The team has spent some time since their last defeat on new tactics.</span><span class="thespropform">a while ago/some time ago</span><span class="example"><span class="neutral">· </span>The cafe was taken over a while ago.</span><span class="example"><span class="neutral">· </span>We arranged the meeting some time ago -- were you not informed?</span></div></span></span>'''
    AFairlyLongTime_time_headword_pre = 'For the longest time, I thought Nathan was Asian.</span></div></span></span>'
    pattern_AFairlyLongTime_time_headword = re.compile(r'%s%s' % (AFairlyLongTime_time_headword_pre, section_common_post))
    pattern_AFairlyLongTime_time_headword_n = 0

    AFairlyLongTime_while_headword_pre = 'The site had only flooded once within living memory.</span></div></span></span>'
    pattern_AFairlyLongTime_while_headword = re.compile(r'%s%s' % (AFairlyLongTime_while_headword_pre, section_common_post))
    pattern_AFairlyLongTime_while_headword_n = 0
    # 52
    ToBeGettingNearerToAPersonOrVehicleInFrontOfYou_content = '''<span class="section"><span class="secheading">to be getting nearer to a person or vehicle in front of you</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">be catching up</span></span><div class="content"><span class="example"><span class="neutral">· </span>On the last lap of the race, Gemma started to catch up, and it looked as though she could still win.</span><span class="thespropform">be catching up with</span><span class="example"><span class="neutral">· </span>Looking back I could see that the rest of the group were catching up with us.</span></div></span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">be gaining on/be closing on</span></span><div class="content"><span class="def"> to be steadily getting nearer to a person or vehicle in front of you that you are chasing or racing against, by going faster than them</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>Donna looked in her rear-view mirror and saw with alarm that the Audi was still gaining on her.</span><span class="example"><span class="neutral">· </span>Now 'Australia II' is closing on the American yacht and it could still win this race.</span></div></span></span>'''
    ToBeGettingNearerToAPersonOrVehicleInFrontOfYou_near_headword_pre = 'The rebels hoped that many of the government troops would join them when they drew near to the city.</span></div></span></span>'
    pattern_ToBeGettingNearerToAPersonOrVehicleInFrontOfYou_near_headword = re.compile(r'%s%s' % (ToBeGettingNearerToAPersonOrVehicleInFrontOfYou_near_headword_pre, section_common_post))
    pattern_ToBeGettingNearerToAPersonOrVehicleInFrontOfYou_near_headword_n = 0
    # 53
    ToBeAlmostAParticularAge_content = '''<span class="section"><span class="secheading">to be almost a particular age</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">be getting on for</span></span><div class="content"><span class="neutral"> </span><span class="registerlab">British</span><span class="def"> used to say that someone is nearly a particular age</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>Old Willis must be getting on for sixty-five.</span><span class="example"><span class="neutral">· </span>The Queen was getting on for eighty and only the elderly could remember her coronation.</span></div></span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">be pushing</span></span><div class="content"><span class="thespropform">be pushing 40/50/65 etc</span><span class="def"> to be almost a particular age, especially when this is quite old or be doing a particular activity</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>When you're pushing seventy it's not surprising when you start forgetting things.</span><span class="example"><span class="neutral">· </span>What astonishes me is the ease with which this man, pushing seventy-five, can play his trumpet for hours at a time.</span></div></span></span>'''
    ToBeAlmostAParticularAge_age_headword_pre = 'a forty-something couple from Orlando</span></div></span></span>'
    pattern_ToBeAlmostAParticularAge_age_headword = re.compile(r'%s%s' % (ToBeAlmostAParticularAge_age_headword_pre, section_common_post))
    pattern_ToBeAlmostAParticularAge_age_headword_n = 0
    # 54
    WhenSomethingIsIntendedToDoSomething_content = '''<span class="section"><span class="secheading">when something is intended to do something</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">be intended to do something</span></span><div class="content"><span class="def"> to be done or made for a particular purpose</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>The dress I was given was intended to fit someone much smaller.</span><span class="example"><span class="neutral">· </span>The tests are intended to help teachers improve their teaching.</span></div></span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">be meant to do something/be supposed to do something</span></span><div class="content"><span class="def"> to be intended to have a particular result or effect - use this especially when the result or effect is not achieved</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>The new laws are supposed to prevent tax fraud.</span><span class="example"><span class="neutral">· </span>'There's a Nightmare in My Closet' is a sweet book meant to help children confront their fears.</span></div></span></span>'''
    WhenSomethingIsIntendedToDoSomething_intend_headword_pre = 'He was convicted of possession of cocaine with intent to sell.</span></div></span></span>'
    pattern_WhenSomethingIsIntendedToDoSomething_intend_headword = re.compile(r'%s%s' % (WhenSomethingIsIntendedToDoSomething_intend_headword_pre, section_common_post))
    pattern_WhenSomethingIsIntendedToDoSomething_intend_headword_n = 0
    # 55
    WaysOfBeginningALetter_content = '''<span class="section"><span class="secheading">ways of beginning a letter</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">Dear Sir/Sirs/Sir or Madam</span></span><div class="content"><span class="def"> use this in formal letters when you do not know the person's name</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>Dear Sir or Madam, I am writing to ask for your help ...</span></div></span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">Dear Mr Wiggins/Ms Harper</span></span><div class="content"><span class="def"> use this in formal letters</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>Dear Mr Bartholomew, thank you for your quick response.</span></div></span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">Dear Jim/Sarah etc</span></span><div class="content"><span class="def"> use this when you know the person well enough to use his or her first name</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>Dear Jackie, How are you?</span></div></span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">Hi/Hey</span></span><div class="content"><span class="neutral"> </span><span class="registerlab">especially American</span><span class="def"> use this in e-mails and letters to friends</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>Hi, how's it going?</span><span class="example"><span class="neutral">· </span>Hey Jenny - good to hear from you again.</span></div></span></span>'''
    WaysOfBeginningALetter_letter_headword_pre = 'The e-mail address for the dictionaries department is dict.edit@pearsoned-ema.com.</span></div></span></span>'
    pattern_WaysOfBeginningALetter_letter_headword = re.compile(r'%s%s' % (WaysOfBeginningALetter_letter_headword_pre, section_common_post))
    pattern_WaysOfBeginningALetter_letter_headword_n = 0

    WaysOfBeginningALetter_dear_headword_pre = '''No, you can't have an ice-cream - they're too dear.</span></div></span></span>'''
    pattern_WaysOfBeginningALetter_dear_headword = re.compile(r'%s%s' % (WaysOfBeginningALetter_dear_headword_pre, section_common_post))
    pattern_WaysOfBeginningALetter_dear_headword_n = 0
    
    WaysOfBeginningALetter_sir_headword_pre = 'Longman Language Activator</span>'
    pattern_WaysOfBeginningALetter_sir_headword = re.compile(r'%s%s' % (WaysOfBeginningALetter_sir_headword_pre, section_common_post))
    pattern_WaysOfBeginningALetter_sir_headword_n = 0

    WaysOfBeginningALetter_madam_headword_pre = 'Longman Language Activator</span>'
    pattern_WaysOfBeginningALetter_madam_headword = re.compile(r'%s%s' % (WaysOfBeginningALetter_madam_headword_pre, section_common_post))
    pattern_WaysOfBeginningALetter_madam_headword_n = 0

    WaysOfBeginningALetter_hi_headword_pre = 'Good evening, Ray. Let me introduce David Bruce.</span></div></span></span>'
    pattern_WaysOfBeginningALetter_hi_headword = re.compile(r'%s%s' % (WaysOfBeginningALetter_hi_headword_pre, section_common_post))
    pattern_WaysOfBeginningALetter_hi_headword_n = 0
    # 56
    ToMakePeopleNoticeYou_content = '''<span class="section"><span class="secheading">to make people notice you</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">get attention/attract attention</span></span><div class="content"><span class="def"> to try to make someone notice you, by doing something that they will notice</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>Young children sometimes behave badly simply in order to get attention.</span><span class="thespropform">get/attract somebody's attention</span><span class="example"><span class="neutral">· </span>Phil was trying to attract the waiter's attention.</span></div></span></span>'''
    ToMakePeopleNoticeYou_notice_headword_pre = '''Their house has a pink door. You can't miss it.</span></div></span></span>'''
    pattern_ToMakePeopleNoticeYou_notice_headword = re.compile(r'%s%s' % (ToMakePeopleNoticeYou_notice_headword_pre, section_common_post))
    pattern_ToMakePeopleNoticeYou_notice_headword_n = 0
    # 57
    ToStartTalkingAboutASubject_content = '''<span class="section"><span class="secheading">to start talking about a subject</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">get onto</span></span><div class="content"><span class="thespropform">get onto the subject/topic/question of</span><span class="def"> to start talking about a subject after talking about something else that is connected to it in some way</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>How on earth did we get onto the subject of dogs?</span><span class="example"><span class="neutral">· </span>Whenever Ma got onto that subject, my head would start to spin.</span></div></span></span>'''
    ToStartTalkingAboutASubject_subject_headword_pre = 'We cover the curriculum by choosing things the kids will be interested in.</span></div></span></span>'
    pattern_ToStartTalkingAboutASubject_subject_headword = re.compile(r'%s%s' % (ToStartTalkingAboutASubject_subject_headword_pre, section_common_post))
    pattern_ToStartTalkingAboutASubject_subject_headword_n = 0
    # 58
    ToKeepSayingTheSameThingInAnAnnoyingWay_content = '''<span class="section"><span class="secheading">to keep saying the same thing in an annoying way</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">keep saying/asking/telling etc</span></span><div class="content"><span class="example"><span class="neutral">· </span>She kept saying how rich her father was.</span><span class="example"><span class="neutral">· </span>Don't keep telling me what to do - I know how to bake a cake.</span><span class="example"><span class="neutral">· </span>The kids keep asking what time it is.</span></div></span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">go on about</span></span><div class="content"><span class="def"> to keep talking about something in an annoying way</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>She was going on about what a genius her brother is.</span><span class="thespropform">go on and on about something</span><span class="example"><span class="neutral">· </span>I don't think I can stand another evening of Ted going on and on about his health problems.</span></div></span></span>'''
    ToKeepSayingTheSameThingInAnAnnoyingWay_repeat_headword_pre = 'She paused to recap on the story so far.</span></div></span></span>'
    pattern_ToKeepSayingTheSameThingInAnAnnoyingWay_repeat_headword = re.compile(r'%s%s' % (ToKeepSayingTheSameThingInAnAnnoyingWay_repeat_headword_pre, section_common_post))
    pattern_ToKeepSayingTheSameThingInAnAnnoyingWay_repeat_headword_n = 0
    # 59
    WhatYouCallYourMother_content = '''<span class="section"><span class="secheading">what you call your mother</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">Mum</span></span><div class="content"><span class="neutral"> </span><span class="registerlab">British</span><span class="variant"> <span class="lexvar">/Mom</span><span class="neutral"> </span><span class="registerlab">American</span></span><span class="neutral"> </span><span class="registerlab">spoken</span><span class="def"> a name you use to talk to your mother</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>Mum, where can we play?</span><span class="example"><span class="neutral">· </span>Happy birthday, Mom!</span><span class="example"><span class="neutral">· </span>I told Mum that I wasn't going to be home for dinner tonight.</span></div></span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">Mummy</span></span><div class="content"><span class="neutral"> </span><span class="registerlab">British</span><span class="variant"> <span class="lexvar">/Mommy</span><span class="neutral"> </span><span class="registerlab">American</span></span><span class="neutral"> </span><span class="registerlab">informal</span><span class="def"> a name for your mother - used especially by young children or when you are talking to young children</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>'Good night Mummy,' said Ben.</span><span class="example"><span class="neutral">· </span>Don't cry - Mommy'll be back soon.</span></div></span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">Mother</span></span><div class="content"><span class="def"> a formal way of talking to your mother</span><span class="neutral">: </span><span class="example"><span class="neutral">· </span>I think I can make my own decisions, Mother - I'm forty now you know!</span></div></span></span>'''
    WhatYouCallYourMother_mother_headword_pre = 'her children rather than working elsewhere<span class="neutral">\)</span></span></div></span></span>' # use '\)' instead of ')'
    pattern_WhatYouCallYourMother_mother_headword = re.compile(r'%s%s' % (WhatYouCallYourMother_mother_headword_pre, section_common_post))
    pattern_WhatYouCallYourMother_mother_headword_n = 0
    # 60
    ForPeopleOfOneSex_content = '''<span class="section"><span class="secheading">for people of one sex</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">single-sex</span></span><div class="content"><span class="example"><span class="neutral">· </span>Single-sex schools often achieve better academic results because there is no rivalry between the sexes.</span><span class="example"><span class="neutral">· </span>Churches rarely have single-sex choirs these days.</span></div></span></span>'''
    ForPeopleOfOneSex_sex_headword_pre = 'a unisex toilet</span></div></span></span>'
    pattern_ForPeopleOfOneSex_sex_headword = re.compile(r'%s%s' % (ForPeopleOfOneSex_sex_headword_pre, section_common_post))
    pattern_ForPeopleOfOneSex_sex_headword_n = 0
    # 61
    pattern_no = re.compile(r'no matter what/how much etc')
    pattern_no_n = 0
    # 62
    pattern_notYoung = re.compile(r'The bar was fill with ageing hippies')
    pattern_notYoung_n = 0
    # 63
    pattern_thesaurus_at_approximately = re.compile(r'<span class="refhwd">approximate</span>')
    pattern_thesaurus_at_approximately_n = 0
    # 64
    pattern_ago_headword_body = re.compile(r'They first met at\/in\/fifteen years ago')
    pattern_ago_headword_body_n = 0
    # 65
    pattern_intimidating_headword_body = re.compile(r'ɪˈtɪmədeɪtɪŋ')
    pattern_intimidating_headword_body_n = 0

    with open(filename, encoding="utf8") as ifile:
        for line in ifile:
            # ======================================= read only to get the test_name =======================================
            line_is_test_name = False
            if state == STATE_TEST_ENDED:
                state = STATE_TEST_STARTED
                test_name = line.strip()
                line_is_test_name = True
            if pattern_test_end.search(line):
                # no natter what the state is, end everything if we see the test end pattern.
                state = STATE_TEST_ENDED
                test_name = 'init_invalid_name'
            # ======================================= do the modifications =================================================
            # 'keyword' is the 866 key used in LLA book.
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

            ## LLA check keyword heading fix. 'someone who cheats' -> 'to make sure that something is true or correct' 12 times (check check sure sureness certain double-check verifiable verification verify confirm ascertain ascertainable).
            if any(test_name == c for c in ["check", "sure", "sureness", "certain", "double-check", "verifiable", "verification", "verify", "confirm", "ascertain", "ascertainable"]):
                line11,n = pattern_check.subn(r'to make sure that something is true or correct', line10)
                pattern_check_n += n
            else:
                line11 = line10
            # txt = 4c877648f9a562d067d834be283e73b1

            ## LLA competition keyword heading fix. 'someone who likes competing' -> 'competition' 4 times (competition championship tournament contest).
            if any(test_name == c for c in ["competition", "championship", "tournament", "contest"]):
                line12,n = pattern_competition.subn(r'competition', line11)
                pattern_competition_n += n
            else:
                line12 = line11
            # txt = 8270cb59ecf162b6a4901690a3e1accc

            ## LLA completely keyword heading fix. 'a complaint' -> 'completely and in every way' 17 times (completely, absolutely, fully, totally, entirely, wholly, utterly, positively, complete, completeness, total, absolute, utter, sense, through, whole-hearted, whole-heartedly).
            if any(test_name == c for c in ["completely", "absolutely", "fully", "totally", "entirely", "wholly", "utterly", "positively", "complete", "completeness", "total", "absolute", "utter", "sense", "through", "whole-hearted", "whole-heartedly"]):
                line13,n = pattern_completely.subn(r'<span class="secheading">completely and in every way</span><span class="exponent">', line12)
                pattern_completely_n += n
            else:
                line13 = line12
            # txt = e5abd38a12e034145c0d587bd8cdac67

            ## LLA dead keyword heading fix. 'darkness' -> 'no longer alive' 13 times (dead, dead, deadness, late, lateness, doornail, lifeless, lifelessly, lifelessness, deceased, posthumous, posthumously, pushing).
            if any(test_name == c for c in ["dead", "deadness", "late", "lateness", "doornail", "lifeless", "lifelessly", "lifelessness", "deceased", "posthumous", "posthumously", "pushing"]):
                line14,n = pattern_dead.subn(r'<span class="secheading">no longer alive</span><span class="exponent">', line13)
                pattern_dead_n += n
            else:
                line14 = line13
            # txt = f24024935f9fb97ad30751621cb9a4b1
                
            ## LLA depend/it depends keyword heading fix. 'looking or smelling delicious' -> 'when what happens is influenced by other facts or events' 7 times (depend, according to, determined, dictate, hinge, hinged, decided).
            if any(test_name == c for c in ["depend", "according to", "determined", "dictate", "hinge", "hinged", "decided"]):
                line15,n = pattern_depend.subn(r'when what happens is influenced by other facts or events', line14)
                pattern_depend_n += n
            else:
                line15 = line14
            # txt = a55390aed2416d58ab4086db8790772c

            ## LLA doubt keyword heading fix. 'not caring about something' -> 'when you think something is unlikely to happen or be true' 13 times (think, doubt, doubt, doubter, doubtful, doubtfully, dubious, dubiously, dubiousness, surprised, thought, sure, sureness).
            if any(test_name == c for c in ["think", "doubt", "doubter", "doubtful", "doubtfully", "dubious", "dubiously", "dubiousness", "surprised", "thought", "sure", "sureness"]):
                line16,n = pattern_doubt.subn(r'<span class="secheading">when you think something is unlikely to happen or be true</span><span class="exponent">', line15)
                pattern_doubt_n += n
            else:
                line16 = line15
            # txt = 67626bafc7ae6965d323499029847386

            ## LLA each other keyword heading fix. 'happening during the time that something else happens' -> 'ways of saying that two or more people do something to each other' 9 times (each, one another, exchange, exchangeable, mutual, reciprocal, reciprocally, two-way, trade).
            if any(test_name == c for c in ["each", "one another", "exchange", "exchangeable", "mutual", "reciprocal", "reciprocally", "two-way", "trade"]):
                line17,n = pattern_eachother.subn(r'ways of saying that two or more people do something to each other', line16)
                pattern_eachother_n += n
            else:
                line17 = line16
            # txt = 6d1e5509a69c748deeaaa7a0d955aa0a

            ## LLA equipment keyword heading fix. 'not having equal rights' -> 'things you use for doing something' 6 times (equipment, tool, apparatus, gear, kit, stuff).
            if any(test_name == c for c in ["equipment", "tool", "apparatus", "gear", "kit", "stuff"]):
                line18,n = pattern_equipment.subn(r'things you use for doing something', line17)
                pattern_equipment_n += n
            else:
                line18 = line17
            # txt = 

            ## LLA especially keyword heading fix. 'unable to escape' -> 'more than usual or more than others' 13 times (especially, particularly, specially, particular, particular, above, most, least, notably, people, more, anyone, special).
            if any(test_name == c for c in ["especially", "particularly", "specially", "particular", "particular", "above", "most", "least", "notably", "people", "more", "anyone", "special"]):
                line19,n = pattern_especially_ever.subn(r'<span class="secheading">more than usual or more than others</span><span class="exponent">', line18)
                pattern_especially_n += n
            else:
                line19 = line18
            # txt = 

            ## LLA ever keyword heading fix. 'unable to escape' -> 'at any time in the past or future' 4 times (ever, time, history, life).
            if any(test_name == c for c in ["ever", "time", "history", "life"]):
                line20,n = pattern_especially_ever.subn(r'<span class="secheading">at any time in the past or future</span><span class="exponent">', line19)
                pattern_ever_n += n
            else:
                line20 = line19
            # txt = 

            ## LLA fairly/quite keyword heading fix. 'when a situation or decision is fair' -> 'more than a little, but not very' 7 times (fairly, quite, pretty, moderately, rather, somewhat, reasonably).
            if any(test_name == c for c in ["fairly", "quite", "pretty", "moderately", "rather", "somewhat", "reasonably"]):
                line21,n = pattern_fairlyquite.subn(r'more than a little, but not very', line20)
                pattern_fairlyquite_n += n
            else:
                line21 = line20
            # txt = 
            
            ## LLA fed up keyword heading fix. 'someone who is liked more than other people' -> 'feeling tired, bored, or annoyed' 4 times (enough, pissed, tether, jaded).
            if any(test_name == c for c in ["enough", "pissed", "tether", "jaded"]):
                line22,n = pattern_fedup.subn(r'feeling tired, bored, or annoyed', line21)
                pattern_fedup_n += n
            else:
                line22 = line21
            # txt = 

            ## LLA finally keyword heading fix. 'types of film' -> 'when something happens after a long time' 10 times (finally, eventually, end, end, at, last, later, one, day, time).
            if any(test_name == c for c in ["finally", "eventually", "end", "at", "last", "later", "one", "day", "time"]):
                line23,n = pattern_finally.subn(r'<span class="secheading">when something happens after a long time</span><span class="exponent">', line22)
                pattern_finally_n += n
            else:
                line23 = line22
            # txt = 
            
            ## LLA flow keyword heading fix. 'with lots of hills or mountains' -> 'when liquid moves or comes out of something' 12 times (flow, flow, pour, run, leak, drip, ooze, gush, trickle, squirt, spurt, cascade).
            if any(test_name == c for c in ["flow", "pour", "run", "leak", "drip", "ooze", "gush", "trickle", "squirt", "spurt", "cascade"]):
                line24,n = pattern_flow.subn(r'when liquid moves or comes out of something', line23)
                pattern_flow_n += n
            else:
                line24 = line23
            # txt = 22b1af20b0e5e65c9c76547eb7a94762

            ## LLA in order to keyword heading fix. 'when a law court decides that someone is innocent' -> 'in order to get something, achieve something, or make something happen' 4 times (order, so, for, view).
            if any(test_name == c for c in ["order", "so", "for", "view"]):
                line25,n = pattern_inorderto_insist.subn(r'in order to get something, achieve something, or make something happen', line24)
                pattern_inorderto_n += n
            else:
                line25 = line24
            # txt = 0092c29a20e1779a9d6de8e2e85f529c

            ## LLA insist keyword heading fix. 'when a law court decides that someone is innocent' -> 'to say firmly that someone must do something or that something must happen' 10 times (insist, demand, foot, adamant, adamantly, won't, answer, insistent, insistently, insistence).
            if any(test_name == c for c in ["insist", "demand", "foot", "adamant", "adamantly", "won't", "answer", "insistent", "insistently", "insistence"]):
                line26,n = pattern_inorderto_insist.subn(r'to say firmly that someone must do something or that something must happen', line25)
                pattern_insist_n += n
            else:
                line26 = line25
            # txt = f26a18dca85a7777c82f1fd9e4e218db

            ## LLA instructions keyword heading fix. 'using instinct rather than knowledge' -> 'information about how to do something or about what to do' 7 times (instruction, brief, recipe, manual, guide, handbook, cookbook).
            if any(test_name == c for c in ["instruction", "brief", "recipe", "manual", "guide", "handbook", "cookbook"]):
                line27,n = pattern_instructions.subn(r'information about how to do something or about what to do', line26)
                pattern_instructions_n += n
            else:
                line27 = line26
            # txt = 465c40502a64a6c2e1a1c0c4cb940a9a

            ## LLA kick keyword heading fix. 'when you are forced to stay somewhere' -> 'kick' 4 times (kick, kick, knee, boot).
            if any(test_name == c for c in ["kick", "knee", "boot"]):
                line28,n = pattern_kick.subn(r'kick', line27)
                pattern_kick_n += n
            else:
                line28 = line27
            # txt = fb2e8dbaa1671bbf1ba5776224f8ce0c

            ## LLA maybe keyword heading fix. 'material for making clothes, curtains etc' -> 'when you think something may happen or may be true, but you are not sure' 14 times (maybe, perhaps, may, might, could, possible, chance, possibly, conceivable, conceivably, you, never, know, who).
            if any(test_name == c for c in ["maybe", "perhaps", "may", "might", "could", "possible", "chance", "possibly", "conceivable", "conceivably", "you", "never", "know", "who"]):
                line29,n = pattern_maybe.subn(r'when you think something may happen or may be true, but you are not sure', line28)
                pattern_maybe_n += n
            else:
                line29 = line28
            # txt = a82c74aece1777d16e644d432d41d5d4

            ## LLA never keyword heading fix. 'to make someone feel nervous' -> 'never' 8 times (never, ever, million, millionth, millionth, moment, time, known).
            if any(test_name == c for c in ["never", "ever", "million", "millionth", "moment", "time", "known"]):
                line30,n = pattern_never.subn(r'never', line29)
                pattern_never_n += n
            else:
                line30 = line29
            # txt = 60132130a87d2f7a4e1c7ab7476daa00

            ## LLA no matter what/how much etc keyword heading fix. 'to shake your head as a way of saying no' -> 'no matter what/how much etc' 13 times (no, no, matter, however, whatever, whichever, whoever, regardless, irrespective, never, mind, come, may).
            if any(test_name == c for c in ["no", "matter", "however", "whatever", "whichever", "whoever", "regardless", "irrespective", "never", "mind", "come", "may"]):
                line31,n = pattern_nomatter.subn(r'no matter what/how much etc',line30)
                pattern_nomatter_n += n
            else:
                line31 = line30
            # txt = 2341d3c749066e53320e203674ac5276

            ## LLA once keyword heading fix. 'old-fashioned in a pleasant way' -> 'on one occasion in the past' 7 times (once, one, time, occasion, stage, point, day).
            if any(test_name == c for c in ["once", "one", "time", "occasion", "stage", "point", "day"]):
                line32,n = pattern_once.subn(r'on one occasion in the past', line31)
                pattern_once_n += n
            else:
                line32 = line31
            # txt = 9594b63e633bfc518898d5841b0da383

            ## LLA partly keyword heading fix. 'to be a part of something' -> 'not completely' 9 times (partly, partially, half, completely, entirely, extent, point, degree, part).
            if any(test_name == c for c in ["partly", "partially", "half", "completely", "entirely", "extent", "point", "degree", "part"]):
                line33,n = pattern_partly.subn(r'<span class="secheading">not completely</span><span class="exponent"><span onclick="d8018d6852bc49e3b3e655364cf1439c.toggle(this)" class="expandable"><span class="arrow">►</span> <span class="exp display">partly', line32)
                pattern_partly_n += n
            else:
                line33 = line32
            # txt = bf6a7968c1bf1f1b7cd0586c8ab00e1a
                
            ## LLA pass/go past keyword heading fix. 'the people at a party' -> 'to go past a place, person, or thing' 4 times (by, pass, pass, overtake).
            if any(test_name == c for c in ["by", "pass", "overtake"]):
                line34,n = pattern_passgopast.subn(r'to go past a place, person, or thing', line33)
                pattern_passgopast_n += n
            else:
                line34 = line33
            # txt = b851bfe0489a8fa5f5ca35fa7ec4e108

            ## LLA pattern keyword heading fix. 'on one occasion in the past' -> 'pattern' 5 time (pattern, design, marking, motif, patterning).
            if any(test_name == c for c in ["pattern", "design", "marking", "motif", "patterning"]):
                line35,n = pattern_pattern.subn(r'<span class="secheading">pattern</span><span class="exponent">', line34)
                pattern_pattern_n += n
            else:
                line35 = line34
            # txt = aa8b1a8b35183ec77eff2efc0d9dec5b

            ## LLA point at keyword heading fix. 'a person or group of people you play against' -> 'to point at someone or something, to show which one you mean' 4 times (point, indicate, gesture, towards).
            if any(test_name == c for c in ["point", "indicate", "gesture", "towards"]):
                line36,n = pattern_pointat.subn(r'to point at someone or something, to show which one you mean', line35)
                pattern_pointat_n += n
            else:
                line36 = line35
            # txt = 56aec3bbb3d307a5192609588aa67fc3
                
            ## LLA pour keyword heading fix. 'to make something possible' -> 'to make liquid or a substance come out of a container' 6 times (pour, spill, empty, sprinkle, tip, drizzle).
            if any(test_name == c for c in ["pour", "spill", "empty", "sprinkle", "tip", "drizzle"]):
                line37,n = pattern_pour.subn(r'to make liquid or a substance come out of a container', line36)
                pattern_pour_n += n
            else:
                line37 = line36
            # txt = a8e00cf58de06170cd0aab3266c2c94e

            ## LLA public services keyword heading fix. 'when a lot of people can see you or know about what is happening' -> 'things that are provided for people to use' 4 times (service, amenity, utility, supply).
            if any(test_name == c for c in ["service", "amenity", "utility", "supply"]):
                line38,n = pattern_publicservices.subn(r'things that are provided for people to use', line37)
                pattern_publicservices_n += n
            else:
                line38 = line37
            # txt = 11d38e174f4eb296da9538adc30a5e55

            ## LLA realize keyword heading fix. 'when pictures, films etc do not make things seem real' -> 'to notice or understand something that you did not notice or understand before' 10 times (realize, occur, sink, dawn, strike, hit, wake, fact, click, home).
            if any(test_name == c for c in ["realize", "occur", "sink", "dawn", "strike", "hit", "wake", "fact", "click", "home"]):
                line39,n = pattern_realize.subn(r'to notice or understand something that you did not notice or understand before', line38)
                pattern_realize_n += n
            else:
                line39 = line38
            # txt = 8d81ec886df0295fb2855a92d5696cb8

            ## LLA rubbish/garbage keyword heading fix. 'to move over a surface while pressing against it' -> 'things that you throw away because you do not want them' 7 times (rubbish, garbage, trash, waste paper, litter, refuse, waste).
            if any(test_name == c for c in ["rubbish", "garbage", "trash", "waste paper", "litter", "refuse", "waste"]):
                line40,n = pattern_rubbishgarbage.subn(r'things that you throw away because you do not want them', line39)
                pattern_rubbishgarbage_n += n
            else:
                line40 = line39
            # txt = ea395405b863f95022739fa376b5a29a

            ## LLA rumour keyword heading fix. 'rules of acceptable behaviour' -> 'things that people say, which may or may not be true' 10 times (rumour, speculation, gossip, scandal, report, talk, hearsay, hear, grapevine, rumoured).
            if any(test_name == c for c in ["rumour", "speculation", "gossip", "scandal", "report", "talk", "hearsay", "hear", "grapevine", "rumoured"]):
                line41,n = pattern_rumour.subn(r'things that people say, which may or may not be true', line40)
                pattern_rumour_n += n
            else:
                line41 = line40
            # txt = 88ebbc2c648fbd85bf07a8c23c0e29a6

            ## LLA since keyword heading fix. 'not having a lot of decoration or things added' -> 'since a particular time or event in the past' 5 times (since, ever, for, from, start).
            if any(test_name == c for c in ["since", "ever", "for", "from", "start"]):
                line42,n = pattern_since.subn(r'since a particular time or event in the past', line41)
                pattern_since_n += n
            else:
                line42 = line41
            # txt = 41eb4d45e4af2b0f9e0d4a03085ebfd9

            ## LLA so/therefore keyword heading fix. 'what you say to tell someone that you are sorry' -> 'ways of saying what the result of something is' 7 times (so, so, therefore, such, result, consequently, then).
            if any(test_name == c for c in ["so", "therefore", "such", "result", "consequently", "then"]):
                line43,n = pattern_sotherefore.subn(r'ways of saying what the result of something is', line42)
                pattern_sotherefore_n += n
            else:
                line43 = line42
            # txt = ed728eef7f4dc06aa4748dbb74723891

            ## LLA special keyword heading fix. 'not able to speak' -> 'special' 6 times (special, special, specially, particular, unique, uniqueness).
            if any(test_name == c for c in ["special", "specially", "particular", "unique", "uniqueness"]):
                line44,n = pattern_special_speed.subn(r'special', line43)
                pattern_special_n += n
            else:
                line44 = line43
            # txt = 37a48265d004c7668585dfcba39a4824
                
            ## LLA speed keyword heading fix. 'not able to speak' -> 'how fast something moves or is done' 7 times (speed, speed, rate, pace, velocity, momentum, per).
            if any(test_name == c for c in ["speed", "rate", "pace", "velocity", "momentum", "per"]):
                line45,n = pattern_special_speed.subn(r'how fast something moves or is done', line44)
                pattern_speed_n += n
            else:
                line45 = line44
            # txt = 3021c5d96a512a73541abb2eb5a53cf3

            ## LLA system keyword heading fix. 'to try to make someone feel sorry for you' -> 'a system' 6 times (system, set-up, network, framework, structure, mechanism).
            if any(test_name == c for c in ["system", "set-up", "network", "framework", "structure", "mechanism"]):
                line46,n = pattern_system.subn(r'a system', line45)
                pattern_system_n += n
            else:
                line46 = line45
            # txt = 82983756585a199072a3c3abbc21a3f3

            ## LLA thirsty keyword heading fix. 'what you say when you think something is true, but you are not sure' -> 'feeling that you want to drink something' 10 times (thirsty, thirstily, drink, dry, dryness, parched, dehydrate, dehydrated, dehydration, thirst).
            if any(test_name == c for c in ["thirsty", "thirstily", "drink", "dry", "dryness", "parched", "dehydrate", "dehydrated", "dehydration", "thirst"]):
                line47,n = pattern_thirsty.subn(r'feeling that you want to drink something', line46)
                pattern_thirsty_n  += n
            else:
                line47 = line46
            # txt = 1c324d2d252207bedefc50679305e70d

            ## LLA tool keyword heading fix. 'to use the toilet' -> 'a tool' 6 times (tool, instrument, gadget, device, implement, utensil).
            if any(test_name == c for c in ["tool", "instrument", "gadget", "device", "implement", "utensil"]):
                line48,n = pattern_tool.subn(r'a tool', line47)
                pattern_tool_n += n
            else:
                line48 = line47
            # txt = 251f2f8c8640c5cd84c25208275db9ad
                
            ## LLA until keyword heading fix. 'when things are spread around in a messy way' -> 'continuing to a particular time or event and then stopping' 3 times (until, up, from).
            if any(test_name == c for c in ["until", "up", "from"]):
                line49,n = pattern_until.subn(r'continuing to a particular time or event and then stopping', line48)
                pattern_until_n += n
            else:
                line49 = line48
            # txt = 85d7c68b989b446f2de7555490ba6326

            ## LLA working keyword heading fix. 'to not work hard enough' -> 'when a machine/system etc works properly' 8 times (work, working, order, go, up, run, operational, operationally).
            if any(test_name == c for c in ["work", "working", "order", "go", "up", "run", "operational", "operationally"]):
                line50,n = pattern_working.subn(r'when a machine/system etc works properly', line49)
                pattern_working_n += n
            else:
                line50 = line49
            # txt = 1e5030fa85a3b7c139baafd8972b42fd, 20240109 release 1

            ## LLA section addition. Add 'a fairly long time' section 3 times (time, time, while_noun).
            if test_name == 'time':
                line51,n = pattern_AFairlyLongTime_time_headword.subn(r'%s%s%s' % (AFairlyLongTime_time_headword_pre, AFairlyLongTime_content, section_common_post), line50)
                pattern_AFairlyLongTime_time_headword_n += n
            elif test_name == 'while':
                line51,n = pattern_AFairlyLongTime_while_headword.subn(r'%s%s%s' % (AFairlyLongTime_while_headword_pre, AFairlyLongTime_content, section_common_post), line50)
                pattern_AFairlyLongTime_while_headword_n += n
            else:
                line51 = line50
            # txt = cabd1c390db7c0c6172a35361f3fe79e

            ## LLA section addition. Add 'to be getting nearer to a person or vehicle in front of you' section 3 times (near, near, near).
            if test_name == 'near':
                line52,n = pattern_ToBeGettingNearerToAPersonOrVehicleInFrontOfYou_near_headword.subn(r'%s%s%s' % (ToBeGettingNearerToAPersonOrVehicleInFrontOfYou_near_headword_pre, ToBeGettingNearerToAPersonOrVehicleInFrontOfYou_content, section_common_post), line51)
                pattern_ToBeGettingNearerToAPersonOrVehicleInFrontOfYou_near_headword_n += n
            else:
                line52 = line51
            # txt = df5f37ebf3a44384ca5ad79af27cba15

            ## LLA section addition. Add 'to be almost a particular age' section 2 times (age, age).
            if test_name == 'age':
                line53,n = pattern_ToBeAlmostAParticularAge_age_headword.subn(r'%s%s%s' % (ToBeAlmostAParticularAge_age_headword_pre, ToBeAlmostAParticularAge_content, section_common_post), line52)
                pattern_ToBeAlmostAParticularAge_age_headword_n += n
            else:
                line53 = line52
            # txt = aa7201334943d24b62afb4d10fcd766e

            ## LLA section addition. Add 'when something is intended to do something' section 1 time (intend).
            if test_name == 'intend':
                line54,n = pattern_WhenSomethingIsIntendedToDoSomething_intend_headword.subn(r'%s%s%s' % (WhenSomethingIsIntendedToDoSomething_intend_headword_pre, WhenSomethingIsIntendedToDoSomething_content, section_common_post), line53)
                pattern_WhenSomethingIsIntendedToDoSomething_intend_headword_n += n
            else:
                line54 = line53
            # txt = 28b0f25793337562502e00d572cabd75

            ## LLA section addition. Add 'ways of beginning a letter' section 5 times (letter, dear_adj, sir, madam, hi).
            if test_name == 'letter':
                line55,n = pattern_WaysOfBeginningALetter_letter_headword.subn(r'%s%s%s' % (WaysOfBeginningALetter_letter_headword_pre, WaysOfBeginningALetter_content, section_common_post), line54)
                pattern_WaysOfBeginningALetter_letter_headword_n += n
            elif test_name == 'dear':
                line55,n = pattern_WaysOfBeginningALetter_dear_headword.subn(r'%s%s%s' % (WaysOfBeginningALetter_dear_headword_pre, WaysOfBeginningALetter_content, section_common_post), line54)
                pattern_WaysOfBeginningALetter_dear_headword_n += n
            elif test_name == 'sir':
                line55,n = pattern_WaysOfBeginningALetter_sir_headword.subn(r'%s%s%s' % (WaysOfBeginningALetter_sir_headword_pre, WaysOfBeginningALetter_content, section_common_post), line54)
                pattern_WaysOfBeginningALetter_sir_headword_n += n
            elif test_name == 'madam':
                line55,n = pattern_WaysOfBeginningALetter_madam_headword.subn(r'%s%s%s' % (WaysOfBeginningALetter_madam_headword_pre, WaysOfBeginningALetter_content, section_common_post), line54)
                pattern_WaysOfBeginningALetter_madam_headword_n += n
            elif test_name == 'hi':
                line55,n = pattern_WaysOfBeginningALetter_hi_headword.subn(r'%s%s%s' % (WaysOfBeginningALetter_hi_headword_pre, WaysOfBeginningALetter_content, section_common_post), line54)
                pattern_WaysOfBeginningALetter_hi_headword_n += n
            else:
                line55 = line54
            # txt = 3792b2dc5c82ed7d86a30e4c6d785f6b

            ## LLA section addition. Add 'to make people notice you' section 2 times (notice, notice).
            if test_name == 'notice':
                line56,n = pattern_ToMakePeopleNoticeYou_notice_headword.subn(r'%s%s%s' % (ToMakePeopleNoticeYou_notice_headword_pre, ToMakePeopleNoticeYou_content, section_common_post), line55)
                pattern_ToMakePeopleNoticeYou_notice_headword_n += n
            else:
                line56 = line55
            # txt = 87c421383cef1312cdd0e2a273b30e0f
            
            ## LLA section addition. Add 'to start talking about a subject' section 2 times (subject, subject).
            if test_name == 'subject':
                line57,n = pattern_ToStartTalkingAboutASubject_subject_headword.subn(r'%s%s%s' % (ToStartTalkingAboutASubject_subject_headword_pre, ToStartTalkingAboutASubject_content, section_common_post), line56)
                pattern_ToStartTalkingAboutASubject_subject_headword_n += n
            else:
                line57 = line56
            # txt = bc58d6c83c22c874f4d604d88e46fa52

            ## LLA section addition. Add 'to keep saying the same thing in an annoying way' section 2 times (repeat, repeat).
            if test_name == 'repeat':
                line58,n = pattern_ToKeepSayingTheSameThingInAnAnnoyingWay_repeat_headword.subn(r'%s%s%s' % (ToKeepSayingTheSameThingInAnAnnoyingWay_repeat_headword_pre, ToKeepSayingTheSameThingInAnAnnoyingWay_content, section_common_post), line57)
                pattern_ToKeepSayingTheSameThingInAnAnnoyingWay_repeat_headword_n += n
            else:
                line58 = line57
            # txt = 
            
            ## LLA section addition. Add 'what you call your mother' section 1 time (mother).
            if test_name == 'mother':
                # when for replacement, don't use '\)', use ')'
                mother_headword_pre2 = 'her children rather than working elsewhere<span class="neutral">)</span></span></div></span></span>'
                line59,n = pattern_WhatYouCallYourMother_mother_headword.subn(r'%s%s%s' % (mother_headword_pre2, WhatYouCallYourMother_content, section_common_post), line58)
                pattern_WhatYouCallYourMother_mother_headword_n += n
            else:
                line59 = line58
            # txt = 

            ## LLA section addition. Add 'for people of one sex' section 1 time (sex).
            if test_name == 'sex':
                line60,n = pattern_ForPeopleOfOneSex_sex_headword.subn(r'%s%s%s' % (ForPeopleOfOneSex_sex_headword_pre, ForPeopleOfOneSex_content, section_common_post), line59)
                pattern_ForPeopleOfOneSex_sex_headword_n += n
            else:
                line60 = line59
            # txt = 

            ## LLA no keyword heading fix. 'no matter what/how much etc' -> 'to shake your head as a way of saying no' 2 times (no, no).
            if test_name == 'no':
                line61,n = pattern_no.subn(r'to shake your head as a way of saying no', line60)
                pattern_no_n += n
            else:
                line61 = line60
            # txt = 

            ## LLA 'not young' section fix. 'The bar was fill with ageing hippies' -> 'The bar was filled with ageing hippies' 7 times (ancient, elderly, middle-aged, old, wizened, wrinkled, young).
            if any(test_name == c for c in ["ancient", "elderly", "middle-aged", "old", "wizened", "wrinkled", "young"]):
                line62,n = pattern_notYoung.subn(r'The bar was filled with ageing hippies', line61)
                pattern_notYoung_n += n
            else:
                line62 = line61
            # txt = 0fade275811b5a2c5252ddefd9e65fe3 20240120 release 2

            ## LDOCE6 main body fix. 'see thesaurus at approximate' -> 'see thesaurus at approximately' 4 times (about, around, circa, roughly).
            if any(test_name == c for c in ["about", "around", "circa", "roughly"]):
                line63,n = pattern_thesaurus_at_approximately.subn(r'<span class="refhwd">approximately</span>', line62)
                pattern_thesaurus_at_approximately_n += n
            else:
                line63 = line62

            ## LDOCE6 main body fix. 'They first met at/in/fifteen years ago' -> 'They first met at/in/on fifteen years ago' 1 time (ago).
            if test_name == 'ago':
                line64,n = pattern_ago_headword_body.subn(r'They first met at/in/on fifteen years ago', line63)
                pattern_ago_headword_body_n += n
            else:
                line64 = line63

            ## LDOCE6 main body fix. 'ɪˈtɪmədeɪtɪŋ' -> 'ɪnˈtɪmədeɪtɪŋ' 1 time (intimidating).
            if test_name == 'intimidating':
                line65,n = pattern_intimidating_headword_body.subn(r'ɪnˈtɪmədeɪtɪŋ', line64)
                pattern_intimidating_headword_body_n += n
            else:
                line65 = line64
            # txt = 7899184ab97cfc5bc80632d9253bbee7 20240122 release 3

            # to add new here:
            # <title>. 'XXX' -> 'YYY' Z times (1, 2, ..., Z).

            line_final = line65
            with open(output, 'a', encoding="utf8") as the_file:
                the_file.write(line_final)

    print("\nSummary:")

    if not debug:
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
        assert pattern_competition_n == 4
        assert pattern_completely_n == 17
        assert pattern_dead_n == 13
        assert pattern_depend_n == 7
        assert pattern_doubt_n == 13
        assert pattern_eachother_n == 9
        assert pattern_equipment_n == 6
        assert pattern_especially_n == 13
        assert pattern_ever_n == 4
        # 21
        assert pattern_fairlyquite_n == 7
        assert pattern_fedup_n == 4
        assert pattern_finally_n == 10
        assert pattern_flow_n == 12
        assert pattern_inorderto_n == 4
        assert pattern_insist_n == 10
        assert pattern_instructions_n == 7
        assert pattern_kick_n == 4
        assert pattern_maybe_n == 14
        assert pattern_never_n == 8
        # 31
        assert pattern_nomatter_n == 13
        assert pattern_once_n == 7
        assert pattern_partly_n == 9
        assert pattern_passgopast_n == 4
        assert pattern_pattern_n == 5
        assert pattern_pointat_n == 4
        assert pattern_pour_n == 6
        assert pattern_publicservices_n == 4
        assert pattern_realize_n == 10
        assert pattern_rubbishgarbage_n == 7
        # 41
        assert pattern_rumour_n == 10
        assert pattern_since_n == 5
        assert pattern_sotherefore_n == 7
        assert pattern_special_n == 6
        assert pattern_speed_n == 7
        assert pattern_system_n == 6
        assert pattern_thirsty_n == 10
        assert pattern_tool_n == 6
        assert pattern_until_n == 3
        assert pattern_working_n == 8
        # 51
        assert pattern_AFairlyLongTime_time_headword_n == 2
        assert pattern_AFairlyLongTime_while_headword_n == 1
        # 52
        assert pattern_ToBeGettingNearerToAPersonOrVehicleInFrontOfYou_near_headword_n == 3
        # 53
        assert pattern_ToBeAlmostAParticularAge_age_headword_n == 2
        # 54
        assert pattern_WhenSomethingIsIntendedToDoSomething_intend_headword_n == 1
        # 55
        assert pattern_WaysOfBeginningALetter_letter_headword_n == 1
        assert pattern_WaysOfBeginningALetter_dear_headword_n == 1
        assert pattern_WaysOfBeginningALetter_sir_headword_n == 1
        assert pattern_WaysOfBeginningALetter_madam_headword_n == 1
        assert pattern_WaysOfBeginningALetter_hi_headword_n == 1
        # 56
        assert pattern_ToMakePeopleNoticeYou_notice_headword_n == 2
        # 57
        assert pattern_ToStartTalkingAboutASubject_subject_headword_n == 2
        # 58
        assert pattern_ToKeepSayingTheSameThingInAnAnnoyingWay_repeat_headword_n == 2
        # 59
        assert pattern_WhatYouCallYourMother_mother_headword_n == 1
        # 60
        assert pattern_ForPeopleOfOneSex_sex_headword_n == 1
        # 61
        assert pattern_no_n == 2
        # 62
        assert pattern_notYoung_n == 7
        # 63
        assert pattern_thesaurus_at_approximately_n == 4
        # 64
        assert pattern_ago_headword_body_n == 1
        # 65
        assert pattern_intimidating_headword_body_n == 1

    output_md5 = hashlib.md5(open(output,'rb').read()).hexdigest()
    print("%s md5: %s" % (output, output_md5))
    if not debug:
        #assert output_md5 == '1e5030fa85a3b7c139baafd8972b42fd' #20240109 release 1
        #assert output_md5 == '0fade275811b5a2c5252ddefd9e65fe3' #20240120 release 2
        assert output_md5 == '7899184ab97cfc5bc80632d9253bbee7' #20240122 release 3

    print("Done with the job, totally takes %s s" % (time.time() - start_time))


def generate_change_log():
    pattern_chagne_log = re.compile(r'## ')
    log_file = 'change_log.txt'
    log_id = 1
    log_content = ''

    # read current file and generate the change log.
    with open('src/generate_ldoce6enen_bugfix.py', encoding="utf8") as ifile:
        for line in ifile:
            m = pattern_chagne_log.search(line)
            for itr in re.finditer(pattern_chagne_log, line):
                target_log = line[itr.start()+3:].strip()
                #print(target_log)
                log_content += "%s. %s\n" % (log_id, target_log)
                log_id += 1

    with open(log_file, 'w', encoding="utf8") as the_file:
        the_file.write(log_content)

if __name__ == '__main__':
    do_the_job()
    generate_change_log()
