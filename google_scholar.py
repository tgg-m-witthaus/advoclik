from bs4 import BeautifulSoup
import requests
import re
import sys
from urllib2 import urlopen, Request
import csv

# Add % (first, last, school) to complete
BASE_SEARCH = "https://scholar.google.com/citations?mauthors=%s+%s+%s&hl=en&view_op=search_authors"
BASE_URL = 'https://scholar.google.com'


def get_search_result(first, last, school):
    link = BASE_SEARCH % (first, last, school)
    page = urlopen(link)
    soup = BeautifulSoup(page)

    # Find the link to the first result
    try:
        rv = BASE_URL + soup.findAll('h3', {"class":"gsc_1usr_name"})[0].findAll('a')[0]['href']
    except:
        rv = None
    # Try without school if no return
    if rv is None:
        try:
            link = BASE_SEARCH % (first, last, "")
            page = urlopen(link)
            soup = BeautifulSoup(page)
            rv = BASE_URL + soup.findAll('h3', {"class":"gsc_1usr_name"})[0].findAll('a')[0]['href']
        except:
            rv = None
    return rv

def get_h_and_cites(first, last, school):
    print first + " " + last + " " + school
    scholar_page = get_search_result(first, last, school)
    if scholar_page is None:
        return None, None
    page = urlopen(scholar_page)
    soup = BeautifulSoup(page)

    # get table
    table_cells = soup.findAll("td", {"class": "gsc_rsb_std"})

    # pull hindex and cites
    try:
        h = int(table_cells[2].text)
    except:
        h = None
    try:
        cites = int(table_cells[0].text)
    except:
        cites = None

    return h, cites

def add_h_and_cites_to_csv(csv_filepath):
    # Takes in a csv with names and schools, returns csv with extra columns for h and cites
    f = csv.writer(open("cites_and_h_scores_econ_profs.csv", "wb+"))
    f.writerow(['last', 'first', 'current', 'grad', 'undergrad', 'year', 'h_score', 'citations'])

    # open csv given
    with open(csv_filepath, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == "Last":
                continue
            h, cites = get_h_and_cites(row[1].strip().replace(' ', '+'), row[0].strip().replace(' ', '+'), row[2].strip().replace(' ', '+'))
            if h is None:
                h = "NA"
            if cites is None:
                cites = "NA"
            print h
            print cites
            f.writerow([row[0], row[1], row[2], row[3], row[4], row[5], h, cites])
