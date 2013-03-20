import json
import oauth2 as oauth
import pprint

def get_tweets():
	f= open('../resource/tweet.txt','r')
	tweet = json.loads(f.readline())
	return tweet

def get_uid(tweet):
	return tweet['user']['id']

def get_tweetid(tweet):
	return tweet['id']

# extracts the user_details in the tweet json object.
def get_author_details(tweet):
	# Will have to change as per yahoo format
	uid = tweet['user']['id']
	verified = tweet['user']['verified']
	followers_count = tweet['user']['followers_count']
	description = tweet['user']['description']
	name = tweet['user']['name']
	screen_name = tweet['user']['screen_name']
	created_at = tweet['user']['created_at']
	time_zone  = tweet['user']['time_zone']
	text = tweet['text']
	
	return tweet['user']

# Make call to twitter API version to get all followers of user with uid
def get_followers(uid,type,version,client):

	cursor = '-1'
	limit_remaining = 4
	followers =[]
	count = 0

	# Loop to get all the pages of response
	while(limit_remaining > 3 and cursor!='0'):
		count +=1	
		if (count==3):
			break
		api_call = "https://api.twitter.com/"+str(version)+"/followers/ids.json?cursor="+cursor+"&used_id="+str(uid)
		if(type==1):
			api_call = "https://api.twitter.com/"+str(version)+"/followers/ids.json?cursor="+cursor+"&user_id="+str(uid)
		response, data = client.request(api_call)
		data_json = json.loads(data)
		
		# print pprint.pprint(response)
		if(response['status']=='200'):
			followers = followers + data_json['ids']
			cursor = data_json['next_cursor_str']
		else:
			break
		if(version==1):
			limit_remaining = int(response['x-ratelimit-remaining'])
		else:
			limit_remaining = int(response['x-rate-limit-remaining'])

	entry = {
			 "author" : uid,
			 "followers" : followers,
			 "response"	 : response
			 }	
	return entry


# Batch request to Twitter API version to get details of all users in uids
def get_user_details_batch(uids,type,version,client):

	api_call = "https://api.twitter.com/"+str(version)+"/users/lookup.json?user_id="+str(uids)
	if(type==1):
		api_call = "https://api.twitter.com/"+str(version)+"/users/lookup.json?screen_name="+str(uids)

	api_call = "https://api.twitter.com/1/users/lookup.json?screen_name=agarwalpranaya,swamy39"

	response, data = client.request(api_call)
	return [response,data]


def get_user_details(uid,type):
	CONSUMER_KEY = "YSXXstxTV3rJFRAmX9HyQ"
	CONSUMER_SECRET = "96ZZ8qoULMeptOiumnYYPcl2WmzVgPQdNlLeSkGG4yU"
	ACCESS_KEY = "121059967-SVLSt2qIwLQXPYAKVzZIHquQFHR2g3kkWFrGZeee"
	ACCESS_SECRET = "zUXxk8EI7tf4nJLtWqxrYbCQ83z0yTm83AYaXrLTyU"

	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)
	
	api_call = "https://api.twitter.com/1/users/show.json?user_id="+str(uid)
	if(type==1):
		api_call = "https://api.twitter.com/1/users/show.json?screen_name="+str(uid)
	
	response, data = client.request(api_call)
	return [response,data]