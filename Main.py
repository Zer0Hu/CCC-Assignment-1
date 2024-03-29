import time
import numpy as np
import re
from Utils import read_file, extract_sentiment, extract_created_at

# Read files
file_1 = 'twitter-1mb.json'
file_2 = 'twitter-50mb.json'


t0 = time.time() # Initial time when start reading

# Create two 3D-array to store sentiment scores and number of tweets in every hour respectively
SHAPE = (12,31,24) # (month,day,hour)
hour_sentiment = np.zeros(shape=SHAPE, dtype=float) 
hour_count = np.zeros(shape=SHAPE,dtype=int) 
# fill both arrays with zeros first, sentiment scores would be float and number of tweets would be an integer

for row in read_file(file_2):

    # extract every tweet's sentiment score and datetime 
    sentiment = extract_sentiment(row)
    datetime = extract_created_at(row)

    # record them in the array
    if (datetime is not None):
        #index starts from 0, month and day start from 1, so minus one
        hour_count[datetime[0]-1, datetime[1]-1, datetime[2]] += 1

        if (sentiment is not None):
            hour_sentiment[datetime[0]-1, datetime[1]-1, datetime[2]] += sentiment


print("run time:", time.time() - t0) # Using the time when finish reading 
# minus initial time to record the time needed to read the file


# 


