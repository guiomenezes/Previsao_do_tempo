import datetime
import smtplib
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', 'window-size=1000,1000', '--disable-notifications', '--headless']

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option("prefs", {'download.prompt_for_download':False, 
        "profile.default_content_setting_values.notifications":2,
        "profile.default_content_setting_values.automatic_downloads": 1
        })
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def enviar_previsao():
    driver = iniciar_driver()

    driver.get('https://www.tempo.com/peruibe.htm')
    sleep(5)

    temp_atual = driver.find_element(By.XPATH, "//*[@id='d_hub_1']/div[1]/div/div/div/div/span[1]").text
    condicao_atual = driver.find_element(By.XPATH, "//div/span[@class='descripcion']").text

    titulo_amanha = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/section[2]/div/ul/li[2]/span/span[1]").text
    temp_max_amanha = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/section[2]/div/ul/li[2]/span/span[4]/span[1]").text
    temp_min_amanha = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/section[2]/div/ul/li[2]/span/span[4]/span[3]").text
    titulo_dia2 = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/section[2]/div/ul/li[3]/span/span[1]").text
    temp_max_dia2 = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/section[2]/div/ul/li[3]/span/span[4]/span[1]").text
    temp_min_dia2 = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/section[2]/div/ul/li[3]/span/span[4]/span[3]").text
    titulo_dia3 = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/section[2]/div/ul/li[4]/span/span[1]").text
    temp_max_dia3 = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/section[2]/div/ul/li[4]/span/span[4]/span[1]").text
    temp_min_dia3 = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/section[2]/div/ul/li[4]/span/span[4]/span[3]").text

    #Envio de e-mail com as informações

    #Primeiro passo - Configurações de login
    EMAIL_ADDRESS = 'guilherme.test.emails@gmail.com'
    EMAIL_PASSWORD = 'fyds rjhs xwog oanb'

    #Criar e enviar o email
    data_hoje = datetime.datetime.now().strftime('%d/%m/%Y')
    mail = EmailMessage()
    mail['Subject'] = f'Previsão do tempo para os próximos três dias - {data_hoje}.'
    mensagem = f'''
        Previsão do tempo em Peruíbe.<br>
        <strong>Temperatura atual:</strong> {temp_atual}C<br>
        <strong>Condição atual:</strong> {condicao_atual}<br><br>

        <strong>{titulo_amanha}</strong> — Máxima: {temp_max_amanha}C — Mínima: {temp_min_amanha}C<br>
        <strong>{titulo_dia2}</strong> — Máxima: {temp_max_dia2}C — Mínima: {temp_min_dia2}C<br>
        <strong>{titulo_dia3}</strong> — Máxima: {temp_max_dia3}C — Mínima: {temp_min_dia3}C<br>
        '''
    mail['From'] = EMAIL_ADDRESS
    mail['To'] = 'guilherme.menezes@outlook.com'
    mail.add_header('Content-Type', 'text/html')
    mail.set_payload(mensagem.encode('utf-8'))

    #Enviar email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as email:
        email.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        email.send_message(mail)

while True:
    print(f'Executando em {datetime.datetime.now()}')
    enviar_previsao()
    print('E-mail enviado. Aguardando 24 horas.')
    sleep(86400)
