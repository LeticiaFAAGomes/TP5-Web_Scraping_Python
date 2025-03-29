azul, negrito, reset = '\x1b[38;5;117m', '\033[1m', '\x1b[22m'


class Metadado:
    def __init__(self, **dados):
        '''
        Esta função inicializa um novo registro de dados.
        
        Args:
            dados(dict): refere-se à um dicionario de dados.
        '''
        self.dados = dados


    def encontrarTamanho(self, lista, cabecalho):
        '''
        Esta função acha o tamanho máximo que uma string ocupa.
    
        Args:
            lista(list): Refere-se aos dados que irão ter os caracteres contados.
            cabecalho(list[str]): Refere-se a chave do dicionário
        
        Returns:
            int: número máximo de caracteres que dados pode ocupar em uma linha.
        '''
        return max(len(str(dado.dados.get(cabecalho, ''))) for dado in lista) + 4


    def formatar(self, lista):
        '''
        Esta função retorna uma tabela com os dados da lista.
        
        Args:
            lista(list): Refere-se aos dados de uma lista
        
        Returns:
            str: Retorna uma string com dados formatados em tabela.
        '''
        cabecalhos = lista[0].dados.keys()
        tamanhos = {cabecalho: self.encontrarTamanho(lista, cabecalho) for cabecalho in cabecalhos}

        cabeçalhos_formatados = '┃ ' + ' ┃ '.join(f'{cabecalho:{tamanhos[cabecalho]}}' for cabecalho in cabecalhos) + ' ┃'
        qtdCaracteres = sum([tamanhos[nome]+3 for nome in cabecalhos])-1
        resultado = []

        resultado.append(f'{negrito}{azul}┏{"┅"*qtdCaracteres}┓\n{cabeçalhos_formatados}\n┠{"━"*qtdCaracteres}┨{reset}')
        for ocorrencia in lista:
            campos = '┃ ' + ' ┃ '.join(f'{str(ocorrencia.dados.get(nome, "")):{tamanhos[nome]}}' for nome in cabecalhos) + ' ┃'
            resultado.append(campos)
        resultado.append(f'┗{"━"*qtdCaracteres}┛')
        return '\n'.join(resultado)
        