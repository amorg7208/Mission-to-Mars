# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### JPL Space Images Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

#browser.quit()

# # Mission to Mars Challenge: D1 Scrape High-Resolution Mars' Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# Scrape page into Soup
html = browser.html
soup = soup(html, "html.parser")

# 3. Write code to retrieve the image urls and titles for each hemisphere.
#look for all the links then
moon_links = browser.find_by_css("a.product-item img")
#loop through each link in the length of moon_links(hypothetically this could update to be more than four)
for i in range (len(moon_links)):
    #create a dictionary to hold links and titles
    moon_dictionary = {}
    #find links, click links, save links to dictionary
    browser.find_by_css("a.product-item img")[i].click()
    full_image = browser.find_by_text("Sample").first
    img_url = full_image["href"]
    moon_dictionary["img_url"] = img_url
    #find title, click title, save title to dictionary
    moon_title = browser.find_by_css("h2.title").text
    moon_dictionary["moon_title"] = moon_title
    hemisphere_image_urls.append(moon_dictionary)
    #go back to main url and repeate loop
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()