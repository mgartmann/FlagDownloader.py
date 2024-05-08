import requests
import urllib.request
from pathlib import Path

FLAG_TARGET_LOCATION = Path(__file__).parent / "flags"

def download_flag(flag_url, country_code):
    urllib.request.urlretrieve(flag_url, FLAG_TARGET_LOCATION / "{}.svg".format(country_code))
    
def get_country_data(country):
    url = "https://restcountries.com/v3.1/name/{}?fields=name,flags,cca2".format(country)
    response = requests.get(url)
    
    if(not response.ok):
        raise Exception("Country code could not be retrieved. Code: {}"
                        .format(response.status_code))
    
    country_data = response.json()
    
    if len(country_data) > 1:
        index = choose_country(country_data, country)
    else:
        index = 0
    
    return country_data[index]

def choose_country(country_list, country):
    print("Multiple countries were found for your input {}:".format(country))
    for i in range(0,len(country_list)-1):
        print(str(i) + ": " + country_list[i]["name"]["common"])
        
    while 1:
        index = int(input("Enter your desired country by number: "))
        if index > 0 and index < len(country_list)-1:
            return index
        else:
            print("Number not possible. Try again.")

FLAG_TARGET_LOCATION.mkdir(exist_ok=True)
countries = input('Enter your desired countires comma separated: ')
countries_list = countries.split(",")

for country_name in countries_list:
    country = get_country_data(country_name)
    print("Start download of {} flag...".format(country["cca2"]))
    download_flag(country["flags"]["svg"], country["cca2"])
    print("Done.")

print("All flags have been downloaded and saved to {}".format(FLAG_TARGET_LOCATION))