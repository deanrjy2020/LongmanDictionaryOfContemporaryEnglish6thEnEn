# LongmanDictionaryOfContemporaryEnglish6thEnEn

mdx
0, setups
    Windows安装 3.14.2
    C:\Python314\Scripts\ 和 C:\Python314\ 放到path里面.
    pip install readmdict bs4 lxml
    python -m pip install beautifulsoup4 lxml
1, 解压LongmanDictionaryOfContemporaryEnglish6thEnEn.mdx得到LongmanDictionaryOfContemporaryEnglish6thEnEn.txt
    注意, 解压会把得到的txt排序, 和原来的txt的md5可能不一样了.
2, 压缩txt得到mdx, md5应该是一样的. 参数如下:
    source选txt
    target给一个xxx.mdx
    style/data空着
    Original format MDict(Html)
    Ecoding UTF-8(Unicode)
    只勾选Strip Key
    Title: "Longman Dictionary of Contemporary English 6th edition"
    Description: faq-index
    Index block size 32
    record block size 64
    by email, 空着
    本地时间改为 20160912 下午4点前, 5点美国时间对应中国0913号, md5不一样了.

mdd
1, 解压LongmanDictionaryOfContemporaryEnglish6thEnEn.mdd得到文件夹
2, 参数和上面一样,
    source空着
    target给xxx.mdd
    style空着
    data选文件夹
    Options和上面一样, 不动
    勾选Build Data archive only
    修改本地时间2016 05 21
    连续两次build MD5是一样的
    时间不同md5是不一样的
    每次update mdd后重新解压比较文件

html基础:
    HTML = 一棵树（DOM 树）, 用欧路空白处右击, 调试
    tag 是节点, tag本身几乎没有语义, 真正的“语义”是通过 class 给的
        <tag>内容</tag>
        比如
            <span>aback</span>
            <div>definition</div>
            span	行内容器（轻量节点）
            div	块级容器（结构节点）
            a	链接 / 锚点
            img	图片
            ul / li	列表
    class = 这个节点“是什么”, class 才是语义，tag 只是容器
        chwd, 词性, noun, verb等 
        hwd	headword（词头）
        pos	part of speech
        def	definition
        example	example sentence
        secheading	LLA 大类
        exponent	LLA 子条目
        content	解释正文
    文本是叶子


Change log:

Rules:
a) don't manually modify the faq-index, do all with program.
b) do manually, and then do program, the same md5.

1,
制作日期：2023/12/17 by Dean</li><li>修改内容：<br><ol><li>修复跳转按钮上单词+右上角数字+词性当中单词+右上角数字缺失的问题，与Amazon 182MB版mdx保持一致，采用正则表达式搜索替换，将有词性的索引替换17699次，没有词性的索引替换314次</li></ol></li> <li>

has_part_of_speech replaced 17699 times
no_part_of_speech replaced 314 times
2715e9a0ca8b393b86ab7b126a8b8aa0 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

2,
replaced left/right Chinese double/single qoute
“ 21, fixed
” 21, fixed
'
‘ 23009, fixed
’ 107587, fixed
f66404bbb8fe43651e83a58fe19228ae *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

"" 96-> "
'' 3685-> "
3f61853dee93536d4664dc0a7e5c8b77 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

,,. 10-> ' …'
dc32db04d7622f8d0ded4452a8b673ce *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

Hegira calendar
ˌ... ˈ...,.ˌ.. ˈ...   1->   ˈhedʒərə,ˈkæləndə
a654595ae5d345304158af4b8275b67e *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

.,. 8-> .     do this after Hegira calendar
24e73e7c14f20b92c3fef442fcb4915b *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

:,. 2-> ' …'
e9b608879534161c02ef3ddf620fb297 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

class="expr">how far…   1->  class="expr">how far …
08e60a5c182934c9c3ac271bc171f859 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

bioprospect  use \$  \. in re.
<span class="neutral"> /</span><span class="amevarpron"><span class="neutral"> $ </span>ˌ...... ˈ...</span><span class="neutral">/</span>   3-> ''    #remove
1bf4b50de133df1efd1ef8ddc9748a78 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

self-congratulation remove 2, see code
862cf05e0586a6ae0d080595f80798e9 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

self-regulation remove 2, see code
6d1f8218a5475b02c30ec8fcae8f4b21 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

..... 6-> .   # after above two, total 10
78eceb2442f0198d1d70d32afcd9186b *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt
    

augustine_st_capillary_action remove 2
</span>ˌ.... ˈ..</span>
a7b9f757987f4992b030186fb9f48ce2 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

augustine_st_2 remove 1
9a049af4d06e13682ddb3e47375fff08 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

