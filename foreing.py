from bs4 import BeautifulSoup
from splitter import cutter
import requests


def get_weather(req_type: str, airport: str) -> str:
	# https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=KDEN&hoursBeforeNow=1
    url = f'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource={req_type}s&requestType=retrieve&format=xml&stationString={airport}&hoursBeforeNow=1'
    xml = requests.get(url)
    soup = BeautifulSoup(xml.content, 'lxml')
	# print(soup)
    try:
        results = int(soup.data['num_results'])
        answer = soup.find('raw_text').text if results > 0 else 'not in database'
        weather_text = ''
        if len(answer) >= 2000:
            splitted_answer = cutter(answer)
            for answers in splitted_answer:
                weather_text += answers
        else:
            weather_text = answer
        return weather_text
    except Exception:
        return 'not in database'


if __name__ == '__main__':
	get_weather()
