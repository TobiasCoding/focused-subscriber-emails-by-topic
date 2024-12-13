import os

def build_database():
    path = os.path.dirname(os.path.abspath(__file__))
    mails_by_category_path = os.path.join(path, 'mails_by_category.json')
    with open(mails_by_category_path, 'w') as file:
        file.write('''
    {
    "electoral": [],
    "no_electoral": []
    }
    ''')

    # Usuarios por categoría
    destinatarios_path = os.path.join(path, 'users.json')
    with open(destinatarios_path, 'w') as file:
        file.write('''
    {
        "test": {
            "test@test.com": ["Test", "Test office"]
        },
        "all_categorys": {
            "user1@mail.com": ["name1 lastname1", "office1"],
            "user2@mail.com": ["name2 lastname2", "office2"]
        },
        "electoral": {
            "user3@mail.com": ["name3 lastname3", "office3"]
        },
        "no_electoral": {}
    }
    ''')

    media_path = os.path.join(path, 'media.json')
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
        "fenix951": "Multiplataforma Fenix La Rioja",
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
        "laletrachica": "La Letra Chica",
        "eldia": "El Día",
        "dataclave": "Data Clave",
        "elfuertediario": "Diario El Fuerte",
        "nden": "Nden",
        "ole": "Diario Olé",
        "loquepasa": "Lo que pasa",
        "diputadosbsas": "Diputados de la Provincia de Buenos Aires",
        "infogei": "Info GEi",
        "lapoliticaonline" : "La Política Online",
        "cronista": "El Cronista",
        "ambito": "Ámbito Financiero",
        "tycsports": "TyC Sports",
        "eldestapeweb": "El Destape Web",
        "casarosada": "Casa Rosada",
        "conicet": "CONICET",
        "dw": "Deutsche Welle (DW)"
    }
    ''')

    tld_path = os.path.join(path, 'tld.lst')
    with open(tld_path, 'w') as file:
        file.write('["com.ar","gob.ar","org.ar","int.ar","net.ar","mil.ar","tur.ar","musica.ar","bet.ar","com.br","com.py","com","ar","info","net","org","biz","name","pro","aero","asia","cat","coop","edu","gov","int","jobs","mil","mobi","museum","post","tel","travel","xxx","barcelona","email","eurovision","eus","fútbol","gal","google","madrid","microsoft","pizza","restaurant","taxi","tienda","arpa","root","example","invalid","localhost","test","nato","ac","ad","ae","af","ag","ai","al","am","ao","aq","ar","as","at","au","aw","ax","az","ba","bb","bd","be","bf","bg","bh","bi","bj","bm","bn","bo","br","bs","bt","bw","by","bz","ca","cc","cd","cf","cg","ch","ci","ck","cl","cm","cn","co","cr","cu","cv","cw","cx","cy","cz","de","dj","dk","dm","do","dz","ec","ee","eg","er","es","et","eu","fi","fj","fk","fm","fo","fr","ga","gd","ge","gf","gg","gh","gi","gl","gm","gn","gp","gq","gr","gs","gt","gu","gw","gy","hk","hm","hn","hr","ht","hu","id","ie","il","im","in","io","iq","ir","is","it","je","jm","jo","jp","ke","kg","kh","ki","km","kn","kp","kr","kw","ky","kz","la","lb","lc","li","lk","lr","ls","lt","lu","lv","ly","ma","mc","md","me","mg","mh","mk","ml","mm","mn","mo","mp","mq","mr","ms","mt","mu","mv","mw","mx","my","mz","na","nc","ne","nf","ng","ni","nl","no","np","nr","nu","nz","om","pa","pe","pf","pg","ph","pk","pl","pm","pn","pr","ps","pt","pw","py","qa","re","ro","rs","ru","rw","sa","sb","sc","sd","se","sg","sh","si","sk","sl","sm","sn","so","sr","st","su","sv","sx","sy","sz","tc","td","tf","tg","th","tj","tk","tl","tm","tn","to","tr","tt","tv","tw","tz","ua","ug","uk","us","uy","uz","va","vc","ve","vg","vi","vn","vu","wf","ws","ye","yt","za","zm","zw","bv","gb","sj","bl","bq","eh","mf","ss","um","an","bu","cs","dd","tp","yu","zr"]')

    electoral_criteria_path = os.path.join(path, 'electoral_criteria.lst')
    with open(electoral_criteria_path, 'w') as file:
        file.write('"electoral", "partido", "interna", "contable", "macri", "cristina", "cfk", "milei", "ucr-", "peronista", "justicialista", "libertario", "pj-", "pro-", "financiamiento"')

    strong_words_path = os.path.join(path, 'strong_words.lst')
    with open(strong_words_path, 'w') as file:
        file.write('"FISCALIA FEDERAL", "FISCALÍA FEDERAL", "JUZGADO FEDERAL", "CÁMARA FEDERAL DE LA PLATA", "CAMARA FEDERAL DE LA PLATA", "LA PLATA", "DEPARTAMENTO JUDICIAL", "ALEJO RAMOS PADILLA", "JUAN FRANCISCO PAIVA", "JUAN FRANCISCO LUENA", "LAURA ROTETA", "ELECTORAL", "INTERNA", "CONTABLE", "APODERADO", "MACRI", "CRISTINA", "CFK", "MILEI", " PJ ", "PARTIDO JUSTICIALISTA", "PARTIDO", "LIBERTAD AVANZA", " PRO ", " UCR", "PERONISTA", "RADICAL", "LIBERTARIO", "URNA", "URNAS", "ELECTORES", "VOTANTES", "ELECCIONES"')

