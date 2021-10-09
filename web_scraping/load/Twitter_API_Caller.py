import langid
import twitter

def fetch_twitter_data(sia, api, start, end, coin, size = 50):
    """
    Given sentiment analyzer, a date range and coin:
    1) Get size twitter posts about that coin.
    2) Get sentiment scores.
        restrict_score must be in the format >int or <int
        max value for size is 100
    Date ranges are expected in 'YYY-MM-DD' format
    Returned tweets are already filtered to be in English and pulled from "popular" for the time span.
    I am not sure what metric twitter uses to define whether a tweet counts as popular or not, but this
    does not return all tweets for teh day sorted form most to least popular, as removing the popular flag
    returned more tweets.
    """
                
    def get_sentiment(posts, sia):
        """Given a set of posts, runs sentiment analysis on the titles and returns the posts with the analysis."""
        for post in posts:
            post['sentiment_scores'] = sia.polarity_scores(post['text'])
        return posts
    
    # convert twitter module to object     
    res = api.GetSearch(term = coin, count = size, since = start, until = end, lang='en', result_type='popular')
    posts = []
    for status in res:
        posts.append({
            'text': status.text,
            'created:': status.created_at,
            'favorites': status.favorite_count,
            'retweets': status.retweet_count,
            'followers': status.user.followers_count
        })
        
    # get sentiment analysis
    posts = get_sentiment(posts, sia)
    return posts