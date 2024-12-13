import os, json, imaplib, datetime, email, re, ast
keys_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "keys.json")
keys = json.loads(open(keys_path, 'r').read())
yandex_username = keys["yandex_username"]
yandex_app_password = keys["yandex_app_password"]
from email.header import decode_header
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

list_of_electoral_category_criteria = ast.literal_eval(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'electoral_criteria.lst'), 'r').read())

def get_mails():
  mails_electorales = ""
  mails_no_electorales = ""

  mail = imaplib.IMAP4_SSL('imap.yandex.com', 993) # Conectar al servidor IMAP de Yandex
  
  # OBTENER DATOS Y CATEGORIZAR
  try:
    mail.login(yandex_username, yandex_app_password)   # Iniciar sesión

    mail.select("inbox")   # Seleccionar la bandeja de entrada

    status, messages = mail.search(None, "ALL")  # Buscar todos los correos en la bandeja de entrada

    email_ids = messages[0].split()  # Convertir la lista de IDs de mensajes a una lista normal

    if not email_ids:
      print("No hay correos en la bandeja de entrada.")
      return False

    for email_id in email_ids:
      res, msg = mail.fetch(email_id, "(RFC822)")     # Obtener el correo por ID

      def extraer_emails(texto):
        patron_email = r'<(.*?)>'
        emails = re.findall(patron_email, texto)
        return emails[0]

      for response_part in msg:     # Extraer el contenido del mensaje
        if isinstance(response_part, tuple):
          msg = email.message_from_bytes(response_part[1])

          subject, encoding = decode_header(msg["Subject"])[0]
          if isinstance(subject, bytes):   # Si el asunto es en bytes, decodificarlo a str
              subject = subject.decode(encoding if encoding else 'utf-8')

          fecha = msg["Date"]   # Obtener la fecha del correo y convertirla a formato datetime
          fecha_correo = parsedate_to_datetime(fecha).replace(tzinfo=None)

          # print("from: "+ extraer_emails(msg.get("From")))
          # print("subject: "+subject)
          # print("fecha correo: "+fecha_correo)

          # Calcular si han pasado más de 5 días
          dias_diferencia = (datetime.now() - fecha_correo).days <= 5
          #extraer_emails(msg.get("From")) == "googlealerts-noreply@google.com") &
          if ( subject.startswith("Alerta de Google:") & dias_diferencia):
            # print("FROM: " + extraer_emails(msg.get("From")))
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
    mail.logout()  # Cerrar la conexión
    if (bool(mails_electorales) | bool(mails_no_electorales)):
      return [mails_electorales, mails_no_electorales]
    else:
      return [False, False]