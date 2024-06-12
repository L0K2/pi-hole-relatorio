import sqlite3
from tabulate import tabulate

# Função para exportar dados de uma tabela para um arquivo txt
def export_to_txt(db_path, table_name, output_file):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Executar a consulta para obter todos os dados da tabela
    cursor.execute(f"SELECT * FROM {table_name} WHERE client IN ('192.168.0.190', '192.168.0.104', '192.168.0.100', '127.0.0.1')")
    
    # Obter os nomes das colunas
    column_names = [description[0] for description in cursor.description]
    #Cria matrix que irá conter os dados da query e a inicializa com cabeçalhos/colunas
    data = [column_names]
    #Itera sobre o resultado da query adicionando a matarix de dados
    for row in cursor.fetchall():
        data.append(row)


    table = tabulate(data, headers="firstrow", tablefmt="grid")
    # Abrir o arquivo de saída em modo de escrita
    with open(output_file, 'w') as file:
        # Escreve a tabela de resultado no arquivo de output
        file.write(table)
    

    # Fechar a conexão com o banco de dados
    conn.close()
    print(f"Dados exportados com sucesso para {output_file}")

# Exemplo de uso
db_path = 'pihole-FTL.db'
table_name = 'queries'
output_file = 'output.txt'

export_to_txt(db_path, table_name, output_file)
