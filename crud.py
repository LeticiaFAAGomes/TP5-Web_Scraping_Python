from conexao_db import *
from modelos import *
from starlette.staticfiles import StaticFiles 
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
conn = conectar()
cursor = conn.cursor()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static") 
 

def consultar_tabelas(comando, tp):
    '''
    Esta função consulta as tabelas do SQLite3 a partir de um comando.
    
    Args:
        comando(str): Refere-se ao comando SQL.
    
    Returns:
        str: Retorna o resultado do comando SQL formatado em tabela.
    '''
    lista, armazenamento = [], []
    cursor.execute(comando)
    informacoes = cursor.fetchall()
    nomeColunas = [nome[0] for nome in cursor.description]
    try:
        for informacao in informacoes:
            dados = {coluna: resultado for coluna, resultado in zip(nomeColunas, informacao)}
            lista.append(Metadado(**dados))
            armazenamento.append(dados)
            
    except Exception as ex:
        print(ex)
    
    return Metadado().formatar(lista) + '\n', armazenamento
            


def criar_tabelas(comando):
    '''
    Esta função cria tabelas no SQLite3 a partir de um comando.
    
    Args:
        comando(str): Refere-se à um comando SQL.
    '''
    try:
        cursor.execute(comando)
            
    except Exception as ex:
        print(ex)


def criar_insert(comando, valores):
    '''
    Esta função insere INSERTs em uma tabela no SQLite3 a partir de um comando.
    
    Args:
        comando(str): Refere-se à um comando SQL.
        valores(str): Refere-se aos dados à serem adicionados na tabela.
    '''
    try:
        cursor.executemany(comando, valores)
                
    except Exception as ex:
        print(ex)
        