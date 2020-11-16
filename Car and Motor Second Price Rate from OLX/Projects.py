from selenium import webdriver
import pandas as pd
import numpy as np
from time import sleep 

path = "chromedriver.exe"
home = ["https://www.olx.co.id/mobil-bekas_c198", "https://www.olx.co.id/motor-bekas_c200"]

driver = webdriver.Chrome(path)
 
mobil_bekas = []
motor_bekas = []

for cat in range(2): 
    driver.get(home[cat])
    sleep(3)
    #Mau ambil berapa banyak? 1 muatan ada sekitar 20 iklan, karena tidak berbentuk page, maka diambil berapa banyak klik "muat lebih"
    for click in range(20):
        driver.find_element_by_class_name("rui-3sH3b.rui-3K5JC.rui-1zK8h").click()
        sleep(2)

    cardlist = driver.find_elements_by_class_name("EIR5N")

    link_temp = []
    for item in cardlist: 
        tipe = item.find_element_by_class_name("_2tW1I").text 
        harga = item.find_element_by_class_name("_89yzn").text
        harga = harga.replace("Rp ", "")
        harga = harga.replace(".", "")
        
        #ubah range harga
        if cat == 0:
            batas_bawah = 0
            batas_atas = 500000000
        else:
            batas_bawah = 0
            batas_atas = 20000000

        if batas_bawah < int(harga) < batas_atas:
            link_temp.append(item.find_element_by_tag_name("a").get_attribute("href"))

    for iklan in link_temp:
        driver.get(iklan)
        try:
            detail = driver.find_elements_by_class_name("_25oXN")
            entity = driver.find_elements_by_class_name("_2vNpt")
            temp_dict = {}
            for idx in range(len(detail)):
                temp_dict[detail[idx].text] = entity[idx].text
            temp_dict['url'] = iklan
            temp_dict['Harga'] = driver.find_element_by_class_name("_2xKfz").text
            if cat == 0:
                mobil_bekas.append(temp_dict)
            if cat == 1:
                motor_bekas.append(temp_dict)
        except:
            print(iklan)
            pass

driver.close()


pd.DataFrame(mobil_bekas).to_excel("Mobil_Bekas.xlsx")
pd.DataFrame(motor_bekas).to_excel("Motor_Bekas.xlsx")