import csv
import json
from crawling import scrape_google_and_order
from download import download_pdf
from text_reading import read_and_reorder_pdf
from write_results import write_stats
import pandas as pd
import time
import re


years_to_search = ["2017", "2018", "2019", "2020", "2021", "2022"]
doubt_count = 0
doubt_list = {}
found_list = {}
conclusions_found = []

msci_list = pd.read_csv("Google Crawling/msci.csv")["Name"]

not_allowed_terms = [
    ' inc',
    ' group',
    " class",
    " ltd",
    " plc",
    " ag",
    " sa",
    " corp"
]

# to comment
f = open('doubt_results_0.json', 'w')
f = open('found_results_0.json', 'w')

# TODO associate last company done to variables last_year and last_company and start for loop at last company ONLY for the first iteration

for year in years_to_search: 

    with open('Google Crawling/dax.csv') as csv_file:
        dax_reader = csv.reader(csv_file, delimiter='\n')

        for i, companyRow in enumerate(dax_reader):
            print(companyRow[0])
            scrape_google_and_order(companyRow[0] + " sustainability report " + year + " filetype:pdf", year, companyRow[0])
            with open('last_company_done.txt','w') as write_file:
                write_file.write(year + "-" + companyRow[0] + "\n")

        # for company in msci_list:
        #     company = str.lower(company)
        #     for word in not_allowed_terms:
        #         found = re.search(word + "(\s|$)", company)
        #         if found:
        #             company = company.split(word, 1)[0]
        #     print(company)
        #     scrape_google_and_order(company + " sustainability report " + year + " filetype:pdf", year, company)
        #     with open('last_company_done.txt','w') as write_file:
        #         write_file.write(year + "-" + company + "\n")
        #     time.sleep(0.8)
        
        doubt_count = write_stats(year, "0", doubt_count, conclusions_found)

    

# Reinit variables for new recap after text reading
doubt_count = 0
doubt_list_new = {}
conclusions_found = []

#to comment
f = open('doubt_results_1.json', 'w')
f = open('found_results_1.json', 'w')


for year in years_to_search:

    # if doubt_list[str(year]:
    
    for result in doubt_list[year]:
        print(result)
        #if not (result["company"] == "Henkel" and year == "2020"):
        filepath = download_pdf(result["link"], year, result["company"])
        read_and_reorder_pdf(filepath, year, result["company"], result["query"], result["link"], doubt_list_new, found_list)
        

    for result in found_list[year]:
        print(result)
        download_pdf(result["link"], year, result["company"])
    
    doubt_count = write_stats(year, "1", doubt_count)


    

    #TODO O-I
    # lire fichier direct au download
    # lire fichier last_company pour reprendre au dernier
    # ecrire dans le fichier quand un fichier est telechargé pour reprendre au suivant
    # Verifier le bug pdf could not be found RWE 2018

    # regler pb append conclusion

