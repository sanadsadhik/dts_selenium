from selenium import webdriver
import time
import random
import string
import xlsxwriter
import itertools
import pathlib
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from datetime import date , timedelta
from datetime import datetime
from selenium.webdriver.common.keys import Keys

date_object = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
driver = webdriver.Chrome("/Users/ssadhik/PycharmProjects/pythonProject/driver/chromedriver")
# driver.get("https://dts.juniper.net/staging1/?tab=product")
driver.get("http://dts.juniper.net/?tab=product")

### LOGIN TO THE DASHBOARD
time.sleep(10)
uid = driver.find_element_by_xpath("//div[@class = 'placeholderContainer']/input[@type = 'email']")
uid.send_keys("ssadhik@juniper.net")
submit_usr = driver.find_element_by_id("idSIButton9")
submit_usr.click()
time.sleep(5)
pwd = driver.find_element_by_xpath("//div[@class = 'placeholderContainer']/input[@type = 'password']")
pwd.send_keys("Juniper@226389")
time.sleep(5)
# submit = driver.find_element_by_id("idSIButton9")
# submit.send_keys("Keys.ENTER")
submit = driver.find_element_by_xpath("//input[@type = 'submit']")
submit.click()
driver.fullscreen_window()

# #creating the excel sheet
workbook = xlsxwriter.Workbook("/Users/ssadhik/PycharmProjects/pythonProject/Reports/DTS-report-" + str(date_object) + ".xlsx")
bold = workbook.add_format({'bold': True})
cell_format = workbook.add_format()
worksheet = workbook.add_worksheet("DTS-report")
worksheet.write('A1', 'TESTCASE', bold) # first cell
worksheet.write('B1', 'RESULT', bold) # 2 column

window_before = driver.window_handles[0] #window handling
window_before_title = driver.title
print(window_before_title)
#
try:
    table_data = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "myGridSummary")))
    # table_data = driver.find_element_by_id("pro-report")
    time.sleep(7)
    if table_data:
        worksheet.write('A3', 'TABLE LOAD', bold)
        cell_format.set_bg_color('green')
        worksheet.write('B3','PASS',cell_format)
    else:
        print("Loading took too much time!")
        worksheet.write('A3', 'TABLE LOAD', bold)
        cell_format.set_bg_color('red')
        worksheet.write('B3', 'FAIL', cell_format)

