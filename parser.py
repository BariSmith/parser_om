
import csv
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import time
import lxml

from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import io
import urllib3
import urllib.request
import re
import pandas as pd
start_time = time.time()

headers = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
}



def get_source_html(url):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    driver = webdriver.Chrome(
        executable_path='/home/vadym_a/Documents/chromedriver')
    # driver.maximize_window()
    driver.minimize_window()

    try:
        driver.get(url=url)
        time.sleep(1)
        driver.find_element(by=By.CLASS_NAME, value="pagination")
        with open('source_page.html', 'w') as file:
            file.write(driver.page_source)              
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def get_items_urls(file_path):
    with open(file_path) as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    items_divs = soup.find_all('div', class_ = 'product-inner')

    urls = []
    for item in items_divs:
        items_url = item.find('div', class_='cap-wrap').find('div', class_='caption').find('div', class_='h4').find('a').get('href')
        urls.append(items_url)
   
        
    

    with open('items_url.txt', 'a') as file:
        for url in urls:
            file.write(f'https://it-blok.com.ua/{url}\n')
            
            lines = open('items_url.txt', 'r').readlines()
            lines_set = set(lines)
            
            out  = open('items_url.txt', 'w')
            
            for line in lines_set:
                out.write(line)
        
           
        return '[INFO] Urls collected successfully!'


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]
        time.sleep(1)
        
    
    result_data = []
    for url in urls_list:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        time.sleep(1)


        try:
            item_name = soup.find('div', class_='pp-all-inf').find('div', class_='pp-m-blok').find('h1').text.strip()
            # print(item_name)
        except Exception as _ex:
            item_name = None
        
        try:
            item_price = soup.find('span', class_='autocalc-product-special').text.strip()
            # print(item_price)
        except Exception as _ex:
            item_price = None
            
        try:
            item_reviews = soup.find('ul', class_='nav nav-tabs').find('a', {'href' : "#tab-review"}).text.strip()
            # print(item_reviews)
        except Exception as _ex:
            item_reviews = None

       
        # try:
        #     item_image_link = soup.find_all('img')
        #     # for item in item_image_link:
        #     #     print(item['data-lazy'])
            
        #     print(item_image_link)
        # except Exception as _ex:
        #     item_image_link = None
        #     print('[INFO] Without Image')

        try:
            item_videocard = soup.find(text='Видеокарта').findNext().text.strip()
            # print(item_videocard)
        except Exception as _ex:
            item_videocard = None

        try:
            item_memory_of_videocard = soup.find(text='Объем видеопамяти').findNext().text.strip()
            # print(item_memory_of_videocard)
        except Exception as _ex:
            item_memory_of_videocard = None
        
        try:
            item_cpu = soup.find(text='Процессор').findNext().text.strip()
            # print(item_cpu)
        except Exception as _ex:
            item_cpu = None
        
        try:
            item_cores_of_cpu = soup.find(text='Количество ядер').findNext().text.strip()
            # print(item_cores_of_cpu)
        except Exception as _ex:
            item_cores_of_cpu = None

        try:
            item_ram = soup.find(text='Объем памяти ОЗУ').findNext().text.strip()
            # print(item_ram)
        except Exception as _ex:
            item_ram = None
        
        try:
            item_ssd = soup.find(text='Диск SSD').findNext().text.strip()
            # print(item_ssd)
        except Exception as _ex:
            item_ssd = ' - '

        try:
            item_hdd = soup.find(text='Объем HDD').findNext().text.strip()
            # print(item_hdd)
        except Exception as _ex:
            item_hdd = ' - '

        try:
            item_motherboard = soup.find(text='На чипсете').findNext().text.strip()
            # print(item_motherboard)
        except Exception as _ex:
            item_motherboard = None

        result_data.append({
            'Name': item_name,
            'Price': item_price,
            'Reviews': item_reviews,
            'Videocard': item_videocard,
            'Memory of videocard': item_memory_of_videocard,
            'CPU' : item_cpu,
            'Cores of CPU': item_cores_of_cpu,
            'RAM': item_ram,
            'SSD': item_ssd,
            'HDD': item_hdd,
            'Motherboard': item_motherboard
            })
    
        df = pd.DataFrame(result_data)

        df.to_csv('final_data.csv')
            
            
            


def main():
    '''Tут вказано 15 сторінок так 
     як це номіналька кількість сторінок
      на зараз зчитати цю кількість не має можливості '''
    
    for p in range(1, 4):
        url = f'https://it-blok.com.ua/computeri.html?page={p}'
        get_source_html(url)
        get_items_urls(file_path='/home/vadym_a/Documents/source_page.html')
    time.sleep(2)
    try:
        get_data(file_path='/home/vadym_a/Documents/items_url.txt')
    except Exception as _ex:
        print(f'Invalid URL')
        
    finish_time = time.time() - start_time
    
    print(f'Time wait: {finish_time}')


if __name__ == '__main__':
    main()