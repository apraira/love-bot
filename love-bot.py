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


# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
print('connected to Twitter')

class StreamListener(tweepy.StreamListener):
    tweet_counter = 0
    nkata = 0
    total_predict = 0
    name = "Love Prediction"
    api.update_profile(name)
    titel_sebelum = ""
    
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
            elif nfolls < 5:
                    
                time.sleep(20)
                api.update_status("@" + status.user.screen_name + " " + 'Sorry, your followers must be more than 5.', in_reply_to_status_id=status.id)
                print(str(StreamListener.tweet_counter) + ". (less than 5 followers)" + status.user.screen_name +
                                  ": " + status.text + " ( replied )")

            elif 'count' in status.text.lower() or 'hitung' in status.text.lower():
                kata2= status.text.lower()
                ls = kata2.replace("@predictyourlove", "")
                ls = ls.split()
 
                matches = [match for match in ls if "@" in match]
 
                unem = matches[0].replace("@", "")

                angka = random.randint(1, 100)

                if StreamListener.titel_sebelum == "sad":
                    angka = random.randint(16, 100)
                elif StreamListener.titel_sebelum == "not enough":
                    angka = random.randint(31, 100)
                elif StreamListener.titel_sebelum == "lovey":
                    angka = random.randint(51, 100)
                elif StreamListener.titel_sebelum == "slow":
                    angka = random.randint(66, 100)
                elif StreamListener.titel_sebelum == "goodenough":
                    angka = random.randint(96, 100)
                elif StreamListener.titel_sebelum == "perfect":
                    angka = random.randint(0, 15)
                elif unem == 'meivean' or unem == 'reinantares':
                    angka = 100
                else:
                     angka = angka

                ang = str(angka) +"%"
                    
                if angka > 0 and angka < 16:
                    kata2 = "Your score with @/ "+unem + ": " + ang + ". Sorry, but your love is as likely to bear fruit as a mango tree planted on an Antarctic glacier."
                        
                    titel = "sad"
                    
                elif angka > 15 and angka < 31:
                    kata2 = "Your score with @/ "+unem + ": " + ang + ". Your love is as strong as the love between most children and their vegetables ??? insubstantial."
                        
                    titel = "not enough"

                elif angka > 30 and angka < 51:
                    kata2 = "Your score with @/ "+unem + ": " + ang + ". Love like this can be seen in the eyes of a dog wanting to continue playing fetch with its exhausted owner ??? longing, yet not currently viable."
                                              
                    titel = "lovey"

                elif angka > 50 and angka < 66:
                    kata2 = "Your score with @/ "+unem + ": " + ang +  ". Your love is comparable to rush hour traffic. Slow and frustrating, but possible to navigate through persistence and sheer force of will."
                        
                    titel = "slow"

                elif angka > 65 and angka < 96:
                    kata2 = "Your score with @/ "+unem + ": " + ang + ". Good enough. Might as well check love off your list of things society believes you should've accomplished by now."
                        
                    titel = "goodenough"

                elif angka > 95 and angka < 101:
                    kata2 = "Your score: " + ang + ", Congratulations you and @/" + unem + " are made to spend your lives together."                        
                    titel = "perfect"
                   
            
                    

                StreamListener.titel_sebelum = titel
                time.sleep(60)

                   
                api.update_status("@" + status.user.screen_name + " " + kata2, in_reply_to_status_id=status.id)
                StreamListener.tweet_counter += 1
                StreamListener.total_predict += 1

                #logs
                print(str(StreamListener.tweet_counter) + ".  " +
                status.user.screen_name + ": " + status.text + " ( replied )")

                    


                    

            else:
                #get list of user followers
                folls = api.followers(user_id=target_user_id, screen_name=target_user.screen_name, count=5)
                angka = random.randint(1,4)

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
                    

                time.sleep(60)

                   
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
