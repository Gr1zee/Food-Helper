import requests
from googletrans import Translator

api_url = 'https://api.calorieninjas.com/v1/nutrition?query='


def search_dishes(dish, mass):
    query = str(mass) + "g" + " " + translate(dish)
    if query:
        response = requests.get(api_url + query, headers={'X-Api-Key': 'ysUI9RJ681c46u5gGghrfA==BMxPohr2HoeiXhaV'})
        if response.status_code == requests.codes.ok and response.json()["items"]:
            return response.json()
        else:
            return None
    else:
        return None


def translate(word, lang="en"):
    translator = Translator()
    if lang == "ru":
        translation = translator.translate(word, dest='ru')
    else:
        translation = translator.translate(word, dest='en')
    if translation:
        return translation.text
    else:
        return None

def parser(json):
    data = []
    name = json["name"]