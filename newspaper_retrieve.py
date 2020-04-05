import datetime
from datetime import timedelta
import argparse
import os
import json
import pandas as pd

import newspaper
# from newspaper import Article

webarchive_header = 'http://web.archive.org/web'


def collect_news(base_url, sdate, edate):
    base_info = args.base_url.replace('/', '.').split('.')
    name_idx = base_info.index("www") + 1
    name = base_info[name_idx]

    all_urls = []
    missing = []
    sdate = datetime.datetime.strptime(sdate, "%Y-%m-%d").date()   # start date
    edate = datetime.datetime.strptime(edate, "%Y-%m-%d").date()   # start date

    delta = edate - sdate

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)

        output_path = os.path.join('output', name + '_' + day.strftime("%Y%m%d") + '.json')
        if os.path.exists(output_path):
            continue

        timestamp = day.strftime("%Y%m%d") + '000000'
        url = '/'.join([webarchive_header, timestamp, base_url])
        print(url)
        nn = newspaper.build(url, memoize_articles=False)

        print(len(nn.articles))

        day_data = []
        for article in nn.articles:
            # if len(day_data) > 3:
            #     break

            try:
                article.download()
                article.parse()
            except Exception as e:
                print(e)
                missing.append({'base': base_url, 'day': day.strftime("%Y-%m-%d"), 'article_url': article.url})

            publish_date = article.publish_date
            if publish_date is None:
                publish_date = day

            article_data = {
                'url': article.url,
                'publish_data': publish_date.strftime("%Y-%m-%d"),
                'content': article.text,
                # 'html': article.html,
                'title': article.title,
                'keywords': article.keywords
            }

            day_data.append(article_data)

        with open(os.path.join('output', 'missing.json'), 'w+') as f:
            f.write(json.dumps(missing))

        with open(output_path, 'w+') as f:
            f.write(json.dumps(day_data))

def collect_news_tiny(url, publish_date_tw, newspaper_name):

    missing = []
    all_urls = []

    output_path = os.path.join('output', newspaper_name+url.replace("/", "")[-5:] +'.json')

    print(url)
    nn = newspaper.build(url, memoize_articles=False)

    print(len(nn.articles))

    day_data = []
    day = publish_date_tw
    for article in nn.articles:
        # if len(day_data) > 3:
        #     break

        try:
            article.download()
            article.parse()
        except Exception as e:
            print(e)

        publish_date = article.publish_date
        if publish_date is None:
            publish_date = day

        article_data = {
            'url': article.url,
            'publish_data': str(publish_date),
            'content': article.text,
            # 'html': article.html,
            'title': article.title,
            'keywords': article.keywords
        }

        day_data.append(article_data)

    with open(os.path.join('output', 'missing.json'), 'w+') as f:
        f.write(json.dumps(missing))

    with open(output_path, 'w+') as f:
        f.write(json.dumps(day_data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #parser.add_argument('-u', '--base-url', type=str, required=True, help="base url")

    parser.add_argument('-s', '--since', type=str, required=True, help="start time \%Y-\%m-\%d")
    parser.add_argument('-t', '--to', type=str, required=True, default=None, help="end time \%Y-\%m-\%d")

    parser.add_argument('-f', '--filename', type=str, required=True, help="csv file from twitter_scrap")
    parser.add_argument('-i', '--index', type=int, default=0, help="starting csv row")
    parser.add_argument('-n', '--newpaper', type=str, default="", help="newspaper name")

    # parser.add_argument('-o', '--output', type=str, required=True,  help="username from which to scrape")

    args = parser.parse_args()

    df_urls = pd.read_csv(args.filename)

    df_urls["url"] = df_urls["tweet"].apply(lambda tweet : tweet[tweet.find("http"):].split(" ")[0])

    for entry in df_urls[args.index:].iterrows():
        if entry[1]["url"] is not None and "http" in entry[1]["url"]:
            collect_news_tiny(entry[1]["url"], entry[1]["date"], args.newpaper)

    # collect_news(args.base_url, args.since, args.to)
    # collect(args.key_word, args.since, args.to, output_file)