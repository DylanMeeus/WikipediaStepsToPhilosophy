import sys
import urllib2
from bs4 import BeautifulSoup

""" Program to find how to get to the Philosophy Wikipedia page from any other wikipedia page """

"""idea: fastest way to philosophy from any webpage?"""


# test chain
# number -> mathematical object -> abstract object ->  referent -> linguistics -> scientific -> knowledge -> awareness
# -> quality -> philosophy

# set headers
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection' : 'keep-alive'}


baseUrl = "https://en.wikipedia.org"

global articlesEncountered # The articles that were found when searching for philosophy

def findPhilosophy(startUrl):
    global articlesEncountered
    foundPhilosophy = False # false while we have not hit the "Philosophy" Wikipedia page
    currentUrl = startUrl
    while(foundPhilosophy == False):
        print "Looking for philosophy from: " + currentUrl

        # Load the current page
        request = urllib2.Request(currentUrl, headers=hdr)
        wikiPage = urllib2.urlopen(request)
        soup = BeautifulSoup(wikiPage.read(),"html.parser")
        pageName = soup.find("h1",id="firstHeading").contents[0] # IDs are unique so there should only be one of these in the document.
        articlesEncountered.append(pageName)

        if(pageName == "Philosophy"):
            foundPhilosophy = True
        else:
            # Find the first URL in the article
            pageContent = soup.find('div',id="mw-content-text")
            contentLinks = pageContent.find_all('a')

            # Remove disambiguation link
            withoutDisambiguation = filter(isValidUrl,contentLinks)
            firstLink = withoutDisambiguation[0]["href"]
            nextUrl = baseUrl + firstLink if firstLink.startswith("/wiki/") else firstLink # Append the base URL if the URL starts with /wiki, otherwise we have a full URL
            currentUrl = nextUrl



def isValidUrl(link):
    isValid = True

    # Exclude disambiguations
    if link.has_attr("class") and "mw-disambig" in link.attrs["class"]:
         isValid = False

    # Exclude files (such as images, video references, ..)
    if link["href"].startswith("/wiki/File:"):
        isValid = False

    return isValid



def main():
    global articlesEncountered
    articlesEncountered = []
    #start = raw_input("Enter the wikipedia URL from which to start the search:")
    start = "https://en.wikipedia.org/wiki/Number"
    findPhilosophy(start)
    print "Done, path used:"
    pathString = ""
    for article in articlesEncountered:
        pathString += (article + " -> " if article != articlesEncountered[len(articlesEncountered)-1] else article)

    print pathString

main()