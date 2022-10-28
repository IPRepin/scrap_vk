import json
import os.path

import requests
from tqdm import tqdm
from config import vk_token
from config import vk_api_version
from pprint import pprint


def get_wall_posts(group_name):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=40&access_token={vk_token}&v={vk_api_version}"
    req = requests.get(url)
    src = req.json()


    # проверяем существуел ли директолрия с именем группы
    if os.path.exists(f'{group_name}'):
        print(f"Директория с именем {group_name} уже существует.")
    else:
        os.mkdir(group_name)

    #сохраняем данные в json чтобы видексть структуру
    with open(f"{group_name}/{group_name}.json,", "w", encoding="utf8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # собираем список ID новых постов
    id_posts_lst = []
    posts = src["response"]["items"]
    for post  in posts:
        post = post["id"]
        id_posts_lst.append(post)

    '''Проверка, если файла не существует, значит это первый парсинг группы
    (отправляем все новые посты). Иначе начинаем проверку и отправляем только 
    новые посты'''
    if not os.path.exists(f"{group_name}/exist_posts_{group_name}.txt"):
        print("Файла с ID постов не существует, создаем файл!")
        with open(f"{group_name}/exist_posts_{group_name}.txt", "w", encoding="utf-8") as file:
            for item in id_posts_lst:
                file.write(str(item) + "\n")

        #извлекаем данные из постов
        for post in posts:

            post_id = post["id"]
            print(f'Отправляем пост с ID {post_id}')

            try:
                if "attachments" in post:
                    post = post["attachments"]
                    #извлекаем фото
                    if post[0]["type"] == "photo":
                        if len(post) == 1:
                            post_foto = post[0]["photo"]["photo_1280"]
                            print(post_foto)
                        else:
                            for post_item_photo in post:
                                post_foto = post_item_photo["photo"]["photo_1280"]
                                print(post_foto)


            except Exception:
                print(f"Что-то не так с постом ID {post_id}!")


    else:
        print("Файл с ID постов найден, начинаем выборку свежих постов!")




def main():
    group_name = input("Ведите название группы: ")
    get_wall_posts(group_name)

if __name__ == '__main__':
    main()
