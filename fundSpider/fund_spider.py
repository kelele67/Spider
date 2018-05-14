import os, sys
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from datetime import datetime
import pandas as pd


class Fund(unittest.TestCase):

    def datelist(self, beginDate, endDate):
        # beginDate, endDate是形如‘20160601’的字符串或datetime格式
        date_l=[datetime.strftime(x,'%Y-%m-%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
        return date_l

    def setUp(self):
        ch_driver = os.path.abspath(r"/usr/local/bin/chromedriver")
        os.environ["webdriver.chrome.driver"]= ch_driver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "http://fund.eastmoney.com"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.flist = [] # fund list
        f1 = open("flist.txt",'r')
        self.flist = list(map(str.strip, f1.readlines()))
        f1.close()

    def test_fund(self):
        flist = self.flist
        driver = self.driver
        start_date_list = self.datelist('20170501', '20180515')[::20]
        end_date_list = self.datelist('20170501', '20180515')[19::20]
        date_list = zip(start_date_list, end_date_list)
        for f in flist:
            for start_date, end_date in date_list:
                driver.get(self.base_url + "/f10/jjjz_%s.html" % (f))
                driver.find_element_by_id("lsjzSDate").clear()
                driver.find_element_by_id("lsjzSDate").send_keys(start_date)
                driver.find_element_by_id("lsjzEDate").clear()
                driver.find_element_by_id("lsjzEDate").send_keys(end_date)
                driver.find_element_by_css_selector("input.search").click()
                time.sleep(1)
                try:
                    div = driver.find_element_by_id("jztable")
                    table = div.find_elements_by_tag_name("table")
                    tbody = table[0].find_elements_by_tag_name("tbody")
                    t_rows = tbody[0].find_elements_by_tag_name('tr')
                    for row in t_rows:
                        with open(f +'.csv','a', encoding='utf8') as fp:
                            writer = csv.writer(fp, dialect='excel')
                            tds = row.find_elements_by_tag_name('td')
                            datas = [f, tds[0].text, tds[1].text, tds[2].text, tds[3].text]
                            print(datas)
                            writer.writerow(datas)
                except Exception as msg:
                    print(msg)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()