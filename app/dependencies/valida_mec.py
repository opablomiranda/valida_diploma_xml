from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import url_to_be
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from fastapi import HTTPException, status
import os

'''     
O Objetivo é Receber um arquivo de diploma em XML e validar no MEC se ele é válido ou não.

Retornos:
True - Diploma Válido e em Conformidade com o MEC
False - Diploma inválido

'''

def validar_diploma_mec(file_path):
    
    try:
        #Criando o caminho absoluto do arquivo
        file_path_abs= os.path.abspath(file_path)

        #file_path = '/home/ubuntu/workspace/pmirandaf/valida_diploma_xml/app/dependencies/diploma-erro.xml'
        url_validador = 'https://verificadordiplomadigital.mec.gov.br/diploma'

        url_resultado='https://verificadordiplomadigital.mec.gov.br/detalhes'

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080') 
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        wait = WebDriverWait(driver, 20)


        driver.get(url_validador)

        #Encontrando o botão de input na página
        file_input = driver.find_element(By.ID,"select-file")


        #Enviando o caminho absoluto do arquivo que quero fazer upload no input
        file_input.send_keys(file_path_abs)

        #driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/button/div/div/span').click()

        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.styles__Container-k79jbo-0.eiruAi span')))

        button.click()
        '''
        Após inserir o arquivo e clicar em Verificar, é carregada a página detalhes que possui o resultado da verificação do diploma em XML 
        '''
        #Aguardando a página detalhes carregar
        wait.until(url_to_be(url_resultado))

        '''
        Colhendo a informação sobre o resultado da validação
        True - Diploma Digital em Conformidade
        False - Diploma Digital Inválido

        '''
        elementos=driver.find_element(By.XPATH ,'//*[@id="content"]/div/div[1]/div[2]/p')

        #Pegando o texto da página que informa se está em conformidade ou inválido o diploma
        elementos=str(elementos.text).strip()

        #Se o diploma é válido, a página detalhes mostra essa informação
        if elementos == 'Diploma Digital em Conformidade':
            driver.quit()
            return True
        
        #Se o diploma é inválido, a página detalhes mostra essa informação
        elif elementos == 'Diploma Digital Inválido':
            driver.quit()
            return False
         
    except NoSuchElementException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Elemento não encontrado na página.")
    except TimeoutException as exc:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Tempo limite excedido durante a interação com a página.")
    except WebDriverException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro no WebDriver: {exc}")
