# To collect Hong Kong weather data from 'http://www.tianqihoubao.com/weather/top/xianggang.html'
import requests
import re
from bs4 import BeautifulSoup as Soup
import datetime
# import csv 不需要这个了，直接在调用的时候再写入就好了~


# Get the latest weather information from the website.
def get_latest_weather(month_num, date_num):
    html = requests.get('http://www.tianqihoubao.com/lishi/xianggang/month/2018{0}.html'.format(month_num))
    bs = Soup(html.text, 'lxml')
    # print(bs.prettify())
    if month_num == '01':  # 这是网页的错误，有两个1月1日
        latest_list = bs.select('table tr:nth-of-type({0}) td'.format(int(date_num) + 2))
    else:
        latest_list = bs.select('table tr:nth-of-type({0}) td'.format(int(date_num) + 1))

    # Data_Collection
    date = latest_list[0].get_text().strip()
    date = date[:4] + '-' + date[5:7] + '-' + date[8:10]
    print('Got the weather of {0} Successfully. Yep! '.format(date))
    weather = latest_list[1].get_text()
    temp = latest_list[2].get_text()
    wind = latest_list[3].get_text().strip().replace(' ', '')

    [high_temp, low_temp] = re.findall(r'\d+', temp)

    # Data_Transformation
    if '雨' in weather:
        rainy_or_not = 1
    else:
        rainy_or_not = 0

    if '晴' in weather:
        sunny_or_not = 1
    else:
        sunny_or_not = 0

    weekday_num = int(datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:10])).strftime("%w"))
    # print(weekday_num)
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

    return [int(date[:4] + date[5:7] + date[8:10]), weekend_or_not, free_or_not, part_free_or_not, high_temp, low_temp, sunny_or_not, rainy_or_not, breeze_or_not]


if __name__ == '__main__':
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    month_of_yesterday = yesterday.strftime('%m')
    date_of_yesterday = yesterday.strftime('%d')
    print(get_latest_weather(month_of_yesterday, date_of_yesterday))
