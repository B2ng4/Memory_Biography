import requests
import json

from config import MEMORY_TOKEN



def upload_bio(name:str,placeOfBirth:str, date:str, placeOfDeath:str, citizenship:str, education:str, occupation:str, awards:str, biography:str, epitaphy = "КРАТКАЯ ЭПИТАФИЯ", user="Пользователь"):
    date = date.split(" ")
    start = (date[0]).split(".")
    end = (date[1]).split(".")


    data_start = {
        "day":start[0],
        "month":start[1],
        "year":start[2],

    }

    data_end = {
        "day": end[0],
        "month": end[1],
        "year": end[2],
    }



    url = "https://mc.dev.rand.agency/api/page/79051330"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {MEMORY_TOKEN}"
    }



    dat = {
        "name": name,
        "start": data_start,
        "end": data_end,
        "epitaph": epitaphy,
        "author_epitaph": "АВТОР ЭПИТАФИИ",
        "page_type_id": "1",

        "biographies": [
            {

                "title": "Биография",
                "description": biography,
                "page_id": 8800,
                "created_at": "2023-12-28T07:16:33.000000Z",
                "updated_at": "2023-12-28T07:16:33.000000Z",
                "order": 1,
                "checked": True
            },
          ],
        "page_information": [
            {

                "page_id": 8800,
                "title": "pageInformation.placeOfBirth",
                "is_system": True,
                "description": placeOfBirth,
                "created_at": "2023-12-28T07:16:33.000000Z",
                "updated_at": "2023-12-28T07:16:33.000000Z"
            },
            {

                "page_id": 8800,
                "title": "pageInformation.placeOfDeath",
                "is_system": True,
                "description": placeOfDeath,
                "created_at": "2023-12-28T07:16:33.000000Z",
                "updated_at": "2023-12-28T07:16:33.000000Z"
            },


            {

                "page_id": 8800,
                "title": "pageInformation.citizenship",
                "is_system": True,
                "description": citizenship,
                "created_at": "2023-12-28T07:16:33.000000Z",
                "updated_at": "2023-12-28T07:16:33.000000Z"
            },
            {

                "page_id": 8800,
                "title": "pageInformation.education",
                "is_system": True,
                "description": education,
                "created_at": "2023-12-28T07:16:33.000000Z",
                "updated_at": "2023-12-28T07:16:33.000000Z"
            },
            {

                "page_id": 8800,
                "title": "pageInformation.occupation",
                "is_system":True,
                "description": occupation,
                "created_at": "2023-12-28T07:16:33.000000Z",
                "updated_at": "2023-12-28T07:16:33.000000Z"
            },
            {

                "page_id": 8800,
                "title": "pageInformation.awards",
                "is_system": True,
                "description": awards,
                "created_at": "2023-12-28T07:16:33.000000Z",
                "updated_at": "2023-12-28T07:16:33.000000Z"
            }
        ],



    }

    response = requests.put(url, headers=headers, data=json.dumps(dat))

    if response.status_code == 200:
        return True
    else:
        print(f"Request failed with status code {response.status_code}")

