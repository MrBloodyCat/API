from operator import length_hint
from flask import jsonify, render_template
import random
import os
import json
from fuzzywuzzy import process
from PIL import Image

with open('data_anime.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('data_hentai.json', 'r', encoding='utf-8') as file:
    data2 = json.load(file)

# apis
async def as_apis():
    list_1 = os.listdir(f'./data/gif')
    list_2 = os.listdir(f'./data/nsfw')
    list_3 = ['type_en', 'type_ru', 'year', 'rating', 'genres_en', 'genres_ru']
    list_4 = ['censored', 'genres', 'year']
    return render_template('apis.html', list_1 = list_1, list_2 = list_2, list_3 = list_3, list_4 = list_4)

# стартовая страничка
async def as_welcome():
    return render_template('welcome.html')

# документация
async def as_docs():
    return render_template('docs.html')

# случайная гифка
async def as_get_gif(id):
    list = []
    if id == 'list':  
        x = {'list': os.listdir(f'./data/gif')}
        return jsonify(x)

    if id not in os.listdir(f'./data/gif'):
        x = {'status': {'message': 'Bad Request', 'status_code': 400}}
        return jsonify(x)

    for names in os.listdir(f'./data/gif/{id}'):
        list.append(names)
    name = random.randrange(length_hint(list))

    img = Image.open(f"./data/gif/{id}/{list[name]}")
    (width, height) = img.size

    x = {'url': f'https://disapi.ru/gif/{id}/{list[name]}', 'width': width, 'height': height}
    return jsonify(x)

# случайная nsfw
async def as_get_nsfw(id):
    list = []
    if id == 'list':  
        x = {'list': os.listdir(f'./data/nsfw')}
        return jsonify(x)

    if id not in os.listdir(f'./data/nsfw'):
        x = {'status': {'message': 'Bad Request', 'status_code': 400}}
        return jsonify(x)
        
    for names in os.listdir(f'./data/nsfw/{id}'):
        list.append(names)
    name = random.randrange(length_hint(list))

    img = Image.open(f"./data/nsfw/{id}/{list[name]}")
    (width, height) = img.size

    x = {'url': f'https://disapi.ru/nsfw/{id}/{list[name]}', 'width': width, 'height': height}
    return jsonify(x)

# случайная мем
async def as_get_meme():
    list = os.listdir(f'./data/meme')
    len = length_hint(list)
    number = random.randint(0, len - 1)
    x = {'url': f'https://disapi.ru/meme/{list[number]}'}
    return jsonify(x)

# случайное аниме
async def as_get_anime():
    len = length_hint(data)
    number = random.randint(1, len)
    x = data[f'{number}']
    return jsonify(x)

# случайный хентай
async def as_get_hentai():
    len = length_hint(data2)
    number = random.randint(1, len)
    x = data2[f'{number}']
    return jsonify(x)

# случайное аниме по запросу
async def as_get_anime_type(type, id):
    type_list = ['type_en', 'type_ru', 'year', 'rating', 'genres_en', 'genres_ru']
    list = []
    if type not in type_list:
        x = {'status': {'message': 'Bad Request', 'status_code': 400}}
        return jsonify(x)

    if id == 'list':
        if type == 'genres_en' or type == 'genres_ru':
            for number in data:
                if data[number][type]:
                    for text in data[number][type]:
                        if text not in list:
                            list.append(text)
        else:
            for number in data:
                if data[number][type]:
                    if data[number][type] not in list:
                        list.append(data[number][type])
        x = {'list': list}
        return jsonify(x)

    if type == 'genres_en' or type == 'genres_ru':
        for number in data:
            if data[number][type]:
                if id in data[number][type]:
                    list.append(number)

    else:
        for number in data:
            if data[number][type]:
                if str(data[number][type]) == id:
                    list.append(number)

    len = length_hint(list)
    number = random.randint(0, len - 1)
    if len == 0:
        x = {'status': {'message': 'Not Found', 'status_code': 404}}

    else:
        x = data[list[number]]

    return jsonify(x)

# случайный хентай по запросу
async def as_get_hentai_type(type, id):
    type_list = ['censored', 'genres', 'year']
    list = []
    if type not in type_list:
        x = {'status': {'message': 'Bad Request', 'status_code': 400}}
        return jsonify(x)

    if id == 'list':
        if type == 'genres':
            for number in data2:
                if data2[number][type]:
                    for text in data2[number][type]:
                        if text not in list:
                            list.append(text)
        else:
            for number in data2:
                if data2[number][type] not in list:
                    list.append(data2[number][type])
        x = {'list': list}
        return jsonify(x)

    if type == 'genres':
        for number in data2:
            if data2[number][type]:
                if id in data2[number][type]:
                    list.append(number)

    else:
        for number in data2:
            if str(data2[number][type]) == id:
                list.append(number)

    len = length_hint(list)
    number = random.randint(0, len - 1)
    if len == 0:
        x = {'status': {'message': 'Not Found', 'status_code': 404}}

    else:
        x = data2[list[number]]

    return jsonify(x)

# поиск аниме по названию
async def as_get_anime_find(lang, id):
    list = []
    if lang == 'ru':
        name = 'name_ru'
    elif lang == 'en':
        name = 'name_en'
    else:
        x = {'status': {'message': 'Bad Request', 'status_code': 400}}
        return jsonify(x)

    for number in data:
        list.append(data[number][name])
    
    x = process.extract(id, list, limit=3)

    for all_anime in data:
        if data[all_anime][name] == x[0][0]:
            anime_1 = data[f'{all_anime}']
        if data[all_anime][name] == x[1][0]:
            anime_2 = data[f'{all_anime}']
        if data[all_anime][name] == x[2][0]:
            anime_3 = data[f'{all_anime}']

    x = {'top_1': anime_1, 'top_2': anime_2, 'top_3': anime_3}
    return jsonify(x)

# поиск хентая по названию 
async def as_get_hentai_find(id):
    list = []
    for number in data2:
        list.append(data2[number]['name'])
    
    x = process.extract(id, list, limit=3)

    for all_anime in data2:
        if data2[all_anime]['name'] == x[0][0]:
            anime_1 = data2[f'{all_anime}']
        if data2[all_anime]['name'] == x[1][0]:
            anime_2 = data2[f'{all_anime}']
        if data2[all_anime]['name'] == x[2][0]:
            anime_3 = data2[f'{all_anime}']

    x = {'top_1': anime_1, 'top_2': anime_2, 'top_3': anime_3}
    return jsonify(x)