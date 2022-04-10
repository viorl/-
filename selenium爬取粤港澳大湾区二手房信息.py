import time
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.keys import Keys
import csv
import requests

'''广州、深圳、珠海、佛山、惠州、东莞、中山、江门、肇庆、香港、澳门'''
'''楼盘名称、区域、单价、面积、户型、配套资源、发布时间'''

def sele_f():  # selenium反爬
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(options=option)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
               Object.defineProperty(navigator, 'webdriver', {
                 get: () => undefined
               })
             """
    })
    driver.implicitly_wait(10)
    chrome_options = Options()
    chrome_options.add_argument('--proxy-server=127.0.0.1:8080')
    return driver

def py_a(driver): # a网站的爬虫操作
    reall = driver.page_source  # 返回str文本
    titles = re.findall('<a class="".*? data-is_focus="" data-sl="">(.*?)</a>', reall, re.S)  # 楼盘名称
    # print(len(titles))
    addressesl = re.findall('<div class=".*?">.*?data-el="region">(.*?) </a>.*?<a href=".*?" target="_blank">(.*?)</a> </div>', reall,re.S)  # 区域
    addresses = []
    for i in addressesl:
        i = i[0] + '-' + i[1]
        addresses.append(i)
    # print(len(addresses))

    prices = re.findall('<div class="priceInfo">.*?data-price=".*?"><span>(.*?)</span></div></div>', reall,re.S)  # 单价
    # print(len(prices))

    areas = re.findall('<div class="houseInfo"><span class="houseIcon"></span>.*?\| (.*?平米).*?</div>', reall)  # 面积
    # print(len(areas))

    htypes = re.findall('<div class="houseInfo"><span class="houseIcon"></span>(.*?) \| .*?平米.*?</div>',reall)  # 户型
    # print(len(htypes))

    collocations = re.findall(
        '<div class="houseInfo"><span class="houseIcon"></span>.*? \|.*? \|.*? \|(.*?)\|.*? \|.*? \| .*? </div>', reall)  # 配套资源
    # print(len(collocations))

    times = re.findall('<div class="followInfo"><span class="starIcon"></span>.*? / (.*?)</div>', reall,
                       re.S)  # 发布时间
    # print(len(times))

    for title, address, price, area, htype, collocation, timel in zip(titles, addresses, prices, areas, htypes,
                                                                      collocations, times):
        zipl = {
            '楼盘名称': title,
            '区域': address,
            '单价': price,
            '面积': area,
            '户型': htype,
            '配套资源': collocation,
            '发布时间': timel
        }
        print(zipl)
        writer.writerow([title, address, price, area, htype, collocation, timel])
    time.sleep(5)


def py_b(driver,city_names_eng): # b网站的爬虫操作
    reall = driver.page_source  # 返回str文本
    '''楼盘名称、区域、单价、面积、户型、配套资源、发布时间'''
    titles = re.findall('<p class="tit">.*?title=".*?">(.*?)</a>', reall, re.S)  # 楼盘名称
    #print(len(titles))
    # print(titles)

    addressesl = re.findall(
        '<p class="attr">.*?<a href=".*?" title=".*?">(.*?)</a>.*?<a href=".*?" title=".*?">(.*?)</a></span>',
        reall, re.S)  # 区域
    addresses = []
    for i in addressesl:
        i = i[0] + '-' + i[1]
        addresses.append(i)
    # print(len(addresses))

    prices = re.findall('<div class="price">.*?<p class="sub">单价(.*?)</p>', reall, re.S)  # 单价
    # print(len(prices))

    areas = re.findall('<span>建筑面积(.*?)</span><em class="line"></em>', reall)  # 面积
    # print(len(areas))

    htypes = re.findall(
        '<div class="text">.*?<p class="tit">.*?<p class="attr">.*?<span>\n\t\t\t\t\t\t\t\t\t\t\t\t(.*?)\n\t\t\t\t\t\t\t\t\t\t</span><em class="line"></em>.*?<span>.*?</span><em class="line"></em>.*?<span>.*?</span><em class="line"></em>.*?<span>.*?</span>.*?</p>',
        reall, re.S)  # 户型
    #print(len(htypes))

    collocations = re.findall('㎡</span>.*?</p>.*?<p class="attr">.*?<span>(.*?)</span><em class="line">', reall,
                              re.S)  # 配套资源
    collocations = collocations[1:]
    # print(len(collocations))

    timel = re.findall('<div class="text">.*?<p class="tit">.*?<a href="(.*?)" target="_blank"', reall, re.S)
    times = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    for j in timel:
        time.sleep(7)
        try:
            timel2 = 'https://'+city_names_eng+'.leyoujia.com'+ str(j)
            #print(timel2)
            getting = requests.get(timel2, headers)
            a = re.findall('<span class="w2"><em>挂牌时间</em>(.*?)</span>', getting.text, re.S)
            a = a[0]
            times.append(a)  # 发布时间
        except:
            times.append('error')
            time.sleep(5)
    # print(len(times))

    for title, address, price, area, htype, collocation, timel in zip(titles, addresses, prices, areas, htypes,
                                                                      collocations, times):
        zipl = {
            '楼盘名称': title,
            '区域': address,
            '单价': price,
            '面积': area,
            '户型': htype,
            '配套资源': collocation,
            '发布时间': timel
        }
        print(zipl)
        writer.writerow([title, address, price, area, htype, collocation, timel])




def selel_a(city_names):    # a网站的slelnium操作
    # 可以使用搜索框选择城市
    '''1,打开网页 2，逐个输入城市名 逐次 调用爬虫'''

    driver = sele_f() # 反爬

    # 请求页面
    url = 'https://www.lianjia.com/city/' # 链家初始页
    driver.get(url)
    for city_name in city_names: # 城市（页数（爬虫））
        '''selenium 操作'''
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/input').send_keys(city_name) # 输入城市名
        WebDriverWait(driver,3)
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/a').click() # 搜索
        WebDriverWait(driver,5)
        time.sleep(2)
        handles = driver.window_handles # 获取所有页面句柄
        driver.switch_to.window(handles[1]) # 切换爬虫窗口
        driver.find_element_by_xpath('//*[@id="findHouse"]').click()
        print('正在抓取 *',city_name,'* 二手房信息')
        for j in range(1,20):
            WebDriverWait(driver,3)
            time.sleep(3)
            print('正在爬取第 ',j,' 页')
            py_a(driver)  # 爬虫操作
            if j==1:
                driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[7]/div[2]/div/a[5]').send_keys(Keys.ENTER) # 相对链接，添加send_keys操作 绝对链接即可用click
            elif j==2:
                driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[7]/div[2]/div/a[7]').send_keys(Keys.ENTER) # 相对链接，添加send_keys操作 绝对链接即可用click
            elif j==3:
                driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[7]/div[2]/div/a[8]').send_keys(Keys.ENTER) # 相对链接，添加send_keys操作 绝对链接即可用click
            else:
                driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[7]/div[2]/div/a[9]').send_keys(Keys.ENTER) # 相对链接，添加send_keys操作 绝对链接即可用click

            # 1 //*[@id="content"]/div[1]/div[7]/div[2]/div/a[5]
            #  2 //*[@id="content"]/div[1]/div[7]/div[2]/div/a[7]
            # 3 //*[@id="content"]/div[1]/div[7]/div[2]/div/a[8]
            # 4 //*[@id="content"]/div[1]/div[7]/div[2]/div/a[9]
            # 5 //*[@id="content"]/div[1]/div[7]/div[2]/div/a[9]

            #driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[8]/div[2]/div/a[5]').click() # 点击下一页 # 点击不了?
        print(city_name,'已爬取完毕')
        driver.close()
        driver.switch_to.window(handles[0]) # 切换原始窗口
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/input').clear()  # 清除搜索框

        time.sleep(3)

def selel_b(city_names):      # b网站的slelnium操作
    # 可以使用搜索框选择城市
    '''1,打开网页 2，逐个输入城市名 逐次 调用爬虫'''

    driver = sele_f()  # 反爬
    city_names_eng = ['guangzhou', 'shenzhen', 'zhuhai', 'foshan', 'huizhou', 'dongguan', 'zhongshan', 'jiangmen', 'zhaoqing', 'xianggang', 'aomen']
    # 请求页面
    url = 'https://guangzhou.leyoujia.com/esf/'  # 初始页
    driver.get(url)
    en = 0
    for city_name in city_names:  # 城市（页数（爬虫））
        '''selenium 操作'''

        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/span[2]/a').click()  # 打开滑窗
        time.sleep(5)
        try:
            driver.find_element_by_xpath('//*[@id="boundCity"]/div[2]/div[1]/input').send_keys(city_name) # 输入城市名
            WebDriverWait(3,driver)
            driver.find_element_by_xpath('//*[@id="city-result"]/li/a').click() # 选择城市
            time.sleep(3)
            try:
                driver.find_element_by_xpath('//*[@id="expertDialog"]/div/div/div[2]/a').click() # 广告页关闭
            except:
                pass
            driver.find_element_by_xpath('//*[@id="common-search"]/button').click() # 搜索按钮
            WebDriverWait(3,driver)
            print('正在抓取 *', city_name, '* 二手房信息')
            for j in range(1, 20):
                WebDriverWait(driver, 3)
                time.sleep(7)
                print('正在爬取第 ', j, ' 页')
                py_b(driver,city_names_eng[en])  # 爬虫操作
                WebDriverWait(2,driver)
                if j==1:
                    driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[5]/div/div[2]/a[10]').send_keys(Keys.ENTER)
                elif j>=2:
                    driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[5]/div/div[2]/a[12]').send_keys(Keys.ENTER)
                # driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[8]/div[2]/div/a[5]').click() # 点击下一页 # 点击不了?
            print(city_name, '已爬取完毕')
            en +=1
            time.sleep(3)
        except:
            print('无',city_name,'二手房')
            pass






def urll(): # 所有爬虫网站入口
    city_names = ['广州','深圳','珠海','佛山','惠州','东莞','中山','江门','肇庆','香港','澳门']

    print('正在爬取lianjia.com。。。')
    selel_a(city_names)

    print('正在爬取leyoujia.com。。。')
    selel_b(city_names)




if __name__ == '__main__':
    fp = open('./lou.csv', 'w+', newline='', encoding='utf-8-sig')  # 写入csv
    writer = csv.writer(fp)
    writer.writerow(['楼盘名称', '区域', '单价', '面积', '户型', '配套资源', '发布时间'])
    urll() # 爬虫入口
    fp.close()






