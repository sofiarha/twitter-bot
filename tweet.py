import tweepy
import requests
# allows us to use the operating system and load environment variables 
import os
from dotenv import load_dotenv
# allows the bot to choose one artwork at random
from random import randint

# pulling the keys and secrets from our .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# debugging statement: checking to see we get our correct keys and secrets
print(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# handles authentication
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# also handles authentication 
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# debugging statement: making sure we have loaded the variables
print('we loaded the auth variables')

def tweet_a_woman(tweepy_client):
    # debugging: checking to see that the function is running
    print('fetching women from the MET...')

    r1 = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/search?q=cat")
    parsed = r1.json()

    # grabbing a random work from the top 6000
    number = randint(1, 600)

    # grabbing data about the individual work
    obj_id = parsed['objectIDs'][number]
    r2 = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}")
    parsed = r2.json()

    # getting title, artist, gender, url
    if parsed['title'] != '':
       title = f"Title: {parsed['title']}"
    else:
        title = f"Title: Unknown"
    if parsed['artistDisplayName'] != '':
       artist = f"Artist: {parsed['artistDisplayName']}"
    else:
       artist = 'Artist: Unknown'
    if parsed['artistGender'] != '':
        gender = parsed['artistGender']
    else:
        gender = 'Artist Gender: Not marked'
    url = parsed['objectURL']

    # getting image (have to use the other auth)
    image_url = parsed['primaryImage']
    img = requests.get(image_url)
    img_content = img.content
    with open('image.jpg', 'wb') as handler:
        handler.write(img_content)
    media = api.media_upload(filename='image.jpg')
    media_id = media.media_id

    # setting up the tweet text
    tweet_text = f"{title}, {artist}, {gender}. See more: {url}"
    print('tweeting women from the MET...')
    api.update_status(status=tweet_text, media_ids=[media_id])
 
# calling the function with the auth data as parameter
tweet_a_woman(client)

