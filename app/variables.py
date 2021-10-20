#Variables for html files

K_Bitcoin = db.Table('K_BITCOIN', db.metadata, autoload=True, autoload_with=db.engine)
K_Cardano = db.Table('K_CARDANO', db.metadata, autoload=True, autoload_with=db.engine)
K_Ethereum = db.Table('K_ETHEREUM', db.metadata, autoload=True, autoload_with=db.engine)

bref1='static/images/Actual_vs_Predictions_Bitcoin_just_market.svg'
bref2='static/images/Actual_vs_Predictions_Bitcoin_just_reddit.svg'
bref3='static/images/Actual_vs_Predictions_Bitcoin_all_data.svg'
cref1='static/images/Actual_vs_Predictions_Cardano_just_market.svg'
cref2='static/images/Actual_vs_Predictions_Cardano_just_reddit.svg'
cref3='static/images/Actual_vs_Predictions_Cardano_all_data.svg'
href1='static/images/Actual_vs_Predictions_Ethereum_just_market.svg'
href2='static/images/Actual_vs_Predictions_Ethereum_just_reddit.svg'
href3='static/images/Actual_vs_Predictions_Ethereum_all_data.svg'

pre_processing=f'All preprocessing is done in Python.
- The Kaggle data is clean and required no preprocessing.
- The Yahoo Finance data is scraped from Yahoo Finance in groups of 100.  These groups are then combined and sorted by date.  No other processing is required.
- For the Reddit data, posts are pulled from an API.  Posts that are not in English (as identified by langid) are dropped.  Posts with duplicate titles are dropped.  Finally, the NLTK library is used to run a sentiment analysis on the post title and the sentiment data (positive, negative, neutral, composite) is added to each post.
- For the Twitter data, posts are pulled from an API.  The API request only returns English results.  Desired features are pulled out of twitter.module.status objects into a list of generic objects.  The NLTK library is used to run a sentiment analysis on the post text and the sentiment data (positive, negative, neutral, composite) is added to each post.'
