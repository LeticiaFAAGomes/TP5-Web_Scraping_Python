from bs4 import BeautifulSoup
import requests
import os
import google.generativeai as genai
import google.api_core.exceptions
from dotenv import load_dotenv
from dateutil.parser import parse 
import time

eventos, dados_eventos, metadados= [], [], []

load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_KEY')
genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel(model_name='gemini-2.0-flash')


def achar_url(url):
    '''
    Esta função faz com que a URL de um site se torne manipulável no Python.
    
    Args:
        url: Refere-se a URL de um site.
    Returns:
        bs4.BeautifulSoup: Retorna um HTML estruturado para o Python.
    '''
    html = requests.get(url).content
    return BeautifulSoup(html, 'html.parser')


def achar_texto(atributo, nome, tipo=None, restricao=None):
    '''
    Esta função encontra o texto especificado da tag HTML
    
    Args:
        atributo(str): Refere-se ao tipo de atributo do HTML.
        nome(False/str): Refere-se ao valor do atributo HTML.
        tipo(None/str): Refere-se a decisao entre find_all() ou find();
        restricao(str/None): Refere-se a um nome específico de uma tag HTML. 
    
    Returns:
        bs4.element.Tag / str: retorna o elemento HTML encontrado.
    '''
    if (tipo):
        nomes, c = '', 0
        for attr in soup.find_all(attrs={atributo:nome}):
            if restricao == attr.get_text(strip=True):
                return attr
            if c > 0: nomes += ' '
            c+=1
            nomes += attr.get_text(strip=True)
        return nomes
    return soup.find(attrs={atributo:nome})


def achar_informacoes(url):
    '''
    Esta função encontra o tipo e o nome do evento com ajuda do Gemini IA.
    
    Args:
        url: Refere-se a URL de um site.
        
    Returns:
        tuple: 
            tipo(str): Retorna tipo de evento.
            nome(str): Retorna ao nome do evento.
    '''
    try:
        prompt = 'Defina o tipo de evento (música, teatro, arte, stand-up etc.) a partir da URL especificada em apenas uma palavra.'
        tipo = model.generate_content([url, prompt]).text.strip() 

        prompt = '''Analise a url lendo as informações e responda apenas o nome do evento 
        (caso seja show (não clássico), responda como o nome da banda), sem qualquer outra informação adicional'''
        nome = model.generate_content([url, prompt]).text.strip() 
        
        return tipo, nome
        
    except (google.api_core.exceptions.ResourceExhausted):
        time.sleep(5)
        return achar_informacoes(url)


def padronizar_data(data):
    '''
    Esta função padroniza a data para o formato: AAAA-MM-DD
    
    Returns:
        str: Retorna data no formato: AAAA-MM-DD.
    '''
    return parse(data, fuzzy=True).strftime('%Y-%m-%d')
        
        
def padronizar_local(local):
    '''
    Esta função padroniza o local no formato "local, cidade, país" com ajuda do Gemini IA.
    
    Args:
        url: Refere ao local não padronizado.
        
    Returns:
        str: Retorna o local padronizado no formato: local, cidade, país
    '''
    try:
        prompt='''Pesquise o local e padronize(em português) apenas organizando no formato "nome do local, cidade, país", 
        sem qualquer informação adicional'''
        
        return model.generate_content([local, prompt]).text.strip()
    
    except (google.api_core.exceptions.ResourceExhausted):
        time.sleep(5)
        return padronizar_local(local)


def definir_ambiente(local, data):
    '''
    Esta função define o tipo de ambiente com base no local e no clima do local na data.
    
    Args: 
        local(str): Refere-se ao local do evento.
        data(str): Refere-se a data do evento
    Returns:
        str: Retorna o tipo de ambiente do evento.
    '''
    try: 
        prompt = f'''
        Analise o local e informações, considere também o clima previsto na data do evento ({data}). 
        Depois responda apenas com expressão "Ar Livre" ou "Fechado" de acordo com a probabilidade do evento, sem qualquer outra informação adicional.
        '''
        response = model.generate_content([local, prompt])
        
        return response.text.strip()
    
    except (google.api_core.exceptions.ResourceExhausted, ValueError):
        time.sleep(5)
        return definir_ambiente(local, data)


def add_evento(nome, tipo):
    '''
    Esta função adiciona um dicionário para a lista `eventos`.
    
    Args:
        nome(str): Refere-se ao nome do evento.
        tipo(str): Refere-se ao tipo do evento.
    '''
    eventos.append({'id':len(eventos)+1, 'nome': nome, 'tipo':tipo})


def add_dado_evento(id_evento, data, local):
    '''
    Esta função adiciona um dicionário para a lista `dados_eventos`.
    
    Args:
        id_evento(str): Refere-se ao id do evento.
        data(str): Refere-se a data do evento.
        local(str): Refere-se ao local do evento.
    '''
    dados_eventos.append({'id':len(dados_eventos)+1, 'id_evento':id_evento, 'data': data, 'local':local})
    
    
def add_metadado(id_evento, tipo, metadado):
    '''
    Esta função adiciona um dicionário para a lista `metadados`.
    
    Args:
        id_evento(str): Refere-se ao id do evento.
        url(str): Refere-se a URL do evento.
        ambiente(str): Refere-se ao ambiente do evento.
    '''
    metadados.append({'id':len(metadados)+1,'id_evento':id_evento, 'tipo':tipo, 'metadado':metadado})         


