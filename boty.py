import requests

import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from download_imagens import baixar_e_salvar_imagem  # Importa a função do outro arquivo
from helpers import salvar_conteudo_html

def obter_conteudo(link, url_base):
    # Se a URL é relativa, concatena com a URL base
    if not link.startswith('http'):
        link = urljoin(url_base, link)

    response = requests.get(link)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Erro ao obter conteúdo de {link}. Código de status: {response.status_code}")
        return None

# Cria a pasta "imagens" se não existir
if not os.path.exists("imagens"):
    os.makedirs("imagens")

# URL da página a ser clonada
url = "https://programareceitasparasecar.com/"

# Faz a requisição à página
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Converte o conteúdo para o formato BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Pega os links para os arquivos CSS e JavaScript
    links_css = [link.get("href") for link in soup.find_all("link", rel="stylesheet")]
    links_js = [script.get("src") for script in soup.find_all("script", src=True)]

    # Obtém o conteúdo dos arquivos CSS e JavaScript
    css_content = "\n".join([obter_conteudo(link, url).decode("utf-8") for link in links_css if link])
    js_content = "\n".join([obter_conteudo(link, url).decode("utf-8") for link in links_js if link])

    # Obtém os URLs das imagens
    links_imagens = [img['src'] for img in soup.find_all('img', src=True)]

    # Obtém o conteúdo das imagens
    imagens = [baixar_e_salvar_imagem(link, url, "imagens") for link in links_imagens if link]
    
    # Modifica o HTML para incluir o conteúdo CSS e JavaScript
    conteudo_html = str(soup)
    conteudo_html = conteudo_html.replace("</head>", f"<style>{css_content}</style></head>")
    conteudo_html = conteudo_html.replace("</body>", f"<script>{js_content}</script></body>")

    # Salva o conteúdo clonado em um arquivo HTML
    nome_arquivo = "pagina_clonada.html"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_html)
    print("Conteúdo clonado (com CSS e JavaScript) salvo em", nome_arquivo)
else:
    print("Erro ao acessar a página. Código de status:", response.status_code)