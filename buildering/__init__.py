# -*- coding: utf-8 -*-
'''
from selenium import webdriver

driver = webdriver.PhantomJS()

driver.get("http://www.amazon.com/reviews/B004UKJS68")
d = driver
a= driver.find_element_by_class_name("CMpaginate").find_elements_by_tag_name('a')
for i in a:
    print i.get_attribute('href')

print driver.current_url

driver.get('http://www.amazon.com/gp/cdp/member-reviews/AVBLGXSWRN666?ie=UTF8&display=public&page=1&sort_by=MostRecentReview')

a = len('Reviews Written by')
a =driver.find_elements_by_tag_name('tbody')[1].find_elements_by_class_name('reviewText')
print driver.find_element_by_tag_name('tbody').text
for i in a:
    print i.text

driver.quit()

'''