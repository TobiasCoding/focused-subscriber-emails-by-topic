import sys, os, json, subprocess, sys, urllib.parse, imaplib, email, re, pytz, ast

path = os.path.dirname(os.path.abspath(__file__))

if not os.path.isfile(os.path.join(path, 'database', 'tld.lst')):
  sys.path.append('./database')
  from database.build_database import build_database
  build_database()

sys.path.append('./functions')
from functions.get_mails import get_mails
from functions.parse_and_build_mail import parse_and_build_mail
from functions.send_mails import send_mails
from functions.send_statistics import send_statistics

try:
    __import__('sib_api_v3_sdk')
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sib_api_v3_sdk'])
try:
    __import__('brevo')
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'brevo-python'])



mail_body_data = ""
mails_no_electorales = ""

users = open(os.path.join(path, 'database', 'users.json'), 'r').read()
users = json.loads(users)


destinatario_test = users["test"]
users_ambos = users["all_categorys"]
users_electorales = users["electoral"]
users_electorales.update(users_ambos)
users_no_electorales = users["no_electoral"]
users_no_electorales.update(users_ambos)

num_suscriptores = len(users["all_categorys"]) + len(users["electoral"]) + len(users["no_electoral"])

media = json.loads(open(os.path.join(path, 'database', 'media.json'), 'r').read())

tld_pattern = ast.literal_eval(open(os.path.join(path, 'database', 'tld.lst'), 'r').read())

if __name__ == "__main__":
    try:
        users = open(os.path.join(path, 'database', 'users.json'), "r").read()
    except:
        print("Building databases...")
        build_database()
        print("Databases builded!")

    mails_by_category_path = os.path.join(path, "database", "mails_by_category.json")
    mails_by_category = json.loads(open(mails_by_category_path, 'r').read())
    list_of_previous_electoral_urls = mails_by_category["electoral"]
    list_of_previous_no_electoral_urls = mails_by_category["no_electoral"]

    for i, option in enumerate(["Mails electorales", "Mails no electorales", "Todos los mails", "Prueba", "Destinatario particular", "Enviar todo pero antes enviar mail de prueba", "Enviar estadísticas", "Cerrar"]):
        print(f"{i+1}) {option}")

    while True:
      option_a = int(input("Select option:"))

      if option_a > 0 and option_a < 7:
        body_electoral, body_no_electoral = parse_and_build_mail(list_of_previous_electoral_urls, list_of_previous_no_electoral_urls)

      if option_a == 1:
        print("MAILS ELECTORALES")
        send_mails(body_electoral, users_electorales, "Electoral")

      elif option_a == 2:
        print("MAILS NO ELECTORALES")
        send_mails(body_no_electoral, users_no_electorales, "No Electoral")

      elif option_a == 3:
        print("TODOS LOS MAILS")
        send_mails(body_electoral, users_electorales, "Electoral")
        send_mails(body_no_electoral, users_no_electorales, "No Electoral")

      elif option_a == 4:
        print("TEST")
        send_mails(body_electoral, destinatario_test, "Electoral")
        send_mails(body_no_electoral, destinatario_test, "No Electoral")

      elif option_a == 5:
        print("DESTINATARIO PARTICULAR")
        users = users_electorales | users_no_electorales

        print("Seleccionar destinatario:")
        for i, user in enumerate(users):
          print(f'{i+1}. {user}')
        print(f'{len(users)+1}. Definir otro destinatario')

        second_bucle = True
        while second_bucle:
          option_b = int(input("> ")) -1
          if ((option_b >= 0) & (option_b <= len(users)+1)):
            if (option_b == len(users)+1):
              name_destinatario = input("Nombre: ")
              mail_destinatario = input("Mail: ")
              users[mail_destinatario] = name_destinatario
              destinatario = {mail_destinatario : name_destinatario}
            else:
              name_destinatario = list(users.values())[option_b]
              mail_destinatario = list(users.keys())[option_b]
              destinatario = {mail_destinatario : name_destinatario}

            while second_bucle:
              option_b = input(f"Qué mails desea enviar a {name_destinatario} ({mail_destinatario})?\n1. Electorales\n2. No electorales\n3. Todos\n4. Cancelar\n> ")
              try:
                option_b = int(option_b)
                if option_b == 1:
                    print("Enviando mails electorales")
                    send_mails(body_electoral, destinatario, "Electoral")
                    second_bucle = False

                elif option_b == 2:
                    print("Enviando mails no electorales")
                    send_mails(body_no_electoral, destinatario, "No Electoral")
                    second_bucle = False

                elif option_b == 3:
                    print("Enviando mails electorales y no electorales")
                    send_mails(body_electoral, destinatario, "Electoral")
                    send_mails(body_no_electoral, destinatario, "No Electoral")
                    second_bucle = False

                elif option_b == 4:
                    print("Cancelado")
                    second_bucle = False
                else:
                    print("Opción no válida")
              except:
                print("ERROR: Opción no válida")
          else:
            print("Opción no válida")

      elif option_a == 6:
        print("MAIL A TODOS PREVIA PRUEBA")
        send_mails(body_electoral, destinatario_test, "Electoral")
        send_mails(body_no_electoral, destinatario_test, "No Electoral")

        send = True
        while send:
          option_b = input("Enviar mails a todos los users? (y/n)\n> ")
          if option_b.lower() == "n":
            print("Reporte cancelado.")
            send = False
          elif option_b.lower() == "y":
            send_mails(body_electoral, users_electorales, "Electoral")
            send_mails(body_no_electoral, users_no_electorales, "No Electoral")
            print("Mails enviados!")
            send = False
          else:
            print("Opción no válida")
        break

      elif option_a == 7:
        print("ESTADISTICAS")
        while True:
          users = input("Definir destinatario/s\n1) Todos\n2) Test\n> ")

          if users == "1":
            users = users_electorales | users_no_electorales  # Concatenar dos diccinarios
            break

          elif users == "2":
            users = destinatario_test
            break

          else:
            print("Opción no válida")
        send_statistics(users, list_of_previous_electoral_urls, list_of_previous_no_electoral_urls)
        break

      elif option_a == 8:
        print("Close program")
        break

      else:
        print("Invalid option")