import requests
from vars_for_requests import headers
import os

def download_pdf(link, yearString, companyName):

    try:
        response = requests.get(link, headers=headers, timeout=30)
    except:
        print("GET REQUEST FAILED")
        with open('Exception_at_download.txt','w') as f:
            f.write(companyName)
            f.write(yearString)
            f.write(link)
    
    # print(response)
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