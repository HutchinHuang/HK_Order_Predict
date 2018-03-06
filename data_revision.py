# To regain data from Internet in case the data set got lost accidentallty.
# To collect Hong Kong weather data from 'http://www.tianqihoubao.com/weather/top/xianggang.html'
import requests
import re
from bs4 import BeautifulSoup as Soup
import datetime
import csv


# Get certain-date weather infomation from the website.
def collect_certain_weather(year_num, month_num, date_num):
    html = requests.get('http://www.tianqihoubao.com/lishi/xianggang/month/{0}{1}.html'.format(year_num, month_num))
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
    # 得到起止日期间的所有日期。
    start = '2017-12-09'
    end = input('请输入昨天的日期，例如2018-03-04：\n')

    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')

    datelist = [datestart.strftime('%Y-%m-%d')]
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        datelist.append(datestart.strftime('%Y-%m-%d'))

    print(datelist)

    with open('HK_dataset.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['date', 'weekend_or_not', 'free_or_not', 'part_free_or_not', 'high_temp', 'low_temp', 'sunny_or_not', 'rainy_or_not', 'breeze_or_not'])
        for one_date in datelist:
            spamwriter.writerow(collect_certain_weather(one_date[:4], one_date[5:7], one_date[8:]))
