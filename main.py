from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service



# Inicialize o driver do Selenium (neste caso, estou usando o Firefox)
print("Abrindo o webdriver")
gecko_driver_path = "/usr/local/bin/geckodriver"
service = Service(gecko_driver_path)
driver = webdriver.Firefox(service=service)


print(f"{driver} aberto ")
# Abra a página da web
driver.get("https://verificadordiplomadigital.mec.gov.br/diploma")

print(f"Get na pagina https://verificadordiplomadigital.mec.gov.br/diploma")

# Espere até que o botão "Escolher arquivo" esteja clicável
print(f"Esperando contagem")
wait = WebDriverWait(driver, 10)

print(f"Contagem finalizada")
choose_file_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Escolher arquivo')]")))
print(f"Achando o escolher arquivo na pagina")

# Clique em um elemento diferente que dispara o evento de clique no botão "Escolher arquivo"
# Neste exemplo, vamos clicar no texto "Escolher arquivo"

print(f"Achando o escolher arquivo na pagina")
choose_file_button_text = driver.find_element(By.XPATH, "//span[contains(text(), 'Escolher arquivo')]")

wait = WebDriverWait(driver, 10)

print(f"Indo clicar no botão")
choose_file_button_text.click()

wait = WebDriverWait(driver, 10)
print(f"botão clicado")
# Localize o elemento de input do arquivo após clicar no texto
# Esperamos que o elemento fique visível

print(f"selecionando arquivo")
file_input = wait.until(EC.visibility_of_element_located((By.ID, "select-file")))
print("Clique no arquivo")

# Insira o caminho do arquivo XML que você deseja carregar
print(f"pegando o diploma")
file_input.send_keys("home/ubuntu/workspace/pmirandaf/valida_diploma_xml/diploma.xml")

print(f"diploma selecionado")
# Espere até que o botão "Verificar" esteja clicável

print(f"Indo verificar o diploma")
verify_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Verificar')]")))

# Clique no botão "Verificar"
verify_button.click()
print(f"Clicado o botão de verificar")

# Espere até que a página de detalhes seja carregada (após o redirecionamento)

print(f"Esperando o carregamento dos detalhes")
wait.until(EC.url_to_be("https://verificadordiplomadigital.mec.gov.br/detalhes"))

print(f"Carregamento de detalhes finalizado")
# Verifique se a mensagem de confirmação está presente na página de detalhes


confirmation_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'ksHDuE')]//span[contains(@class, 'kZYWkb')]")))
print(f"Confirmação da tela de verificação")
# Verifique se o texto contém a mensagem desejada
if "Diploma Digital em Conformidade" in confirmation_message.text:
    print("O diploma está em conformidade.")
else:
    print("O diploma não está em conformidade.")

# Feche o navegador após terminar
driver.quit()