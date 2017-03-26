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

startUrl = "https://en.wikipedia.org/wiki/Number"
baseUrl = "https://en.wikipedia.org"

def findPhilosophy():
    foundPhilosophy = False # false while we have not hit the "Philosophy" Wikipedia page
    currentUrl = "https://en.wikipedia.org/wiki/Quality_(philosophy)"
    while(foundPhilosophy == False):
        print "Looking for philosophy from: " + currentUrl

        # Load the current page
        request = urllib2.Request(currentUrl, headers=hdr)
        wikiPage = urllib2.urlopen(request)
        soup = BeautifulSoup(wikiPage.read(),"html.parser")
        pageName = soup.find("h1",id="firstHeading").contents[0] # IDs are unique so there should only be one of these in the document.
        print pageName


        if(pageName == "Philosophy"):
            foundPhilosophy = True
        else:
            # Find the first URL in the article
            pageContent = soup.find('div',id="mw-content-text")
            contentLinks = pageContent.find_all('a')

            # Remove disambiguation link
            withoutDisambiguation = filter(isValidUrl,contentLinks)


            nextUrl = baseUrl + withoutDisambiguation[0]["href"] # I should check the formatting of this
            currentUrl = nextUrl



def isValidUrl(link):
    isValid = True

    if link.has_attr("class") and "mw-disambig" in link.attrs["class"]:
         isValid = False

    return isValid



def main():
    findPhilosophy()
    print "Done"


main()