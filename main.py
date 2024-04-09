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

'''
O Objetivo é Receber um arquivo de diploma em XML e validar no MEC se ele é válido ou não.

Retornos:
True - Diploma Válido e em Conformidade com o MEC
False - Diploma inválido

'''
file_path = '/home/ubuntu/workspace/pmirandaf/valida_diploma_xml/diploma-erro.xml'
url_validador = 'https://verificadordiplomadigital.mec.gov.br/diploma'

url_validado='https://verificadordiplomadigital.mec.gov.br/detalhes'

options = Options()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

wait = WebDriverWait(driver, 20)

driver.get(url_validador)

#Encontrando o botão de input na página
file_input = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/input')

#Enviando o caminho do arquivo que quero fazer upload no input
file_input.send_keys(file_path)


#Clicando no botão verificar
driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/button/div/div/span').click()

'''
Após inserir o arquivo e clicar em Verificar, é carregada a página detalhes que possui o resultado da verificação do diploma em XML 
'''

wait.until(url_to_be('https://verificadordiplomadigital.mec.gov.br/detalhes'))


driver.save_screenshot('screenshot.png')


'''
Colhendo a informação sobre o resultado da validação
True - Diploma Digital em Conformidade
False - Diploma Digital Inválido

'''

elementos=driver.find_element(By.XPATH ,'//*[@id="content"]/div/div[1]/div[2]/p')

elementos=str(elementos.text).strip()


if elementos == 'Diploma Digital em Conformidade':
    print(True)
elif elementos == 'Diploma Digital Inválido':
    print(False)





driver.quit()
