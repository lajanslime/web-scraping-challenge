# Define a function called `scrape` that will execute all of your scraping code from the `mission_to_mars.ipynb` notebook and return one Python dictionary containing all of the scraped data. 


# It will be a good idea to create multiple smaller functions that are called by the `scrape()` function. 
# Remember, each function should have one 'job' (eg. you might have a `mars_news()` function that scrapes the NASA mars news site and returns the content as a list/tuple/dictionary/json)
# HINT: the headers in the notebook can serve as a useful guide to where one 'job' ends and another begins. 

# Import Splinter, BeautifulSoup, and Pandas
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs



def init_browser():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def mars_news(): 

    #initialize Browser
    browser = init_browser()

    #Visit Nasa News Url 
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    
    # Convert the browser html to a soup object
    html = browser.html
    soup = bs(html, 'html.parser')

    # .find() the content title and save it as `news_title`
    article = soup.find_all('div', class_='content_title')
    news_title = article[1].text
    paragraph_text = soup.find('div', class_='article_teaser_body').text

    mars_news = {
        'news_title' : news_title,
        'paragraph_text' :  paragraph_text
    }

    return mars_news

def featured_image(): 

    #initialize Browser
    browser = init_browser()

    # Visit JPL space images Mars URL 
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)

    # Find and click the full image button
    browser.find_by_xpath('/html/body/div[1]/div/a/button').click()

    # Parse the resulting html with soup
    html = browser.html
    soup =  bs(html, 'html.parser')

    # find the relative image url
    relative_image_url = soup.find('img', class_="fancybox-image")["src"]
    
    # Use the base url to create an absolute url
    absolute_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{relative_image_url}'

    return absolute_image_url


def mars_facts(): 
    # Create a dataframe from the space-facts.com mars page
    mars = 'https://space-facts.com/mars/'
    mars_df = pd.read_html(mars)
    mars_df = mars_df[0]

    # Assign the columns
    mars_df.columns = ['Description', 'Value']

    # Set the index to the `Description`
    mars_df.set_index('Description', inplace=True)

    # Save html code
    # mars_df.to_html('table.html')
    
    return mars_df.to_html()

def hemispheres(): 

    #initialize Browser
    browser = init_browser()
    # visit the USGS astrogeology page for hemisphere data from Mars
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)

    # Parse the resulting html with soup
    html = browser.html
    soup =  bs(html, 'html.parser')

    # List of hemispheres
    h3 = soup.div.find_all('h3')
    hemispheres = [i.text.replace(' Enhanced', '') for i in h3]

    # Next, loop through those links, click the link, find the sample anchor, return the href

    list_of_hemispheres = []

    for i in hemispheres:
        # Click into hemisphere page
        browser.links.find_by_partial_text(i).click()

        # We have to find the elements on each loop to avoid a stale element exception
        html = browser.html
        soup =  bs(html, 'html.parser')
        sample = soup.find('div', { "class" : "downloads"})
        # Next, we find the Sample image anchor tag and extract the href
        sample_image = sample.a['href']
        
        # Get Hemisphere title
        hemisphere_title = i

        # Append hemisphere object to list
        hemisphere_obj = {
            "img_url" : sample_image,
            "title"   : hemisphere_title
        }
        list_of_hemispheres.append(hemisphere_obj)
        
        # Navigate backwards with browser.back()
        browser.back()
        
    # Quit the browser
    browser.quit()

    return list_of_hemispheres

def scrape(): 
    mars_dict = {
        "mars_news": mars_news(),
        "featured_image": featured_image(),
        "mars_facts": mars_facts(),
        "hemispheres": hemispheres()
    }

    return mars_dict


if __name__ == '__main__':
    print(scrape())

















    

    


