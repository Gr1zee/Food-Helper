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


def dish_hendler(list_products):
    total_mass = 0
    total_calories = 0
    total_fat = 0
    total_protein = 0
    total_carbohydrates = 0

    for item in list_products['items']:
        total_mass += float(item['serving_size_g'])
        total_calories += float(item['calories'])
        total_fat += float(item['fat_total_g'])
        total_protein += float(item['protein_g'])
        total_carbohydrates += float(item['carbohydrates_total_g'])

    # подсчет КБЖУ на 100 грамм блюда
    relatively_calories = round((total_calories * 100) / total_mass, 4)
    relatively_fat = round((total_fat * 100) / total_mass, 4)
    relatively_protein = round((total_protein * 100) / total_mass, 4)
    relatively_carbohydrates = round((total_carbohydrates * 100) / total_mass, 4)
    res = {'relatively_calories': relatively_calories, 'relatively_fat': relatively_fat,
           'relatively_protein': relatively_protein,
           'relatively_carbohydrates': relatively_carbohydrates}
    total_res = {'total_mass': total_mass, 'total_calories': total_calories, 'total_fat': total_fat,
                 'total_protein': total_protein, 'total_carbohydrates': total_carbohydrates}
    result = {'total': total_res, 'relatively': res}
    return result


def translate(word):
    translator = Translator()
    translation = translator.translate(word, dest='en')
    if translation:
        return translation.text
    else:
        return None
