import sys, re, ast, os

sys.path.append('./helpers')
from helpers.get_medio import get_medio

def build_body(urls):
    print("--------------------------------\nLISTADO DE NOTICIAS ENCONTRADAS")
    while True:
      for i, (url, title) in enumerate(urls.items(), start=1):
        print(f'{i + 1}) {url}')

      urls_a_quitar = input("Desea remover alguna URL? Indique los IDs separados por comas si así lo desea, sino presione enter:\n> ").split(",")

      if urls_a_quitar:
        for value in urls_a_quitar:
          try:
            index = int(value) - 1  # Convertir a índice (base 0)
            if 0 <= index < len(urls):
                key_to_remove = list(urls.keys())[index]
                urls.pop(key_to_remove)
            else:
                print(f"ID inválido: {value}")
          except:
            print("ERROR: introdujo valores no válidos")
        continuar = input("LISTADO FINAL. Continuar (y/n)?\n> ")
        if continuar.lower() == "y":
          break
        else:
          print("Quitar URLs nuevamente")

    strong_words_route = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'strong_words.lst')
    list_of_strong_words = ast.literal_eval(open(strong_words_route, 'r').read())
    new_mail_body = ""
    for url_id, (url, title) in enumerate(urls.items()):
        if "Ziulu" in title:
          pass
        else:
          for word in list_of_strong_words:
            if word in title.upper():
              title = re.sub(rf"(?i)\b{word}\b", f"<span style='color: #2E8B57; font-weight: bold;'>{word}</span>", title, flags=re.IGNORECASE)

          new_mail_body += f'''
          <div style='border: 2px solid black; padding: 20px; margin: 20px; border-radius: 8px; background-color: #f9f9f9;'>
            <p style='font-size: 1.3em; margin-top: 1.2em;'>
              <span style='font-weight: bold;'>{url_id+1})</span> {title} (...)
              <br/>
              <span style='display: block; margin-top: 0.7em;'> Medio: <span style='font-weight: bold;'>{get_medio(url)}</span></span>
              <br/>
              <span style='display: block;'> Enlace: {url}</span>
            </p>
          </div>'''
    return new_mail_body