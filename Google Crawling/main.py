import json
from crawling import scrape_google_and_order
from download import download_pdf
from text_reading import read_and_reorder_pdf
from write_results import write_stats
import os, time
import shutil
import dropbox
from make_company_list import make_clean_list

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

companies = make_clean_list()

dbx = dropbox.Dropbox('sl.BfETvybupeFZL7XDB3riszW1D7fXDg1Sa4N6W8JYkLEWENJp7rWzSNtnQhAxEWZrU2jUPpKiGP5Z_XRtsV0fbxGHIsGJ68TVu-EA7qNs9J0CTHgq1e7q-gxkaMDHrz_FGTOdwZPZ-Pc:EUR')

# PART 1 : FIND LINKS
last_year_index, last_comp_index = find_where_to_start('stopped_search_at.txt')
year_changed = False

for year in years_to_search[last_year_index:]: 

    # when we change year, we want to start at the first comany (-1 because we want to start 0 and we do +1)
    if year_changed:
        last_comp_index = -1
    if last_comp_index+1 == len(companies):
        break
    for company in companies[last_comp_index+1:]:
        print(company)
        scrape_google_and_order(company + " sustainability report " + year + " filetype:pdf", year, company)
        f = open('stopped_search_at.txt','w')
        f.write(year + "-" + company)
        time.sleep(0.8)
    
    year_changed = True

    write_stats(year, "0")


#TO COMMENT WHEN DOWNLOAD STARTED
original_found = 'found_results_0.json'
new_found = 'found_results_1.json'
shutil.copyfile(original_found, new_found)

# PART 2 : DOWNLOAD AND READ PDFS
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
                    filepath = download_pdf(result["link"], year, result["company"], dbx, "doubt")
                    read_and_reorder_pdf(filepath, year, result["company"], result["query"], result["link"], dbx)
                    is_doubt = True
                    # if filepath != None:
                    #     os.remove(filepath)
                    break
        if year in found_list.keys() and not is_doubt:
   
            for result in found_list[year]:
                if company in result.values():
                    print(result)
                    filepath = download_pdf(result["link"], year, result["company"], dbx, "found")
                    # if filepath != None:
                    #     os.remove(filepath)
                    break

        f = open('stopped_download_at.txt','w')
        f.write(year + "-" + company)

    year_changed = True
    
    write_stats(year, "1")