soup = achar_url('https://www.metallica.com/tour/2025-04-26-toronto-ontario-canada.html')
local = padronizar_local(achar_texto('class', 'event-header-eventName').get_text(strip=True) + ', ' + achar_texto('class', 'desktop', 'all'))
data = padronizar_data(achar_texto('class', 'event-header__date').get_text(strip=True))
tipo, nome = achar_informacoes('https://www.metallica.com/tour/2025-04-26-toronto-ontario-canada.html')
ambiente = definir_ambiente(local, data)

add_evento(nome, tipo)
add_dado_evento(len(eventos), data, local)
add_metadado(len(eventos), 'url', 'https://www.metallica.com/tour/2025-04-26-toronto-ontario-canada.html')
add_metadado(len(eventos), 'ambiente', ambiente)


soup = achar_url('https://www.linkinpark.com/tour')
local = padronizar_local(achar_texto('class', 'venue', 'all', 'Scotiabank Arena').get_text(strip=True) + ', ' + achar_texto('class', ['city-country'], 'all', 'Toronto, ON').get_text(strip=True))
data = padronizar_data(achar_texto('class', 'starts-at', 'all', '08 Aug 2025').get_text(strip=True))
tipo, nome = achar_informacoes('https://www.linkinpark.com/tour')
ambiente = definir_ambiente(local, data)

add_evento(nome, tipo)
add_dado_evento(len(eventos), data, local)
add_metadado(len(eventos), 'url', 'https://www.linkinpark.com/tour')
add_metadado(len(eventos), 'ambiente', ambiente)


soup = achar_url('https://www.ironmaiden.com/tour/run-for-your-lives-world-tour/')
local = padronizar_local(achar_texto('class', 'tour-info-col', 'all', 'Trondheim Rocks (Festival)').get_text(strip=True) + ', ' + achar_texto('class', 'tour-info-col', 'all', 'Trondheim, NORWAY').get_text(strip=True))
data = padronizar_data(achar_texto('class', 'tour-info-col', 'all', '5 Jun 2025').get_text(strip=True))
tipo, nome = achar_informacoes('https://www.ironmaiden.com/tour/run-for-your-lives-world-tour/')
ambiente = definir_ambiente(local, data)

add_evento(nome, tipo)
add_dado_evento(len(eventos), data, local)
add_metadado(len(eventos), 'url', 'https://www.ironmaiden.com/tour/run-for-your-lives-world-tour/')
add_metadado(len(eventos), 'ambiente', ambiente)


soup = achar_url('https://www.sampaingressos.com.br/afonso+padilha+stand+up+comedy+no+marte+hall+sp+marte+hall')
local = padronizar_local(achar_texto('class', 'local_espetaculo').get_text(strip=True) + ', ' + achar_texto('class', 'endereco_local_espetaculo').get_text(strip=True))
data = padronizar_data(achar_texto('class', 'texto_temporada').get_text(strip=True))
tipo, nome = achar_informacoes('https://bit.ly/afonso-padilha-stand-up-comedy')
ambiente = definir_ambiente(local, data)

add_evento(nome, tipo)
add_dado_evento(len(eventos), data, local)
add_metadado(len(eventos), 'url', 'https://bit.ly/afonso-padilha-stand-up-comedy')
add_metadado(len(eventos), 'ambiente', ambiente)


soup = achar_url('https://www.sampaingressos.com.br/mateus+solano+em+o+figurante+teatro+renaissance')
local = padronizar_local(achar_texto('class', 'local_espetaculo').get_text(strip=True) + ', ' + achar_texto('class', 'endereco_local_espetaculo').get_text(strip=True)) 
data = padronizar_data(achar_texto('class', 'texto_temporada').get_text(strip=True))
tipo, nome = achar_informacoes('https://bit.ly/mateus-solano-em-o-figurante')
ambiente = definir_ambiente(local, data)

add_evento(nome, tipo)
add_dado_evento(len(eventos), data, local)
add_metadado(len(eventos), 'url', 'https://bit.ly/mateus-solano-em-o-figurante')
add_metadado(len(eventos), 'ambiente', ambiente)


soup = achar_url('https://bit.ly/54o-festival-de-inverno-de-campos-do-jordao')
local = padronizar_local(achar_texto('p', False, 'all', '6 de julho, sábado, 16h00 – Parque Capivari').get_text(strip=True)[28:])
data = padronizar_data(achar_texto('p', False, 'all', '6 de julho, sábado, 16h00 – Parque Capivari').get_text(strip=True)[:10]+ '2025')
tipo, nome = achar_informacoes('https://camposdojordao.com.br/54o-festival-de-inverno-de-campos-do-jordao-2024-tudo-sobre-a-programacao-e-ingressos-gratuitos.html')
ambiente = definir_ambiente(local, data)

add_evento(nome, tipo)
add_dado_evento(len(eventos), data, local)
add_metadado(len(eventos), 'url', 'https://bit.ly/54o-festival-de-inverno-de-campos-do-jordao')
add_metadado(len(eventos), 'ambiente', ambiente)
