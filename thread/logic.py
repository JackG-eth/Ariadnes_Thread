import requests
import json
import re
import argparse
from companies_house.api import CompaniesHouseAPI
ch = CompaniesHouseAPI('yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt')
#_XsK-777wV5nXZwx2bgAaANU3kWTZ8p_1jWwarok
#yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt

# like to add checks to remove duplicate companies
def get_company_info(company_no):
    """
    Retrieves information about a company from Companies House.
    Args:
        company_no (str): Registered company number.
    Returns:
        Information Companies House holds on the company.
    """

    companyInfoDict = ch.get_company(company_no)
    if(bool(companyInfoDict) == False):
        raise Exception("Company Does Not Exist!")


    storedInfo = {}
    name = '';
    has_been_liquidated = 0
    has_insolvency_history = 0
    registered_office_is_in_dispute = 0
    for key, val in companyInfoDict.items():
        if(key == 'company_name'):
            name = val;
        if(key == 'has_been_liquidated'):
            if(val == True):
                has_been_liquidated = 1;
        if(key == 'has_insolvency_history'):
            if(val == True):
                has_insolvency_history = 1;
        if(key == 'registered_office_is_in_dispute'):
            if(val == True):
                registered_office_is_in_dispute = 1;

    storedInfo["Company Name: "] = name
    storedInfo["has_been_liquidated: "] = has_been_liquidated
    storedInfo["has_insolvency_history: "] = has_insolvency_history
    storedInfo["registered_office_is_in_dispute: "] = registered_office_is_in_dispute

    return storedInfo
    for key, val in storedInfo.items():
        print(key,val)


"""
Finds information about all companies associated through officers with the starting company.

Args:
    company_no (str):  The company number we want to search associated companies with.
    depth (int): The depth of search in the graph of companies.

Returns:
    A list of information about all associated companies up to the given depth.
"""
def getCompanyScore(company_no):
    storedInfo = get_company_info(company_no)
    investPercentage = 3;
    for key, val in storedInfo.items():
        if(key == 'has_been_liquidated'):
            if(val == 1):
                investPercentage-=1
        if(key == 'has_insolvency_history'):
            if(val == 1):
                investPercentage-=1
        if(key == 'registered_office_is_in_dispute'):
            if(val == 1):
                investPercentage-=1
    return (str((investPercentage/3)*100) + "%")


def get_Officers_Companies(OfficerID,company_no,depth):
    officerApp = ch.list_officers_appointments(OfficerID)
    comDictLenApp = len(officerApp['items'])
    name = '';
    company_id = '';
    #create dictionary to store these companies
    finalDict = {}
    for i in range(comDictLenApp):
        for key, val in officerApp['items'][i].items():
            if(key == 'appointed_to'):
                name = val['company_name']
                company_id =val['company_number']
                finalDict["Company Name: " + str(i)] = name
                finalDict["Company ID: " + str(i)] = company_id
                ## maybe comment out this line depending on levels to prevent exceeding call limit
                finalDict["investPercentage: " + str(i)] = getCompanyScore(company_id)
                if(company_no != company_id):
                    if(depth > 1):
                        finalDict["Company ID: " + str(i)] = get_associated_companies_info_by_company(company_id, depth-1)
                    else:
                        finalDict["Company ID: " + str(i)] = company_id
    return finalDict


# List containing a list of that companies list?
def get_associated_companies_info_by_company(company_no,depth):

    #company_info = get_company_info(company_no)
    companyDirectors = ch.list_company_officers(company_no)
    if(bool(companyDirectors) == False):
        raise Exception("Company Does Not Exist!")
    #print(companyDirectors
    ## somehow configure depth into this Add (later)
    comDictLen = len(companyDirectors['items'])
    storedInfo = {}
    for i in range(comDictLen):
        nameAndOfficerID = {}
        name = '';
        officerId = '';
        for key, val in companyDirectors['items'][i].items():
            if(key == 'name'):
                name = val;
            if(key == 'links'):
                string = val['officer']['appointments']
                m = re.search(r'.{10}(.*?)\/', string)
                officerId=m.group(1)

        nameAndOfficerID["Name: "] = name
        nameAndOfficerID["OfficerId: "] = officerId
        storedInfo["Director: " + str(i)] = nameAndOfficerID



    Final = {}
    # For each officer get their companies
    for key, val in storedInfo.items():
        officerName = val['Name: ']
        officerID = val['OfficerId: ']

        Final["Officer " + str(officerName)] = get_Officers_Companies(officerID,company_no,depth)

    return Final
