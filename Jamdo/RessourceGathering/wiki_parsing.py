import requests
import json
import mwparserfromhell
import re



URL = "https://en.wikipedia.org/w/api.php"

## TYPE --------
## 1 = events --
## 2 = births --
## 3 = deaths --
#---------------


def output_data(year, month, day, type):

    url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext&redirects=1" \
          "&titles="+str(year)
    monthDict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December',
                 13: 'Nobel Prizes'}

    month_name = monthDict[month]
    nextMonth = month+1
    nextMonthName = monthDict[nextMonth]


    request = requests.get(url)
    r_text = request.json()

    page = next(iter(r_text['query']['pages'].values()))
    clean_page = str(mwparserfromhell.parse(page['extract']))

    ## events_births_deaths[1] is events
    ## events_births_deaths[2] is births
    ##events_births_deaths[3] is deaths
    events_births_deaths = re.split("=== January ===", clean_page)
    ##print("size = " + str(len(events_births_deaths)))
    ##print(categories[1])
    if type == 2:
        events_in_month = re.split("=== "+nextMonthName+" ===", events_births_deaths[2])[0]
    elif type == 3:
        events_in_month = re.split("=== " + nextMonthName + " ===", events_births_deaths[3])[0]
    else:
        events_in_month = re.split("=== " + nextMonthName + " ===", events_births_deaths[1])[0]

    if month > 1:
        events_in_month = re.split("=== "+month_name+" ===", events_in_month)
        events_in_month = events_in_month[1]
    ##print(events_in_month)
    ## events_in_month IS ALL THE EVENTS IN A SPECIFIC MONTH

    events_in_day = re.split(month_name, events_in_month)
    ## events in day is all the events in a day format I.E   "day digit - evetn description"
    ##index for days will be from [1 to len(events_in_days)-1}
    ##print(events_in_day)
    numbers = events_in_day[1][1:3]

    if numbers[1].isdigit():
        numbers = numbers
    else:
        numbers = numbers[0]

    ##print(numbers)
    day_info = re.split(numbers, events_in_day[1])
    dict_for_event_per_day = {str(year)+" "+month_name+" "+numbers:  day_info[1].replace("\n", " -")
                                        .replace("\u2013", ". ")}
    ##print(dict_for_event_per_day)
    ##print(dict_for_event_per_day)
    for x in range(2, len(events_in_day)-1):
        numbers = events_in_day[x][1:3]
        ##print(x)
        if numbers[1].isdigit():
            numbers = numbers
            day_info = re.split(numbers, events_in_day[x])
            dict_for_event_per_day.update({str(year) + " " + month_name + " " + numbers: day_info[1].replace("\n", " -")
                                          .replace("\u2013", "")})
        elif numbers[0].isdigit() and not numbers[1].isdigit():
            numbers = numbers[0]
            day_info = re.split(numbers, events_in_day[x])
            dict_for_event_per_day.update({str(year) + " " + month_name + " " + numbers: day_info[1].replace("\n", " -")
                                          .replace("\u2013", "")})
    ##return events_in_month
    return dict_for_event_per_day



    PARAMS = {
        'action': "query",
        'list': "search",
        'srsearch': year,
        'format': "json"
    }
    S = requests.Session()
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()






'''''
if DATA['query']['search'][0]['title'] == year:
    print("Your search page '" + SEARCHPAGE + "' exists on English Wikipedia")
'''


##print(output_data(1948, 1, 1, 1))
test = output_data(1948, 2, 30, 1)
##print(test["1948 January 30"])







