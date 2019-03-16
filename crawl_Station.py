# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 11:44:28 2019

@author: Alexios
"""
from bs4 import BeautifulSoup
import urllib3
import re


class Crawl_Station():
    
    # List with infromation to store
    hold = ['Temperature','Humidity','Dewpoint','Wind','Barometer',"Today's Rain",'Rain Rate','Storm Total','Monthly Rain','Yearly Rain','Wind Chill','THW Index','Heat Index']
    date_format= '.{1,2}:.{2}., ././.{2}'

    """
        Constructor 
        Parameters: 
            url: string of url station to be crawled
            hold: array of fields we need to keep
    """
    def __init__(self, url, hold=None):
        self.URL=url
        if hold is not None:
            self.hold=hold
    
    """
        Function which get a string contains time and date, split them 
        with regex and return them. 
    """
    def __getTimeDate(self,date):
        date=date.replace(',','')
        time  = re.split('(\d{1,2}:\d{2})', date)
        t = time[1].strip() #time 
        d = time[2].strip() #date
        return (t,d)
    
    """
        Function which do request , finds the fields we want adn return them 
        as dictionary            
    """
    def getInfo(self):
        info={}
        # craete http 
        http = urllib3.PoolManager()
        # do request
        try:
            request = http.request('GET', self.URL)
            #print(request.geturl())
            assert request.status == 200
            print('Connection estabilshed in station : ' + self.URL)
        except:
            import warnings
            warnings.warn('Connection couldnt estabilshed in station: '+self.URL,Warning)
            return {}
        
        try:
            soup = BeautifulSoup(request.data) # 'lxml' ,'html.parser'
            #soup = BeautifulSoup(request.data.decode('utf-8','ignore'))
            # Find time and date from 
            
            #get time for old format site
            date = soup.find('strong',style="font-weight: 400")
            #if failed then is using the new format
            if date == None:
                #date = list(soup.find('div',{'class':"headline gradient"}).stripped_strings)[1]
                date = soup.find('div',{'class':"headline gradient"})
                date = list(date.stripped_strings)[1]
            else:
                date = date.text
            
            try:
                time,date = self.__getTimeDate(date)
                info['Date'] = date
                info['TimeDavis'] = time
                #print(info)
            except :
                import warnings
                warnings.warn('Error Reading station Date and Time. Setting Current date and time',Warning)
                from datetime import datetime
                info['Date'] = datetime.now().strftime("%d/%m/%Y")
                info['TimeDavis'] = datetime.now().strftime("%H:%M")
            
            #check format of site .
            format_new =   soup.find('div',{'class':"headline gradient"})
            
            if format_new:
                print('site use new format')
                results = soup.find_all('div',{'class':"line"})
                return self.new_format(info,results)
            else:
                print('site use old format')
                results = soup.find_all('tr')
                return self.old_format(info,results)
            
            return info
        
        except  Exception as e:
            import warnings
            warnings.warn('Error Reading data from station: '+str(self.URL)+'\nMessage error: \n'+str(e),Warning)
            return {};

    """
        old format site
    """
    def old_format(self,info,results):
        # Find all rows from table in site
        #for every row
        for row in results :
            strong = row.find_all('td') # get strong tags 'font',{'color':"Brown"}
            # if size is 2 , means that row contains name and value
            if len(strong) == 2:
                var= list(strong[0].stripped_strings)
                if var: 
                    var =var[0]
                if var and str(var) in self.hold:
                    #print(strong[1])
                    value=strong[1].find('font')
                    value= list(value.stripped_strings)
                    value = ' '.join(value)
                    #print(str(var) +" : " +value)
                    info[str(var)]=value
        
        return(info)    

    """
        new format site
    """
    def new_format(self,info,results):
        # Find all rows from table in site
        #for every row
        
        for row in results :
            divName = row.find('div',{'class':"lleft"})
            if divName:
                divName = list(divName.stripped_strings)[0]
            # if size is 2 , means that row contains name and value
            if divName!= None and divName in self.hold:
                divValue = row.find('div',{'class':"lright"}).text
                info[divName]=divValue
        
        return(info)        

#href="http://penteli.meteo.gr/stations/thessaloniki/"
#href="http://penteli.meteo.gr/stations/upatras/"
#url = 'http://www.meteo.gr/stations/sfakia'
#c = Crawl_Station(href)
#print(c.getInfo())