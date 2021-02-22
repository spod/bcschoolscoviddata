#! /usr/bin/env python3

import re
from bs4 import BeautifulSoup

html_doc = ""
with open('data/test_vch_school_exposures.html', 'r') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

sd_re = re.compile('School\ District\ \d\d|Independent\ schools')

exp = soup.find(text="Current exposures")

sd = exp.find_next('span', string=sd_re)
while sd is not None:
    print(sd.text)
    school_exps = sd.find_next('div')
    ps = school_exps.find_all('p')
    for p in ps:
        if p.text.strip() != '':
            print(p.text)
    sd = sd.find_next('span', string=sd_re)

exp = soup.find(text="Past exposures")
head = exp.find_next('span', text='Archive')
old_exps = head.find_next('div')