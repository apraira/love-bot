from tweepy import (Stream, OAuthHandler)
from tweepy.streaming import StreamListener
import time
from os import environ
import tweepy
from urllib3.exceptions import ProtocolError
import random

# V1
#tes
#sekarang lagi make piku
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# V2
"""auth = tweepy.OAuthHandler("S9hbAHn4H5t8R6S3NTJ6B49YV", "KTjZgdPAJaeybGaf8W9yIOgnyn6yPy6R9AuxvkX8Ur92T2erOB")
auth.set_access_token("1387765093556002830-7BjDgpPPXNxqIwSzAbDuvCiRpNNNq5", "S7ZnTZnIAVcs1vwTNEmNVFeu5blRiebuLr7G1hhrZxTLR")"""

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
print('connected to Twitter')

class StreamListener(tweepy.StreamListener):
    tweet_counter = 0
    nkata = 0
    total_predict = 0
    name = "Love Prediction"
    api.update_profile(name)
    
    print('starting prediction')
    
    def on_status(self, status):
        # Static variable
        maks = 5
        
        
        
        #Dynamic Variabel
        target_user_id = status.user.id
        target_user = api.get_user(target_user_id)
        
        user = api.me()
        
        user_a = user.id
        user_b = target_user_id
        
        #to check apakah dah follow apa belum
        stats = api.show_friendship(source_id=user_a, source_screen_name=user.screen_name, target_id=user_b, target_screen_name=target_user.screen_name)
        
        #ngecek jumlah followers
        nfolls = status.user.followers_count
        
        #list kata0
        
        #jika jumlah tweet yang di reply < 5
        
        if StreamListener.tweet_counter < maks:
            
            #jika dia follow akun
            if stats[0].followed_by == True:

                if status.is_quote_status == True:
                    
                    print("> (is quoted)" + status.user.screen_name +
                               ": " + status.text + " ( skipped )")

                elif 'RT' in status.text:
                    
                    print("> (is retweeted)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                elif status.in_reply_to_status_id != None:
                    
                    print("> (is replyied)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                #kalo followers kurang dari 40
                elif nfolls < 40:
                    
                    time.sleep(20)
                    api.update_status("@" + status.user.screen_name + " " + 'Sorry, your followers must be more than 40.', in_reply_to_status_id=status.id)
                    print(str(StreamListener.tweet_counter) + ". (less than 40 followers)" + status.user.screen_name +
                                  ": " + status.text + " ( replied )")

                else:
                    #get list of user followers
                    folls = api.followers(user_id=target_user_id, screen_name=target_user.screen_name, count=40)
                    angka = random.randint(1,39)

                    kata2 = ["Congratulations " + target_user.screen_name + ", your soulmate is " + folls[angka].name + " (@/" + folls[angka].screen_name +")",
                             "Fate brings people together, Congratulations " + target_user.screen_name + " & " + folls[angka].name + " (@/" + folls[angka].screen_name + ") maybe you guys are expected to be together",
                             "We don't meet people by accident. They are meant to cross our path. So does you & " +  folls[angka].name +  " (@/" + folls[angka].screen_name + "), Congratulations :)",
                             "The best love is unexpected. Congratulations! you meet " +folls[angka].name + " (@/" + folls[angka].screen_name + ") by fate. We hope there will be an instant connection.",
                             "When it's time for soul to meet, there's nothing on earth that can prevent them from meeting, Congratulations " + target_user.screen_name + " & " + folls[angka].name + " (@/" + folls[angka].screen_name + ")"]                           
                             

                    #update status 
                    fix = ""
                    
                    if StreamListener.nkata < 4:
                        fix = kata2 [StreamListener.nkata]
                        StreamListener.nkata += 1
                    else:
                        fix = kata2 [StreamListener.nkata]
                        StreamListener.nkata = 0
                    
                    time.sleep(20)
                    api.update_status("@" + status.user.screen_name + " " + fix, in_reply_to_status_id=status.id)


                    StreamListener.tweet_counter += 1
                    StreamListener.total_predict += 1

                    #logs
                    print(str(StreamListener.tweet_counter) + ".  " +
                    status.user.screen_name + ": " + status.text + " ( replied )")

            #Jika dia belom follow akun
            else:

                if status.is_quote_status == True:
                    
                    print("> (is quoted)" + status.user.screen_name +
                               ": " + status.text + " ( skipped )")

                elif 'RT' in status.text:
                    
                    print("> (is retweeted)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                elif status.in_reply_to_status_id != None:
                    
                    print("> (is replyied)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                #reply suruh follow dulu
                else:
                    time.sleep(20)
                    api.update_status("@" + status.user.screen_name + " " + 'Please follow us first, then try again', in_reply_to_status_id=status.id)
                   
                    print(">"  +
                        status.user.screen_name + ": must follow first"  + " ( replied )") 
            
            
            
        #jika jumlah tweet yang di reply > 5
        else:
            print('Max num reached = ' +
                              str(StreamListener.tweet_counter))
            StreamListener.tweet_counter = 0
            print('Istirahat 3 Menit')
            time.sleep(60*3)
            print ("starting prediction again")
            
        
        print('============================')
        print('max number: ' + str(StreamListener.tweet_counter))
        print('total prediction today: ' + str(StreamListener.total_predict))
        print('============================')
            
        
             
        
                      
                      
        
            
    def on_limit(self,track):
        print ("Horrors, we lost %d tweets!" % track)
        
    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

while True:
    try:
        stream.filter(track=["@predictyourlove"], stall_warnings=True)

    except Exception as e:
        print (e)
        time.sleep(1)  # to avoid craziness with Twitter
        continue