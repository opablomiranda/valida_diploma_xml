from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import url_to_be
from selenium.webdriver.common.keys import Keys
import time




file_path = "/home/ubuntu/workspace/pmirandaf/valida_diploma_xml/diploma.xml"
url_validador = "https://verificadordiplomadigital.mec.gov.br/diploma"

url_validado="https://verificadordiplomadigital.mec.gov.br/detalhes"

options = Options()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

wait = WebDriverWait(driver, 20)

driver.get(url_validador)

file_input = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[3]/input")
file_input.send_keys(file_path)

driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[3]/button/div/div/span").click()




wait.until(url_to_be("https://verificadordiplomadigital.mec.gov.br/detalhes"))





if wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'em Conformidade')]"))):

    print("Diploma é Válido!")

if wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Inválido')]"))):
    print("Diploma é inválido!")

driver.close()

