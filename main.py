# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 18:01:51 2019

@author: Alexios
"""
import crawl_Station as cS
import time
from datetime import datetime
import os
import sys
import schedule 

import Proxies as prox

class Crawling:
    # list of weather stations
    stations_url = ['http://penteli.meteo.gr/stations/paramythia/',
                    'http://penteli.meteo.gr/stations/preveza/',
                    'http://penteli.meteo.gr/stations/upatras/',
                    'http://penteli.meteo.gr/stations/isthmos/',
                    'http://penteli.meteo.gr/stations/pireas/',
                    'http://penteli.meteo.gr/stations/heraclionport/',
                    'http://penteli.meteo.gr/stations/alexandroupolis/',
                    'http://penteli.meteo.gr/stations/thessaloniki/',
                    ]
    # list of headers stations
    headnames = ['TimeCrawled','Date','TimeDavis','Temperature','Humidity','Dewpoint','Wind','Barometer',"Today's Rain",
            'Rain Rate','Storm Total','Monthly Rain','Yearly Rain','Wind Chill',
            'THW Index','Heat Index']
    
    """
        Constructor 
    """    
    def __init__(self,folder,interval,num_prox = 3):
        self.folder=folder
        self.interval=interval
        self.num_prox = num_prox
        if not os.path.exists(self.folder):
            print('Folder '+self.folder+' does not exist, creating now.')
            os.makedirs(self.folder)
    
    def setStations(self,stations):
        self.stations_url = []
        self.stations_url=stations
    
    """
        Function LOAD STATIONS from file
    """
    def load_stations(self,filename,davis=True):
        stations = []
        import csv
        with open(filename, newline='') as csvfile:
            input_file = csv.DictReader(csvfile, delimiter=';', quotechar='|')
            for row in input_file:
                if row['DAVIS'] == 'True':
                    print(row['URL'])
                    stations.append(row['URL'])
        return stations

    def load_stations_v2(self, filename):
        stations = []
        import csv
        with open(filename, newline='') as csvfile:
            input_file = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in input_file:
                #print(row[1])
                stations.append(row[1])
        return stations
	
    """
        Function append file
    """
    def writeLogFile(self, date,count):
        filename = 'logs.txt'
        
        if not os.path.isfile(filename):
               file = open(filename, 'w')
               file.close()
               
        with open(filename, "a") as myfile:
            myfile.write('Crawling date: '+ date +' . Stations good: '+ str(count) + '/'+ str(len(self.stations_url))+'\n')
        
    """
        Function Create SCV File with Headers
    """
    def createCSV(self,name):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        import csv
        name = name.replace('-','_')
        filename = self.folder+'/'+name+'.csv'
        if os.path.exists(filename):
            print('File '+filename+ ' exist')
            return 
        try:
            with open(filename, 'w', newline='') as csvfile:
                print('Creating '+filename)
                wr = csv.DictWriter(csvfile,delimiter=';',fieldnames = self.headnames,quoting=csv.QUOTE_NONE)
                wr.writeheader()
        except Exception as e:
            import warnings
            warnings.warn('Error Creating File: '+filename +'\n Exception raised traceback :\n'+str(e),Warning)
    
    """
        Function Append CSV File with Data
    """    
    def writeCSV(self,name,data): 
        import csv
        name = name.replace('-','_')
        filename = self.folder+'/'+name+'.csv'
        try:
            with open(filename,'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile,delimiter=';', fieldnames=self.headnames)
                writer.writerow(data)
        except Exception as e:
            import warnings
            warnings.warn('Error appending File: '+filename +'\n Exception raised traceback :\n'+str(e),Warning)
    

    def createBackup(self):
        now = datetime.now()
        timestamp = now.strftime("%H-%M %d-%m-%Y")
        try:
            print('Creating back up')
            folder_backup=self.folder+'_backup/'
            if not os.path.exists(folder_backup):
                os.makedirs(folder_backup)
            
            #create back up
            back_up_file_name= folder_backup +str('backup '+timestamp)
            import tarfile
            with tarfile.open(back_up_file_name + '.tar.gz', mode='w:gz') as archive:
                archive.add(self.folder, recursive=True)
            
            print('Back up created in folder '+folder_backup+' with name '+str('backup '+timestamp))
        except Exception as e:
            import warnings
            warnings.warn('Error creating zip cack up File: '+back_up_file_name +'\n Exception raised traceback :\n'+str(e),Warning)
    
        
    
    """
    
    """
    def crawl_job(self):
        count =0;
        now = datetime.now()
        current_time = now.strftime("%H:%M %d-%m-%Y")
        print('\n====== Starting Crawling at : '+ str(current_time)+' ==============================\n')
            
        count_prox = 1
        
        if  self.num_prox >0:
            proxy = prox.Proxies(number_of_proxies=1).getProxiesAllInOne()[0]
            
        for url in self.stations_url:
            # Get name 
            name =  url.split('stations')[-1].replace('/','')
            # Get Proxy { ip: xxxx , port: xxxxx}
            if self.num_prox >0 and count_prox % self.num_prox == 0:
                print("Searching for new proxy")
                proxy = prox.Proxies(number_of_proxies=1).getProxiesAllInOne()[0]
            
            count_prox+=1    
            # create Instance for crawl
            cs = cS.Crawl_Station(url,proxy=proxy)
            # Get Data
            data=cs.getInfo()
            if len(data) >= 6:
                count+=1
            #print(data)
            data['TimeCrawled'] = now.strftime("%H:%M")
            self.writeCSV(name,data)
            #time.sleep(5)
                
        now = datetime.now()
        current_time = now.strftime("%H:%M %d-%m-%Y")
        print('\n====== Crawling Ended at '+ current_time +' ==============================\n')    
        self.writeLogFile(current_time,count)
        #self.createBackup()
        
        
    def sched_local(self):
        schedule.every(1).hour.at(self.interval).do(self.crawl_job)
        #schedule.every(30).minutes.do(self.crawl_job)
        schedule.every().day.at("00:30").do(self.createBackup)
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    

if __name__ == "__main__":
    
    #FOLDER = '/home/islab/weatherdata'
    FOLDER = 'RetrievedData'  # Folder to store csv files
    INTERVAL = ':52'          # Every Hour at xx:01 start crawling 
    STATIONS = 'stations_selection.csv' #CSV with stations url
    CHANGE_PROXY = 3;         # Number of crawled stations until rotate proxy. Set by default to 3
    #Create object of crawl
    c = Crawling(FOLDER,INTERVAL,CHANGE_PROXY)
    # Load stations url from csv with davis stations
    #stations = c.load_stations(STATIONS) #Read Stations with dictionary header
    stations = c.load_stations_v2(STATIONS)#Read stations without headers
    #print('Number of loaded stations: '+str(len(stations))
    # Set stations to crawler
    c.setStations(stations)
    print('Starting script with parameters: '+'\n Folder: '+FOLDER+'\n INTERVAL: every hour at .'+INTERVAL+'\n')
    
    # Create csv for each station
    for s in c.stations_url:
        name = s.split('stations')[-1].replace('/','')
        c.createCSV(name) 
        
    # Start schedule
    c.sched_local()
