# PRECONFIGURACIONES Y OBTENCIÓN DE DATOS
# -----------------------------------------------------------------------------------------------

from google.colab import drive
import os, json

destinatarios_path = '/content/drive/My Drive/envio_de_mails/destinatarios.txt'

destinatarios_ambos = open(destinatarios_path, 'r').read()
destinatarios = json.loads(destinatarios_ambos)

destinatarios_ambos = destinatarios["ambos"]

destinatarios_electorales = destinatarios["electoral"]
destinatarios_electorales.update(destinatarios_ambos)

destinatarios_no_electorales = destinatarios["no_electoral"]
destinatarios_no_electorales.update(destinatarios_ambos)

destinatario_test = {"example@example.com": "Test",} # Definir correo para enviar mails de prueba

# Nombres de medios para capitalizar correctamente
media_path = '/content/drive/My Drive/envio_de_mails/media.txt'
media = json.loads(open(media_path, 'r').read())

# Lista de dominios de nivel superior (TLDs) para análisis de URLs
import ast
media_path = '/content/drive/My Drive/envio_de_mails/tld.txt'
tld_pattern = ast.literal_eval(open(media_path, 'r').read())

# Lista de palabras que se analizan en las urls para clasificar por categoria
electoral_criteria_path = '/content/drive/My Drive/envio_de_mails/electoral_criteria.txt'
list_of_electoral_category_criteria = ast.literal_eval(open(electoral_criteria_path, 'r').read())

# Lista de palabras que se resaltan en los mails. Deben ir todas en mayúscula por el funcionamiento interno de la app para evitar conflictos de mayúscula o minúsculas
strong_words_path = '/content/drive/My Drive/envio_de_mails/strong_words.txt'
list_of_strong_words = ast.literal_eval(open(strong_words_path, 'r').read())

# Listas de mails enviados anteriormente
mails_by_category_path = '/content/drive/My Drive/envio_de_mails/mails_by_category.txt'
mails_by_category = json.loads(open(mails_by_category_path, 'r').read())

list_of_previous_electoral_urls = mails_by_category["electoral"]
list_of_previous_no_electoral_urls = mails_by_category["no_electoral"]


# LIBRERIAS
# -----------------------------------------------------------------------------------------------
import subprocess, sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sib_api_v3_sdk'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'brevo-python'])
import urllib.parse
import imaplib, email, re, pytz
from email.header import decode_header
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

# CONEXIÓN AL MAIL
# -----------------------------------------------------------------------------------------------

# Conexión a Brevo: API key
brevo_api_key = ''  # Definir aquí tu API KEY de Brevo

# Conexión a Yandex
username = "example@yandex.com"       # Definir aquí tu correo de Yandex
password = "password-example"         # Contraseña de aplicación en Yandex (obtenerla previamente)
mail = imaplib.IMAP4_SSL('imap.yandex.com', 993) # Conectar al servidor IMAP de Yandex


# CÓDIGO
# -----------------------------------------------------------------------------------------------
mail_body_data = ""
mails_no_electorales = ""
mails_electorales = ""

def get_mails():
  global mail_body_data, mails_electorales, mails_no_electorales

  # OBTENER DATOS Y CATEGORIZAR
  try:
      mail.login(username, password)
      mail.select("inbox")
      status, messages = mail.search(None, "ALL")

      email_ids = messages[0].split()

      if not email_ids:
          print("No hay correos en la bandeja de entrada.")
          return False

      for email_id in email_ids:
          # Obtener el correo por ID
          res, msg = mail.fetch(email_id, "(RFC822)")

          def extraer_emails(texto):
              patron_email = r'<(.*?)>'
              emails = re.findall(patron_email, texto)
              return emails[0]

          # Extraer el contenido del mensaje
          for response_part in msg:
              if isinstance(response_part, tuple):
                  msg = email.message_from_bytes(response_part[1])

                  # Decodificar el asunto
                  subject, encoding = decode_header(msg["Subject"])[0]
                  if isinstance(subject, bytes):
                      # Si el asunto es en bytes, decodificarlo a str
                      subject = subject.decode(encoding if encoding else 'utf-8')

                  # Obtener la fecha del correo y convertirla a formato datetime
                  fecha = msg["Date"]
                  fecha_correo = parsedate_to_datetime(fecha).replace(tzinfo=None)

                  # print("from: "+ extraer_emails(msg.get("From")))
                  # print("subject: "+subject)
                  # print("fecha correo: "+fecha_correo)

                  # Calcular si han pasado más de 5 días
                  dias_diferencia = (datetime.now() - fecha_correo).days <= 5

                  if ((extraer_emails(msg.get("From")) == "googlealerts-noreply@google.com") & subject.startswith("Alerta de Google:") & dias_diferencia):
                    # print("FROM: " + extraer_emails(msg.get("From")))
                    # print("SUBJECT: " + subject)
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                mail_body_data = part.get_payload(decode=True).decode()  # Decodificar el cuerpo
                                # print(mail_body_data) # ----------------------------------------------------------------- DEBUG: IMPRIMIR CUERPO A PARSEAR
                                # print("Cuerpo:", mail_body_data)  # Mostrar el cuerpo
                    else:
                        mail_body_data = msg.get_payload(decode=True).decode()

                    for electoral_category_criteria in list_of_electoral_category_criteria:
                      if (electoral_category_criteria in subject):
                        mails_electorales += mail_body_data
                      else:
                        mails_no_electorales += mail_body_data
                  mail_body_data = ""

  finally:
      # Cerrar la conexión
      mail.logout()
      if (bool(mails_electorales) | bool(mails_no_electorales)):
        return True
      else:
        return False

