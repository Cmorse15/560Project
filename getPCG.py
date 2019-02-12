import requests
import json
import pandas as pd
from lxml import html

'''
this can be made better easily so that column headers are integers
make it to_excel not to csv maybe?
'''

def getAllOrganizationNames():
    url = "https://www.pickclickgive.org/index.cfm/pfdorgs.orgs?"
    organizationNames = []
    for letter in ['3', '4', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Y']:
        #for startrow in []
        params = {'letter':letter}
        resp = requests.get(url, params)
        htmlString = html.fromstring(resp.content)
        data = htmlString.xpath('//tr[td[@class="fineprint"]]/td[2]/strong/a/text()')
        organizationNames.extend(data)
    #the above loop misses some when letter=A because there are 50 of 162 results shown at a time
    #below takes care of the rest
    for startrow in [51, 101, 151]: #pages 2, 3, 4 of the orgs that start with 'A'
        resp = requests.post('https://www.pickclickgive.org/index.cfm/pfdorgs.orgs/', data = {'startrow' : startrow, 'letter' : 'A'})
        htmlString = html.fromstring(resp.content)
        data = htmlString.xpath('//tr[td[@class="fineprint"]]/td[2]/strong/a/text()')
        organizationNames.extend(data)
    #organizationNames now contains all of the names
    return organizationNames

def getDonorData(name):
    url = 'https://www.pickclickgive.org/index.cfm/pfdorgs.info/' + name.replace(" ", "-")
    resp = requests.get(url)
    htmlString = html.fromstring(resp.content)
    data = htmlString.xpath('//div[h4[text() = "Past Contributions"]]//text()')
    data = data[2:] #remove the first three things from list they are formatting
    del data[::3] #remove more formatting
    return data #in form ["2010", ' $1300']



def getOrganizationData(nameList):
    df = pd.DataFrame(columns=['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', 'Total'], index = nameList)#.fillna(0)
    for org in nameList:
        donorData = getDonorData(org)
        for i in range(0, len(donorData), 2):
            df.at[org, donorData[i].replace(":","")] = float(donorData[i+1].replace(",","").replace(" ","").replace("$",""))
    return df


def main():
    nameList = getAllOrganizationNames()
    df = getOrganizationData(nameList)
    newFile = open('PCG_Donor_Data.csv', "w+")
    newFile.write(df.to_csv())



if __name__ == "__main__":
    main()



'''
url = 'https://www.pickclickgive.org/index.cfm/pfdorgs.info/Arctic-Education-Foundation'
url2 = 'https://www.pickclickgive.org/index.cfm/pfdorgs.info/' + 'Arctic-Education-Foundation'
resp = requests.get(url2)
htmlString = html.fromstring(resp.content)
data = htmlString.xpath('//div[h4[text() = "Past Contributions"]]//text()')
data = data[2:] #remove the first three things from list they are formatting
del data[::3] #remove more formatting
print(data)
getDonorData('Arctic-Education-Foundation')
'''


'''
df = pd.DataFrame(columns=['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', 'Total'])
df = df.append(pd.DataFrame(index = ['yee']), sort=True)
df.at['yee','2009'] = 100
print(df)
'''
