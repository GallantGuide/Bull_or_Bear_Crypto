# packages for api request
import requests as re
import time

#language detection
import langid

#package for sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

def fetch_reddit_data(sia, start, end, coin, restrict_score = '>0', size = 500, fields = [
    'num_comments', 'title', 'score', 'upvote_ratio', 'subreddit']):
    """
    Given sentiment analyzer, a date range and coin:
    1) Get size reddit posts about that coin sorted from highest to lowest score.
    2) Remove duplicated posts.
    3) Remove non-english posts.
    4) Get sentiment scores.
        restrict_score must be in the format >int or <int
        max value for size is 500
    """
    
    def make_api_request(start, end, coin, restrict_score, size, fields):
        base_url = 'https://api.pushshift.io/reddit/search/submission/'
        params = {
            'title': coin,
            'fields': fields,
            'sort_type': 'score',
            'score': restrict_score,
            'after':  create_epoch(start, '00:00:01'),
            'before': create_epoch(end, '23:59:59'),
            'size': size
        }
        return re.get(base_url, params).json()['data']
    
    def create_epoch(date, clock):
        """Given date (format = ‘mm/dd/yyyy’) and clock (format = 'HH:MM:SS') return the Epoch."""
        date_time = f"{date} {clock}"
        pattern = '%m/%d/%Y %H:%M:%S'
        return int(time.mktime(time.strptime(date_time, pattern)))
    
    def deduplicate_titles(posts):
        """Removes posts based on duplicate titles.
        Caveot: posts with identical titles from different authors will be lost.
        However, this should only affect a small proportion of the data and will 
        catch posts resubmitted by bot accounts.s"""
        def titler(post):
             titles.append(post['title'])
             return post

        titles = []
        return [titler(post) for post in posts if post['title'] not in titles]
    
    def get_english_posts(posts):
        english_posts = []

        for post in posts:
            if langid.classify(post['title'])[0] == 'en':
                english_posts.append(post)
        return english_posts
                
    def get_sentiment(posts, sia):
        for post in posts:
            post['sentiment_scores'] = sia.polarity_scores(post['title'])
        return posts
    
    # API request
    posts = make_api_request(start, end, coin, restrict_score, size, fields)
    # remove duplicate titles
    posts = deduplicate_titles(posts)
    # remove non-english posts
    posts = get_english_posts(posts)
    # get sentiment and add to data
    return get_sentiment(posts, sia)