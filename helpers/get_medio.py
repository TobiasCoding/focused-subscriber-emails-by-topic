import os, ast, json

tld_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'tld.lst')
tld_pattern = ast.literal_eval(open(tld_path, 'r').read())

media_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'media.json')
media = json.loads(open(media_path, 'r').read())

def get_medio(url):
  for tld in tld_pattern:
    if f'.{tld}/' in url:
      name = url.split(tld)[0].split("//")[-1]
      if name.startswith("www."):
        name = name[4:]
      name = name.replace(".","")
      try:
        return media[name]
      except:
        return name.capitalize()
  print(f"ERROR: Missing TLD. URL: {url}")
  return None