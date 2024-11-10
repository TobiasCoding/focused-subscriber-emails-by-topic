# CREAR BASE DE DATOS
# CREAR LISTADO DESDE CERO (SOLO LA PRIMERA VEZ QUE SE EJECUTA)

from google.colab import drive
import os

if not os.path.isdir('/content/drive/My Drive'):
    drive.mount('/content/drive')

!mkdir -p '/content/drive/My Drive/envio_de_mails'

mails_by_category_path = '/content/drive/My Drive/envio_de_mails/mails_by_category.txt'
with open(mails_by_category_path, 'w') as file:
    file.write('''
{
  "electoral": [],
  "no_electoral": []
}
''')

# Usuarios por categoría
destinatarios_path = '/content/drive/My Drive/envio_de_mails/destinatarios.txt'
with open(destinatarios_path, 'w') as file:
    # Primer lugar: usuario test
    # Segundo lugar: usuarios inscriptos en ambos listados
    # Tercer lugar: usuarios electorales
    # Cuarto lugar: usuarios no electorales
    file.write('''
{
    "test": {
        "example@example.com": "Test",
    },
    "ambos": {
        "example@example.com": "Test",
    },
    "electoral": {
        "example@example.com": "Test",    
    },
    "no_electoral": {
        "example@example.com": "Test",
    }
}
''')

media_path = '/content/drive/My Drive/envio_de_mails/media.txt'
with open(media_path, 'w') as file:
    file.write('''
{
    "0221": "0221",
    "agencianova": "Agencia Nova",
    "clarin": "Diario Clarín",
    "lanacion": "Diario La Nación",
    "infocronos": "Info Cronos",
    "codigobaires": "Código Baires",
    "latecla": "La Tecla",
    "chacabucoenred": "Chacabuco en Red",
    "elcorreografico": "El Correo Gráfico",
    "elciudadano": "El Ciudadano",
    "elpais": "El País",
    "elgrafico": "El Gráfico",
    "pagina12": "Diario Página 12",
    "tiempoargentino": "Tiempo Argentino",
    "c5n": "C5N",
    "telefe": "TELEFE",
    "a24": "América 24 (A24)",
    "infobae": "Infobae",
    "cronica": "Crónica",
    "perfil": "Diario Perfil",
    "tn": "Todo Noticias (TN)",
    "cnnespanol": "CNN en Español",
    "ole": "Diario Olé",
    "cronista": "El Cronista",
    "ambito": "Ámbito Financiero",
    "tycsports": "TyC Sports",
    "eldestapeweb": "El Destape Web",
    "casarosada": "Casa Rosada",
    "conicet": "CONICET",
    "dw": "Deutsche Welle (DW)"
}
''')

tld_path = '/content/drive/My Drive/envio_de_mails/tld.txt'
with open(tld_path, 'w') as file:
  file.write('["com.ar","gob.ar","org.ar","int.ar","net.ar","mil.ar","tur.ar","musica.ar","bet.ar","com.br","com.py","com","ar","info","net","org","biz","name","pro","aero","asia","cat","coop","edu","gov","int","jobs","mil","mobi","museum","post","tel","travel","xxx","barcelona","email","eurovision","eus","fútbol","gal","google","madrid","microsoft","pizza","restaurant","taxi","tienda","arpa","root","example","invalid","localhost","test","nato","ac","ad","ae","af","ag","ai","al","am","ao","aq","ar","as","at","au","aw","ax","az","ba","bb","bd","be","bf","bg","bh","bi","bj","bm","bn","bo","br","bs","bt","bw","by","bz","ca","cc","cd","cf","cg","ch","ci","ck","cl","cm","cn","co","cr","cu","cv","cw","cx","cy","cz","de","dj","dk","dm","do","dz","ec","ee","eg","er","es","et","eu","fi","fj","fk","fm","fo","fr","ga","gd","ge","gf","gg","gh","gi","gl","gm","gn","gp","gq","gr","gs","gt","gu","gw","gy","hk","hm","hn","hr","ht","hu","id","ie","il","im","in","io","iq","ir","is","it","je","jm","jo","jp","ke","kg","kh","ki","km","kn","kp","kr","kw","ky","kz","la","lb","lc","li","lk","lr","ls","lt","lu","lv","ly","ma","mc","md","me","mg","mh","mk","ml","mm","mn","mo","mp","mq","mr","ms","mt","mu","mv","mw","mx","my","mz","na","nc","ne","nf","ng","ni","nl","no","np","nr","nu","nz","om","pa","pe","pf","pg","ph","pk","pl","pm","pn","pr","ps","pt","pw","py","qa","re","ro","rs","ru","rw","sa","sb","sc","sd","se","sg","sh","si","sk","sl","sm","sn","so","sr","st","su","sv","sx","sy","sz","tc","td","tf","tg","th","tj","tk","tl","tm","tn","to","tr","tt","tv","tw","tz","ua","ug","uk","us","uy","uz","va","vc","ve","vg","vi","vn","vu","wf","ws","ye","yt","za","zm","zw","bv","gb","sj","bl","bq","eh","mf","ss","um","an","bu","cs","dd","tp","yu","zr"]')

electoral_criteria_path = '/content/drive/My Drive/envio_de_mails/electoral_criteria.txt'
with open(electoral_criteria_path, 'w') as file:
  file.write('"electoral", "partido", "interna", "contable", "financiamiento"')

strong_words_path = '/content/drive/My Drive/envio_de_mails/strong_words.txt'
with open(strong_words_path, 'w') as file:
  file.write('"FISCALIA FEDERAL", "FISCALÍA FEDERAL", "JUZGADO FEDERAL", "CÁMARA FEDERAL DE LA PLATA", "CAMARA FEDERAL DE LA PLATA", "LA PLATA", "DEPARTAMENTO JUDICIAL", ""ELECTORAL", "INTERNA", "CONTABLE", "APODERADO", "PARTIDO", "URNA", "URNAS", "ELECTORES", "VOTANTES", "ELECCIONES"')
