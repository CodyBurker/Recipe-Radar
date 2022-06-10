import requests
import pandas as pd

# Given a query, get recipes
def get_recipe(query, api_key:str) -> pd.DataFrame:
    url =  "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"
    querystring = {"query":query}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    try:
        response_json = response.json()
    except ValueError:
        print('No JSON response')
        return None
    try:
        df = pd.DataFrame(response_json['results'])
    except KeyError:
        print('No results')
        return response_json
    return df


# Given a recipe, get the flavor profile
def get_taste(recipe_id: int, api_key: str) -> dict:
    url="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/%i/tasteWidget.json" % recipe_id
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }
    querystring = {"normalize":"false"}
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    try:
        response_json = response.json()
    except ValueError:
        print('No JSON response')
        return None
    return response_json