import requests
import os
import csv
from bs4 import BeautifulSoup
import random
import json
import fitz

user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

for _ in user_agent_list:
    #Pick a random user agent
    user_agent = random.choice(user_agent_list)

print(user_agent)

#Set the headers 
headers = {'User-Agent': user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            'Cache-Control': 'no-cache'
}

# from itertools import cycle

# list_proxy = [
#                 'https://176.113.73.104:3128',
#                 'https://176.113.73.99:3128',
#                 'https://67.205.190.164:8080',
#                 'https://46.21.153.16:3128',
#                 'https://84.17.35.129:3128',
#                 'https://104.248.59.38:80',
#                 'https://12.156.45.155:3128',
#                 'https://176.113.73.102:3128',
#                 'https://142.11.222.22:80',
#                 'https://107.178.9.186:8080',
#                 'https://34.29.41.58:3128',
#                 'https://137.184.197.190:80',
#                 'https://194.186.127.60:80'
#             ]

# proxy_cycle = cycle(list_proxy)
# proxy = next(proxy_cycle)
# print(proxy)
# proxy = {
#    "http": proxy,
#     "https":proxy
# }

def scrape_google_and_order(query, year, doubt_count, company):
    print(year)

    # set the list of formats of company names wished in the url
    companySmall = company.lower()
    companySmallNoSpace = companySmall.replace(" ", "")
    #companyNoSpace = company.replace(" ", "")
    #companyUnderscore = company.replace(" ", "_")
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
    soup = BeautifulSoup(html.text, 'html.parser')

    # Find all google search results (g class) and sub-results (d4rhi class)
    allData = soup.find_all("div",{"class":["g", "d4rhi"]})

    first_link = allData[0].find('a').get('href')
    most_relevant_link = first_link

    # Going through the first two results in case the 2nd is better than the 1st
    first_iteration = True
    for data in allData[:2]:
        link = data.find('a').get('href')
        splittedLink = link.rsplit('/', 1)
        splittedFilename = splittedLink[1].split(".pdf")
        filename = splittedFilename[0]+".pdf"

    
        if any(companyName in str.lower(link) for companyName in allowed_names_in_link) and ((year in filename) or ((year_2_digits != "20") and (year_2_digits in filename))) and ("report" in link or "Report" in link or "bericht" in link or "Bericht" in link):
            
                if year not in found_list.keys():
                    found_list[year] = []
                most_relevant_link = link
                found_list[year].append({'query': query, 'link': most_relevant_link})
                download_pdf(most_relevant_link,year,company)
                break
                
        else:

            # If the first link is doubtful, we try again with the second, and if the second is also, then we wright the first link in the doubt_file
            if not first_iteration:
                
                filepath = download_pdf(most_relevant_link,year,company)
                #filepath = "resultPDFs/" + company + "/" + year + "_report.pdf"
                print("To be checked : " + link)

                #Create dict table sorted by year
                if year not in doubt_list.keys():
                    doubt_list[year] = []

                pdf_text_is_relevant = check_pdf_txt(filepath, year, company)
                if not pdf_text_is_relevant:
                    doubt_count +=1
                    doubt_list[year].append({'query': query, 'link': most_relevant_link})
                elif pdf_text_is_relevant == 403:
                    doubt_list[year].append({'query': query, 'link': most_relevant_link, 'error': 'PDF could not be read'})
                else:
                    if year not in found_list.keys():
                        found_list[year] = []
                    found_list[year].append({'query': query, 'link': most_relevant_link})

            first_iteration = False

    
    return most_relevant_link, doubt_count


def download_pdf(link, yearString, companyName):

    response = requests.get(link, headers=headers)
    print(response.status_code)
    if response.status_code == 200 and ".pdf" in link:

        if not os.path.exists("resultPDFs/"+companyName):
            os.makedirs("resultPDFs/"+companyName)

        pdf = open(os.path.join("resultPDFs/"+companyName, yearString+"_report.pdf"), 'wb')
        pdf.write(response.content)
        pdf.close()

        filepath = "resultPDFs/" + companyName + "/" + yearString + "_report.pdf"
        return filepath
    else:
        return None

def check_pdf_txt(pdf, year, companyName):
    
    if pdf != None:
        file = fitz.open(pdf)

        #txt = open('linde_2017_report.txt', 'wb')

        #pageNum = 0
        textInPages = ''
        for page in file.pages(0,3):
            #pageNum += 1
            # Extract text
            textOnePage = page.get_text()
            textInPages += textOnePage
        
        allowed_terms = [
            'sustainability',
            'sustainable',
            'annual',
            'environmental',
            'responsibility',
            'emission'

        ]

        if companyName == 'KplusS':
            companyName = 'K+S'
        elif 'oe' in companyName:
            companyName = companyName.replace('oe','ö')

        if any(word in str.lower(textInPages) for word in allowed_terms) and ("report" in str.lower(textInPages) or "information" in str.lower(textInPages)) and year in textInPages and str.lower(companyName) in str.lower(textInPages):
            return True
        else:
            return False
    else:
        return 403

years_to_search = [2017, 2018, 2019, 2020, 2021, 2022]


doubt_count = 0
doubt_list = {}
found_list = {}
conclusions_found = []

for year in years_to_search:
    to_find_per_year = 0

    with open('Google Crawling/dax.csv') as csv_file:
        dax_reader = csv.reader(csv_file, delimiter='\n')

        for i, companyRow in enumerate(dax_reader):
            print(companyRow[0])
            to_find_per_year += 1
            scraping_result = scrape_google_and_order(companyRow[0] + " sustainability report " + str(year) + " inurl:pdf", str(year), doubt_count, companyRow[0])
            doubt_count = scraping_result[1]
    
     
        found_per_year = len(found_list[str(year)])*100/to_find_per_year
        conclusions_found.append(str(year) + " : " + str(found_per_year) + "% were found\n")

    
    
    conclusion_doubt = str(doubt_count) + " might be wrong :"
    
    
    # writing the data into the files
    with open('doubtful_results.txt','w') as write_file: 
      write_file.write(conclusion_doubt)
      json.dump(doubt_list, write_file, indent=4)
    with open('found_results.txt','w') as write_file: 
      for percentage in conclusions_found :
          write_file.write(percentage)
      json.dump(found_list, write_file, indent=4)

# TEST
# companyRow = "Deutsche Boerse"
# year = 2018
# scrape_google_and_order("Deutsche Boerse sustainability report 2018 inurl:pdf", str(year), 0, companyRow)

#TODO str.lower( for link and list of words in if)
#MAN 2020