import re, json, urllib, os

def clean_url(url):
    crop_url = url.split("https://www.google.com/url?rct=j&sa=t&url=")[1]
    decode_url = urllib.parse.unquote(crop_url)
    patron1 = r"(.*?)&ct=ga&cd="
    url_sin_agregados = re.findall(patron1, decode_url)
    if (url_sin_agregados):
        return url_sin_agregados[0]
    else:
        return decode_url

def clean_content(content):
    return content.replace("\r", "").replace("\n", " ").replace("Google News", "").replace("Seguí todas las", "").replace(" noticias", "")


def get_links(body, category, send_last_mails):
    results = {}   # Crear un diccionario para almacenar los resultados

    mails_by_category_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'mails_by_category.json')
    mails_by_category = json.loads(open(mails_by_category_path, 'r').read())
    list_of_previous_electoral_urls = mails_by_category["electoral"]
    list_of_previous_no_electoral_urls = mails_by_category["no_electoral"]

    id = -1
    id2 = 0
    patterns = [r'>\s*([^=]+?)\s*\.\.\.\s*<([^>]+)>', r'===\s*(.*?)\s*===\s*(.*?)(?:\.\.\.|$)\s*<([^>]+)>']
    for pattern in patterns:
      id+=1
      id2+=1
      matches = re.findall(pattern, body, re.DOTALL)   # Buscar coincidencias usando la primera expresión regular
      for match in matches:
        content = match[id].strip()  # Primera iteracion: Contenido entre > y ...   // Segunda iteracion: Contenido entre === y ...
        url = match[id2].strip()  # Primera iteracion: URL entre < >   // Segunda iteracion: URL entre < >
        if url.startswith("https://www.google.com/url?rct=j&sa=t&url="):
          url_cleaned = clean_url(url)
          if category == "electoral":
            if ((url_cleaned not in list_of_previous_electoral_urls) or send_last_mails):
              list_of_previous_electoral_urls.append(url_cleaned)
              results[url_cleaned] = clean_content(str(content)) # Guardar en el diccionario
          elif category == "no_electoral":
            if ((url_cleaned not in list_of_previous_no_electoral_urls) or send_last_mails):
              list_of_previous_no_electoral_urls.append(url_cleaned)
              results[url_cleaned] = clean_content(str(content)) # Guardar en el diccionario

    return results