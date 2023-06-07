import requests
from bs4 import BeautifulSoup
from config import headers

import json
from write_results import write_json

def scrape_google_and_order(query, year, company):
    """Scrapes the google, chooses the best link between the 2 first results and sorts the found link according to the keywords found inside

    Args:
        query (string): google search query
        year (string): year of searched report
        company (string): company of searched report
    """
    print(year)

    # set the list of formats of company names wished in the url
    companySmall = company.lower()
    companySmallNoSpace = companySmall.replace(" ", "")
    companySmallUnderscore = companySmall.replace(" ", "_")
    companySmallDash = companySmall.replace(" ", "-")
    companySmallNoDot = companySmall.replace(".", "")
    companySlice0 = companySmall.split(" ")[0]

    allowed_names_in_link = [
        companySmall,
        companySmallNoSpace,
        companySmallUnderscore,
        companySmallDash,
        companySmallNoDot,
        companySlice0
    ]
    if(len(company.split(" ")) > 1):    
        companySlice1 = companySmall.split(" ")[1]
        allowed_names_in_link.append(companySlice1)
    else:
        companySlice1 = ""

    most_relevant_link, allData = scrape_google(query)

    # Going through the first two results in case the 2nd is better than the 1st
    first_iteration = True

    for data in allData[:2]:
        link = data.find('a').get('href')

        if not link == None:
            splittedLink = link.rsplit('/', 1)
            splittedFilename = splittedLink[1].split(".pdf")
            filename = splittedFilename[0]+".pdf"

            if any(companyName in str.lower(link) for companyName in allowed_names_in_link) and (year in filename) and ("report" in link or "Report" in link or "bericht" in link or "Bericht" in link):
                most_relevant_link = link
                write_json({'company': company, 'query': query, 'link': most_relevant_link}, 'found_results_0.json', year)
                break
                    
            else:
                # If the first link is doubtful, we try again with the second, and if the second is also, then we wright the first link in the doubt_file
                if not first_iteration:
                    write_json({'company': company, 'query': query, 'link': most_relevant_link}, 'doubt_results_0.json', year)
                first_iteration = False



def scrape_google(query):
    """Scrapes the google search results for given query

    Args:
        query (string): search query

    Returns:
        string, array: links found
    """
    url = "https://www.google.com/search?q=" + query
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    allData = soup.find_all("div",{"class":["g", "d4rhi"]})
    first_link = allData[0].find('a').get('href')
    most_relevant_link = first_link
    return most_relevant_link, allData