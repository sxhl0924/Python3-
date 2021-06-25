#fetch data from TasteDive

import requests_with_caching
import json

def get_movies_from_tastedive(movie_title):
    baseurl = "https://tastedive.com/api/similar"
    params_dic = {}
    params_dic["q"] = movie_title
    params_dic["type"] = "movies"
    params_dic["limit"] = 5
    this_page_cache = requests_with_caching.get(baseurl, params = params_dic)
    return json.loads(this_page_cache.text)

get_movies_from_tastedive("Black Panther")

# extracts just the list of movie titles from a dictionary returned by get_movies_from_tastedive

def extract_movie_titles(dic):
    movie_list = dic["Similar"]["Results"]
    title_list = [movie_list[i]["Name"] for i in range(len(movie_list))]
    return title_list

#extract_movie_titles(get_movies_from_tastedive("Tony Bennett"))

# write a function, called get_related_titles. It takes a list of movie titles as input.
#gets five related movies for each from TasteDive, extracts the titles for all of them

def get_related_titles(lst):
    combined_list = []
    for movie_title in lst:
        related_titles = extract_movie_titles(get_movies_from_tastedive(movie_title))
        for title in related_titles:
            if title not in combined_list:
                combined_list.append(title)
    return combined_list

get_related_titles(["Black Panther", "Captain Marvel"])

#fetch data from OMDB

def get_movie_data(movie_title):
    baseurl = "http://www.omdbapi.com/"
    param = {}
    param['t']= movie_title
    param['r']= "json"
    this_page_cache = requests_with_caching.get(baseurl, params = param)
    print(this_page_cache.url)
    print(this_page_cache.text)
    return json.loads(this_page_cache.text)

get_movie_data("Baby Mama")

#takes an OMDB dictionary result for one movie and extracts the Rotten Tomatoes rating as an integer
def get_movie_rating(dic):
    try:
        rating = dic["Ratings"][1]["Value"]
        try:
            return int(float(rating)*100)
        except:
            return int(rating[:-1])
    except:
        return 0

get_movie_rating(get_movie_data("Deadpool 2"))

#get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
def get_sorted_recommendations(movie_list):
    related_titles = get_related_titles(movie_list)
    return sorted(related_titles, key = lambda movie_title: (get_movie_rating(get_movie_data(movie_title)), movie_title), reverse = True)

get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
