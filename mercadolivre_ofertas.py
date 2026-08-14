# Irei estar atualizando o código, caso o link do Mercado Livre esteja modificado/atualizado no momento.

import requests
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from datetime import datetime
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1&page=1&price=0.0-100.0"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
produtos = soup.find_all('div', class_='poly-card__content')

dados_produtos = []
total_produtos = 0

for produto in produtos:
    título = product.find('a', class_='poly-component__title') if 'product' in locals() else produto.find('a', class_='poly-component__title')
    título = produto.find('a', class_='poly-component__title')
    preço_elemento = produto.find('span', class_='andes-money-amount poly-price__amount andes-money-amount--cents-superscript')
    
    if título and preço_elemento:
        preço = preço_elemento.text
        link = título.get('href')
        total_produtos += 1
        
        dados_produtos.append({
            "nome": título.text.strip(),
            "preco": preço,
            "link": link
        })
        
        print(f'Título: {título.text.strip()}')
        print(f'Preço: {preço}')
        print(f'Link: {link}')
        print('-'*50)

agora = datetime.now().strftime('%d/%m/%Y às %H:%M')
pdf = canvas.Canvas('mercadolivre_ofertas.pdf')

def desenhar_cabecalho(pdf_obj):
    pdf_obj.setFont("Helvetica-Bold", 18)
    pdf_obj.setFillColor(HexColor("#1A365D"))
    pdf_obj.drawString(50, 780, "Relatório de Web Scraping: Ofertas Mercado Livre")

    pdf_obj.setFont("Helvetica", 10)
    pdf_obj.setFillColor(HexColor("#4A5568"))
    pdf_obj.drawString(50, 758, f"Fonte: Mercado Livre  |  Processado em: {agora}")

    pdf_obj.setStrokeColor(HexColor("#0D9488"))
    pdf_obj.setLineWidth(1.5)
    pdf_obj.line(50, 745, 562, 745)

    pdf_obj.setFont("Helvetica-Bold", 11)
    pdf_obj.setFillColor(HexColor("#1A365D"))
    pdf_obj.drawString(50, 720, "Produto")
    pdf_obj.drawString(300, 720, "Preço")
    pdf_obj.drawString(400, 720, "Link da Oferta")

    pdf_obj.setStrokeColor(HexColor("#E2E8F0"))
    pdf_obj.setLineWidth(0.5)
    pdf_obj.line(50, 712, 562, 712)

desenhar_cabecalho(pdf)

posicao_y = 690
pdf.setFont("Helvetica", 9)
pdf.setFillColor(HexColor("#2D3748"))

for item in dados_produtos:
    if posicao_y < 50:
        pdf.showPage()
        desenhar_cabecalho(pdf)
        posicao_y = 690
        pdf.setFont("Helvetica", 9)
        
    nome_cortado = item["nome"][:35]
    link_cortado = "Acessar Oferta"
    
    pdf.setFillColor(HexColor("#2D3748"))
    pdf.drawString(50, posicao_y, nome_cortado)
    pdf.drawString(300, posicao_y, item["preco"])
    
    pdf.setFillColor(HexColor("#2563EB"))
    pdf.drawString(400, posicao_y, link_cortado)
    
    pdf.linkURL(item["link"], (400, posicao_y - 2, 480, posicao_y + 10), relative=0)
    
    posicao_y -= 25

pdf.save()

print(f'\033[4m{total_produtos} produtos disponíveis na oferta do dia no Mercado Livre\033[m')
print("Arquivo 'mercadolivre_ofertas.pdf' gerado com sucesso!")
# Última atualização do código: 17/08/2026
