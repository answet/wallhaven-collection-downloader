#!/usr/bin/python3

import requests
import argparse
import os

def download_wallpaper(url, name):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            with open(name, 'wb') as file:
                file.write(res.content)
            print("New wallpaper downloaded:", name)
        else:
            print("Error al descargar:", res.status_code)
    except Exception as e:
        print("Ocurrio un error:",e)


def list_wallpapers(user,id,count):
    page = 1

    while count > 0:
        r = requests.get(f'https://wallhaven.cc/api/v1/collections/{user}/{id}?page={page}')
        r = r.json()["data"]
        
        count -= 24
        page  +=  1

        for wallpaper in r:
            url = wallpaper["path"]
            name_wall = url.split("-")
            name_wall = name_wall[1]
        
            download_wallpaper(url, name_wall)


def list_collections(collections,username):
    collections = collections.json()["data"]
    option = 0

    for collection in collections:
        link = f'https://wallhaven.cc/user/{username}/favorites/{collection["id"]}'
        option += 1
        print(f'{option}) {collection["label"]} : {collection["count"]} wallpapers\n{link}\n')
            
    choice = int(input("Numero de coleccion: ")) - 1
    if (choice >= 0) and (choice < option):
        id = collections[choice]["id"]
        count = collections[choice]["count"]
        path = os.path.join(os.getcwd(),f"{collections[choice]['label']}")
        if not os.path.exists(path):
            os.mkdir(path)
        os.chdir(path)
        list_wallpapers(username,id,count)


def main():
    parser = argparse.ArgumentParser(description="Este programa es para descargar colecciones de wallpapers de la pagina Wallhaven.")
    parser.add_argument("-u","--user", help="Mostrar las colecciones de un usuario",metavar="<username>")
    args = parser.parse_args()
    
    path_pictures = os.path.expanduser("~/Pictures")
    path_wallpapers = os.path.join(path_pictures,"Wallpapers")

    if not os.path.exists(path_wallpapers):
        os.mkdir(path_wallpapers)
    os.chdir(path_wallpapers)

    if args.user:
        collections = requests.get(f'https://wallhaven.cc/api/v1/collections/{args.user}')
        if collections.status_code == 200:
            list_collections(collections,args.user)

if __name__== "__main__":
    main()
