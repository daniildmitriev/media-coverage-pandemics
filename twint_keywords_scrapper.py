import twint
import pandas as pd
import argparse
import os

columns = ['cashtags', 'date', 'hashtags', 'hour', 'link', 'name', 'nlikes', 'nreplies', 'nretweets', 'tweet', 'user_id', 'username']


def collect(search_term, start_time, end_time, output_file):
    config = twint.Config()
    config.Search = search_term
    config.Stats = True
    config.Verified = True
    config.Show_hashtags = True
    config.Pandas = True
    config.Since = start_time
    if end_time:
        config.Until = end_time
    # config.Limit = 3
    config.Profile_full = False  # Set to True gives better results but much slower

    twint.run.Search(config)
    df = twint.output.panda.Tweets_df
    df_clean = df[columns]
    df_clean.to_csv(output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-k', '--key-word', type=str, required=True, help="key-word to search for")
    parser.add_argument('-f', '--since', type=str, required=True, help="start time")
    parser.add_argument('-t', '--to', type=str, required=False, default=None, help="end time")
    # parser.add_argument('-o', '--output', type=str, required=True,  help="username from which to scrape")

    args = parser.parse_args()

    if args.to:
        outname = args.key_word + '_' + args.since + '_' + args.to + '.csv'
    else:
        outname = args.key_word + '_' + args.since + '.csv'
    output_file = os.path.join('output', outname)
    collect(args.key_word, args.since, args.to, output_file)
