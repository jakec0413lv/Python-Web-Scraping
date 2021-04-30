import requests
from bs4 import BeautifulSoup
import pandas

base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s="
l = [] #Initialize List

for page in range(0, 30, 10): #Iterate through multiple pages

    r = requests.get(base_url + str(page), headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div",{"class":"propertyRow"})

    for item in all:
        d={} #Intialize Dictionary

        d["Address"] = item.find_all("span", {"class":"propAddressCollapse"})[0].text
        try:
            d["Locality"] = item.find_all("span", {"class":"propAddressCollapse"})[1].text
        except:
            d["Locality"] = None
        d["Price"] = item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ", "") #Remove blank spaces/ new line characters (.replace())

        try: #Ignore None types
            d["Beds"] = item.find("span",{"class" : "infoBed"}).find("b").text
        except:
            d["Beds"] = None
        try: #Ignore None types
            d["Sq Ft"] = item.find("span",{"class" : "infoSqFt"}).find("b").text
        except:
            d["Sq Ft"] = None
        try: #Ignore None types
            d["Full Baths"] = item.find("span",{"class" : "infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"] = None
        try: #Ignore None types
            d["Half Baths"] = Noneitem.find("span",{"class" : "infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"] = None
        #Extract Elements Without Unique Identifiers

        for column_group in item.find_all("div", {"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),
                                                    column_group.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text
        l.append(d)

#Data Frame Creation
df = pandas.DataFrame(l)
df.to_csv("RealEstateData.csv")