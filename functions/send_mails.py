from __future__ import print_function
import time, subprocess, sys, json, pytz, os
from pprint import pprint
from datetime import datetime, timedelta

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

keys_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "keys.json")
keys = open(keys_path, 'r').read()
keys = json.loads(keys)

def send_mails(body, users, category_name):
  print(f"MAILS {category_name.upper()}")

  if (len(body)>0):
    if not len(users):
      print(f"No hay users {category_name}")
      return False
  else:
    print(f"No hay mails {category_name}")
    return False

  buenos_aires_tz = pytz.timezone("America/Argentina/Buenos_Aires")  # Definir la zona horaria de Buenos Aires
  fecha_hora_buenos_aires = datetime.now(buenos_aires_tz).strftime("%d/%m/%Y %H:%M")  # Obtener la fecha y hora actual en Buenos Aires

  html = ""
  
  add_advice_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "add_advice.html")

  new_advice = open(add_advice_path).read()
  if new_advice:
    html += new_advice

  html+=f'''<h2 style="color: #2F4F4F; font-weight: bold; text-align: center;">Reporte {category_name}</h2>
  <h3 style="color: #2F4F4F; text-align: center;">{fecha_hora_buenos_aires} Hs.</h3>
  <hr style="border-top: 1px solid #2F4F4F;">
  <h3 style="color: #4B0082;">Titulares Recientes</h3>
  {body}
  <br/>
  <br/>
  _______________________________
  <br/>
  <p style="color: #696969; font-size: 0.9em; text-align: center;">Este reporte incluye solo noticias de los últimos 5 días, no reitera noticias enviadas anteriormente y se genera de manera automática. Es decir que no hay análisis humano de las noticias, por lo que pueden haber falsos positivos. No necesariamente responde a la totalidad de noticias disponibles en internet. No responda a este correo.</p>
  <p style="color: #2F4F4F; text-align: center;">Walsh Legal Analytics</p>'''

  while True:
    send = input('''Enviar mail? (y/n)\n> ''')
    if send == "n":
      print("Reporte cancelado.")
      break
    elif send == "y":
      configuration = sib_api_v3_sdk.Configuration()

      configuration.api_key['api-key'] = keys["brevo_api_key"]

      api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
      # params = {"parameter":"My param value","subject":"New Subject"}

      for correo, nombre in users.items():
        print("-- Enviando mail a: " + str(correo))
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email":correo,"name":nombre[0]}],
            # bcc=[{"name":"John Doe","email":"news.mailing@yandex.com"}],
            # cc=[{"email":"news.mailing@yandex.com","name":"Janice Doe"}],
            reply_to={"email":"news.mailing@yandex.co","name":"Walsh Legal Analytics"},
            # headers={"Some-Custom-Name":"unique-id-1234"},
            html_content= f'<h4>Hola! {nombre[0].split(" ")[0]} estos son los titulares de hoy:</h4><br/><br/>'+html,
            sender={"name":"Walsh Legal Analytics","email":"news.mailing@yandex.com"},
            subject=f"Reporte {category_name} del {fecha_hora_buenos_aires}"
        )

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
      print(f"Mails {category_name} enviados!")
      break
    else:
      print("Opción no válida")