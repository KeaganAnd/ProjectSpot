import requests

def getPovertyData():
    '''https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEPOVALL_PT&for=state:01&YEAR=2023
    
    https://www.census.gov/data/developers/data-sets/Poverty-Statistics.html

    Refrence for variable names:
    https://api.census.gov/data/timeseries/poverty/saipe/variables.html
    '''

    stateID = "01"

    request = requests.get(f"https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEPOVALL_PT&for=state:{stateID}&YEAR=2023")
    print(request.json())

getPovertyData()