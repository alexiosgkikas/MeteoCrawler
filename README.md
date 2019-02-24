# MeteoCrawler
## Retrieve Meteorological Data from Meteo Stations in Greece
Using Python 3
### Required Libraries
- Schedule https://pypi.org/project/schedule/
- Beautiful Soup 4 https://pypi.org/project/beautifulsoup4/
- Urllib 3  https://pypi.org/project/urllib3/
- Fake agent https://pypi.org/project/fake-useragent/

### Supports:
- Retrieve list of Meteo stations list, with working status of each.
- Reading csv with urls or user define stations.
- Use proxies retrieve from site: https://www.sslproxies.org/ and set rotation 
- Each station writes in seperate csv ('station_name.csv').
- Support Schedule task. By default is running every 1 hour for crawling and every 12:30 am create back up. Be careful, it runs as 'while True' and not as Service. If you close the running window it would stop and would need re-run, and previous data would not erased.   
- Log file with status of how many stations data, retrieved. 
