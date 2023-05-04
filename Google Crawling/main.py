import csv
import json
from crawling import scrape_google_and_order
from download import download_pdf
from text_reading import read_and_reorder_pdf
from write_results import write_result_files
import pandas as pd


years_to_search = [2017, 2018, 2019, 2020, 2021, 2022]
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
    " ag"
]


for year in years_to_search: 

    with open('Google Crawling/dax.csv') as csv_file:
        dax_reader = csv.reader(csv_file, delimiter='\n')

        for i, companyRow in enumerate(dax_reader):
            print(companyRow[0])
            scrape_google_and_order(companyRow[0] + " sustainability report " + str(year) + " filetype:pdf", str(year), companyRow[0], found_list, doubt_list)

        for company in msci_list:
            company = str.lower(company)
            for word in not_allowed_terms:
                company = company.split(word, 1)[0]
            print(company)
            scrape_google_and_order(company + " sustainability report " + str(year) + " filetype:pdf", str(year), company, found_list, doubt_list)

    doubt_count = write_result_files(year, 0, found_list, doubt_list, conclusions_found, doubt_count)

# Reinit variables for new recap after text reading
doubt_count = 0
doubt_list_new = {}
conclusions_found = []

for year in doubt_list:
    
    for result in doubt_list[year]:
        print(result)
        if not (result["company"] == "Henkel" and year == "2020"):
            filepath = download_pdf(result["link"], year, result["company"])
            read_and_reorder_pdf(filepath, year, result["company"], result["query"], result["link"], doubt_list_new, found_list)

    for result in found_list[year]:
        print(result)
        download_pdf(result["link"], year, result["company"])

    print(doubt_list_new)

    doubt_count = write_result_files(year, 1, found_list, doubt_list_new, conclusions_found, doubt_count)
    
