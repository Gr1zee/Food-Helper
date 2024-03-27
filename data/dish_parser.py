import requests
from googletrans import Translator

api_url = 'https://api.calorieninjas.com/v1/nutrition?query='


def search_dishes(dish):
    query = translate(dish)
    response = requests.get(api_url + query, headers={'X-Api-Key': 'ysUI9RJ681c46u5gGghrfA==BMxPohr2HoeiXhaV'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)


def translate(word):
    translator = Translator()
    translation = translator.translate(word, dest='en')
    return translation.text