two_words_no_phonetic_symbol 93 remove
printed the detailed log for the 93, looks good.
e77ba439502aae8bc0ee6526c02d1605 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

two_words_no_phonetic_symbol round2 7 remove
printed the detailed log for the 7, looks good.
9b1f12cb0690c2c88384ef03416f72b1 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

soy sauce 1 remove
e5b992f6eb3923eed3ae00596fab5908 *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

' ....' 181-> ' …'
9b8719932bbada2a23f858e4fdc09dbf *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt

351'....' = [a-z]\.\.\.\. 243 + >.... 108
'....' 351-> ' …'
fixed all '....' issue.

redo?
英语中的省略号是三点，但是如果是在句末的话，还得加上该句子的标点符号。如： Would you like ...? 所以你所说的情况是：该省略号出现在陈述句的句尾，也就是省略号加上一个句号，所以就成了四点。

9a877679c671a62a47c4900010df208c *src/LongmanDictionaryOfContemporaryEnglish6thEnEn_py.txt



above all check that it has the same as manual modification


back quote issue
'`' 275
    ' ` '  189 - 79 = 110
        ' ` ([^<]*)''  79 
            ' ` ([^<]*)' '  25 空格结尾, 直接替换左边, 去掉左边的空格, 仔细检查过
            ` ([^<]*)'[^\s] 54 非空格结尾
                ` ([^<]*)'\.   10 , 点结尾, 和空格结尾一样, 仔细检查过
                ` ([^<]*)',   4   和空格结尾一样, 仔细检查过
                ` ([^<]*)'[str]   's  32  don't   6   you're   2 = 40, todo, 检查