def parse_mails():
  global body_electoral, body_no_electoral

  def get_links(body, category):
    results = {}   # Crear un diccionario para almacenar los resultados

    pattern_1 = r'===\s*(.*?)\s*===\s*(.*?)(?:\.\.\.|$)\s*<([^>]+)>'  # Expresión regular para capturar datos entre === y el primer ...

    matches_1 = re.findall(pattern_1, body, re.DOTALL)   # Buscar coincidencias usando la primera expresión regular

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

    for match in matches_1:
        content = match[1].strip()  # Contenido entre === y ...
        url = match[2].strip()      # URL entre < >
        if url.startswith("https://www.google.com/url?rct=j&sa=t&url="):
          url_cleaned = clean_url(url)
          if category == "electoral":
            if url_cleaned not in list_of_previous_electoral_urls:
              list_of_previous_electoral_urls.append(url_cleaned)
              results[url_cleaned] = clean_content(str(content)) # Guardar en el diccionario
          elif category == "no_electoral":
            if url_cleaned not in list_of_previous_no_electoral_urls:
              list_of_previous_no_electoral_urls.append(url_cleaned)
              results[url_cleaned] = clean_content(str(content)) # Guardar en el diccionario

    pattern_2 = r'>\s*([^=]+?)\s*\.\.\.\s*<([^>]+)>'
    matches_2 = re.findall(pattern_2, body, re.DOTALL)   # Buscar coincidencias usando la segunda expresión regular
    for match in matches_2:
      content = match[0].strip()  # Contenido entre > y ...
      url = match[1].strip()  # URL entre < >
      if url.startswith("https://www.google.com/url?rct=j&sa=t&url="):
        url_cleaned = clean_url(url)
        if category == "electoral":
          if url_cleaned not in list_of_previous_electoral_urls:
            list_of_previous_electoral_urls.append(url_cleaned)
            results[url_cleaned] = clean_content(str(content))
        elif category == "no_electoral":
          if url_cleaned not in list_of_previous_no_electoral_urls:
            list_of_previous_no_electoral_urls.append(url_cleaned)
            results[url_cleaned] = clean_content(str(content))
    return results

  dict_urls_electorales = get_links(mails_electorales, "electoral")
  dict_urls_no_electorales = get_links(mails_no_electorales, "no_electoral")

  if ((not len(dict_urls_electorales)) & (not len(dict_urls_no_electorales))):
    print("No hay URLs nuevas")
    return None

  # Actualizar listados de URLs por categorias
  with open(mails_by_category_path, 'w') as file:
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

  def get_medio(url):
      for tld in tld_pattern:
        if f'.{tld}' in url:
          name = url.split(tld)[0].split("//")[-1]
          if name.startswith("www."):
            name = name.replace("www.", "")
          return media.get(name.replace(".",""))
      return None  # En caso de que no haya coincidencia

  def build_body(urls):
    url_id = 0
    new_mail_body = ""
    print('''--------------------------------
NOTICIAS ENCONTRADAS''')
    for url, title in urls.items():
        url_id += 1
        print(f'''    > {url_id}) {title}
      {url}''')
        for word in list_of_strong_words:
          if word in title.upper():
            title = re.sub(rf"(?i)\b{word}\b", f"<span style='color: #2E8B57; font-weight: bold;'>{word}</span>", title, flags=re.IGNORECASE)

        new_mail_body += f'''
        <div style='border: 2px solid black; padding: 20px; margin: 20px; border-radius: 8px; background-color: #f9f9f9;'>
          <p style='font-size: 1.3em; margin-top: 1.2em;'>
            <span style='font-weight: bold;'>{url_id})</span> {title} (...)
            <br/>
            <span style='display: block; margin-top: 0.7em;'> Medio: <span style='font-weight: bold;'>{get_medio(url)}</span></span>
            <br/>
            <span style='display: block;'> Enlace: {url}</span>
          </p>
        </div>'''

    return new_mail_body

  if dict_urls_electorales:
    body_electoral = build_body(dict_urls_electorales)
  if dict_urls_no_electorales:
    body_no_electoral = build_body(dict_urls_no_electorales)

  print("--------------------------------")

  if (bool(body_electoral) | bool(body_no_electoral)):
    return True
  else:
    return False

