# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = []
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data
def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p
def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    return img_url
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")
def hemispheres(browser):
    # 1. Use browser to visit the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url+'index.html')
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    #look for all the links then
    #moon_links = browser.find_by_css("a.product-item img")
    #loop through each link in the length of moon_links(hypothetically this could update to be more than four)
    for i in range (4):
        #create a dictionary to hold links and titles
        #moon_dictionary = {}
        #find links, click links, save links to dictionary
        browser.find_by_css("a.product-item img")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        hemi_data['img_url'] = url+ hemi_data['img_url']
        #full_image = browser.find_by_text("Sample").first
        #img_url = full_image["href"]
        #moon_dictionary["img_url"] = img_url
        #find title, click title, save title to dictionary
        #moon_title = browser.find_by_css("h2.title").text
        #moon_dictionary["moon_title"] = moon_title
        hemisphere_image_urls.append(hemi_data)
        #go back to main url and repeat loop
        browser.back()
    return hemisphere_image_urls
def scrape_hemisphere(html_text):
    hemi_soup=soup(html_text, "html.parser")
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        Sample_elem = hemi_soup.find("a", text="Sample").get("hrer")
    except AttributeError:
        title_elem=None
        Sample_elem=None
    hemispheres ={
        "title": title_elem,
        "img_url": Sample_elem
    }
    return hemispheres
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
