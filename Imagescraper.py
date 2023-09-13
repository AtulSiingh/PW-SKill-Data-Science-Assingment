from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
driver = webdriver.Chrome()


from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
def get_absolute_date(relative_time):
    absolute_time = []
    for i in relative_time:        
        if i.find('hours')>0:
            hours = int(i.split(" ")[0])
            tm_absolute = datetime.now() - pd.Timedelta(hours=hours)
            dt_string = tm_absolute.strftime("%d %b %Y")
            absolute_time.append(dt_string)
        elif i.find('day')>0:
            days = int(i.split(" ")[0])
            tm_absolute = datetime.now() - pd.Timedelta(days=days)
            dt_string = tm_absolute.strftime("%d %b %Y")
            absolute_time.append(dt_string)
        elif i.find('week')>0:
            weeks = int(i.split(" ")[0])
            tm_absolute = datetime.now() - pd.Timedelta(weeks=weeks)
            dt_string = tm_absolute.strftime("%d %b %Y")
            absolute_time.append(dt_string)
        elif i.find('month')>0:
            months = int(i.split(" ")[0])
            tm_absolute = datetime.now() - relativedelta(months=months)
            dt_string = tm_absolute.strftime("%d %b %Y")
            absolute_time.append(dt_string)
        elif i.find('year')>0:
            years = int(i.split(" ")[0])
            tm_absolute = datetime.now() - relativedelta(years=years)
            dt_string = tm_absolute.strftime("%d %b %Y")
            absolute_time.append(dt_string)

    return absolute_time

import pandas as pd
import time
def get_yt_data(url):
    driver.get(url)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 200)")    
    
    # First Get Titles and URL    
    url_elems = driver.find_elements(By.XPATH,"//a[@id='video-title-link']")
    url_elems5 = url_elems[0:5] 
    top5titles = []
    top5urls = []
    for i in url_elems5:
        top5titles.append(i.get_attribute('title'))
        top5urls.append(i.get_attribute('href'))

    # Get Thumbnail URL's
    images = driver.find_elements(By.TAG_NAME,'img')
    img_links = []    
    for i in images:    
        link = i.get_attribute('src')
        if str(link).find('i.ytimg.com')>0:
            img_links.append(link)
    top5thumbnails = img_links[0:5]

    # Get Views and Relative time
    views_elements = driver.find_elements(By.XPATH,"//span[@class='inline-metadata-item style-scope ytd-video-meta-block']")
    view_count = []
    rel_time = []
    for i in views_elements:  
        meta_string = i.text      
        if meta_string.find('views')>0:      
            view_count.append(meta_string)
        elif meta_string.find('ago')>0:
            rel_time.append(meta_string)
    
    top5views = view_count[0:5]
    top5_reltime = rel_time[0:5]

    # converting relative time to absolute dates with custom function get_absolute_date
    try:
        abs_date =get_absolute_date(top5_reltime)
    except Exception as e:
        print('Exception Occured and handled :',e)    
    
    # Creating a Final dictionary for converting to dataframe
    yt_dict = {'title':top5titles,'uploadDate':abs_date,'views':top5views,'videoURL':top5urls,'thumbnailURL':top5thumbnails}

    # Converting to dataframe
    yt_df = pd.DataFrame(yt_dict)

    return yt_df   
    
url = "https://www.youtube.com/@PW-Foundation/videos"
PW_df = get_yt_data(url)
print(PW_df)


