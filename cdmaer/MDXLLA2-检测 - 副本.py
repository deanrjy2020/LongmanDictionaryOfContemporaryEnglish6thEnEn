#检测LLA
from readmdict import MDX
from bs4 import BeautifulSoup as bs

def c(bstr):
    return str(bstr, encoding='utf-8').strip()
def t(obj):
    return obj.get_text().strip() if obj is not None else ''

list1=open('LLAsetter1.txt', encoding='utf-8').read().split('\n')
listdc1=[obj.split('@')[1] for obj in list1]
list2=open('LLAsetter2.txt', encoding='utf-8').read().split('\n')
listdc2=[obj.split('@')[1] for obj in list2]
list2sent=[obj.split('@')[-1] for obj in list2]
logfile=open('LLAlogAmazon.txt', 'a', encoding='utf-8')

#mdx=MDX(r'LDOCE6_New\LDOCE6EN04.mdx')
mdx=MDX(r'D:\下载\电子词典\朗文\LDOCE6_New\1-Amazon-154M\LDOCE6_Amazon_0109.mdx')

for key, value in mdx.items():
    #if c(key)=='broad':break
    if c(key)[:]!='word-set-' and c(value)[0]!='@':
        soup=bs(c(value), 'lxml')
        for entry in soup.select('body>div>span[class=entry]'):
            hwd=t(entry.select_one('span[class=hwd]'))
            pos=t(entry.select_one('span[class=pos]'))
            for entry1 in entry.select('div[class=at-link]>span[class=entry]'):
                if entry1.span.string=='Longman Language Activator':
                    f=open('LLAlog0109new.txt', 'a', encoding='utf-8')
                    for section in entry1.select('span[class~=section]'):
                        title=section.span.string
                        dc=''
                        for exp in section.select('span[class="exp display"]'):
                            dc+=exp.get_text().strip()+'|'
                            
                        if dc in listdc1:
                            basetitle=list1[listdc1.index(dc)].split('@')[0]
                            if basetitle==title:
                                pass
                                #print('In list1 and same title: \n', hwd, pos, title)
                            else:
                                logfile.write('\t'.join(('list1 alert: ', hwd, pos, basetitle, title))+'\n')
                        elif dc in listdc2:
                            liju1=section.select_one('span[class=example]').get_text()[2:]
                            if liju1 in list2sent:
                                basetitle=list2[list2sent.index(liju1)].split('@')[0]
                                if basetitle!=title:
                                    logfile.write('\t'.join(('list2 alert: ', hwd, pos, basetitle, title))+'\n')
                        else:
                            logfile.write('\t'.join(('oops!', hwd, dc))+'\n')
logfile.close()
    
