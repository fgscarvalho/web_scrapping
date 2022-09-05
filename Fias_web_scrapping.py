from datetime import date
from bs4 import BeautifulSoup as bs
from pyrsistent import b
import requests
import csv


def create_soup(urls):
    request = requests.get(urls)
    soup = bs(request.content)

    return soup

def find_urls(soup,string):
    url_original = 'https://sambo.sport'
    classe_ = soup.find(class_=string)
    finded_hrefs = classe_.find_all('a', href=True)

    urls =[]

    #update the url for continents federations
    for row in finded_hrefs:
        urls.append(url_original + row['href'])
    
    return urls

def find_name(soup):
    text = soup.find(class_="b_title p_main_title p_federation__main_title").text
    return text

def find_address(soup):
    if soup.find(class_="contacts_el contacts_address ico_before") is not None:
        text = soup.find(class_="contacts_el contacts_address ico_before").get_text(separator=" ").strip()
        if text == '':
            return None
        return text
    return None

def find_phone(soup):
    all_data = soup.find_all(class_="contacts_el contacts_lnk contacts_phone ico_before")
    for data in all_data:
        if '+' in data.text:
            return data.text
    return None
    
    

def find_email(soup):
    all_data = soup.find_all(class_="contacts_el contacts_lnk contacts_email ico_before")
    for data in all_data:
        if '@' in data.text:
            return data.text
    return None

def find_website(soup):
    all_data = soup.find_all(class_="contacts_el contacts_lnk contacts_site ico_before")

    for data in all_data:
        if 'http:' in data['href']:
            return data['href']
    return None


def main():
    #this list will store every dictionary of each club
    my_list = []
    today_ = date.today()
    date_list ='{}/{}/{}'.format(today_.day, today_.month, today_.year)
    fias_url = 'https://sambo.sport/en/federations'

    fias_soup = create_soup(fias_url)
    continents_urls = find_urls(fias_soup,"mobile_hide")
    
    for link in continents_urls[1:]:  
        continents_soup = create_soup(link)
        f_urls = find_urls(continents_soup,"p_federation__list")


        my_cont_dict = {}

        my_cont_dict['name'] = find_name(continents_soup)
        my_cont_dict['address'] = find_address(continents_soup)
        my_cont_dict['phone'] = find_phone(continents_soup)
        my_cont_dict['email'] = find_email(continents_soup)
        my_cont_dict['website'] = find_website(continents_soup)
            
        my_cont_dict['Country'] = None
        my_cont_dict['Recorded By'] = 'Felipe Carvalho'
        my_cont_dict['Recorded Date'] = date_list

        my_list.append(my_cont_dict)
        for row in f_urls:


            my_dict = {}
            f_soup = create_soup(row)
            country = f_soup.find(class_="p_federation__country").text
  
            my_dict['name'] = find_name(f_soup)
            my_dict['address'] = find_address(f_soup)
            my_dict['phone'] = find_phone(f_soup)
            my_dict['email'] = find_email(f_soup)
            my_dict['website'] = find_website(f_soup)
            
            my_dict['Country'] = country
            my_dict['Recorded By'] = 'Felipe Carvalho'
            my_dict['Recorded Date'] = date_list

            my_list.append(my_dict)
    
    return my_list

res = main()
