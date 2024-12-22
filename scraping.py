import pandas as pd
from bs4 import BeautifulSoup   
import requests
import re

def get_iata_code(city, csv_file=r'static\cleaned_airports-codepublic.csv'):
    df = pd.read_csv(csv_file, sep=';', header=0)

    # is input already a IATA code?
    city_airports = df[df['Airport Code'].str.match(city, case=False)]
    if len(city)==3 and not city_airports.empty:
        print(city_airports.to_dict())
        response = pd.DataFrame({
            'City': city_airports['Airport Name'].to_list(),
            'Code': city_airports['Airport Code'].to_list()
            })
    else:
        city_airports = df[(df['City Name'].str.contains(city, case=False, na=False)) | (df['Airport Name'].str.contains(city, case=False, na=False)) | (df['Airport Code'].str.contains(city, case=False, na=False))]

    iata_codes = city_airports['Airport Code'].to_list()
    city_names = city_airports['Airport Name'].to_list()

    df = pd.DataFrame({'City': city_names, 'Code': iata_codes})
    result_dict = df.set_index('City')['Code'].to_dict()
    return result_dict

def get_airport_name_by_iata(iata, csv_file=r'static\cleaned_airports-codepublic.csv'):
    df = pd.read_csv(csv_file, sep=';', header=0)
    airport = df[df['Airport Code'].str.match(iata, case=False)]
    
    return f'{airport['City Name'].to_string(index=False)} ({airport['Airport Name'].to_string(index=False)})'

def get_info(code, category, csv_file=r'static\cleaned_airports-codepublic.csv'):
    df = pd.read_csv(csv_file, sep=';', header=0)
    airport = df[df['Airport Code'].str.contains(code, case=False, na=False)]
    info = airport[category].values[0]
    return info

#przykład użycia

# city_name = "KRK"
# iata_codes = get_iata_code(city_name)

# for key, value in iata_codes.items():
#     city = get_info(value,'City Name')
#     print(city)
#     print(f'{city}, {key}: {value}')

def is_route_possible(base, to): #zwraca boola czy dane połączenie istnieje
    url = f'https://www.flightconnections.com/flights-from-{base}-to-{to}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    text = soup.select_one('body > div.site-content > div.route-page > div.route-page-segment.route-page-info > div:nth-child(3) > div.route-page-info-cell > div.route-page-info-text > span')
    try:
        text = text.get_text()
    except:
        return 'No Direct'
    else:
        if text == '0 minutes':
            return False
        return True

def list_routes_from(base, code): #zwraca listę połączeń z jakiegoś miasta
    url = f'https://www.flightconnections.com/flights-from-{base}-{code}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    connections = soup.select('#popular-destinations [data-a]')

    routes_city = []
    for element in connections:
        data_a_value = element.get('data-a')
        if data_a_value:
            routes_city.append(data_a_value)    
    return routes_city

def is_reservation_possible(base, to): #sprawdza czy rezerwacja jest możliwa, jeżeli możliwa jest z przesiadką to zwraca listę miast "przesiadkowych" 
    if is_route_possible(base, to):
        return True
    else:
        url = f'https://www.flightconnections.com/flights-from-{base}-to-{to}'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        cities = soup.select('.via-destination')
        codes = soup.select('.flight-path-via')
        routes_city = []
        routes_code = []

        for element in cities:
            city = element.get_text()
            if city:
                routes_city.append(city) 
        
        for element in codes:
            code = element.get('data-connections')
            if code:
                routes_code.append(code) 

        if len(routes_city) == 0:
            return False

        df = pd.DataFrame({'City': routes_city, 'Code': routes_code})
        result_dict = df.set_index('City')['Code'].to_dict()
        
        return result_dict
    
def airlines_details(base, to):
    airlines_list = []
    if is_route_possible(base, to) == True:
        url = f'https://www.flightconnections.com/flights-from-{base}-to-{to}'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        airline_elements = soup.find_all('a', class_='airline-schedule-button btn')
        airlines = [element.get_text(strip=True) for element in airline_elements]
        for airline in airlines:
            airlines_list.append(airline)
    return airlines_list

def airline_code(airline):
    match = re.search(r'\((.*?)\)', airline)
    if match:
        return match.group(1)
    return None


#print(airlines_details('krk', 'bcn'))
#print(is_reservation_possible('krk', 'ktw'))
#list_routes_from('krakow', 'krk')
#print(is_route_possible('krk', 'lax'))


