import json
from crawling import scrape_google_and_order
from download import download_pdf
from text_reading import read_and_reorder_pdf
from write_results import write_stats
import os, time
import shutil
import make_company_list
from make_company_list import msci_list
# from config import dbx

def find_where_to_start(file):
    """reads where the code last stopped in txt files (at which company and which year)

    Args:
        file (string): filepath of the txt to read

    Returns:
        int, int : indexes of year and company where it stopped
        bool : if the search or download has started
    """

    last_comp_file = open(file,'r')
    last_comp_line = last_comp_file.read()
    last_comp_file.close()

    if not last_comp_line == "" and not last_comp_line == "\n":
        last_year = last_comp_line.split('--')[0]
        last_comp = last_comp_line.split('--')[1]
        last_comp_index = list(companies).index(last_comp)
        last_year_index = years_to_search.index(last_year)
        started = True
    else:
        started = False
        last_year_index = 0
        last_comp_index = -1
    
    return last_year_index, last_comp_index, started


def find_links(last_comp_index, last_year_index):
    """loops through years and companies starting at specific index and scrapes google results for given query - then writes where it stopped

    Args:
        last_comp_index (int): index of company where it stopped
        last_year_index (int): index of year where it stopped
    """
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
            f.write(year + "--" + company)
            time.sleep(0.8)
        
        year_changed = True
        write_stats(year, "0")


def copy_found_file():
    """copies the list of found companies before download to new file 
    """
    original_found = 'found_results_0.json'
    new_found = 'found_results_1.json'
    shutil.copyfile(original_found, new_found)

def init_result_lists():
    """reads list result files and convert it in json tables

    Returns:
        array of dicts : lists of links
    """
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
    
    return doubt_list, found_list


def download_from_doubt_links(year, result, is_doubt):
    """downloading pdf from given doubtful link and reading it

    Args:
        year (srting)
        result (dict): element of doubt_list
        is_doubt (bool): if the link searched for is in the doubt_list or not

    Returns:
        bool: if the link searched for is in the doubt_list or not
    """
    
    print(result)
    filepath = download_pdf(result["link"], year, result["company"], "doubt")
    read_and_reorder_pdf(filepath, year, result["company"], result["query"], result["link"])
    is_doubt = True
    # if filepath != None:
    #     os.remove(filepath)
    
    return is_doubt

def download_from_found_links(year, result):
    """downloading pdf from given found link

    Args:
        year (string): _description_
        result (dict): element of found_list
    """
    print(result)
    filepath = download_pdf(result["link"], year, result["company"], "found")
    # if filepath != None:
    #     os.remove(filepath)
                

def download_read_pdfs(last_comp_index, last_year_index, doubt_list, found_list):
    """loops through years and companies starting at specific index and downloads report for given link
     Different behaviour if link searched for is in doubt_list or found_list - then writes where it stopped

    Args:
        last_comp_index (int): index of company where it stopped
        last_year_index (int): index of year where it stopped
        doubt_list (array of dicts): doubtful list of links
        found_list (array of dicts): right links
    """
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
                        is_doubt = download_from_doubt_links(year, result, is_doubt)
                        break

            if year in found_list.keys() and not is_doubt:
                for result in found_list[year]:
                    if company in result.values():
                        download_from_found_links(year, result)
                        break

            f = open('stopped_download_at.txt','w')
            f.write(year + "--" + company)

        year_changed = True
        write_stats(year, "1")


years_to_search = ["2017", "2018", "2019", "2020", "2021", "2022"]
companies = make_company_list.make_clean_list(msci_list)
last_year_index_search, last_comp_index_search, seach_started = find_where_to_start('stopped_search_at.txt')
last_year_index_dl, last_comp_index_dl, download_started = find_where_to_start('stopped_download_at.txt')
if not download_started:
    find_links(last_comp_index_search, last_year_index_search)
    copy_found_file()
doubt_list, found_list = init_result_lists()
download_read_pdfs(last_comp_index_dl, last_year_index_dl, doubt_list, found_list)




