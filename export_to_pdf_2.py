from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, Frame
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import sqlite3
from datetime import datetime

def add_footer(canvas, doc, db_path):
    width, height = letter
    canvas.saveState()
    # Rodapé com o nome do banco de dados
    canvas.setFont('Helvetica', 8)
    canvas.drawString(inch, 0.75 * inch, f"Database: {db_path}")
    # Rodapé com a data de geração do PDF
    canvas.drawString(inch, 0.5 * inch, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    canvas.restoreState()

def export_domains_to_pdf(db_path, table_name, output_file):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Executar a consulta para contar os domínios
    cursor.execute(f"SELECT domain, client, COUNT(*) AS vezes FROM {table_name} WHERE client = '192.168.0.190' GROUP BY domain")
    
    # Obter os resultados da consulta
    data = cursor.fetchall()
    
    # Fechar a conexão com o banco de dados
    conn.close()
    
    # Criar um documento PDF
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    
    # Criar uma tabela com os resultados da consulta
    table_data = [["Domínio", "Cliente", "Quantidade"]]  # Cabeçalho da tabela
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
    
    # Função para adicionar o rodapé com o argumento db_path
    def add_footer_with_db(canvas, doc):
        add_footer(canvas, doc, db_path)
    
    # Adicionar o rodapé a cada página
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 0.75 * inch, id='normal')
    template = PageTemplate(id='footer', frames=frame, onPage=add_footer_with_db)
    doc.addPageTemplates([template])
    
    # Adicionar a tabela ao documento PDF
    doc.build([table])
    
    print(f"Dados exportados com sucesso para {output_file}")

# Exemplo de uso
db_path = 'pihole-database-13-06.db'
table_name = 'queries'  # Substitua 'table_name' pelo nome correto da sua tabela
output_file = 'output.pdf'

export_domains_to_pdf(db_path, table_name, output_file)

