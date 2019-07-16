from bs4 import BeautifulSoup  # To sift through the HTML data
import requests  # To make a search

"""

Given a repository url,

check if it is a Java one and not something else,
then, check to see if it is a

"""


def check_repo_type(repo_url):
    """
    :return: string:
    "non-Java" if not actually a java repo
    "raw" for plain java, or "gradle", "maven", the other one etc etc
    """

    # FIRST ---- IS IT JAVA?

    # get cookies for request
    # cookies = chrome_cookies(repo_url)

    # load the repo page
    response = requests.get(repo_url)

    # get soup objects to go through the HTML data
    soup = BeautifulSoup(response.text, features='html5lib')

    # get the stat switcher off of the github page
    stat_switcher = soup.find("div", {"class": "stats-switcher-wrapper"})

    # get the different languages the repository has
    langs_span = stat_switcher.findAll("span", {"class": "lang"})

    # get out the inner HTML
    langs = [element.decode_contents() for element in langs_span]

    if langs[0].lower() != "java":
        # This isn't a java project, don't bother with it
        return "non-java"

    # SECOND - WHAT KIND OF JAVA PROJECT
    # now check what kind of java project, is it bazel, maven, gradle, ant, or plain (build in commandline - modules
    # may well be missing).
    # (for now I assume raw if build scripts from any of bazel, maven, gradle or ant are missing)

    # first get the files list to inspect them
    file_wrap = soup.find("div", {"class": "file-wrap"})
    table = file_wrap.find("table", {"class": "files js-navigation-container js-active-navigation-container"})
    file_messages = table.findAll("a", {"class": "js-navigation-open"})

    # extract innerHTML content
    file_names = [element.decode_contents() for element in file_messages]

    #print(file_names)

    # now check the files for the relevant scripts:
    if "build.gradle" in file_names:
        return "gradle"
    elif "pom.xml" in file_names:
        return "maven"
    elif "build.xml" in file_names:
        return "ant"
    elif "BUILD" in file_names:
        return "bazel"
    else:
        return "plain-java"


print(check_repo_type("https://github.com/BenjaminPhi5/Mix-Tab"))  # should be non-java
print("--------------------------------------------------------")
print(check_repo_type("https://github.com/TheAlgorithms/Java"))    # should be plain-java
print("--------------------------------------------------------")
print(check_repo_type("https://github.com/google/guava"))          # should be maven
print("--------------------------------------------------------")
print(check_repo_type("https://github.com/ReactiveX/RxJava#rxjava-reactive-extensions-for-the-jvm"))  # should be gradle
print("--------------------------------------------------------")
