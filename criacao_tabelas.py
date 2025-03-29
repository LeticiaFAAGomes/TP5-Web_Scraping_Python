from crud import *
from web_scraping import eventos, dados_eventos, metadados


def executar_tabelas():
    '''Esta função cria todas as tabelas armazenadas nos arquivos .CSV na pasta tabelas e depois insere os dados nelas.'''
    
    criar_tabelas('''
        CREATE TABLE IF NOT EXISTS tb_evento (
            
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            nome  VARCHAR(40) NOT NULL,
            tipo  VARCHAR(15) NOT NULL 
        );              
    ''')
    
    criar_tabelas('''
        CREATE TABLE IF NOT EXISTS tb_dado_evento (
            
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            data       TEXT NOT NULL,
            local      TEXT NOT NULL,
            id_evento  INTEGER NOT NULL,
            
            FOREIGN KEY (id_evento) REFERENCES tb_evento(id)
        );              
    ''')
    
    criar_tabelas('''
        CREATE TABLE IF NOT EXISTS tb_metadado (
            
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo       VARCHAR(15) NOT NULL,
            metadado   TEXT NOT NULL,
            id_evento  INTEGER NOT NULL,
            
            FOREIGN KEY (id_evento) REFERENCES tb_evento(id)
        );              
    ''')
    
    criar_insert('INSERT OR IGNORE INTO tb_evento(id, nome, tipo) VALUES(:id, :nome, :tipo);',
                 [{'id':evento['id'],
                   'nome':evento['nome'],
                   'tipo':evento['tipo']} for evento in eventos])
    
    criar_insert('INSERT OR IGNORE INTO tb_dado_evento(id, data, local, id_evento) VALUES(:id, :data, :local, :id_evento);',
                 [{'id':dado_evento['id'],
                   'data':dado_evento['data'],
                   'local':dado_evento['local'],
                   'id_evento':dado_evento['id_evento']} for dado_evento in dados_eventos])
    
    criar_insert('INSERT OR IGNORE INTO tb_metadado(id, tipo, metadado, id_evento) VALUES(:id, :tipo, :metadado, :id_evento);',
                [{'id':metadado['id'],
                  'tipo':metadado['tipo'],
                  'metadado':metadado['metadado'],
                  'id_evento':metadado['id_evento']} for metadado in metadados])
    