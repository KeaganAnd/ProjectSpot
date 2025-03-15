'''
IGNORE THIS ITS NOT IMPLEMENTED
Spot Finder!
3/14/2025

Project Spot 2025

Use this to add api endpoints to the json. Just makes it easier and doesn't risk the json formatting getting messed up.
'''

import json

countries = []

if __name__ == "__main__":
    url = ""

    while len(url) <= 5:
        url = input("Enter Url: ")
        if len(url) <= 5:
            print("Invalid URL")

    country = ""

    while country != 'q':
        country = input("Enter a supported country (Abbreviation only) or 'q' to finish: ")


    category = input("Enter Category i.e weather: ")

    
