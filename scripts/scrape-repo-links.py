from bs4 import BeautifulSoup  # To sift through the HTML data
from pycookiecheat import chrome_cookies  # to use my github cookies so GitHub thinks its my browser
import requests  # To make a search
import json # for reading the JSON extracted from the page and converting to a python list

# get chrome cookies for the page, note just using the page 1 cookies, don't need to reload the cookies for each page
url = "https://github.com/search?p=1&q=Java&type=Repositories"
cookies = chrome_cookies(url)

# for holding all the found URLs
repo_urls = []

# iterate through the first 100 pages of java repos on github
for i in range(1, 101):
    url = "https://github.com/search?p=" + str(i) + "&q=Java&type=Repositories"

    # load the current page
    response = requests.get(url, cookies=cookies)

    # get soup objects to go through the HTML data
    soup = BeautifulSoup(response.text, features='html5lib')

    # find all repository list items in the page, which contain project links
    mylis = soup.findAll("li", {"class": "repo-list-item"})

    # find all the JSON (that has the link I want) that is in the a tag
    JSON_list = [li_elem.find("a", {"class": "v-align-middle"})["data-hydro-click"] for li_elem in mylis]

    # decode the JSON string to a python dictionary
    tags_dictionary_list = [json.loads(JSON) for JSON in JSON_list]

    print(tags_dictionary_list)

    # extract the urls for the JSON tags, (inside the inner result object inside the payload object inside the JSON
    repo_urls = repo_urls + [tag_elem["payload"]["result"]["url"] for tag_elem in tags_dictionary_list]

    # progress print
    print("page ", i, "done")


# write all the urls to a file
file = open("urls.txt", "w")
for url in repo_urls:
    file.write(url + "\n")

file.close()

print("done fetching urls!")

"""

This script is a preparation script only,
run to generate a csv of links to java repositories

"""

