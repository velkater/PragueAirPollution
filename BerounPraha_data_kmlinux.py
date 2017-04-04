
# coding: utf-8

# In[1]:

import urllib.request
from bs4 import BeautifulSoup
import re
import datetime
import time
import itertools


# In[2]:

def pollution_check(timestamp):
    url = 'http://portal.chmi.cz/files/portal/docs/uoco/web_generator/actual_hour_data_CZ.html'
    with urllib.request.urlopen(url) as response:
        s = response.read()

    soup = BeautifulSoup(s, 'html.parser')
    measurements_all = soup.find_all('tr', 'list-row-odd')[:15]

    for i in [0,1,2,3,8,14]:
        measurement = measurements_all[i]
        values = measurement.find_all('td')[-8:]
        extracted = [m.string.replace(",", ".") if m.string != None else 'None' for m in values]
        extracted = extracted[0:5] + extracted[-1:]
        extracted = ','.join(extracted)
        text = list(measurement.stripped_strings)
        print(text)
        today = datetime.date.today()
        filename = text[0]+ today.strftime('%Y'+'%m') +".csv"
        with open(filename, 'a') as out:
            # Date, Time, Day in week, Place, Index of pollution,
            # SO_2, NO_2, CO, PM_10, O3, PM_2.5
            s = str(datetime.date.today()) + "," +             str(timestamp) + "," +             today.strftime('%A') + "," +              text[1]+             "," + re.findall('\d+', text[4])[0] + "," +             extracted + "\n" 
            out.write(s)
            print(s)


# In[3]:

#times = [datetime.time(i, 0) for i in range(0,24)]
times = [datetime.time(16, 10),datetime.time(16, 20),datetime.time(16, 30)]


# In[16]:

i = 0
l = len(times)
while datetime.date.today() < datetime.date(2017, 6, 30):
    nexttime = times[i]
    if datetime.datetime.now().time() < nexttime:
        time.sleep(10)
    else:
        pollution_check(nexttime)
        i = i + 1
        if i >= l:
            i = 0
        #print('\n')

