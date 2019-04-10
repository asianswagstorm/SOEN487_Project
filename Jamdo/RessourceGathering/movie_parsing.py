import requests
import json
import mwparserfromhell
import re


def output_top_movie(top_number):

    ##max is top 100 hundred

    api_key = "c2b84190b996d9900e662ef19454db80"
    iter_total = 0
    i = 0

    movieDict = dict()
    while iter_total < top_number:
        i += 1
        url = "http://api.themoviedb.org/3/movie/top_rated?api_key=" + api_key + "&language=en-US&page=" + str(i)
        request = requests.get(url)
        json_re = request.json()

        iter_number = len(json_re['results'])
        for x in range(0, iter_number):
            movieDict[x+iter_total] = {'rank': x + 1 + iter_total, 'title': json_re['results'][x]['title'],
                            'vote_average': json_re['results'][x]['vote_average'],
                            'description': json_re['results'][x]['overview'],
                            'release_date': json_re['results'][x]['release_date']}
            ##print(movieDict[x+iter_total])
        iter_total += iter_number

    ##print(len(movieDict))
    for y in range(len(movieDict)-1, top_number-1, -1):
        movieDict.pop(y)

    return movieDict


# json_re2 = output_top_movie(66)






