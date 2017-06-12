#
# !/usr/bin/env python
# Implementation of log analysis
#

import psycopg2


def execute_query(query):
    """Connects to the news database.
       executes an sql query and returns the result.

       Args:
           query: SQL query string to execute.
       Returns:
           results of the SQL query.
    """
    try:
        connection = psycopg2.connect(database="news")
        cursor = connection.cursor()
    except:
        print "Error connecting to database news!!!"

    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results


def formatted_output(query, append, header, num_results, if_str):
    """Function to print formatted output. Prints the result
        of SQL query to the console.

       Args:
           query: SQL query to be executed
           append: Suffix to be printed with each row.
           header: Heading for printed data.
           num_results: the number of results to show.
           if_str: If the second column has to be converted to string
    """
    results = execute_query(query)
    print " "
    print header
    print " "
    if results:
        if if_str:
            if num_results == -1:
                for j in results:
                    print '"' + j[0] + '" - ' + str(j[1]) + " " + append
            else:
                for j in results[:num_results]:
                    print '"' + j[0] + '" - ' + str(j[1]) + " " + append
        else:
            if num_results == -1:
                for j in results:
                    print '"' + j[0] + '" - ' + j[1] + " " + append
            else:
                for j in results[:num_results]:
                    print '"' + j[0] + '" - ' + j[1] + " " + append
    else:
        print "Sorry! There was no data in the table."


def get_popular_articles():
    """Returns most popular three articles of all time"""

    query = """ SELECT ARTICLES.TITLE, LOG_VIEW.VIEW_COUNTS
                FROM ARTICLES, LOG_VIEW
                WHERE LOG_VIEW.PATH LIKE '%'||ARTICLES.SLUG
                ORDER BY LOG_VIEW.VIEW_COUNTS DESC;
            """
    header = "Three Most Popular Articles Of All Time Are:---- "
    formatted_output(query, " views", header, 3, True)


def get_popular_article_authors():
    """Returns most popular article authors of all time"""

    query = """ SELECT AUTHORS.NAME, SUM(AUTHOR_VIEW.ARTICLE_COUNTS) AS AUTHOR_VIEWS
                FROM AUTHORS, AUTHOR_VIEW
                WHERE AUTHOR_VIEW.ARTICLE_AUTHOR = AUTHORS.ID
                GROUP BY AUTHORS.ID
                ORDER BY AUTHOR_VIEWS DESC;
            """
    header = "Most Popular Article Authors Of All Time Are:---- "
    formatted_output(query, " views", header, -1, True)


def get_days_of_errors():
    """Returns days when more than 1% of requests lead to errors"""

    query = """ SELECT TRIM(TO_CHAR(ERROR_DAY, 'MONTH'))
                        || ' '
                        || TO_CHAR(ERROR_DAY, 'DD, YYYY') AS DAY,
                        ROUND(((E.ERROR_COUNTS * 100.00)/R.REQUEST_COUNTS), 2)
                        || '%' AS PERC
                FROM ERRORS_PER_DAY AS E, REQUESTS_PER_DAY AS R
                WHERE E.ERROR_DAY = R.REQUEST_DAY
                AND ((E.ERROR_COUNTS * 100.00)/R.REQUEST_COUNTS) > 1;
            """
    header = "Days On Which More Than 1% Of Requests Lead To Errors:---- "
    formatted_output(query, " errors", header, -1, False)


if __name__ == '__main__':
    print ""
    print "<<<<<<REPORT STARTS>>>>>>"
    get_popular_articles()
    get_popular_article_authors()
    get_days_of_errors()
    print ""
    print "<<<<<<End Of The Report>>>>>>"
    print ""
