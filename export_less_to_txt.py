import sqlite3
from tabulate import tabulate

def export_domains_to_txt(db_path, table_name, output_file):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Executar a consulta para contar os domínios
    cursor.execute(f"SELECT domain, COUNT(*) AS vezes FROM {table_name} WHERE client IN ('192.168.0.190', '192.168.0.104', '192.168.0.100', '127.0.0.1') GROUP BY domain")
    
    #Cria matrix que irá conter os dados da query e a inicializa com cabeçalhos/colunas
    data = [["Domínio", "Vezes"]]
    
    #Itera sobre o resultado da query adicionando a matrix de dados
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
output_file = 'output2.txt'

export_domains_to_txt(db_path, table_name, output_file)
