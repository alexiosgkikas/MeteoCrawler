# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 14:45:47 2019

@author: Alexios
"""

from bs4 import BeautifulSoup
import urllib3
import time
import csv
"""    
"""
 
class Station(object):
    
    def __init__(self,name,url,status,davis=False):
        self.name = name
        self.url = url
        self.status = status
        self.davis = davis
    
    def printAll(self):
        print(' Name: ' + self.name +
              ' Url: ' + self.url +
              ' Status: ' + str(self.status) +
              ' Davis: ' + str(self.davis))
"""
    
"""    
class FindMeteoStations:

    url = 'http://www.meteo.gr/Gmap.cfm'
    def findStations(self):
        #create empty list of stations object
        self.stations = []
        http = urllib3.PoolManager(10)
        r = http.request('GET', self.url)
        soup = BeautifulSoup(r.data)
        # Find all options(drop down menu) of stations
        options = soup.findAll('option')
        
        # Create empty dictionary which hold name and url of station
        # iterate options
        for option in options:
            name = option.string    # Name of station as display from dop down Menu
            url = option["value"]   # Url of station  as retrive from dop down Menu
            if 'stations' in url:
                (url,status,davis) =self.checkConnection(url)
                print(url +' , '+str(status) + ' ,'+ str(davis))
                self.stations.append(Station(name,url,status,davis))
                time.sleep(5)
                
        return self.stations

    def checkConnection(self,url):
        http = urllib3.PoolManager()
        # do request        
        print('Try to connect: ' + url)
        request = http.request('GET', url)
        
        if request.status != 200:
            return (request.geturl(),404,False)
        
        soup = BeautifulSoup(request.data)
        img = soup.findAll('img',src=True)
        return (request.geturl(),200,self.checkDavis(img))
        
        

    def checkDavis(self, img, checkImage='Davis'):    
        for im in img:
            if checkImage in im['src']:
                return True
        return False
  
    def createCSV(self,stations):
        fieldnames = ['STATION','URL','STATUS','DAVIS']
        with open('stations_status.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=';')
            filewriter.writerow(fieldnames)
            for station in stations:
                    filewriter.writerow([str(station.name),str(station.url),str(station.status),str(station.davis)])


        
sta = FindMeteoStations()
s=sta.findStations()
sta.createCSV(s)


        
    