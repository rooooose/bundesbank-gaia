import requests
from vars_for_requests import headers
import os

def download_pdf(link, yearString, companyName):

    try:
        response = requests.get(link, headers=headers, timeout=30)
        status_code = response.status_code
    except:
        status_code = None
        print("GET REQUEST FAILED")
        with open('exception_at_download.txt','a') as f:
            f.write(companyName + '\n')
            f.write(yearString + '\n')
            f.write(link + '\n\n')
    
    # print(response)
    if status_code == 200 and ".pdf" in link:

        if not os.path.exists("resultPDFs/"+companyName):
            os.makedirs("resultPDFs/"+companyName)

        pdf = open(os.path.join("resultPDFs/"+companyName, yearString+"_report.pdf"), 'wb')
        pdf.write(response.content)
        pdf.close()
    
        filepath = "resultPDFs/" + companyName + "/" + yearString + "_report.pdf"
        return filepath
    else:
        return None