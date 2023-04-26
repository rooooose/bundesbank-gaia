import csv
import json
from crawling import scrape_google_and_order
from download import download_pdf
from text_reading import read_and_reorder_pdf
from write_results import write_result_files


years_to_search = [2017, 2018, 2019, 2020, 2021, 2022]
doubt_count = 0
doubt_list = {}
found_list = {}
conclusions_found = []

for year in years_to_search:

    with open('Google Crawling/dax.csv') as csv_file:
        dax_reader = csv.reader(csv_file, delimiter='\n')

        for i, companyRow in enumerate(dax_reader):
            print(companyRow[0])
            scraping_result = scrape_google_and_order(companyRow[0] + " sustainability report " + str(year) + " filetype:pdf", str(year), companyRow[0], found_list, doubt_list)
            # doubt_count = scraping_result[1]
    # print(doubt_list)
    doubt_count = write_result_files(year, 0, found_list, doubt_list, conclusions_found, doubt_count)

# Reinit variables for new recap after text reading
doubt_count = 0
doubt_list_new = {}
conclusions_found = []

for year in doubt_list:
    
    for result in doubt_list[year]:
        print(result)
        filepath = download_pdf(result["link"], year, result["company"])
        read_and_reorder_pdf(filepath, year, result["company"], result["query"], result["link"], doubt_list_new, found_list)

    for result in found_list[year]:
        print(result)
        download_pdf(result["link"], year, result["company"])

    doubt_count = write_result_files(year, 1, found_list, doubt_list_new, conclusions_found, doubt_count)
    

# print(doubt_list)

#TODO loop through doubts list > download and check them all > new doubt list
# loop through found list > download all

# TEST
# companyRow = "E.ON"
# year = 2018
# scrape_google_and_order("E.ON sustainability report #2018# filetype:pdf", str(year), 0, companyRow)

#TODO Refactoring : 3 verschiedene Dateien : scraping, downloading, Text Suche
# 2 verschiedene Output Dateien : 1 vor dem download, 1 nach dem Text suche
# Guacamole ?