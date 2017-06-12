
## About - Log Analysis Project
This project is all about building an internal reporting tool about the newspaper that will use information from the database to discover what kind of articles the site's readers like. The already built database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. 

## How to Setup and Run the project
1. Install Vagrant Virtual Machine.
2. Vagrant VM has PostgreSQL installed and configured.
3. clone or download the project files in loganalysis folder under vagrant as /vagrant/loganalysis
4. Navigate to /vagrant/loganalysis which will have files as
    
    a. newsdata.sql  - Code for setting up Database Schema

    b. loganalysis.py - Various functions to connect to database and also to manipulate database. This file will have the real python code to fetch data as well as for report preparation.

    c. created.sql - SQL queries for creating news Database, connecting to database and also creating views.

5.  Start the Vagrant VM by writing commands as "vagrant up" and "vagrant ssh"
6.  Navigate to loganalysis folder under vagrant directory and use following command to load the data to local database:

               $ psql -f creatDB.sql

7. When all the functions in the loganalysis.py file are complete and ready to run. Run following command to implement the report and to see the output:

                $ python loganalysis.py

    If this command shows result which includes all the data for the report as follows:
   
         a. Three Most Popular Three Articles Of All Time Are:----
         b. Most Popular Article Authors Of All Time Are:---- 
         c. Days On Which More Than 1% Of Requests Lead To Errors:----
    
    It means code is good, Otherwise instructions will be given along with the error.

## Important points for coding SQL files.
1. Database Views have been created in createDB.sql if required but views can also be created by the user separately. Following is the process and View definition which user has to follow if created.sql file is not used:

       * $ psql
       * => CREATE DATABASE news;
       * => \c news
       * => \i newsdata.sql
      
      Then create following views:-
       * => CREATE VIEW LOG_VIEW 
                AS SELECT PATH, COUNT(PATH) AS VIEW_COUNTS FROM LOG 
                GROUP BY PATH 
	        ORDER BY VIEW_COUNTS DESC;
       * => CREATE VIEW AUTHOR_VIEW AS 
    	        SELECT ARTICLES.AUTHOR AS ARTICLE_AUTHOR, LOG_VIEW.VIEW_COUNTS AS ARTICLE_COUNTS
        	FROM ARTICLES, LOG_VIEW 
	        WHERE LOG_VIEW.PATH LIKE '%'||ARTICLES.SLUG; 
       * => CREATE VIEW ERRORS_PER_DAY AS
	        SELECT DATE(TIME) AS ERROR_DAY, COUNT(*) AS ERROR_COUNTS 
        	FROM LOG WHERE STATUS LIKE '4%' OR STATUS LIKE '5%' 
	        GROUP BY ERROR_DAY 
        	ORDER BY ERROR_COUNTS DESC;
       * => CREATE VIEW REQUESTS_PER_DAY AS 
	        SELECT DATE(TIME) AS REQUEST_DAY, COUNT(*) AS REQUEST_COUNTS 
        	FROM LOG
	        GROUP BY REQUEST_DAY 
        	ORDER BY REQUEST_COUNTS DESC;

## Program Design

Program consists of five functions. 

    1. execute_query() - Connects to news database and executes query which is received as string argument and returns the results.

    2. formatted_output() - Prints the received result in a formatted way to the console.

    3. get_popular_articles() - query for fetching most popular articles of all time.

    4. get_popular_article_authors() - query for fetching most popular articles author of all time.

    5. get_days_of_errors() - query for fetching days when more than 1% of requests lead to errors.

In the end of the program all the functions are called.


## Skills involved
1. Python
2. Python-DB-API
3. PostgreSQL database
