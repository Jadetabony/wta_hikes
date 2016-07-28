**Recap of previous day:**
- Over the weekend, I had faced the challenge of figuring out how to scrape trip reports from the WTA website.  My intent was to scrape the trip report links from the hike pages and then request and scrape those pages.  However, I was running into the issue that the urls and text were loaded to the hike page via an Ajax querry (Javascript).  This means that when the page is scraped using requests, it is not in the page HTML files. Sleep was lost over this.

**What I did Today:**
- After talking to Miles, we decided that there were two potential "correct routes" to take for this.  The first is to use the selenium package to make the webscraper act like an actual webpage and wait for the request to load the data into the html.  The second option was to find the actual request and scrape that.  

The second option ended up working beautifully.  Once we finally found the request (adding /@@related_tripreport_listing to the hike link) would bring up the most recent 5 trip reports, as well as links to following trip reports.

Code is stored in TripReportsScraper.ipynb.  I need to migrate this to a .py file.

I have now scraped >78,000 reports, which are stored in a mongodb test/trip_reports, also saved in data/trip_reports.json  and on AWS S3.


**Challenges:**
See Weekend challenge listed above.  I also transitioned from using find and findAll in BeautifulSoup to using 'select'.  I very much wish that the syntax between commands in BeautifulSoup were more consistent.

**Moving Forward:**
Will continue to use selects in BeautifulSoup.
Need to build pipeline to update my mongodb with new trip reports without scraping in reports that I already have.
