import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import os
import webbrowser
import requests
from selenium.webdriver.chrome.options import Options

# --- To do --- #
# 
# ---       --- #
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(diretorio_atual, "output.html")

chrome_options = Options()

# Adicionar a opção de rodar o Chrome em modo headless
chrome_options.add_argument("--headless")  # Roda o Chrome sem abrir a janela gráfica
chrome_options.add_argument("--disable-gpu")  # Desativa o uso de GPU, útil para o headless
chrome_options.add_argument("--no-sandbox")  # Para evitar problemas com o sandbox em alguns sistemas

driver = webdriver.Chrome()

listaPacientes =[]

def loginNoSite():
    driver.get("https://doc.doclogos.com/totalkids/login")

    login_input = driver.find_element(By.XPATH, "//*[@id='m_login']/div/div/div[2]/form/div[1]/input")
    senha_input = driver.find_element(By.XPATH, "//*[@id='m_login']/div/div/div[2]/form/div[2]/input")
    botao_login = driver.find_element(By.XPATH, "//*[@id='m_login_signin_submit']")

    login_input.send_keys("XXXX")
    senha_input.send_keys("XXXX")
    botao_login.click()

def verAgenda():
    driver.get("https://doc.doclogos.com/totalkids/agenda")

def selecionarData():

    #Clicar no botao que abre o calendario
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='m_datepicker_dataselecionada']"))
    )
    botao_calendario = driver.find_element(By.XPATH, "//*[@id='m_datepicker_dataselecionada']")
    botao_calendario.click()
    
    #buscar data atual no calendario
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "today"))
    )
    botao_dia_atual = driver.find_element(By.CLASS_NAME, "today")
    today_data_date = int(botao_dia_atual.get_attribute('data-date'))

    #original para ser usado na vespera#
    next_day_data_date = today_data_date + 86400000 

    #teste dia aleatorio = numero + 86400000 
    #next_day_data_date = 1742256000000 + 86400000 
    ##

    botao_dia_seguinte = driver.find_element(By.CSS_SELECTOR, f'[data-date="{next_day_data_date}"]')
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-date="{next_day_data_date}"]'))
    )


    
    botao_dia_seguinte.click()
    
def buscarPacientes():
    
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-list-item.m-fc-event--metal"))
    )
    pacientes_marcados = driver.find_elements(By.CSS_SELECTOR, ".m-fc-event--metal, .m-fc-event--accent")

    paciente_atual = 0
    pacientes_agenda = 0

    for paciente in pacientes_marcados:
        
        pacientes_agenda+=1

    for i in range(paciente_atual,pacientes_agenda):

        for paciente in pacientes_marcados[paciente_atual:paciente_atual+1]:
        
            paciente_horario = paciente.find_element(By.CSS_SELECTOR, ".fc-list-item-time").text
            paciente_horario = horarioCorrigido(paciente_horario)

            paciente_nome = paciente.find_element(By.CSS_SELECTOR, ".fc-list-item-title a").text
            paciente_nome, paciente_ultimo_nome, paciente_codigo = criarNomeSimplificado(paciente_nome)
            
            listaPacientes.append({
                "horario": paciente_horario,
                "Primeiro nome": paciente_nome,
                "Ultimo nome": paciente_ultimo_nome,
                "Codigo":paciente_codigo
            })

            
        
        paciente_atual+=1

    
    buscarContatoPaciente()

def buscarContatoPaciente():
    
    for paciente in listaPacientes:

        driver.get(f"https://doc.doclogos.com/totalkids/pacientes/manipular/{paciente['Codigo']}")        
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='TELEFONE1']"))
        )
        contato_paciente = driver.find_element(By.XPATH, "//*[@id='TELEFONE1']").get_attribute('value')
        contato_paciente = numeroCorrigido(contato_paciente)
        

        paciente['contato'] = contato_paciente

        print (paciente['horario']+" "+paciente['Primeiro nome']+" "+paciente['Ultimo nome'])
        print ("Whatsapp: "+ paciente['contato'])
        print ("")
        
    print(listaPacientes)

