import pandas as pd
import numpy as np 
from selenium import webdriver
from time import sleep

username = []
skincond = []
recommend = []
datereview = []
review = []
rating = [] 
produk = []
merk = []
kategori = []
price = []

home = 'https://femaledaily.com/category/skincare'
path = 'chromedriver.exe'

driver = webdriver.Chrome(path)
driver.get(home)
sleep(5)

category_column = driver.find_elements_by_class_name('jsx-3413472294.category-landing-column')

list_of_category_title = []
list_of_category_href = []

for i in category_column:
    category = i.find_elements_by_tag_name('a')
    for cat in category:
        list_of_category_title.append(cat.text)
        list_of_category_href.append(cat.get_attribute('href'))

for i in range(len(list_of_category_href)):
    list_of_category_href[i] = list_of_category_href[i][:-1]

category = list(zip(list_of_category_title, list_of_category_href))

for cattittle, cathref in category[:]: #category
    for page in [:]:
        driver.get(cathref+str(page))
        try:
            sleep(5)

            product_list_title = []
            product_list_href = []  
            product_column = driver.find_elements_by_class_name('jsx-2681188818.product-item')

            for i in product_column:
                product = i.find_elements_by_tag_name('a') 
                product_list_title.append(product[1].text)
                product_list_href.append(product[1].get_attribute('href')) 
            
            for i in range(len(product_list_href)):
                product_list_href[i] = product_list_href[i][:-1]

            product = list(zip(product_list_title, product_list_href))
            
            for product, prodhref in product:
                for page2 in range(1,2): #product review page
                    driver.get(prodhref + str(page2))
                    try:
                        card = driver.find_elements_by_class_name('jsx-992468192.item')
                        sleep(5)
                        for item in card:
                            username.append(item.find_element_by_class_name('username').text)
                            review.append(item.find_element_by_class_name('text-content').text)
                            rating.append(len(item.find_element_by_class_name('cardrv-starlist').find_elements_by_class_name('icon-ic_big_star_full')))
                            merk.append(driver.find_element_by_tag_name('h2').text)
                            kategori.append(cattittle)
                            produk.append(product)
                            try:
                                skincond.append(item.find_element_by_class_name('skin').text)
                            except:
                                skincond.append(np.nan)
                            try:
                                recommend.append(item.find_element_by_class_name('recommend').text)
                            except:
                                recommend.append(np.nan) 
                            try:
                                datereview.append(item.find_element_by_class_name('date.review-date').text)
                            except:
                                datereview.append(np.nan)  
                            try:
                                price.append(driver.find_element_by_class_name('jsx-992468192.product-price').text) 
                            except:
                                price.append(np.nan)
                    except:
                        pass
        except:
            pass

driver.close()

df = pd.DataFrame({'Category': kategori,
'Merk': merk,
'Product': produk,
'Price': price,
'UserName': username,
'SkinCond_Age': skincond,
'Recommend': recommend,
'PostDate': datereview,
'Review': review,
'Rating': rating})

df.to_csv('SkincareReview.csv', index = False)
