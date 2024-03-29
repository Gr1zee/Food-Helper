import requests
from googletrans import Translator

api_url = 'https://api.calorieninjas.com/v1/nutrition?query='


def search_product(products):
    query = ''
    for item in products:
        query += item[1] + "g" + " " + translate(item[0]) + ', '
    query = query[:-2]
    if query:
        response = requests.get(api_url + query, headers={'X-Api-Key': 'ysUI9RJ681c46u5gGghrfA==BMxPohr2HoeiXhaV'})
        if response.status_code == requests.codes.ok and response.json()["items"]:
            return response.json()
        else:
            return None
    else:
        return None


def translate(word):
    translator = Translator()
    translation = translator.translate(word, dest='en')
    if translation:
        return translation.text
    else:
        return None

print(search_product(['огурец', '23']))
