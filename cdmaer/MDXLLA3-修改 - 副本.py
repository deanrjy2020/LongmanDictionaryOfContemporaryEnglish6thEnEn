#修正朗文LLA
from readmdict import MDX
from bs4 import BeautifulSoup as bs

def c(bstr):
    return str(bstr, encoding='utf-8').strip()
def t(obj):
    return obj.get_text().strip() if obj is not None else ''
def cleanse(text):
    return ''.join(c for c in text if c.isprintable())

list1=open('LLAsetter1.txt', encoding='utf-8').read().split('\n')
listdc1=[obj.split('@')[1] for obj in list1]
list2=open('LLAsetter2.txt', encoding='utf-8').read().split('\n')
listdc2=[obj.split('@')[1] for obj in list2]
list2sent=[obj.split('@')[-1] for obj in list2]


mdx=MDX(r'LDOCE6_New\LDOCE6EN0202.mdx')
n=0
for key, value in mdx.items():
    n+=1
    fn=str(int(n/5000)+1).zfill(2)
    f=open('LDOCE6_NEW\\file'+fn+'.txt', 'a', encoding='utf-8')

    if c(key)[:]=='word-set-' or c(value)[0]=='@':
        f.write(c(key)+'\n'+c(value)+'\n</>\n')
    else:
        soup=bs(c(value), 'lxml')
        for entry in soup.select('body>div>span[class=entry]'):
            hwd=t(entry.select_one('span[class=hwd]'))
            pos=t(entry.select_one('span[class=pos]'))
            for entry1 in entry.select('div[class=at-link]>span[class=entry]'):
                if entry1.span.string=='Longman Language Activator':
                    for section in entry1.select('span[class~=section]'):
                        title=section.span.string
                        dc=''
                        for exp in section.select('span[class="exp display"]'):
                            dc+=exp.get_text().strip()+'|'
                            
                        if dc in listdc1:
                            basetitle=list1[listdc1.index(dc)].split('@')[0]
                            if basetitle!=title:
                                section.span.string=basetitle
                        elif dc in listdc2:
                            liju1=section.select_one('span[class=example]').get_text()[2:]
                            if liju1 in list2sent:
                                basetitle=list2[list2sent.index(liju1)].split('@')[0]
                                if basetitle!=title:
                                    section.span.string=basetitle
                        else:
                            if title=='never':
                                section.select_one('span[class="exp display"]').string='never'
                            elif title=='continuing to a particular time or event and then stopping':
                                section.select_one('span[class="exp display"]').string='until'
        new_soup_str=''
        for content in soup.body.contents:
            new_soup_str+=cleanse(str(content))
        f.write(c(key)+'\n'+str(soup.link)+new_soup_str+'\n</>\n')
    f.close()
    
