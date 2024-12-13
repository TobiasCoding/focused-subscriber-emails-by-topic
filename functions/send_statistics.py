import matplotlib.pyplot as plt
import base64, os, json, subprocess, sys, sib_api_v3_sdk, pytz, ast, pprint
from io import BytesIO
from sib_api_v3_sdk.rest import ApiException
from datetime import datetime, timedelta

sys.path.append('../helpers')
from helpers.get_medio import get_medio

keys_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "keys.json")
keys = open(keys_path, 'r').read()
keys = json.loads(keys)

def send_statistics(users, list_of_previous_electoral_urls, list_of_previous_no_electoral_urls):

  urls = list(set(list_of_previous_electoral_urls + list_of_previous_no_electoral_urls))

  all_users = ast.literal_eval(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'users.json'), 'r').read())
  dependencias = set()  # tipo de dato set, sólo admite valores únicos
  externos = []
  num_usuarios = 0
  for category in all_users.values():
    for user in category.values():
        if user[1].startwith("Fiscalía") or user[1].startwith("Defensoría") or user[1].startwith("Juzgado") or user[1].startwith("Tribunal") or user[1].startwith("Procuración"):
            dependencias.add(user[1])
        else:
            externos.append(user[0])
        num_usuarios +=1
  num_dependencias = len(dependencias)
  num_externos = len(externos) 

  media_count = {}

  media_total = 0
  for url in urls:
      medio = get_medio(url)
      if medio:
          if len(medio) > 20:
              medio = medio[:20] + "..."
          if medio in media_count:
              media_count[medio] += 1
          else:
              media_count[medio] = 1
          media_total +=1

  # GRÁFICO
  # PARAMETROS
  limit_to_set_in_Others = 2      # When the value exceeds this parameter the value is setted in a group of "Others". Value in %. Example: 1%.
  others_max_per_line = 20        # The maximum of digits to show per line in the "Others" (when in less to limit_to_set_in_Others). Value in digits. Example: "hi" = 2 digits
  min_percent_to_show = 15        # The string of the number in graphic. Value in %. Example: 2%

  # PROCESAMIENTO
  total = sum(media_count.values())

  dictionary = dict(zip(media_count.keys(), media_count.values()))
  sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True)) # Paso 3: Ordenar el diccionario por values de mayor a menor

  sorted_keys = list(sorted_dict.keys())  # Paso 4: Convertir el diccionario ordenado de nuevo en listas
  sorted_values = list(sorted_dict.values())

  others_value = 0
  others_name = "Others <2: "
  others = False
  i = 0
  deleted = []
  others_lines = 1
  limit_to_set_in_Others/=100
  for valor in sorted_values:
      if valor / total < limit_to_set_in_Others:
          others = True
          others_value += float(valor)
          if len(others_name) > others_max_per_line:
            others_lines +=1
            others_max_per_line +=40
            others_name += "\n" + str(sorted_keys[i]) + ", "
          else:
            others_name += str(sorted_keys[i]) + ", "
          deleted.append(i)
      i += 1

  if others:
      for value in sorted(deleted, reverse=True):
          sorted_values.pop(value)
          sorted_keys.pop(value)
      others_name = others_name[:-2]
      sorted_values.append(others_value)
      sorted_keys.append("Otros <2")

  def autopct_function(pct):  # Función personalizada para mostrar porcentajes solo si son mayores al 10%
      return f'{pct:.2f}%' if pct > min_percent_to_show else ''

  fig, ax = plt.subplots()
  ax.set_title(f'Medios con noticias federales de La Plata.\n{media_total} noticias cubiertas de {len(media_count)} medios, desde el 8/11/2024', loc = "center", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
  ax.pie(sorted_values, labels=sorted_keys, autopct=autopct_function)

  plt.figtext(0.5, 0.1, 'Fuente: Walsh Legal Analytics', ha='center', fontsize=10, style='italic')  # Las primeras dos variables input son coordenadas dentro del gráfico, donde (0,0) es la esquina inferior izquierda y (1,1) es la esquina superior derecha.


  buffer = BytesIO()
  plt.savefig(buffer, format='png')  # Guardar la imagen en el buffer
  buffer.seek(0)
  image_base64 = base64.b64encode(buffer.read()).decode('utf-8')  # Convertir a Base64
  buffer.close()

  buenos_aires_tz = pytz.timezone("America/Argentina/Buenos_Aires")
  fecha_hora_buenos_aires = datetime.now(buenos_aires_tz).strftime("%d/%m/%Y %H:%M")

  # Crear el HTML con la imagen incrustada
  html = f"""
  <html>
      <body>
          <h2 style="color: #2F4F4F; font-weight: bold; text-align: center;">Estadísticas de los reportes de Walsh Legal Analytics</h2>
          <h3 style="color: #2F4F4F; text-align: center;">{fecha_hora_buenos_aires} Hs.</h3>
          <div style="text-align: center;">
              <img src="data:image/png;base64,{image_base64}" alt="Gráfica">
          </div>
          <br/>
          {num_usuarios-num_externos} usuarios de {num_dependencias} y {num_externos} usuarios externos (ciudadanos en general)
          <br/>_______________________________
          <br/>
          <p style="color: #696969; font-size: 0.9em; text-align: center;">Este informe se genera de manera automática. No responda a este correo.</p>
          <p style="color: #2F4F4F; text-align: center;">Walsh Legal Analytics</p>
      </body>
  </html>
  """
          # <p style="color: #696969; font-size: 0.9em; text-align: center;">Actualmente hay {num_suscriptores} usuarios suscriptos, pertenecientes a {num_dependencias} dependencias judiciales. Si desea incorporar a una persona o dejar de recibir mails, debería solicitarlo por mail a news.mailing@yandex.com indicando su correo electrónico, nombre, apellido y dependencia.</p>

  configuration = sib_api_v3_sdk.Configuration()

  keys_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "keys.json")
  keys = json.loads(open(keys_path, 'r').read())
  brevo_api_key = keys["brevo_api_key"]

  configuration.api_key['api-key'] = brevo_api_key

  api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

  for mail, user in users.items():
    # Código para enviar el correo (basado en tu ejemplo)
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": mail, "name": user[0]}],
        headers={"Admin": "unique-id-1234"},
        html_content=html,
        sender={"name": "Walsh Legal Analytics", "email": "news.mailing@yandex.com"},
        subject=f"Walsh Legal Analytics: {fecha_hora_buenos_aires}"
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print(f"Exception when calling SMTPApi->send_transac_email: {e}\n")

  print("Mails con estadísticas enviado!")