__author__ = 'pranav_tendolkar'
import requests
import json

proxies = {
  "http": "http://9.51.101.143:3128",
  "https": "http://9.51.101.143:3128",
}

def dumpSansad():
    result = []
    for page in range(1, 40):
        r = requests.get("http://sansad.co/api/legislators", params={'page': page},proxies=proxies).json()
        del r['page']
        result += r['results']
    print result
    with open('sansad.json', 'w') as outfile:
        json.dump(result, outfile)

def dumpmplads():
    apikey='c2a43589b26a0bae2585fc1be870d9f035580d91'
    spendingdata=[]
    r=requests.get("http://api.dataweave.in/v1/mplads/listAllStates", params={'api_key': apikey },proxies=proxies).json()
    print r['data']

    for state in r['data']:
        print 'Dumping data for  '+state
        resp=requests.get("http://api.dataweave.in/v1/mplads/listExpensesByState", params={'api_key': apikey,'page': 1,'state':state },proxies=proxies).json()
        spendingdata+=resp['data']
        print 'page 1'+ str(resp)
        for pagenumber in range(2,resp['count']/10+1):
            resp=requests.get("http://api.dataweave.in/v1/mplads/listExpensesByState", params={'api_key': apikey,'page': pagenumber,'state':state },proxies=proxies).json()
            print 'page'+str(pagenumber) +'  '+ str(resp)
            spendingdata+=resp['data']
    with open('spending.json', 'w') as outfile:
        json.dump(spendingdata, outfile)


def mergedata():
    json_data=open('sansad.json')
    sansad= json.load(json_data)
    json_data.close()

    json_data=open('spending.json')
    spending= json.load(json_data)
    json_data.close()

    districts=[]
    constituencies=[]

    for spend in spending:
        end=str(spend['District']).lower().find('(')

        if end != -1:
            dist=str(spend['District']).lower()[:end].strip()
        else:
            dist=str(spend['District']).lower().strip()
        dist=dist.replace('&','and')
        dist=dist.replace('-',' ')
        dist=dist.replace('i','')
        dist=dist.replace('e','')
        dist=dist.replace('a','')
        spend['match']=dist

        districts.append(spend)
    for sans in sansad:
        if sans['house'] == 'Lok Sabha':
            cons=str(sans['constituency']).lower().replace('-', ' ').replace('i','').replace('e','').replace('a','').strip()
            sans['match']=cons
            constituencies.append(sans)

    matched=[]
    all_districts=[]
    for district in districts:
        all_districts.append(district['match'])
        for const in constituencies:
            if district['match'] == const['match']:
                matched.append(merge(district,const))

    print len(matched)
    for i in matched:
        del i['match']

    with open('final.json', 'w') as outfile:
        json.dump(matched, outfile)


def merge(district, const):
    result=const.copy()
    result['Amount_recommended']=district['Amount_recommended']
    result['Amount_sanctioned']=district['Amount_sanctioned']
    result['Released_by_government_of_India']=district['Released_by_government_of_India']
    result['Percent_of_utilisation_over_released']=district['Percent_of_utilisation_over_released']
    result['Units']=district['Units']
    result['Unspent_balance']=district['Unspent_balance']
    result['Amount_available_with_interest']=district['Amount_available_with_interest']
    result['Expenditure_incurred']=district['Expenditure_incurred']
    result['Entitlement_of_Constituency']=district['Entitlement_of_Constituency']
    result['District']=district['District']
    result['State']=district['State']
    return result

#dumpmplads()
#dumpSansad()
mergedata()