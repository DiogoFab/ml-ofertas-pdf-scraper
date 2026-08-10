# Irei estar atualizando o código, caso o link do Mercado Livre esteja modificado/atualizado no momento.

import requests
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from datetime import datetime
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://www.mercadolivre.com.br/ofertas?price=0.0-100.0&container_id=MLB779362-1"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
produtos = soup.find_all('div', class_='poly-card')

dados_produtos = []
total_produtos = 0

for produto in produtos:
    título = produto.find('a', class_='poly-component__title')
    preço_elemento = produto.find('span', class_='andes-money-amount poly-price__amount andes-money-amount--cents-superscript andes-money-amount--weight-semibold')
    
    if título and preço_elemento:
        preço = preço_elemento.text.strip()
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

pdf.setFont("Helvetica-Bold", 18)
pdf.setFillColor(HexColor("#1A365D"))
pdf.drawString(50, 740, "Relatório de Web Scraping: Ofertas Mercado Livre")

pdf.setFont("Helvetica", 10)
pdf.setFillColor(HexColor("#4A5568"))
pdf.drawString(50, 718, f"Fonte: Mercado Livre  |  Processado em: {agora}")

pdf.setStrokeColor(HexColor("#0D9488"))
pdf.setLineWidth(1.5)
pdf.line(50, 705, 562, 705)

pdf.setFont("Helvetica-Bold", 11)
pdf.setFillColor(HexColor("#1A365D"))
pdf.drawString(50, 680, "Produto")
pdf.drawString(300, 680, "Preço")
pdf.drawString(400, 680, "Link da Oferta")

pdf.setStrokeColor(HexColor("#E2E8F0"))
pdf.setLineWidth(0.5)
pdf.line(50, 672, 562, 672)

posicao_y = 650
pdf.setFont("Helvetica", 9)
pdf.setFillColor(HexColor("#2D3748"))

for item in dados_produtos[:15]:
    nome_cortado = item["nome"][:35]
    link_cortado = "Acessar Oferta"
    
    pdf.drawString(50, posicao_y, nome_cortado)
    pdf.drawString(300, posicao_y, item["preco"])
    
    pdf.setFillColor(HexColor("#2563EB"))
    pdf.drawString(400, posicao_y, link_cortado)
    
    pdf.linkURL(item["link"], (400, posicao_y - 2, 480, posicao_y + 10), relative=0)
    
    pdf.setFillColor(HexColor("#2D3748"))
    posicao_y -= 25

pdf.save()

print(f'\033[4m{total_produtos} produtos disponíveis na oferta do dia no Mercado Livre\033[m')
print("Arquivo 'mercadolivre_ofertas.pdf' gerado com sucesso!")
