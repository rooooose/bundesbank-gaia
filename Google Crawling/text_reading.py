import fitz
from write_results import write_json

def check_pdf_txt(pdf, year, companyName, link):
    
    if pdf != None:
        try:
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

            companySmall = companyName.lower()
            companySlice0 = companyName.split(" ")[0]
            allowed_names = [
                companySmall,
                companySlice0
            ]
            if(len(companyName.split(" ")) > 1):    
                companySlice1 = companySmall.split(" ")[1]
                allowed_names.append(companySlice1)
            else:
                companySlice1 = ""

            if companyName == 'KplusS':
                companyName = 'K+S'
            elif 'oe' in companyName:
                companyName = companyName.replace('oe','ö')

            if any(word in str.lower(textInPages) for word in allowed_terms) and ("report" in str.lower(textInPages) or "information" in str.lower(textInPages)) and year in textInPages and any(companyName in str.lower(textInPages) for companyName in allowed_names):
                return True
            else:
                return False
        except:
            write_json({'company': companyName, 'link': link}, 'exception_at_download.json', year)
            return 403
    else:
        return 403
    

def read_and_reorder_pdf(filepath, year, company, query, link):

    pdf_text_is_relevant = check_pdf_txt(filepath, year, company, link)
    if not pdf_text_is_relevant:
        write_json({'query': query, 'link': link}, 'doubt_results_1.json', year)
    elif pdf_text_is_relevant == 403:
        write_json({'query': query, 'link': link, 'error': 'PDF could not be read'}, 'doubt_results_1.json', year)
    else:
        write_json({'query': query, 'link': link}, 'found_results_1.json', year)
    