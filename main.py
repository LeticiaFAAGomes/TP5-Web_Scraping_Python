from crud import *
import os
if (not os.path.getsize('db_eventos.db') > 0):
    from criacao_tabelas import *
    executar_tabelas()

amarelo = '\x1b[38;5;229m'

@app.get('/') 
async def name(request: Request):  
    return templates.TemplateResponse("index.html", {"request": request, 
                                                     "tp5_1": tp5_1[1],
                                                     "tp5_2": tp5_2[1],
                                                     "tp5_3": tp5_3[1],
                                                     "tp5_4": tp5_4[1],
                                                     "tp5_5": tp5_5[1]})  


# 1. Mostrar todos os eventos com suas datas, localização, e tipo de evento.
print(f'{amarelo}TP5.1 - Mostrar todos os eventos com suas datas, localização, e tipo de evento.')
tp5_1 = consultar_tabelas("""
        SELECT E.nome, E.tipo , D.data, D.local
        FROM tb_evento       E
        JOIN tb_dado_evento  D  ON D.id_evento = E.id     
        ORDER BY D.data;  
    """, "tp5.1")
print(tp5_1[0])

# 2. Mostrar os dados dos 2 eventos mais próximos de iniciar. 
print(f'{amarelo}TP5.2 - Mostrar os dados dos 2 eventos mais próximos de iniciar. ')
tp5_2  = consultar_tabelas("""
        SELECT E.nome, D.local, D.data
        FROM tb_evento      E
        JOIN tb_dado_evento D  ON D.id_evento = E.id
        ORDER BY D.data LIMIT 2;
    """, "tp5.2")
print(tp5_2[0])
 
# 3. Mostrar os eventos que acontecem no Brasil. 
print(f'{amarelo}TP5.3 - Mostrar os eventos que acontecem no Brasil. ')
tp5_3  = consultar_tabelas("""
        SELECT E.nome, D.data, D.local
        FROM tb_evento       E
        JOIN tb_dado_evento  D  ON D.id_evento = E.id
        WHERE D.local LIKE '%Brasil';
    """, "tp5.3")
print(tp5_3[0])

# 4. Mostrar todos os eventos que são ao ar livre. 
print(f'{amarelo}TP5.4 - Mostrar todos os eventos que são ao ar livre. ')
tp5_4  = consultar_tabelas("""
        SELECT E.nome, E.tipo, D.data, D.local, M.metadado AS ambiente
        FROM tb_evento       E
        JOIN tb_dado_evento  D  ON D.id_evento = E.id
        JOIN tb_metadado     M  ON M.id_evento = E.id
        WHERE M.metadado = 'Ar Livre';
    """, "tp5.4")
print(tp5_4[0])

# 5. Mostrar todos os Metadados por evento.
print(f'{amarelo}TP5.5 -  Mostrar todos os Metadados por evento.')
tp5_5  = consultar_tabelas("""
        SELECT E.nome, GROUP_CONCAT(M.tipo, ', ') AS Chaves, GROUP_CONCAT(M.metadado, ', ') AS Metadados
        FROM      tb_evento   E
        LEFT JOIN tb_metadado M ON M.id_evento = E.id
        GROUP BY E.id;
    """, "tp5.5")
print(tp5_5[0])


desconectar(conn)
