#função para salvar o conteúdo HTML da página
def salvar_conteudo_html(conteudo, nome_arquivo):
  with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
    arquivo.write(conteudo)