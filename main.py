from selenium import webdriver
import time
import pandas as pd
import xlsxwriter
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
browser = webdriver.Chrome(options=options)

browser.get("https://web.arbeitsagentur.de/entgeltatlas/tabelle?dkz=15103&geschlecht=1&alter=1&branche=1")
time.sleep(1)

tableHeaderList = []
#Getting the table header Count
headerCount = len(browser.find_elements('xpath',"//th"))
test = browser.find_elements('xpath','//table/thead/tr/th')
# print("test-",test,"-",type(test))
for i in test:
    tableHeaderList.append(i.get_property('innerHTML'))

tableDataList = []

rowDataCount = len(browser.find_elements('xpath',"//table/tbody/tr"))

rowData = browser.find_elements('xpath','//table/tbody/tr')
print(len(rowData))

tableDataList.append(tableHeaderList)
for row in rowData:
    tableData = row.find_elements('xpath','td')
    tempList = []
    for columnData in tableData:
        existsInsideTr = len(columnData.find_elements('xpath','ba-ega-entgelt-betrag/span'))
        if existsInsideTr == 0:
            stringunProcessed = columnData.get_attribute('innerHTML')
            stringunProcessed = stringunProcessed.replace("\n","")
            tempList.append(stringunProcessed.replace("&nbsp", ""))
        else:
            stringunProcessed = columnData.find_element('xpath','ba-ega-entgelt-betrag/span').get_property('innerHTML');
            stringunProcessed.replace("\n","")
            tempList.append(stringunProcessed.replace("&nbsp", ""))
 
    tableDataList.append(tempList)
    
#Saving in excel
with xlsxwriter.Workbook('test.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(tableDataList):
        worksheet.write_row(row_num, 0, data)