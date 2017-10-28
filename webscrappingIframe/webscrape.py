from selenium import webdriver
from bs4 import BeautifulSoup
import json

def read_file_pun():
    f = open(r'C:\Users\Brian\PycharmProjects\parsingIframe\webscrappingIframe\list.txt')
    pun_list = [line.rstrip('\n') for line in f]
    f.close()
    return pun_list

def write_json(pun_dictionary):
    with open(r'C:\Users\Brian\PycharmProjects\parsingIframe\webscrappingIframe\result.txt', 'w') as f:
        json.dump(pun_dictionary, f)

def main():
    pun_list = read_file_pun()
    api_result = [parse_api(pun) for pun in pun_list]
    pun_dictionary = dict(zip(pun_list, api_result))
    pun_dictionary = json.dumps(pun_dictionary)
    write_json(pun_dictionary)


def parse_api(pun):
    chrome_path = r"D:\Program Files (x86)\PythonStuff\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)
    driver.get("https://www2.oktax.onenet.net/GrossProduction/gp_PublicSearchPUNbyLegal.php")
    driver.find_element_by_css_selector("input[type='radio'][value='PUN']").click()
    searchBox = driver.find_element_by_css_selector("#OTCtxtPUN")
    searchBox.send_keys(pun)

    driver.find_element_by_css_selector("input[name='submit']").click()
    link = driver.find_element_by_xpath(
        """//*[@id="container"]/form/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a""")
    link.click()

    driver.switch_to.frame("iframePopup")
    test = driver.page_source
    soup = BeautifulSoup(test, "lxml")
    table = soup.select("#tabs-1")
    data = []
    rows = table[0].find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [element.text.strip() for element in cols]
        data.append([element for element in cols if element])

    driver.close()
    api = data[3][1][5:]
    api_list = api.split(', ')
    return api_list

main()
