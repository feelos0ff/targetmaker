# -*- coding: utf-8 -*-
'''
from selenium import webdriver

driver = webdriver.PhantomJS()

driver.get("http://www.amazon.com/reviews/B004UKJS68")
d = driver
a= driver.find_element_by_class_name("CMpaginate").find_elements_by_tag_name('a')

print driver.current_url

driver.get('http://www.amazon.com/Belkin-Candy-Cover-iPhone-Black/dp/B0094CX5JI/ref=cm_cr-mr-title')

a =driver.find_element_by_id('priceblock_ourprice').text[1:]
print a
driver.quit()

'''
