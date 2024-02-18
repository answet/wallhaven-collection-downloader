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
            print("Error:", res.status_code)
    except Exception as e:
        print("Error:",e)


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

        print(f'\nDone, collection downloaded in {os.getcwd()}')


def list_collections(collections,username):
    collections = collections.json()["data"]
    option = 0

    for collection in collections:
        link = f'https://wallhaven.cc/user/{username}/favorites/{collection["id"]}'
        option += 1
        print(f'{option}) {collection["label"]} : {collection["count"]} wallpapers\n{link}\n')
            
    number_collection = int(input("Collection: ")) - 1
    if (number_collection >= 0) and (number_collection < option):
        id = collections[number_collection]["id"]
        count = collections[number_collection]["count"]
        path = os.path.join(os.getcwd(),f"{collections[number_collection]['label']}")
        if not os.path.exists(path):
            os.mkdir(path)
        os.chdir(path)
        list_wallpapers(username,id,count)


def change_directory():
    path_pictures = os.path.expanduser("~/Pictures")
    path_wallpapers = os.path.join(path_pictures,"Wallpapers")

    if not os.path.exists(path_wallpapers):
        os.mkdir(path_wallpapers)
    os.chdir(path_wallpapers)


def main():
    parser = argparse.ArgumentParser(description="Enter a username, choose a collection, wait for the download, go to /Pictures/Wallpapers.")
    parser.add_argument("user", nargs="*", help="<username>")
    args = parser.parse_args()
       
    if args.user:
        user = args.user[0]
        collections = requests.get(f'https://wallhaven.cc/api/v1/collections/{user}')
        if collections.status_code == 200:
            change_directory()
            list_collections(collections,user)
        else:
            print(f'User {user} does not exist or cannot be found.')
    else:
        print("Use ./app.py -h for help.")

if __name__== "__main__":
    main()
