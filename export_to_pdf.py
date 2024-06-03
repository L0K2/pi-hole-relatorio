from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import sqlite3

def export_domains_to_pdf(db_path, table_name, output_file):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Executar a consulta para contar os domínios
    cursor.execute(f"SELECT domain, COUNT(*) AS vezes FROM {table_name} GROUP BY domain")
    
    # Obter os resultados da consulta
    data = cursor.fetchall()
    
    # Fechar a conexão com o banco de dados
    conn.close()
    
    # Criar um documento PDF
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    
    # Criar uma tabela com os resultados da consulta
    table_data = [["Domínio", "Quantidade"]]  # Cabeçalho da tabela
    table_data.extend(data)  # Adicionar os dados da consulta
    
    # Estilo da tabela
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    
    # Criar a tabela
    table = Table(table_data)
    table.setStyle(style)
    
    # Adicionar a tabela ao documento PDF
    doc.build([table])
    
    print(f"Dados exportados com sucesso para {output_file}")

# Exemplo de uso
db_path = 'pihole-FTL.db'
table_name = 'queries'  # Substitua 'table_name' pelo nome correto da sua tabela
output_file = 'output.pdf'

export_domains_to_pdf(db_path, table_name, output_file)
