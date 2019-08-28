# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 
    executable_path = {"executable_path": "./chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Dictionary for importing to Mnongo
mars_info = {}

# NASA Mars News
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        

        # Splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')


        # Retrieve news_title & news_p
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary from Mars news
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# Featured image
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Splinter module
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)# Visit Mars Space Images through splinter module

        # HTML Object 
        html_image = browser.html

        # Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website  
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scraped route
        featured_image_url = main_url + featured_image_url

        # Display link
        featured_image_url 

        # Dictionary from featured image
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    finally:

        browser.quit()

        

# Mars Weather 
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object 
        html_weather = browser.html

        # Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Grab tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Retrieve news title  
        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

        # Dictionary from Weather tweet
        mars_info['weather_tweet'] = weather_tweet
        
        return mars_info
    finally:

        browser.quit()


# Mars Facts
def scrape_mars_facts():

    # Web site
    facts_url = 'http://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)

    # Mars facts DataFrame 
    mars_df = mars_facts[1]

    # Assign columns
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)

    # Save html code 
    data = mars_df.to_html()

    # Dictionary from Mars facts
    mars_info['mars_facts'] = data
    return mars_info


# Mars Hemispheres
def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retrieve information
        items = soup.find_all('div', class_='item')

        # Empty list for hemisphere urls 
        hiu = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link 
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link containing full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object
            partial_img_html = browser.html
            
            # Beautiful Soup  
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retrieved information into a list of dictionaries 
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu

        
        # Dictionary 

        return mars_info
    finally:

        browser.quit()