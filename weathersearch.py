import requests
import urllib.parse
import inquirer
from pyowm.owm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config

class SearchWeather(object):
    def __init__(self):
        self.api_key = '90e31a8d6a2883ba3c2125d14b248a47'
        self.lang = 'zh_tw'
    
    def main(self):
        search_type = [
                inquirer.List(
                'service',
                message="請選擇查詢方式",
                choices=['目前天氣', '明日天氣', '未來五天天氣'],
            )
        ]
        answers = inquirer.prompt(search_type)
        
        self.search_type = answers['service']
        
        address = str(input("請輸入欲查詢天氣的國家名稱、縣市、地區或地址："))
        
        if len(address) <= 0:
            print("請輸入查詢資料")
            quit
        else:
            self.address = address
       
        position = self.get_latlng(address)
        if len(position[0]['lat']) > 0 and len(position[0]['lon']) > 0:
            self.lat = position[0]['lat']
            self.lon = position[0]['lon']
            self.weather_search()
        else:
            print("查無相關位置資訊")
            quit
        
    
    def get_latlng(self, address):
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        response = requests.get(url).json()
        return response 
    
    def weather_search(self):
        config_dict = get_default_config()
        config_dict['language'] = 'zh_tw'
        owm = OWM(self.api_key, config_dict)
        mgr = owm.weather_manager()
        self.mgr = mgr
        
        if self.search_type == '目前天氣':
            try:
                self.todays_weather()
            except:
                print("目前暫時不提供此查詢服務")
        elif self.search_type == '明日天氣':
            try:
                self.specific_days_weather()
            except:
                print("目前暫時不提供此查詢服務")
        elif self.search_type == '未來五天天氣':
            try:
                self.whole_week_weather()
            except:
                print("目前暫時不提供此查詢服務")
        else:
            print("請選擇查詢條件")
            quit
        
    def todays_weather(self):        
        weather = self.mgr.weather_at_coords(float(self.lat), float(self.lon)).weather 
        print(self.address + "目前的天氣是：" + weather.detailed_status)
        
    def specific_days_weather(self):
        tomorrow = timestamps.tomorrow()
        wheather = self.mgr.forecast_at_coords(float(self.lat), float(self.lon), 'daily').get_weather_at(tomorrow)
        print(self.address + "明天的天氣是：" + wheather)
        
    def whole_week_weather(self):
        daily_data = self.mgr.forecast_at_coords(float(self.lat), float(self.lon), 'daily').forecast
        for weather in daily_data:
            print(self.address + "在" + weather.get_reference_time('iso') + "的天氣是：" + weather.get_status())
        
search = SearchWeather()
search.main()
        