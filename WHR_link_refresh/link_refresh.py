#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import json
import time
import random
from IPython.display import clear_output
from IPython.core.display import display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import subprocess
from selenium.common.exceptions import NoSuchElementException


# In[2]:


with open("info.json", "r") as file:
    info = json.loads(file.read())

video_link_supply_url = info["link_url"]
iOS_file_path = "upload_data/promotion/AppStore/config.json"
GP_file_path = "upload_data/promotion/GooglePlay/config.json"
config_paths = [iOS_file_path, GP_file_path]
upload_command = info["upload_command"]
cdn_url = info["cdn_url"]

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             shell=True, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        if not stdout_line:
            break
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def run_command(cmd):
    for path in execute(cmd):
        print(path, end="")


def ChromeDriver():
    return webdriver.Chrome()


def HeadlessChromeDriver():
    return webdriver.Chrome(chrome_options=chrome_options)


def slow_send_keys(element, keys):
    for key in keys:
        time.sleep(random.random() * 0.5)
        element.send_keys(key)


# In[3]:


driver = HeadlessChromeDriver()


# In[4]:


driver.get(video_link_supply_url)

supply_source = driver.page_source
supply_soup = bs(supply_source, "html.parser")


# In[5]:


target_link = supply_soup.find_all(class_="downloadsTable")[0].find(
    download="We Happy Restaurant - Preview 2.mp4")["href"]


# In[6]:


for config_path in config_paths:
    with open(config_path, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    data[0]["adUrl"] = target_link
    with open(config_path, 'w') as outfile:
        json.dump(data, outfile, indent = 4)


# In[7]:


run_command(upload_command)


# In[8]:


driver = ChromeDriver()


# In[9]:


driver.get("https://console.cloud.tencent.com/cdn/refresh")


# In[10]:


link = driver.find_element_by_link_text("QQ")
link.click()


# In[11]:


time.sleep(random.random()+0.5)
driver.switch_to.frame('ptlogin_iframe')
driver.find_element_by_partial_link_text("登录").click()


# In[12]:


username = driver.find_element_by_id("u")
username.click()
time.sleep(random.random() + 0.5)
username.clear()
slow_send_keys(username, info["username"])
time.sleep(random.random() + 0.5)
password = driver.find_element_by_id("p")
time.sleep(random.random() + 0.5)
password.click()
time.sleep(random.random() + 0.5)
password.clear()
slow_send_keys(password, info["password"])
time.sleep(random.random() + 0.5)
driver.find_element_by_id('login_button').click()
time.sleep(random.random() + 0.5)


# In[13]:


while True:
    try:
        box = driver.find_element_by_class_name("code-list")
        box = box.find_element_by_xpath(".//tbody//tr//td//textarea")
        box.click()
        box.clear()
        box.send_keys(
        "http://www.chillyroom.com/game/promotion/AppStore/config.json"
        "\n"
        "http://www.chillyroom.com/game/promotion/GooglePlay/config.json"
        )
        time.sleep(random.random()+0.5)
        button = driver.find_element_by_class_name("tc-btn")
        button.click()
        time.sleep(1)
        break
    except NoSuchElementException:
        time.sleep(5)


# In[14]:


time.sleep(2)
driver.quit()


# In[ ]:




