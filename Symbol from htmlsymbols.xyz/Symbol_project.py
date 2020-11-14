from selenium import webdriver
import pandas as pd
import numpy as np
from time import sleep

path = "chromedriver.exe"
home = "https://www.htmlsymbols.xyz/unit-symbols"

driver = webdriver.Chrome(path)
driver.get(home)

driver.find_elements_by_class_name("list-grid-container.show-table.mb-4")[0].find_element_by_tag_name("a").get_attribute('href')

link = []

list_container = driver.find_elements_by_class_name("list-grid-container.show-table.mb-4")
for lc in list_container:
    link_list = lc.find_elements_by_tag_name("a")
    for item in link_list:
        link.append(item.get_attribute('href'))

# go to the link
driver.get(link[0])

col = [] 
disp_area = driver.find_elements_by_class_name("displayarea")[:3] 
for item in disp_area:
    item2 = item.find_elements_by_tag_name("td")
    temp_en = []
    for idx in range(0, len(item2), 3):
        col.append(item2[idx].text)  

entity = []
for page in link:
    driver.get(page)
    temp = []
    disp_area = driver.find_elements_by_class_name("displayarea")[:3] 
    for item in disp_area:
        item2 = item.find_elements_by_tag_name("td")
        temp_en = []
        for idx in range(0, len(item2), 3): 
            temp_en.append(item2[idx+1].text) 
        temp.extend(temp_en)
    entity.append(temp)

driver.close()

import pandas as pd
out = pd.DataFrame(entity, columns = col)
out.to_excel('Symbol.xlsx')