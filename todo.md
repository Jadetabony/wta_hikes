## TODO

#### Scrapers
* rewrite scrapers
    * paralellism
    * use scrapy
    * write to storage 
        * buckets for soup
        * psql for databases
    * batching
    
* ETL step
* deploy scrapers on gcp
* automatical update trip reports

#### Testing
* scraper tests
* 

#### Recommender
* rewrite cosine similarity recommender to use numpy based function, rather than GL
* Add in 'to avoid' checklist

#### Reviews
* sentiment of review
* entity recognition

#### Web app
* redo recommender page
* deploy on engine app on gcp
* redirect domain
* security
* collect information about what is searched


## DONE

#### Scrapers
* Create schema for database
    * Tables:
        * hikes
        * trip reports
        * users
