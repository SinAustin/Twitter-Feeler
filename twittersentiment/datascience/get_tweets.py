from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from ..config import *
import os.path
import sys
import os

class listener(StreamListener):
    """ twitter streaming class s"""
    # create txt file to store tweets
    if os.path.isfile('tweets.txt'):
        pass
    else:
        output = open('tweets.txt','a')
        output.write('tweets, time\n')
        output.close() 
    
    def __init__(self):
        """ tweet limit """
        super().__init__()
        self.reset()
    
    def on_status(self, status):
        """  Retrieves the text and publish time for each tweet. 
             Splits the tweet text on "RT" to retrieve  the  main text if the  tweet is apart of a retweet.
             Gets tweets until the count reaches the defines limit
        """
        try:
           
            time = status.created_at
            text = str(status.text)
                
            if text.startswith('RT'):
                text = text.split('RT')[1].replace(',','')
                print(text)
                print(time)
                
                line = str(text + ',' + str(time) + '\n')
                output = open('tweets.txt','a')
                output.write(line)
                output.close()     
            else:
                text = text.split('RT')[0].replace(',','')
                print(text)
                
                line = str(text + ',' + str(time) + '\n')
                output = open('tweets.txt','a')
                output.write(line)
                output.close()

            # count
            self.counter += 1
            print(self.counter)
            
            if self.counter < self.limit:
                return True
            else:
                self.counter ==0
                twitterStream.disconnect()
                
                                    
        except BaseException as e:
            print('failed on_status,',str(e))
            
   
    
    def on_error(self, status):
        print(status)

    def reset(self):
        
        self.counter = 0
        self.limit = 1000
        

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
