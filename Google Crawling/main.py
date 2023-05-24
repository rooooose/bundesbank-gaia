import csv
import json
from crawling import scrape_google_and_order
from download import download_pdf
from text_reading import read_and_reorder_pdf
from write_results import write_stats
import pandas as pd
import re, os
import shutil
import dropbox

def find_where_to_start(file):

    last_comp_file = open(file,'r')
    last_comp_line = last_comp_file.read()
    last_comp_file.close()

    if not last_comp_line == "" and not last_comp_line == "\n":
        last_year = last_comp_line.split('-')[0]
        last_comp = last_comp_line.split('-')[1]
        last_comp_index = list(companies).index(last_comp)
        last_year_index = years_to_search.index(last_year)
    else:
        last_year_index = 0
        last_comp_index = -1
    
    return last_year_index, last_comp_index


years_to_search = ["2017", "2018", "2019", "2020", "2021", "2022"]
# doubt_count = 0

msci_list = pd.read_csv("Google Crawling/msci.csv")["Name"]
dax_list = pd.read_csv("Google Crawling/dax.csv")["COMPANIES"]
# print(dax_list)

not_allowed_terms_old = [
    ' inc',
    ' group',
    " class",
    " ltd",
    " plc",
    " ag",
    " sa",
    " corp",
    " entertainment",
    " holding",
    " holdings",
    " company",
    " reit",
    " pharmaceuticals",
    " pharmaceutical",
    " nv", 
    " industries",
    " communications",
    " corporation",
    " resources",
    " vacations",
    " solutions",
    " a",
    " stapled units",
    " n",
    " units",
    " unit",
    " investment",
    " b",
    " energia",
    " energias"
]

not_allowed_terms = [
    " class",
    " nv", 
    " a",
    " stapled units",
    " n",
    " units",
    " unit",
    " b",
    " i"
]

tolerated_terms = [
    ' inc',
    ' group',
    " ltd",
    " plc",
    " ag",
    " sa",
    " corp",
    " entertainment",
    " holding",
    " holdings",
    " company",
    " reit",
    " pharmaceuticals",
    " pharmaceutical",
    " industries",
    " communications",
    " corporation",
    " resources",
    " vacations",
    " solutions",
    " investment",
    " energia",
    " energias"
]


msci_list = msci_list.apply(str.lower)
for key, company in msci_list.items():
    for word in not_allowed_terms:
        found = re.search(word + "(\s|$)", company)
        if found:
            company = company.split(word, 1)[0]
            msci_list.iloc[key] = company
    
    for word in tolerated_terms:
        found = re.search(word + "(\s|$)", company)
        if found:
            company = company.split(word, 1)[0] + word
            msci_list.iloc[key] = company

companies = pd.concat([dax_list, msci_list])

dbx = dropbox.Dropbox('sl.Be8XAKhHDl66MAaIRYXpOw3AkTX9GS0tsOLdCX-lbblftqGNGiTZm0CDhFsoeXcaH1B8Oc1mYkpDSn4y2PiXuaoy0t3avveBs59x26OsN8RVLVtO2tz1_5b0mtC1waDdwXMReetB1EE:EUR')


last_year_index, last_comp_index = find_where_to_start('stopped_search_at.txt')

year_changed = False

# for year in years_to_search[last_year_index:]: 

    #when we change year, we want to start at the first comany (-1 because we want to start 0 and we do +1)
    # if year_changed:
    #     last_comp_index = -1
    # if last_comp_index+1 == len(companies):
    #     break
    # for company in companies[last_comp_index+1:]:
    #     print(company)
    #     scrape_google_and_order(company + " sustainability report " + year + " filetype:pdf", year, company)
    #     f = open('stopped_search_at.txt','w')
    #     f.write(year + "-" + company)
    #     time.sleep(0.8)
    
    # year_changed = True

    # write_stats(year, "0")



original_found = 'found_results_0.json'
new_found = 'found_results_1.json'
shutil.copyfile(original_found, new_found)

with open('doubt_results_0.json','r') as file:
    try:
        doubt_list = json.load(file)
    except:
        doubt_list = {}

with open('found_results_0.json','r') as file:
    try:
        found_list = json.load(file)
    except:
        found_list = {}

last_year_index, last_comp_index = find_where_to_start('stopped_download_at.txt')

year_changed = False

for year in years_to_search[last_year_index:]:

    if year_changed:
        last_comp_index = -1

    if last_comp_index+1 == len(companies):
        break

    for company in companies[last_comp_index+1:]:

        is_doubt = False

        if year in doubt_list.keys():
            for result in doubt_list[year]:
                if company in result.values():
                    print(result)
                    filepath = download_pdf(result["link"], year, result["company"], dbx)
                    read_and_reorder_pdf(filepath, year, result["company"], result["query"], result["link"], dbx)
                    is_doubt = True
                    if filepath != None:
                        os.remove(filepath)
                    break
        if year in found_list.keys() and not is_doubt:
            # print("look in found results")
            for result in found_list[year]:
                if company in result.values():
                    print(result)
                    filepath = download_pdf(result["link"], year, result["company"], dbx)
                    if filepath != None:
                        os.remove(filepath)
                    break

        f = open('stopped_download_at.txt','w')
        f.write(year + "-" + company)

    year_changed = True
    
    write_stats(year, "1")


# "query": "kanto denka kogyo ltd sustainability report 2017 filetype:pdf",
# "link": "https://www.kantodenka.co.jp/english/sustainability/pdf/sustainability_report_2021e.pdf"
# dans found