# -------------------------------------------------------------------------------------------------
from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

def send_mails(body, destinatarios, categoria):

  # Definir la zona horaria de Buenos Aires
  buenos_aires_tz = pytz.timezone("America/Argentina/Buenos_Aires")

  # Obtener la fecha y hora actual en Buenos Aires
  fecha_hora_buenos_aires = datetime.now(buenos_aires_tz).strftime("%d/%m/%Y %H:%M")

  html1=f'''
  <h2 style="color: #2F4F4F; font-weight: bold; text-align: center;">Reporte {categoria}</h2>
  <h3 style="color: #2F4F4F; text-align: center;">{fecha_hora_buenos_aires} Hs.</h3>
  <hr style="border-top: 1px solid #2F4F4F;">
  <h3 style="color: #4B0082;">Titulares Recientes</h3>
  {body}'''

  html2=f'''
  <br/>
  _______________________________
  <br/>
  <p style="color: #696969; font-size: 0.9em; text-align: center;">Este reporte incluye solo noticias de los últimos 5 días, no reitera noticias enviadas anteriormente y se genera de manera automática. Es decir que no hay análisis humano de las noticias, por lo que pueden haber falsos positivos. No necesariamente responde a la totalidad de noticias disponibles en internet.</p>
  <p style="color: #696969; font-size: 0.9em; text-align: center;">Por favor, no responder a este correo.</p>
  <p style="color: #2F4F4F; text-align: center; font-weight: bold; margin-top: 2em;">Gracias por su tiempo.</p>
  <p style="color: #2F4F4F; text-align: center;">Report</p>
  '''
  #print(html1+html2)

  # FUNCIONALIDAD QUITADA TEMPORALMENTE
  # while True:
  #   # break # --------------------------------- DEBUG
  #   add_urls = input('''Agregar URLs manualmente? (y/n)
  #   > ''')
  #   if add_urls == "n":
  #     break
  #   elif add_urls == "y":
  #     urls = input('''Agregar URLs separadas por comas:
  #     > ''')
  #     list_urls = urls.split(",")
  #     for url in list_urls:
  #       url_id += 1
  #       html1+=f"<br/><h4>  {url_id}) {url}</h4><br/>"
  #     print(html1+"<br/>"+html2)
  #     break
  #   else:
  #     print("Opción incorrecta")

  html = html1+"<br/>"+html2

  while True:
    send = input('''Enviar mail? (y/n)
> ''')
    # send = "y" # --------------------------------- DEBUG
    if send == "n":
      print("Reporte cancelado.")
      break
    elif send == "y":
      configuration = sib_api_v3_sdk.Configuration()

      configuration.api_key['api-key'] = brevo_api_key

      api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

      for correo, nombre in destinatarios.items():
        print("-- Enviando mail a: " + str(correo))
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email":correo,"name":nombre}],
            # bcc=[{"name":"John Doe","email":"example@example.com"}],
            # cc=[{"email":"example@example.com","name":"Janice Doe"}],
            # reply_to={"email":"example@example.com","name":"John Doe"},
            headers={"Some-Custom-Name":"unique-id-1234"},
            html_content=html,
            sender={"name":"Report","email":"example@example.com"}, # Definir aquí el usuario y contraseña registrado en Brevo
            subject=f"Report: {fecha_hora_buenos_aires}"
        )

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
      print(f"Mails {categoria} enviados!")
      break
    else:
      print("Opción no válida")

