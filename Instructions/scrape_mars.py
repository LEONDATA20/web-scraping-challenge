from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_url (url):
    browser =  init_browser()
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup =  bs(html,"html.parser")
    browser.quit()
    return soup


def scrape():
    # create data dict that we can insert into mongo
    mars_data = {}

    # NASA Mars News
    url_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    news_soup = scrape_url(url_news)
    title = news_soup.find('div',class_='list_text').find('a').text
    content = news_soup.find('div',class_='article_teaser_body').text

    mars_data['news_title'] = title
    mars_data['news_p'] = content



    # Featured Image
    url_img='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    img_soup = scrape_url(url_img)
    img_url = img_soup.find('div',class_='img').find('img')['src']
    featured_image_url = f'https://www.jpl.nasa.gov{img_url}'

    mars_data['featured_image_url'] = featured_image_url


    # Mars Weather
    url_weather='https://twitter.com/marswxreport?lang=en'
    weather_soup = scrape_url(url_weather)
    mars_weather = weather_soup.find('div',lang='en').find('span').text

    mars_data['mars_weather'] = mars_weather


    # Mars Facts
    url_table='https://space-facts.com/mars/'
    table_soup = scrape_url(url_table)
    mars_table = str(table_soup.find('tbody'))
    
    mars_data['mars_facts'] = mars_table

    # tables = pd.read_html(url_table)
    # df = tables[0]
    # df.columns=['parameter','value']
    # html_table = df.to_html()
    # facts_table = html_table.replace('\n', ' ')
    #df.to_html('table.html')
    #mars_data['table'] = facts_table
    

    # Mars Hemispheres
    url_mars='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_soup = scrape_url(url_mars)
    items = mars_soup.find_all('div', class_='description')

    hemisphere_image_urls=[]
    for item in items:
        title=item.h3.text
        url=item.find('a')['href']
        z={'title':title,'img_url':f'https://astrogeology.usgs.gov{url}'}
        hemisphere_image_urls.append(z)
    
    md=[]
    for i_url in hemisphere_image_urls:
        image_soup = scrape_url(i_url['img_url'])
        x= image_soup.find('ul').find('a')['href']
        y={'title':i_url['title'],'img_url':x}
        md.append(y)


    mars_data['title_url'] = md
    

    return mars_data










    




















##

#     url_news='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
#     ##browser.visit(url_news)
#     ##time.sleep(1)
#     ##html = browser.html
#     ##soup = bs(html, "html.parser")

#     # Scrape page into Soup
#     html = browser.html
#     soup = bs(html, "html.parser")

#     # Get the average temps
#     avg_temps = soup.find('div', id='weather')

#     # Get the min avg temp
#     min_temp = avg_temps.find_all('strong')[0].text

#     # Get the max avg temp
#     max_temp = avg_temps.find_all('strong')[1].text

#     # BONUS: Find the src for the sloth image
#     relative_image_path = soup.find_all('img')[2]["src"]
#     sloth_img = url + relative_image_path

#     # Store data in a dictionary
#     costa_data = {
#         "sloth_img": sloth_img,
#         "min_temp": min_temp,
#         "max_temp": max_temp
#     }

#     # Close the browser after scraping
#     browser.quit()

#     # Return results
#     return costa_data
# ##