# To collect Hong Kong weather data from 'http://www.tianqihoubao.com/weather/top/xianggang.html'
import requests
import re
from bs4 import BeautifulSoup as Soup
from datetime import datetime


# Get the latest weather infomation from the website.
def get_latest_weather():
    html = requests.get('http://www.tianqihoubao.com/weather/top/xianggang.html')
    bs = Soup(html.text, 'lxml')
    # print(bs.prettify())
    latest_list = bs.select('table tr:nth-of-type(3) td')
    date = latest_list[1].get_text()[:10]
    weather = latest_list[2].get_text()
    wind = latest_list[3].get_text()
    high_temp = latest_list[4].get_text()[:2]
    low_temp = re.search(r'\d+', latest_list[7].get_text()).group(0)
    # print(latest_list)
    # Data_Transformation
    if '雨' in weather:
        rainy_or_not = 1
    else:
        rainy_or_not = 0

    if '晴' in weather:
        sunny_or_not = 1
    else:
        sunny_or_not = 0

    weekday_num = datetime(int(date[:4]), int(date[5:7]), int(date[8:])).strftime("%w")
    if weekday_num == 6 or weekday_num == 0:
        weekend_or_not = 1
    else:
        weekend_or_not = 0

    free_or_not = 0       # 默认不完全免费

    part_free_or_not = 1  # 默认不完全免费（直到3月30日）

    print("注意：3月30日前默认不完全免费，之后需要修改代码！")
    print("此外，如果有其他费用减免的活动，则应当手动更改数据表格")

    if '<' in wind:
        breeze_or_not = 1
    else:
        breeze_or_not = 0

    return [date, weekend_or_not, free_or_not, part_free_or_not, high_temp, low_temp, sunny_or_not, rainy_or_not, breeze_or_not]


if __name__ == '__main__':
    print(get_latest_weather())