better
<span class="nodeword">better</span> than none.</li><li>She had half drained her mug when she said, ` Ah, that's <span class="nodeword">better</span>!</li><li>So let's try: That's <span class="nodewor
big
an class="neutral">Â· </span>Finding people was no <span class="colloinexa">big deal</span> to him. ` That's easy.</span><span class="example"><span class="neutral">Â· </span>But Vassar taught me that
black
/span>Amy leaned forward and put her mug on the <span class="colloinexa">black coffee</span> table. ` She's right, you know.</span><span class="example"><span class="neutral">Â· </span>She served us e
blackness
/span>Amy leaned forward and put her mug on the <span class="colloinexa">black coffee</span> table. ` She's right, you know.</span><span class="example"><span class="neutral">Â· </span>She served us e
brighten
 class="example"><span class="neutral">Â· </span>She <span class="colloinexa">brightened up</span>. ` Still, there's one way to find them.</span><span class="example"><span class="neutral">Â· </span>M
coffee
/span>Amy leaned forward and put her mug on the <span class="colloinexa">black coffee</span> table. ` She's right, you know.</span><span class="example"><span class="neutral">Â· </span>House Minority 
coffee
/span>Amy leaned forward and put her mug on the black <span class="colloinexa">coffee table</span>. ` She's right, you know.</span><span class="example"><span class="neutral">Â· </span>There are like 
drain
half <span class="colloinexa">drained</span> her <span class="colloinexa">mug</span> when she said, ` Ah, that's better!</span><span class="example"><span class="neutral">Â· </span>On the <span class=
evangelical
an><div class="content"><span class="example"><span class="neutral">Â· </span>Hostile, she thought. ` Well, there's a lot of little <span class="colloinexa">evangelical churches</span> in La Perla.</s
forehead
inexa">touched</span> her <span class="colloinexa">forehead</span>, and drew her hand back sharply. ` She's burning up!</span><span class="example"><span class="neutral">Â· </span>She went back to the
fortune
Â· </span>Nora asks, staring into her teacup like a <span class="colloinexa">fortune teller</span>. ` Well, it's leading here, eventually.</span><span class="example"><span class="neutral">Â· </span>I
good
then that's <span class="nodeword">good</span>.</li><li>She had half drained her mug when she said, ` Ah, that's <span class="nodeword">better</span>!</li><li>That's <span class="nodeword">good</span>
skip the 18th replacement for haulier keyword.
mug
ord">mugs</span>.</li><li>She had half drained her <span class="nodeword">mug</span> when she said, ` Ah, that's better!</li><li>She rummaged around and found a teapot and a <span class="nodeword">mug
mug
half <span class="colloinexa">drained</span> her <span class="colloinexa">mug</span> when she said, ` Ah, that's better!</span><span class="example"><span class="neutral">Â· </span>On the <span class=
mug
an class="colloinexa">put</span> her <span class="colloinexa">mug</span> on the black coffee table. ` She's right, you know.</span><span class="example"><span class="neutral">Â· </span>Pete <span clas
pair
 class="colloinexa">pulled</span> on a <span class="colloinexa">pair</span> of jeans and a sweater. ` What's up Dad?</span><span class="example"><span class="neutral">Â· </span>She had <span class="co
respect
class="nodeword">respect</span> of statements which damage its business reputation.</li><li>The Bad ` Un's tactics are relentless in deflecting efforts made towards relationship with you, especially i
seesaw
aw</span> affair.</li><li>Like the other end of a <span class="nodeword">seesaw</span>, Agnes rose. ` Where's Magrat?</li><li>So, lie flat on your back over the pivot on a <span class="nodeword">seesa
slump
le"><span class="neutral">Â· </span>Her <span class="colloinexa">shoulders slumped</span> a little. ` It's Saturday tomorrow.</span><span class="example"><span class="neutral">Â· </span>Her <span clas
slur
xa">speech</span> was <span class="colloinexa">slurred</span>, and she could not believe him drunk. ` Emilio, what's happened?</span><span class="example"><span class="neutral">Â· </span>Her <span cla
stubborn
s to the obvious questions.</span><span class="example"><span class="neutral">Â· </span>He frowned. ` Steve Waugh's the <span class="colloinexa">most stubborn</span> batsman in world cricket.</span></
stubbornly
s to the obvious questions.</span><span class="example"><span class="neutral">Â· </span>He frowned. ` Steve Waugh's the <span class="colloinexa">most stubborn</span> batsman in world cricket.</span></
stubbornness
s to the obvious questions.</span><span class="example"><span class="neutral">Â· </span>He frowned. ` Steve Waugh's the <span class="colloinexa">most stubborn</span> batsman in world cricket.</span></
teller
Â· </span>Nora asks, staring into her teacup like a <span class="colloinexa">fortune teller</span>. ` Well, it's leading here, eventually.</span><span class="example"><span class="neutral">Â· </span>I
that
<span class="nodeword">better</span> than none.</li><li>She had half drained her mug when she said, ` Ah, that's <span class="nodeword">better</span>!</li><li>So let's try: That's <span class="nodewor
that
then that's <span class="nodeword">good</span>.</li><li>She had half drained her mug when she said, ` Ah, that's <span class="nodeword">better</span>!</li><li>That's <span class="nodeword">good</span>
that
<span class="nodeword">better</span> than none.</li><li>She had half drained her mug when she said, ` Ah, that's <span class="nodeword">better</span>!</li><li>So let's try: That's <span class="nodewor
that
then that's <span class="nodeword">good</span>.</li><li>She had half drained her mug when she said, ` Ah, that's <span class="nodeword">better</span>!</li><li>That's <span class="nodeword">good</span>
that
<span class="nodeword">better</span> than none.</li><li>She had half drained her mug when she said, ` Ah, that's <span class="nodeword">better</span>!</li><li>So let's try: That's <span class="nodewor
that
then that's <span class="nodeword">good</span>.</li><li>She had half drained her mug when she said, ` Ah, that's <span class="nodeword">better</span>!</li><li>That's <span class="nodeword">good</span>
word
ble in the blanks on the pages.</span><span class="example"><span class="neutral">Â· </span>The Bad ` Un's strategy is to prevent the <span class="colloinexa">written word</span> from becoming food fo
write
on alphabet letters and blends.</span><span class="example"><span class="neutral">Â· </span>The Bad ` Un's strategy is to prevent the <span class="colloinexa">written word</span> from becoming food fo
32



`... you killed.. `
` Sailing is the perfect antidote for age, Reyes.
` To <span class="nodeword">dearest</span> Polly




... 13740 -> 
    ' ...' 12572
    '>...' 246
    [a-z]\.\.\. 875
    ?... 11
    (... 16
    )... 6
    14



next:

,[^\s0-9]
,[^\s0-9']
,[^\s0-9'"]




bugs:
goodbye, 用单引号了.

glacÃ© icing

 (also St Auˌgustine of ˈHippo) 
Yeager, Charles (Chuck)
self-congratulation ending diff with the web
;, 6
:, 6
,. 117
$ 12
 $ 1, 500 a year for..
  $ 108, 000 for John R.. Sasso,


手动检查中文标点
。？！，、；：『』「」（）〔〕【】～《》〈〉 no match
… 75 matches, ok
· many matches, ok
[] english version
_ english version
/ ok
| ok
^ no match
~ no match
\  no match
all ok above.

有空todo:
─ 0 match
- english version, minus, ok
— 14986 match, ok?
    <span>— 14935, why?
– 16755 matches




@1.24.2024
src\parse_ldoce6enen_special_char_in_headword.py get 230 results, 
    replace the special char with english letter n the headword only.
    replace left/right single/double qoute, with straight ones for all entries.