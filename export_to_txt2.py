import sqlite3

def export_domains_to_txt(db_path, table_name, output_file):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Executar a consulta para contar os domínios
    cursor.execute(f"SELECT domain, COUNT(*) AS vezes FROM {table_name} GROUP BY domain")
    
    # Abrir o arquivo de saída em modo de escrita
    with open(output_file, 'w') as file:
        # Escrever o cabeçalho no arquivo
        file.write("dominio\tvezes\n")
        
        # Iterar sobre os resultados da consulta e escrever no arquivo
        for row in cursor.fetchall():
            # Extrair os valores do domínio e da contagem
            domain, count = row
            
            # Escrever no arquivo no formato desejado
            file.write(f"{domain}\t{count}\n")
    
    # Fechar a conexão com o banco de dados
    conn.close()
    print(f"Dados exportados com sucesso para {output_file}")

# Exemplo de uso
db_path = 'pihole-FTL.db'
table_name = 'queries' 
output_file = 'output2.txt'

export_domains_to_txt(db_path, table_name, output_file)
