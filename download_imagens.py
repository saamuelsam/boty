import os
import requests
from urllib.parse import urljoin, urlparse

def baixar_e_salvar_imagem(link, url_base, pasta_destino):
    # Se a URL é relativa, concatena com a URL base
    if not link.startswith('http'):
        link = urljoin(url_base, link)

    response = requests.get(link)
    if response.status_code == 200:
        # Extrai o nome do arquivo da URL
        nome_arquivo = os.path.basename(urlparse(link).path)

        # Se a extensão do arquivo não estiver presente, acrescenta ".jpg"
        if not nome_arquivo:
            nome_arquivo = "imagem.jpg"

        # Caminho completo do arquivo
        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

        # Salva o conteúdo no arquivo
        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(response.content)

        return caminho_arquivo
    else:
        print(f"Erro ao obter conteúdo de {link}. Código de status: {response.status_code}")
        return None