except Exception as e:
    print(e)
    print("Loading took too much time!")
    worksheet.write('A3', 'TABLE LOAD', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B3', 'FAIL', cell_format)
    exit()

time.sleep(10)
# #
# List of first level hierarchy
grid = driver.find_element_by_id("myGridSummary")
table_grid = grid.find_element_by_class_name("ag-pinned-left-cols-container")
all_hierarchy = table_grid.find_elements_by_css_selector(".ag-group-value")
names = [z.find_element_by_tag_name('span').get_attribute('innerHTML').split('>')[-1] for z in all_hierarchy]
for e in all_hierarchy:
    text_names = e.text  # getting the elemnt to a list
    names.append(text_names)
without_empty_strings = [string for string in names if string != ""]
print("The current hierarchy : ",without_empty_strings)
time.sleep(5)

#
# ##Click the info button
# info = driver.find_element_by_xpath("//div[@class = 'clearfix mr20 mb5']/button[@class = 'infoBtn btn btn-default btn-sm pull-right mr10']")
# info.click()
# data_info = driver.find_element_by_class_name("jconfirm-title")
# # print(data.text)
# if data_info.text == 'Data Logic':
#     print("Info Button Pass")
#     worksheet.write('A4', 'info button', bold)
#     cell_format.set_bg_color('green')
#     worksheet.write('B4', 'PASS', cell_format)
# else:
#     print("Info Button Fail")
#     worksheet.write('A4', 'info button', bold)
#     cell_format.set_bg_color('red')
#     worksheet.write('B4', 'FAIL', cell_format)
# time.sleep(2)
# info_btn = driver.find_element_by_xpath("//div[@class = 'jconfirm-buttons']/button[@class = 'btn btn-default']")
# info_btn.click()
# time.sleep(5)

# get the All Total column cell values
centre_class = driver.find_element_by_class_name("ag-center-cols-clipper")
total_col = centre_class.find_elements_by_xpath("//div[@role = 'row']/div[@col-id = 'totaltotal']/span/a")
# values = [y.find_element_by_tag_name('a').get_attribute('innerHTML').split('>')[-1] for y in row_cell_values]
values_total = []
for y in total_col:
    text_total = y.text  # getting the elemnt to a list
    # print(text_total)
    values_total.append(text_total)
    time.sleep(5)
without_empty_total = [value for value in values_total if value != " "]
print(" All-Total values: ",without_empty_total)
time.sleep(10)



#expand the hierarchy
expand_all = driver.find_element_by_xpath("//div[@class = 'clearfix mr20 mb5']/button[@data-type = 'expand']")
expand_all.click()
if expand_all:
    worksheet.write('A6', 'expand_btn', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B6', 'PASS', cell_format)
else:
    worksheet.write('A6', 'expand_btn', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B6', 'FAIL', cell_format)
# #expand/collapse the columns
# collapse_expand = driver.find_element_by_class_name("ag-header-viewport")
# all_headers = collapse_expand.find_element_by_css_selector(".ag-header-group-cell")
# expand_click = driver.find_element_by_xpath("//div[@class = 'customExpandButton collapsed']/i[@class = 'ag-icon ag-icon-expanded']")
# expand_click.click()
# time.sleep(8)

# get the totalnw Total column cell values
time.sleep(5)
centre_class = driver.find_element_by_class_name("ag-center-cols-clipper")
total_nw = centre_class.find_elements_by_xpath("//div[@role = 'row']/div[@col-id = 'totalothers']/span/a")
# values = [y.find_element_by_tag_name('a').get_attribute('innerHTML').split('>')[-1] for y in row_cell_values]
nw_coltotal = []
for nw in total_nw:
    text_total = nw.text  # getting the elemnt to a list
    # print(text_total)
    nw_coltotal.append(text_total)
    time.sleep(5)
without_empty_nwtotal = [nw for nw in nw_coltotal if nw != " "]
print(" Not working-Total values: ",without_empty_nwtotal)
time.sleep(5)


#graph
pivot_user = driver.find_element_by_class_name("ag-pinned-left-cols-container")
pivot_user1 = pivot_user.find_elements_by_css_selector(".ag-group-value")
# print(len(pivot_user1))
counter = 0
for i in pivot_user1[0:1]: #2 clicks
    try:
        print("going!!")
        tab1 = i.find_element_by_xpath("//span/i[@class = 'fa fa-bar-chart showgraphs']")
        tab1.click()
        counter += 1
        print("Counter is :",counter)
        if tab1.click() == 'success':
            print("Graphs loaded!")
            worksheet.write('A9', 'grid_row_values', bold)
            cell_format.set_bg_color('green')
            worksheet.write('B9', 'PASS', cell_format)
        else:
            print("Graps dint load!")
            worksheet.write('A9', 'grid_row_values', bold)
            cell_format.set_bg_color('red')
            worksheet.write('B9', 'FAIL', cell_format)
    except:
        print("Graps load FAIL!")
        worksheet.write('A9', 'grid_row_values', bold)
        cell_format.set_bg_color('red')
        worksheet.write('B9', 'FAIL', cell_format)
        exit()
time.sleep(4)
## Charts by L2 #####
chart2 = driver.find_element_by_id("accslide2")
tab2 = chart2.find_element_by_xpath("//ul[@class = 'nav nav-tabs']/li/a[@href = '#certchart-l2-wrap']")
tab2.click()
print("Charts by L2 ")

#Total graph by L2#######
# total_l2 = driver.find_element_by_id("certchart-total")
total_all = chart2.find_element(By.ID, "certchart-total")
time.sleep(10)
total1 = total_all.find_elements(By.TAG_NAME, "path")
data_total = total_all.find_elements(By.TAG_NAME, "tspan")
tot_values_graph = []
for lall in data_total:
    list_totalall = lall.get_attribute('textContent')
    # print(list_val)
    tot_values_graph.append(list_totalall)
totalval = [lx1 for lx1 in tot_values_graph if lx1 != "" and lx1.isdigit()]
print("AllTotal L2 values : ", totalval[0:7])
time.sleep(5)

####Working total values
total_working = chart2.find_element(By.ID, "certchart-w")
time.sleep(10)
total_w = total_working.find_elements(By.TAG_NAME, "svg")
working_tot = total_working.find_elements(By.TAG_NAME, "text")
tot_work_graph = []
for lall in working_tot:
    list_totalwork = lall.get_attribute('textContent')
    # print(list_val)
    tot_work_graph.append(list_totalwork)
totalwork = [w1 for w1 in tot_work_graph if w1 != "" and w1.isdigit()]
print("Working Total L2 values : ", totalwork[0:7])
time.sleep(5)

##Not In use values
total_nuse = chart2.find_element(By.ID, "certchart-nw")
time.sleep(10)
tot = total_nuse.find_elements(By.TAG_NAME, "svg")
Not_use = total_nuse.find_elements(By.TAG_NAME, "text")
tot_nouse_graph = []
for nu in Not_use:
    list_totalNotuse = nu.get_attribute('textContent')
    # print(list_val)
    tot_nouse_graph.append(list_totalNotuse)
totalnouse = [nu for nu in tot_nouse_graph if nu != "" and nu.isdigit()]
print("Not in use Total L2 values : ", totalnouse[0:7])
time.sleep(5)

##Not working L2 values
total_nw = chart2.find_element(By.ID, "certchart-others")
time.sleep(10)
tot_nw = total_nw.find_elements(By.TAG_NAME, "svg")
Not_working = total_nw.find_elements(By.TAG_NAME, "text")
tot_notwork_graph = []
for nw in Not_working:
    list_totalNotwork = nw.get_attribute('textContent')
    # print(list_val)
    tot_notwork_graph.append(list_totalNotwork)
totalnowork = [nw for nw in tot_notwork_graph if nw != "" and nw.isdigit()]
print("Not working Total L2 values : ", totalnowork[0:7])
time.sleep(5)

#Hide hcharts
hide_graph = driver.find_element_by_id("chart-div")
close_graph = hide_graph.find_element_by_xpath("//div[@class = 'tab-content dn']/h4/button[@class = 'hidegraphs btn btn-danger btn-sm']")
close_graph.click()



# Check the lists for L2
L2_total = any(item in totalval[0:7] for item in without_empty_total)
if L2_total is True:
    print("All products values matching")
    print("The totalval {} contains some elements of the without_empty_total {}".format(totalval[0:7], without_empty_total))
    worksheet.write('A11', 'L2_alltotal', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B11', 'PASS', cell_format)
else:
    print("All products values is not matching")
    worksheet.write('A11', 'L2_alltotal', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B11', 'FAIL', cell_format)


# Checek the lists for L2
nw_total = any(item in totalnowork[0:7] for item in without_empty_total)
if nw_total is True:
    print("Total not working values matching")
    print("The not working  {} contains some elements of the table values without_empty_total {}".format(totalnowork[0:7], without_empty_nwtotal))
    worksheet.write('A12', 'quick_search_values', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B12', 'PASS', cell_format)
else:
    print("Total not working is not matching")
    worksheet.write('A12', 'quick_search_values', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B12', 'FAIL', cell_format)
time.sleep(4)


#Search text
global_search = driver.find_element_by_id("globalSearch")
global_search.send_keys()
# ***** quick search ********
global_search = driver.find_element_by_id("globalSearchForm")
# ** search from the hierarchy **
quick_input_multiple = global_search.find_element_by_id("globalSearch")
for ele in without_empty_strings:
    if ele != '':
        mul_values = random.sample(without_empty_strings, 1)
        values_enter = quick_input_multiple.send_keys(mul_values[0])
        print(" item from list is: ", mul_values)
        worksheet.write('A5', 'quick_search_values', bold)
        cell_format.set_bg_color('green')
        worksheet.write('B5', 'PASS', cell_format)
    else:
        print("Loading took too much time!")
        worksheet.write('A5', 'quick_search_values', bold)
        cell_format.set_bg_color('red')
        worksheet.write('B5', 'FAIL', cell_format)
    break
# search_btn = driver.find_element_by_xpath("//div[@id = 'globalSearchForm']/button/i[@class = 'fa fa-search']")
# search_btn.click()
time.sleep(4)

#Export Button
if os.path.exists("device_utilization_record_summary.xlsx"):
  os.remove("/Users/ams/Downloads/")
else:
  print("The file does not exist")
export_data = driver.find_element_by_xpath("//div[@class = 'clearfix mr20 mb5']/button[@class = 'exportBtnSummary btn btn-sm pull-right']")
export_data.click()
file = pathlib.Path("/Users/ssadhik/Downloads/")
if file.exists():
    print("File exists!")
    worksheet.write('A7', 'export', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B7', 'PASS', cell_format)
else:
    print("File does not exist!!")
    worksheet.write('A7', 'export', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B7', 'FAIL', cell_format)
time.sleep(4)

#get the cell values
centre_class = driver.find_element_by_class_name("ag-center-cols-clipper")
time.sleep(5)
full_row = centre_class.find_elements_by_xpath("//div[@row-index = '0']/div/span/a")
time.sleep(5)
# values = [y.find_element_by_tag_name('a').get_attribute('innerHTML').split('>')[-1] for y in row_cell_values]
values = []
for x in full_row:
    text_values = x.get_attribute('textContent')  # getting the elemnt to a list
    values.append(text_values)
# print(values)
without_empty_values = [val for val in values if val != ""]
print("Table row values: ",without_empty_values)
time.sleep(5)
if len(without_empty_values) != 0:
    worksheet.write('A8', 'grid_row_values', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B8', 'PASS', cell_format)
else:
    print("List is Empty ")
    worksheet.write('A8', 'grid_row_values', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B8', 'FAIL', cell_format)
# #graph

#graph
pivot_user = driver.find_element_by_class_name("ag-pinned-left-cols-container")
pivot_user1 = pivot_user.find_elements_by_css_selector(".ag-group-value")
# print(len(pivot_user1))
counter = 0
for i in pivot_user1[0:1]: #2 clicks
    try:
        print("going!!")
        tab1 = i.find_element_by_xpath("//span/i[@class = 'fa fa-bar-chart showgraphs']")
        tab1.click()
        counter += 1
        print("Counter is :",counter)
        if tab1.click() == 'success':
            print("Graphs loaded!")
            worksheet.write('A9', 'grid_row_values', bold)
            cell_format.set_bg_color('green')
            worksheet.write('B9', 'PASS', cell_format)
        else:
            print("Graphs dint load!")
            worksheet.write('A9', 'grid_row_values', bold)
            cell_format.set_bg_color('red')
            worksheet.write('B9', 'FAIL', cell_format)
    except:
        print("Graphs load FAIL!")
        worksheet.write('A9', 'grid_row_values', bold)
        cell_format.set_bg_color('red')
        worksheet.write('B9', 'FAIL', cell_format)
        exit()

chart = driver.find_element_by_id("accslide2")
tab1 = chart2.find_element_by_xpath("//ul[@class = 'nav nav-tabs']/li/a[@href = '#certchart-category-wrap']")
tab1.click()
print("Charts by products ")

# get the chart values
###get the All products values #####
# chart = driver.find_element_by_id("accslide2")
time.sleep(5)
gt1 = chart.find_element(By.ID, "certchart-ALL")
time.sleep(10)
m1 = gt1.find_elements(By.TAG_NAME, "svg")
        # a = ActionChains(driver)
        # a.move_to_element(m).perform()
time.sleep(8)
data = gt1.find_elements(By.TAG_NAME, "text")
all_graph_val = []
for val1 in data:
    list_val1 = val1.get_attribute('textContent')
    # print(list_val)
    all_graph_val.append(list_val1)
all_values_graph = [val1 for val1 in all_graph_val if val1 != "" and val1.isdigit()]
print("All product values : ", all_values_graph[0:3])
time.sleep(5)


#### MX graph########
gt2 = chart.find_element(By.ID, "certchart-MX")
time.sleep(10)
m2 = gt2.find_elements(By.TAG_NAME, "svg")
# a = ActionChains(driver)
# a.move_to_element(m).perform()
data2 = gt2.find_elements(By.TAG_NAME, "text")
mx_graph_val = []
for val2 in data2:
    list_val2 = val2.get_attribute('textContent')
    # print(list_val)
    mx_graph_val.append(list_val2)
mx_values_graph = [val2 for val2 in mx_graph_val if val2 != "" and val2.isdigit()]
print("All MX values : ", mx_values_graph[0:3])
time.sleep(8)
#
#### PTX graph########
gt3 = chart.find_element(By.ID, "certchart-PTX")
time.sleep(10)
m3 = gt3.find_elements(By.TAG_NAME, "svg")
# a = ActionChains(driver)
# a.move_to_element(m).perform()
data3 = gt3.find_elements(By.TAG_NAME, "text")
ptx_graph_val = []
for val3 in data3:
    list_val3 = val3.get_attribute('textContent')
    # print(list_val)
    ptx_graph_val.append(list_val3)
ptx_values_graph = [val3 for val3 in ptx_graph_val if val3 != "" and val3.isdigit()]
print("All PTX values : ", ptx_values_graph[0:3])
time.sleep(8)

#### QFX graph########
gt4 = chart.find_element(By.ID, "certchart-QFX")
time.sleep(10)
m4 = gt4.find_elements(By.TAG_NAME, "svg")
# a = ActionChains(driver)
# a.move_to_element(m).perform()
data4 = gt4.find_elements(By.TAG_NAME, "text")
qfx_graph_val = []
for val4 in data4:
    list_val4 = val4.get_attribute('textContent')
    # print(list_val)
    qfx_graph_val.append(list_val4)
qfx_values_graph = [val4 for val4 in qfx_graph_val if val4 != "" and val4.isdigit()]
print("All QFX values : ", qfx_values_graph[0:3])
time.sleep(5)

### SRX graph########
gt5 = chart.find_element(By.ID, "certchart-SRX")
time.sleep(10)
m5 = gt5.find_elements(By.TAG_NAME, "svg")
# a = ActionChains(driver)
# a.move_to_element(m).perform()
data5 = gt5.find_elements(By.TAG_NAME, "text")
srx_graph_val = []
for val5 in data5:
    list_val5 = val5.get_attribute('textContent')
    # print(list_val)
    srx_graph_val.append(list_val5)
srx_values_graph = [val5 for val5 in srx_graph_val if val5 != "" and val5.isdigit()]
print("All SRX values : ", srx_values_graph[0:3])
time.sleep(5)

####-ACX ####
gt6 = chart.find_element(By.ID, "certchart-ACX")
time.sleep(10)
m6 = gt6.find_elements(By.TAG_NAME, "svg")
# a = ActionChains(driver)
# a.move_to_element(m).perform()
data6 = gt6.find_elements(By.TAG_NAME, "text")
acx_graph_val = []
for val6 in data6:
    list_val6 = val6.get_attribute('textContent')
    # print(list_val)
    acx_graph_val.append(list_val6)
acx_values_graph = [val6 for val6 in acx_graph_val if val6 != "" and val6.isdigit()]
print("All ACX values : ", acx_values_graph[0:3])
time.sleep(5)

#####certchart-EX##
gt7 = chart.find_element(By.ID, "certchart-EX")
time.sleep(10)
m7 = gt7.find_elements(By.TAG_NAME, "svg")
# a = ActionChains(driver)
# a.move_to_element(m).perform()
data7 = gt7.find_elements(By.TAG_NAME, "text")
ex_graph_val = []
for val7 in data7:
    list_val7 = val7.get_attribute('textContent')
    # print(list_val)
    ex_graph_val.append(list_val7)
ex_values_graph = [val7 for val7 in ex_graph_val if val7 != "" and val7.isdigit()]
print("All EX values : ", ex_values_graph[0:3])
time.sleep(5)

final_val_list = list(itertools.chain(all_values_graph[0:3], mx_values_graph[0:3],ptx_values_graph[0:3],qfx_values_graph[0:3],srx_values_graph[0:3],acx_values_graph[0:3],ex_values_graph[0:3]))
# print('Merged List:')
print("Final values : ",final_val_list)
check = any(item in final_val_list[0:3] for item in without_empty_values)

if check is True:
    print("Values matching with the table data")
    print("The final_val_list {} contains some elements of the without_empty_values {}".format(final_val_list, without_empty_values))
    worksheet.write('A10', 'Graph_data', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B10', 'PASS', cell_format)
else:
    print("values not matching")
    worksheet.write('A10', 'Graph_data', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B10', 'FAIL', cell_format)


#Hide hcharts
hide_graph = driver.find_element_by_id("chart-div")
close_graph = hide_graph.find_element_by_xpath("//div[@class = 'tab-content dn']/h4/button[@class = 'hidegraphs btn btn-danger btn-sm']")
close_graph.click()




# ****smart filter****

smart_filter = driver.find_element(By.ID,"smartbtn")
smart_filter.click()
time.sleep(5)

# ****custom pivot*****
remove = driver.find_element_by_xpath("//div[@id = 'pivotsdestination']/span/i[@class = 'fa fa-minus-circle psource mr5']")
remove.click()
time.sleep(4)
available_pivots = driver.find_element_by_id("pivotssource")
avail = [x for x in available_pivots.find_elements_by_css_selector(".draggable")]
li_avail = []
time.sleep(5)
success = 0
for item in avail:
    text = item.text  # getting the elemnt to a list
    if text == 'L1':
        success = 1
    li_avail.append(text)
print("The available pivots before are:\n", li_avail)
reorder_pivots = driver.find_element_by_id("pivotsdestination")
reorder = [x for x in reorder_pivots.find_elements_by_css_selector(".draggable")]
li_dest = []
time.sleep(5)
for ele in reorder:
    var = ele.text  # getting the elemnt to a list
    li_dest.append(var)
print("Number of selected-pivots: ", len(li_dest))
if len(li_dest) != 8:
    success = 0
time.sleep(3)
if success == 1:
    print("Pivots reordered")
    worksheet.write('A13', 'Pivots', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B13', 'PASS', cell_format)
else:
    worksheet.write('A13', 'Pivots', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B13', 'FAIL', cell_format)
time.sleep(5)

otr_option = driver.find_element_by_xpath("//input[@value='STORED']")
otr_option.click()
time.sleep(2)
evo_option = driver.find_element_by_xpath("//input[@value='evo']")
evo_option.click()
time.sleep(2)
junos_option = driver.find_element_by_xpath("//input[@value='junos']")
junos_option.click()
time.sleep(2)
apply_button = driver.find_element_by_xpath("//button[@data-type='apply']")
apply_button.click()
time.sleep(10)

# ****Details clicks and info****
table = driver.find_element(By.CLASS_NAME,'ag-center-cols-clipper')
link = table.find_element_by_xpath("//div/div/div/div/div/span/a")
link.click()
time.sleep(8)
window_after = driver.window_handles[1]
driver.switch_to.window(window_after)
window_after_title = driver.title  # get the window title
print(window_after_title)
navbar = driver.find_element_by_class_name("project-title")
if "Details" in navbar.text:
    print("Device details for evo")
    worksheet.write('A14', 'Load_details_page', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B14', 'PASS', cell_format)
else:
    worksheet.write('A14', 'Load_details_page', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B14', 'FAIL', cell_format)
time.sleep(5)

#Resource details modal
table = driver.find_element(By.CLASS_NAME,'ag-center-cols-clipper')
link = table.find_element_by_xpath("//div/div/div/span/span/a[2]")
l_t = link.text
link.click()
time.sleep(5)
title = driver.find_element(By.ID,"resource_title")
if title.text in l_t.upper():
    # print("success")
    worksheet.write('A15', 'Load resource details', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B15', 'PASS', cell_format)
else:
    worksheet.write('A15', 'Load resource details', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B15', 'FAIL', cell_format)
time.sleep(5)

resource_modal = driver.find_element(By.ID,"resourceDetailsModal")
modal_head = resource_modal.find_element(By.CLASS_NAME,"modal-header")
close_button = modal_head.find_element_by_xpath("//button[@class = 'close']/span")
close_button.click()

#OS type -evo and on the rack  verify
fail = 0
table_body = driver.find_element(By.CLASS_NAME,"ag-center-cols-clipper")
rows = table_body.find_elements_by_xpath("//div/div/div/div/div[7]")
for row in rows:
    if row == 'STORED':
        fail = 1
rd_tab = table_body.find_element_by_xpath("//div/div/div/div/div[4]")
time.sleep(3)
expand = rd_tab.find_element(By.TAG_NAME,'i')
expand.click()
rows_ostype = table_body.find_elements_by_xpath("//div/div/div/div/div[9]")
for row in rows_ostype:
    if row == 'junos':
        fail = 1
if fail == 0:
    print("OS type is evo")
    worksheet.write('A16', 'Evo_Smart_filter_verify', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B16', 'PASS', cell_format)
else:
    worksheet.write('A16', 'Evo_Smart_filter_verify', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B16', 'FAIL', cell_format)
driver.close()
driver.switch_to.window(window_before)

time.sleep(5)

# #Verify OS-type Junos and stored
smart_filter1 = driver.find_element(By.ID,"smartbtn")
smart_filter1.click()
time.sleep(3)
junos_option = driver.find_element_by_xpath("//input[@value='junos']")
junos_option.click()
time.sleep(2)
evo_option = driver.find_element_by_xpath("//input[@value='evo']")
evo_option.click()
time.sleep(2)
otr_option = driver.find_element_by_xpath("//input[@value='STORED']")
otr_option.click()
time.sleep(2)
apply_button = driver.find_element_by_xpath("//button[@data-type='apply']")
apply_button.click()
time.sleep(10)

# ****Details clicks and info****
table = driver.find_element(By.CLASS_NAME,'ag-center-cols-clipper')
link = table.find_element_by_xpath("//div/div/div/div/div/span/a")
link.click()
time.sleep(10)
window_after = driver.window_handles[1]
driver.switch_to.window(window_after)
window_after_title = driver.title  # get the window title
print(window_after_title)
navbar = driver.find_element_by_class_name("project-title")
if "Details" in navbar.text:
    print("Device details page")
else:
    print("device details page dint load")

#verify OS and Device state Stored
fail = 0
table_body = driver.find_element(By.CLASS_NAME,"ag-center-cols-clipper")
rows = table_body.find_elements_by_xpath("//div/div/div/div/div[7]")
for row in rows:
    if row == 'ON_THE_RACK':
        fail = 1
rd_tab = table_body.find_element_by_xpath("//div/div/div/div/div[4]")
time.sleep(5)
expand = rd_tab.find_element(By.TAG_NAME,'i')
expand.click()
rows_ostype = table_body.find_elements_by_xpath("//div/div/div/div/div[9]")
for row in rows_ostype:
    if row == 'evo':
        fail = 1
if fail == 0:
    print("OS type is Junos")
    worksheet.write('A17', 'Junos_Smart_filter_verify', bold)
    cell_format.set_bg_color('green')
    worksheet.write('B17', 'PASS', cell_format)
else:
    worksheet.write('A17', 'Junos_Smart_filter_verify', bold)
    cell_format.set_bg_color('red')
    worksheet.write('B17', 'FAIL', cell_format)
driver.close()
driver.switch_to.window(window_before)



workbook.close()
driver.quit()