def send_mails_electorales():
  if (len(body_electoral)>0):
    if (len(destinatarios_electorales)):
      print("MAILS ELECTORALES")
      send_mails(body_electoral, destinatarios_electorales, "Electoral")
    else:
      print("No hay destinatarios electorales")
  else:
    print("No hay mails electorales")

def send_mails_no_electorales():
  if (len(body_no_electoral)>0):
    if (len(destinatarios_no_electorales)):
      print("MAILS NO ELECTORALES")
      send_mails(body_no_electoral, destinatarios_no_electorales, "No Electoral")
    else:
      print("No hay destinatarios no electorales")
  else:
    print("No hay mails no electorales")

if __name__ == "__main__":
  print("Iniciando aplicación...")
  print("Conectando y parseando el mail...")
  if not get_mails():
    print("Error al obtener mails")
    exit()
  else:
    print("Mails obtenidos correctamente")
  if not parse_mails():
    print("No hay nuevos mails")
  else:
    print("URLs parseadas correctamente")

    while True:
      option_a = input('''Select option:
  1. Mails electorales
  2. Mails no electorales
  3. Todos los mails
  4. Prueba
  5. Destinatario particular
  6. Enviar todo pero antes enviar mail de prueba
  7. Cerrar
  > ''')

      if option_a == "1":
        send_mails_electorales()
      elif option_a == "2":
        send_mails_no_electorales()
      elif option_a == "3":
        send_mails_electorales()
        send_mails_no_electorales()
      elif option_a == "4":
        print("TEST")
        send_mails(body_electoral, destinatario_test, "Electoral")
        send_mails(body_no_electoral, destinatario_test, "No Electoral")
      elif option_a == "5":
        print("DESTINATARIO PARTICULAR")
        destinatarios = destinatarios_electorales | destinatarios_no_electorales
        print("Seleccionar destinatario:")
        for i, user in enumerate(destinatarios):
          print(f'{i+1}. {user}')
        print(f'{i+1}. Definir otro destinatario')
        second_bucle = True
        while second_bucle:
          option_b = int(input("> ")) -1
          if ((option_b >= 0) & (option_b <= len(destinatarios)+1)):
            if (option_b == len(destinatarios)+1):
              name_destinatario = input("Nombre: ")
              mail_destinatario = input("Mail: ")
              destinatarios[mail_destinatario] = name_destinatario
              destinatario = {mail_destinatario : name_destinatario}
            else:
              name_destinatario = list(destinatarios.values())[option_b]
              mail_destinatario = list(destinatarios.keys())[option_b]
              destinatario = {mail_destinatario : name_destinatario}
            while second_bucle:
              option_b = input(f'''Qué mails desea enviar a {name_destinatario} ({mail_destinatario})?
  1. Electorales
  2. No electorales
  3. Todos
  4. Cancelar
  > ''')
              if option_b == "1":
                print("Enviando mails electorales")
                send_mails(body_electoral, destinatario, "Electoral")
                second_bucle = False
              elif option_b == "2":
                print("Enviando mails no electorales")
                send_mails(body_no_electoral, destinatario, "No Electoral")
                second_bucle = False
              elif option_b == "3":
                print("Enviando mails electorales y no electorales")
                send_mails(body_electoral, destinatario, "Electoral")
                send_mails(body_no_electoral, destinatario, "No Electoral")
                second_bucle = False
              elif option_b == "4":
                print("Cancelado")
                second_bucle = False
              else:
                print("Opción no válida")
          else:
            print("Opción no válida")
      elif option_a == "6":
        print("MAIL A TODOS PREVIA PRUEBA")
        send_mails(body_electoral, destinatario_test, "Electoral")
        send_mails(body_no_electoral, destinatario_test, "No Electoral")
        send = True
        while send:
          option_b = input('''Enviar mails a todos los destinatarios? (y/n)
  > ''')
          if option_b.lower() == "n":
            print("Reporte cancelado.")
            send = False
          elif option_b.lower() == "y":
            send_mails_electorales()
            send_mails_no_electorales()
            print("Mails enviados!")
            send = False
          else:
            print("Opción no válida")
        break
      elif option_a == "7":
        print("Close program")
        break
      else:
        print("Invalid option")
