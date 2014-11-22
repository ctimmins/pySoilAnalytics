import requests
from dateutil.parser import parse
from datetime import *
from pymongo import MongoClient

APIKey = "2e221f44-fa2c-4daa-869c-8e87caa72072"
stationList = ""

client = MongoClient('mongodb://localhost')
db = client.root

startDate = str(date.today() - timedelta(days=1))

endDate = str(date.today())

cursor = db.CIMIS_Station_List.find()
for result_object in cursor:
    for station in result_object['Stations']:
        URL = "http://et.water.ca.gov/api/data?appKey="+APIKey+"&targets="+station['Number']+"&startDate="+startDate+"&endDate="+endDate+"&dataItems=hly-air-tmp,hly-dew-pnt,hly-eto,hly-net-rad,hly-asce-eto,hly-precip,hly-rel-hum,hly-res-wind,hly-soil-tmp,hly-sol-rad,hly-vap-pres,hly-wind-dir,hly-wind-spd";
        
        r=requests.get(URL,headers={"Accept-Header":"application/json"})
        
        response = r.json()
        
        try:
            for record in response["Data"]["Providers"][0]["Records"]:
            
                point = {}
            
                if(record['HlyAirTmp']['Value'] is not None and record['HlyAirTmp']['Value'] != ""):
                    time = str(int(record["Hour"])/100)
                    
                    if(time == "24"):
                        record["Date"] = datetime.strptime(record["Date"], "%Y-%m-%d")
                        record["Date"] = record["Date"] + timedelta(days=1)
                        record["Date"] = record["Date"].strftime("%Y-%m-%d")
                        time = "00"
                        
                    time = record["Date"]+" "+time+":00:00"
                    time = parse(time)
                    
                    point = {"Time":time,"Station":station['Number'],"HlyAirTmp":record["HlyAirTmp"]["Value"],"HlyDewPnt":record["HlyDewPnt"]["Value"],"HlyEto":record["HlyEto"]["Value"],"HlyPrecip":record["HlyPrecip"]["Value"],"HlyRelHum":record["HlyRelHum"]["Value"],"HlySoilTmp":record["HlySoilTmp"]["Value"],"HlySolRad":record["HlySolRad"]["Value"],"HlyVapPres":record["HlyVapPres"]["Value"],"HlyWindDir":record["HlyWindDir"]["Value"],"HlyWindSpd":record["HlyWindSpd"]["Value"]}
                    
                    
                    db.CIMIS_Data_Cache.update({"Time":time,"Station":station},point,True)
                    #print point 
                    point = {}
        except:
            print "Error with station " + str(station['Number'])