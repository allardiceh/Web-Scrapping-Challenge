
## import dependencies


from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd
import lxml
import os 


## make your function 


def scrape_info():

    ##### Part one: Get Current News 

    ## splinter browser 
    ##os.chmod("./chromedriver", 755)
    executable_path = {'executable_path': '/Users/heatherallardice/Desktop/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
  

    #Titles of each item on the landing page 
    content_title = soup.find('div', class_="content_title")
    output=content_title.find("a").text


    #paragraph of each item on the landing page
    #Titles of each item on the landing page 
    sub_text = soup.find_all( 'div', class_='rollover_description_inner')
    paragraph=sub_text[0].text

    #### Part 2: Featured Image

    # Url to be scraped 
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Click through pages to ge the one you want 
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')


    # make a new soup
    html=browser.html
    soup_2=BeautifulSoup(html, 'html.parser')

    #find the element. In this case it's the Featured Mars Image

    sub_img = soup_2.find( 'figure', class_='lede')


    name=sub_img.a['href']
    featured_image='https://www.jpl.nasa.gov'+ name
   

    ### Scraping the table 

    # Scraping the data from the mars facts web page
    url='https://space-facts.com/mars/'

    tables = pd.read_html(url)
    tables

    # format the table
    type(tables)
    df = tables[0]
    html_table = df.to_html()
  


    ### Scrape the hemishepre images
    ## Steps: 
    #1.Scrape the url
    #2.make the soup
    #3.create a dictonary
    #4.scape the soup and append the dictonary
    #5.put the dictonary into a list


    #url to be scrapped
    url_1='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #make the soup
    response = requests.get(url_1)
    soup_1= BeautifulSoup(response.text, 'html.parser')

    links = soup_1.find_all("a", class_="itemLink product-item")

    hemi = []
    links = soup_1.find_all("div", class_="item")

    for title in links:
        info= title.find("h3").text
        url=title.a["href"]
        image_link = "https://astrogeology.usgs.gov/" + url  
        browser.visit(image_link)#set up the link
        browser.click_link_by_partial_text('Sample')#look for partial phrase
        html=browser.html
        soup_3=BeautifulSoup(html, 'html.parser')#new soup
        downloads = soup_3.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemi.append({"title": info, "img_url": image_url})
        browser.visit(url_1)
    browser.visit(url_1)

    ### put all of the scrapes into  a dictonary 

    mars_dict = {
            
            "news_title": output,
            "news_paragraph": paragraph,
            "featured_image": featured_image,
            "table": html_table,
            "hemisphere_images": hemi
        }
    return mars_dict


