def set_accepted_names(company):

    companySmall = company.lower()
    companySmallNoSpace = companySmall.replace(" ", "")
    companySmallUnderscore = companySmall.replace(" ", "_")
    companySmallDash = companySmall.replace(" ", "-")
    companySmallNoDot = companySmall.replace(".", "")
    companySlice0 = companySmall.split(" ")[0]

    allowed_names_in_link = [
        companySmall,
        companySmallNoSpace,
        companySmallUnderscore,
        companySmallDash,
        companySmallNoDot,
        companySlice0
    ]
    if(len(company.split(" ")) > 1):    
        companySlice1 = companySmall.split(" ")[1]
        allowed_names_in_link.append(companySlice1)
    else:
        companySlice1 = ""
    
    return 