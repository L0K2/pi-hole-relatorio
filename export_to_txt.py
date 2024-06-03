import sqlite3

# Função para exportar dados de uma tabela para um arquivo txt
def export_to_txt(db_path, table_name, output_file):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Executar a consulta para obter todos os dados da tabela
    cursor.execute(f"SELECT * FROM {table_name}")
    
    # Obter os nomes das colunas
    column_names = [description[0] for description in cursor.description]
    
    # Abrir o arquivo de saída em modo de escrita
    with open(output_file, 'w') as file:
        # Escrever os nomes das colunas no arquivo
        file.write('\t'.join(column_names) + '\n')
        
        # Iterar sobre as linhas dos resultados da consulta e escrever no arquivo
        for row in cursor.fetchall():
            row_str = '\t'.join(map(str, row))
            file.write(row_str + '\n')
    
    # Fechar a conexão com o banco de dados
    conn.close()
    print(f"Dados exportados com sucesso para {output_file}")

# Exemplo de uso
db_path = 'pihole-FTL.db'
table_name = 'queries'
output_file = 'output.txt'

export_to_txt(db_path, table_name, output_file)
