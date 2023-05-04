import requests
from bs4 import BeautifulSoup
from vars_for_requests import headers

def scrape_google_and_order(query, year, company, found_list, doubt_list):
    print(year)

    # set the list of formats of company names wished in the url
    companySmall = company.lower()
    companySmallNoSpace = companySmall.replace(" ", "")
    companySmallUnderscore = companySmall.replace(" ", "_")
    companySmallDash = companySmall.replace(" ", "-")
    companySmallNoDot = companySmall.replace(".", "")
    year_2_digits = year[-2:]
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

    url = "https://www.google.com/search?q=" + query
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    # Find all google search results (g class) and sub-results (d4rhi class)
    allData = soup.find_all("div",{"class":["g", "d4rhi"]})

    if len(allData) > 0:

        first_link = allData[0].find('a').get('href')
        most_relevant_link = first_link

        # Going through the first two results in case the 2nd is better than the 1st
        first_iteration = True
        for data in allData[:2]:
            link = data.find('a').get('href')
            splittedLink = link.rsplit('/', 1)
            splittedFilename = splittedLink[1].split(".pdf")
            filename = splittedFilename[0]+".pdf"

            if year not in found_list.keys():
                        found_list[year] = []

            if any(companyName in str.lower(link) for companyName in allowed_names_in_link) and ((year in filename) or ((year_2_digits != "20") and (year_2_digits in filename))) and ("report" in link or "Report" in link or "bericht" in link or "Bericht" in link):
                
                    most_relevant_link = link
                    found_list[year].append({'company': company, 'query': query, 'link': most_relevant_link})
                    # download_pdf(most_relevant_link,year,company)
                    break
                    
            else:

                # If the first link is doubtful, we try again with the second, and if the second is also, then we wright the first link in the doubt_file
                if not first_iteration:

                    #Create dict table sorted by year
                    if year not in doubt_list.keys():
                        doubt_list[year] = []

                    doubt_list[year].append({'company': company, 'query': query, 'link': most_relevant_link})

                first_iteration = False

        
    #     return most_relevant_link
    # else:
    #      return None