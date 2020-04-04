import twint
import pandas as pd
import argparse
import os
import datetime


def collect(username):
    start_date = datetime.datetime(2009,1,1) # date when twitter was founded
    threshold = datetime.datetime(2011,12,31)

    while start_date < threshold:
        end_date = start_date + datetime.timedelta(days = 120)
        c = twint.Config()
        c.Username = username
        c.Until = end_date.strftime("%Y-%m-%d")
        c.Since = start_date.strftime("%Y-%m-%d")
        c.Store_csv = True
        c.Output = username + '_h1n1.csv'
        twint.run.Search(c)
    
    
        start_date = end_date + datetime.timedelta(days = 1)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', type=str, required=True, help="username from which to scrape")
    args = parser.parse_args()
    collect(args.username)


    
    