def numeroCorrigido(telefone):
    numero_apenas_digitos = re.sub(r'\D', '', telefone)  # \D corresponde a qualquer caractere não numérico
    
    if len(numero_apenas_digitos) == 11:
        # Se já tiver 11 dígitos, retorna como está
        return numero_apenas_digitos
    else:
        # Se tiver menos de 11 dígitos, pega os últimos 9 e adiciona o DDD 21
        numero_final = '21' + numero_apenas_digitos[-9:]
        return numero_final

def turnoDoDia():
    horario_atual = datetime.datetime.now().time()
    if horario_atual.hour>=12:
        saudacao = "Boa%20tarde!%20"
        return saudacao
    else:
        saudacao = "Bom%20dia!%20"
        return saudacao

def criarNomeSimplificado(nome):
    nome_parts = nome.split()
    # Adicionao o codigo ao retorno
    nome_codigo=nome_parts[-1].replace("(", "").replace(")", "")
    #-1 representa o ultimo nome
    return nome_parts[0], nome_parts[-2],nome_codigo

def horarioCorrigido(horario):
    horario_errado = horario.split()
    #-1 representa o ultimo nome
    horario_corrigido = horario_errado[0] 
    return horario_corrigido

def outputHTML():
    
    with open(caminho_arquivo, "w") as file:
        file.write("<html><body style='text-align: center;'>\n <p style= 'font-size: 20px;'>CONFIRMAÇÃO CONSULTAS DE AMANHÃ</p>")
        print("Arquivo output.html criado com sucesso!")

    saudacao = turnoDoDia()

    for paciente in listaPacientes:
        
        artigo, pronome_preposicao = generoNome(paciente["Primeiro nome"])

        with open(caminho_arquivo, "a") as file:
            file.write(f"<p> <strong>{paciente["horario"]} {paciente["Primeiro nome"]} {paciente["Ultimo nome"]}</strong> <a href='https://web.whatsapp.com/send/?phone=55{paciente["contato"]}&text={saudacao}Meu%20nome%20%C3%A9%20Gabriel%20e%20serei%20o%20nutricionista%20respons%C3%A1vel%20pela%20consulta%20d{artigo}%20{paciente["Primeiro nome"]}%20{paciente["Ultimo nome"]}%20amanh%C3%A3%20%C3%A0s%20{paciente["horario"]}.%20Confirma%20a%20presen%C3%A7a%20{pronome_preposicao}?' target='_blank'>Whatsapp</a>\n")

    with open(caminho_arquivo, "a") as file:
        file.write("</body></html>\n")
        print("Edição output.html finalizada com sucesso!")

def generoNome(nome):
    # Realizando a requisição à API do Genderize
    url = f"https://api.genderize.io?name={nome}&country_id=BR"
    response = requests.get(url)
    resultado = response.json()

    # Exibindo o resultado (opcional, pode ser removido)
    #print(resultado)

    # Verificando o gênero retornado
    if 'gender' in resultado:
        if resultado['gender'] == 'male':
            artigo = "o"
            pronome_preposicao = "dele"
        elif resultado['gender'] == 'female':
            artigo = "a"
            pronome_preposicao = "dela"
        else:
            artigo = "X"  # Caso o gênero seja desconhecido ou não identificado
            pronome_preposicao = "delX"
    else:
        artigo = "X"  # Caso a API não retorne um gênero
        pronome_preposicao = "delX"

    return artigo, pronome_preposicao


horario_inicio = time.time()
print(f"Inicio: {horario_inicio}")

loginNoSite()
verAgenda()
selecionarData()
buscarPacientes()
outputHTML()

webbrowser.open(f'file://{caminho_arquivo}')

horario_fim = time.time()
print(f"Fim: {horario_fim}")

tempo_execucao = horario_fim - horario_inicio  # Em segundos
print(f"Tempo de execução: {tempo_execucao:.2f} segundos.")

time.sleep(10)

