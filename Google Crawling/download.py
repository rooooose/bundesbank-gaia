import requests
from vars_for_requests import headers
import os
from write_results import write_json
import dropbox

def dropbox_upload(filepath, company):
    dbx = dropbox.Dropbox('sl.BeqfnpLQvybDihTNPcLLa8oiesfQW8_Z7G9cvUPMDDm4pOLUwBGwShRMMp1xr5hyQivPTAxKptkJBjLrzuqehckWMs4XtlU7aygay29r6ef_kIe02MPtxnrV99t5BhveqWrjpoJb3aM')
    
    with open(filepath, "rb") as f:
        # print("cc")
        # filename = filepath.rsplit("/", 1)[1]
        # print(filename)
        dbx.files_upload(f.read(), "/2023-05-19 (msci)/"+company+"/"+filepath, mode=dropbox.files.WriteMode("overwrite"))
    
    os.remove(filepath)

def download_pdf(link, yearString, companyName):

    try:
        response = requests.get(link, headers=headers, timeout=30)
        status_code = response.status_code
        print(status_code)
    except:
        status_code = None

    if status_code == 200:

        pdf = open(yearString + "_report.pdf", 'wb')
        pdf.write(response.content)
        pdf.close()
    
        filepath = yearString + "_report.pdf"

        dropbox_upload(filepath, companyName)
        return filepath
    else:
        print("GET REQUEST FAILED")
        write_json({'company': companyName, 'link': link}, 'exception_at_download.json', yearString)
        return None