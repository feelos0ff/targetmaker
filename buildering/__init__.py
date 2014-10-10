# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.PhantomJS()


print driver.current_url
driver.get('http://www.amazon.com/gp/cdp/member-reviews/A3D8PIJ80A5HTL?ie=UTF8&display=public&page=2&sort_by=MostRecentReview')

#a =driver.find_elements_by_tag_name('tbody')[1].find_elements_by_class_name('reviewText')
#print driver.find_element_by_tag_name('tbody').text
body = driver.find_elements_by_tag_name('tbody')[1] 
print len(body.find_elements_by_css_selector('span[class="h3color tiny"]+a'))
tr = [ i.get_attribute('href') for i in body.find_elements_by_css_selector('span[class="h3color tiny"]+a') ]
print len(tr)
print tr
driver.quit()
