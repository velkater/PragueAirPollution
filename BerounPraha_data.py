
# coding: utf-8

# In[257]:

import urllib.request
from bs4 import BeautifulSoup
import re
import datetime
import time
import itertools


# In[398]:

times = [datetime.time(i, 0) for i in range(9,21)]


# In[ ]:

i = 0
while i < len(times):
    nexttime = times[i]
    if datetime.datetime.now().time() < nexttime:
        time.sleep(10)
    else:
        pollution_check(nexttime)
        i = i + 1            
        #print('\n')


# In[400]:

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
        with open(text[0]+".csv", 'a') as out:
            # Date, Time, Day in week, Place, Index of pollution,
            # SO_2, NO_2, CO, PM_10, O3, PM_2.5
            s = str(datetime.date.today()) + "," +             str(timestamp) + "," +             datetime.date.today().strftime('%A') + "," +              text[1]+             "," + re.findall('\d+', text[4])[0] + "," +             extracted + "\n" 
            out.write(s)
            print(s)


# In[402]:

#pollution_check(datetime.datetime.now().time())


# In[ ]:



