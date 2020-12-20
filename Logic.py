import re
from companies_house.api import CompaniesHouseAPI
ch = CompaniesHouseAPI('_XsK-777wV5nXZwx2bgAaANU3kWTZ8p_1jWwarok')

#_XsK-777wV5nXZwx2bgAaANU3kWTZ8p_1jWwarok
#yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt
"""
Retrieves information about a company from Companies House.
Args:
    company_no (str): Registered company number.
Returns:
    Information Companies House holds on the company.
"""
def get_company_info(company_no):
    companyInfoDict = ch.get_company(company_no)
    #check if the return dictionary is empty or not
    if(bool(companyInfoDict) == False):
        raise Exception("Company Does Not Exist!")


    #initialise new dictonary to store only what we want to know (Editable)
    storedInfo = {}
    """
    Decided for my risk % the most important fields were:
        has_been_liquidated:
        has_insolvency_history:
        registered_office_is_in_dispute:
    """
    name = '';
    has_been_liquidated = 0
    has_insolvency_history = 0
    registered_office_is_in_dispute = 0
    ## If it returns true value is set to 1
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

    # Store in dictionary object
    storedInfo["Company Name: "] = name
    storedInfo["has_been_liquidated: "] = has_been_liquidated
    storedInfo["has_insolvency_history: "] = has_insolvency_history
    storedInfo["registered_office_is_in_dispute: "] = registered_office_is_in_dispute

    return storedInfo

"""
Calculates the RISK % score by calling the get_company_info function and performing some simple arithmatic
    Definitely needs more data but is simple just a test showing how a certain field could be calculated
Args:
    company_no (str):  The company number we want to search associated companies with.

Returns:
    A given score for that particular company
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



"""
Finds all of the companies a particular officer is associated with (depends on depth assigned)
Args:
    company_no (str):  The company number we want to search associated companies with.
    depth (int): How far you want to delve into the database
Returns:
    A dictionary containing that officers associated information
"""
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
                ## Might be worth removing this if statement (just ensures companies are not duplicated (endless loop))
                if(company_id != company_no):
                    finalDict["Company Name: " + str(i)] = name
                    finalDict["Company ID: " + str(i)] = company_id
                    ## maybe comment out this line depending on levels to prevent exceeding call limit
                    finalDict["InvestmentRisk: " + str(i)] = getCompanyScore(company_id)
                    if(company_no != company_id):
                        if(depth > 1):
                            finalDict["Company ID: " + str(i)] = get_associated_companies_info_by_company(company_id, depth-1)
                        else:
                            finalDict["Company ID: " + str(i)] = company_id
    return finalDict


"""
Finds all officers associated with a given company
    # TODO: If i had more time i'd like to add a way to calculate sub risk scores when determining the overall investment RISK
Args:
    company_no (str):  The company number we want to search associated companies with.
    depth (int): How far you want to delve into the database
Returns:
    A dictionary containing officers and their assoicated companeies and risk %
"""
def get_associated_companies_info_by_company(company_no,depth):

    companyDirectors = ch.list_company_officers(company_no)
    if(bool(companyDirectors) == False):
        raise Exception("Company Does Not Exist!")
    comDictLen = len(companyDirectors['items'])
    storedInfo = {}

    ## loop through all officers returned store their (name, OfficerID in sub Dictionary)
    for i in range(comDictLen):
        nameAndOfficerID = {}
        name = '';
        officerId = '';
        # formatting required to exract their ID
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


    """
    Simple recursive call here depending on depth
    Essentially find all of the companies that officer is assocated with and call the entire logic again until the depth is equal to 1
    """
    for key, val in storedInfo.items():
        officerName = val['Name: ']
        officerID = val['OfficerId: ']

        Final["Officer " + str(officerName)] = get_Officers_Companies(officerID,company_no,depth)

    return Final
