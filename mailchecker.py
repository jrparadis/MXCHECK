#checks a domain's mx records to see if it's vulerable to DNS hijacking or configured incorrectly

import subprocess
import time
import sqlite3
import dns.resolver
import re
sql = sqlite3.connect('mailchecker.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS tabley(domain TEXT, originaldomain TEXT)')

#domains to check go here. I recommend https://blog.majestic.com/development/alexa-top-1-million-sites-retired-heres-majestic-million/
listofdomains = '''
'''

#don't ping the mail server if the mail server is one of these domains
ignoredomains = """google.com
gmail.com
googlemail.com
outlook.com
microsoft.com
yahoo.com
hotmail.com
"""



t = 0
info = subprocess.STARTUPINFO()
info.dwFlags = subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = 0
domainnametocheck = listofdomains.split('\n')
for each in domainnametocheck:
    t += 1
    if t == 101:
        print ('100 done')
        t = 0
    try:
        answers = dns.resolver.query(str(each), 'MX')
        for rdata in answers:
            x = rdata.exchange
            b = str(x).split('.')
            domain = str(x)
            c = b[len(b)-3] + '.' + b[len(b)-2]
            if str(c) not in str(ignoredomains):
                pingy = subprocess.Popen('ping ' + str(domain), startupinfo=info, stdout=subprocess.PIPE)
                x2 = pingy.communicate()
                if len(x2[0]) < 300:
                    if each != domain:
                        namesdb = cur.execute("SELECT domain FROM tabley").fetchall()
                        if str(domain) in str(namesdb) or str(each) == str(domain):
                            print (str(t),' | ', str(each), str(domain) + ' in db, skipping')
                        else:
                            cur.execute('INSERT INTO tabley VALUES(?, ?)', [str(domain), str(each)])
                            sql.commit()
                            print (str(t) , ' | added ' + str(domain) + ' | ' + str(each) )
    except Exception as e:
        try:
            print (t, ' | ERROR | ', each, domain, x, ' | error: ', e)
        except:
            print (e)
        pass
