import fitz
from write_results import write_json

def check_pdf_txt(pdf, year, companyName):
    
    if pdf != None:
        file = fitz.open(pdf)
        textInPages = ''
        for page in file.pages(0,3):
    
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
    

def read_and_reorder_pdf(filepath, year, company, query, link):

    #Create dict table sorted by year
    # if year not in doubt_list_new.keys():
    #     doubt_list_new[year] = []

    pdf_text_is_relevant = check_pdf_txt(filepath, year, company)
    if not pdf_text_is_relevant:
        # doubt_list_new[year].append({'query': query, 'link': link})
        write_json({'query': query, 'link': link}, 'doubt_results_1.json', year)
    elif pdf_text_is_relevant == 403:
        write_json({'query': query, 'link': link, 'error': 'PDF could not be read'}, 'doubt_results_1.json', year)
        # doubt_list_new[year].append({'query': query, 'link': link, 'error': 'PDF could not be read'})
    else:
        # if year not in found_list.keys():
        #     found_list[year] = []
        # found_list[year].append({'company': company, 'query': query, 'link': link})
        write_json({'query': query, 'link': link}, 'found_results.json', year)
    