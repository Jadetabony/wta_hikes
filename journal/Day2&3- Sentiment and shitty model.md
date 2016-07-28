**Recap of previous day:**
- On Monday, I acquired all of my training data using the web scraping breakdown I describe in Day1.
- Tuesday was dedicated to learning more about sentiment analysis, however, the repo I was provided has broken links to a coursera course.  I've been watching this one, as it is the only one that I can find regarding NLP on coursera.
- Wednesday, I got my first sentiment analysis parser built, using the TextBlob polarity.  I then built a rating system by splitting the ratings by the 1/5ths.  Therefore, the lowest 20th percentile received a 1, the 20th-40th percentile received a 2 and so on.  This relies on a lot of assumptions.  First off, the accuracy of Textblob sentiment ratings.  Second, the ratings being split as such.  This is highly inaccurate as its incredibly rare that a hike is given a 1, 2, or 3. I need to compare the overall ratings by hike to their listed ratings on the WTA.

Wednesday, I also built my first recommender system with Dato.  For this first model, I built it using a factorization model with hike id, author id and textblob based rating.  It actually worked!

**What I did Today:**
- To do on Thursday:
  * Clean up my code for the recommender and sentiment analyzer.  This really needs to get done.  I think that I need to sit down for 10 minutes and outline my code flow.  
  * Build the pipeline from text processor to recommender
  * Evaluate my recommender models
  * Assuming more time, scrape my training data.

**I also really need to sit down and write out my to-do list for the rest of the time**


**Challenges:**
- Getting my "training" data.  I found a website with both trip reports and ratings (everytrail.com) and have been trying to scrape it.  Its not as consistent as other sites, making this incredibly challenging
- Getting my data into an item similarity recommender. I need to find an example of this.

**Moving Forward:**
- I need to really get organized and structured.  
