import sys, json, ast, os

sys.path.append('./functions')
from functions.get_mails import get_mails

sys.path.append('../helpers')
from helpers.build_body import build_body
from helpers.get_links import get_links

def parse_and_build_mail(list_of_previous_electoral_urls, list_of_previous_no_electoral_urls):
  print("Conectando y parseando el mail...")

  mails_electorales, mails_no_electorales = get_mails()

  if not mails_electorales and not mails_no_electorales:
    print("Error al obtener mails")
  else:
    print("Mails obtenidos correctamente")

  # Agregar a build body
  while True:
    send_last_mails = False
    option_a1 = input("Desea enviar URLs anteriores? (y/n)\n> ")
    if option_a1.lower() == "y":
      send_last_mails = True
      break
    elif option_a1.lower() == "n":
      send_last_mails = False
      break
    else:
      print("Opción no válida")


  list_of_electoral_category_criteria = ast.literal_eval(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'electoral_criteria.lst'), 'r').read())

  dict_urls_electorales = get_links(mails_electorales, "electoral", send_last_mails)
  dict_urls_no_electorales = get_links(mails_no_electorales, "no_electoral", send_last_mails)

  if ((not len(dict_urls_electorales)) & (not len(dict_urls_no_electorales))):
    print("No hay URLs nuevas")
    return None

  # Actualizar listados de URLs por categorias
  with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'mails_by_category.json'), 'w') as file:
    json_data = {
      "electoral": list_of_previous_electoral_urls,
      "no_electoral": list_of_previous_no_electoral_urls
    }
    json.dump(json_data, file, indent=2)

  if (dict_urls_no_electorales):
    keys_to_remove = [] # Se agrega a lista los valores a eliminar para evitar RuntimeError
    for url, value in dict_urls_no_electorales.items():
      for electoral_category_criteria in list_of_electoral_category_criteria:
        if ((electoral_category_criteria in url) | (electoral_category_criteria in value)):
          dict_urls_electorales[url] = value
          keys_to_remove.append(url)
          break
    for key in keys_to_remove:
      dict_urls_no_electorales.pop(key)

  body_no_electoral = ""
  body_electoral = ""

  if dict_urls_electorales:
    body_electoral = build_body(dict_urls_electorales)
  if dict_urls_no_electorales:
    body_no_electoral = build_body(dict_urls_no_electorales)

  if (bool(body_electoral) | bool(body_no_electoral)):
    print("URLs parseadas correctamente")
    return body_electoral, body_no_electoral
  else:
    print("No hay nuevos mails")
    return False