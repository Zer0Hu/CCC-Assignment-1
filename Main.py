import time
import numpy as np
import re
from Utils import read_file, extract_sentiment, extract_created_at
from Utils import calculate_q1,calculate_q2, calculate_q3, calculate_q4
from mpi4py import MPI

# Read files
file_1 = 'twitter-1mb.json'
file_2 = 'twitter-50mb.json'


t0 = time.time() # Initial time when start reading

# initialize MPI - communicator
comm = MPI.COMM_WORLD
# get current rank
rank = comm.Get_rank()
# get total number of ranks
size = comm.Get_size()


# Create two 3D-array to store sentiment scores and number of tweets in every hour respectively
SHAPE = (12,31,24) # (month,day,hour)
hour_sentiment = np.zeros(shape=SHAPE, dtype=float) 
hour_count = np.zeros(shape=SHAPE,dtype=int) 
# fill both arrays with zeros first, sentiment scores would be float and number of tweets would be an integer

for row in read_file(rank, size, file_2):

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

hour_sentiment_gathered = comm.reduce(hour_sentiment, op=MPI.SUM, root=0)
hour_count_gathered = comm.reduce(hour_count, op=MPI.SUM, root=0)



# Calculate using Master node
if rank == 0:

    # Question 1
    max_sentiment, happiest_hour_index = calculate_q1(hour_sentiment_gathered)
    month, day, hour = happiest_hour_index
    am_pm = "am" if hour < 12 else "pm"
    start_hour = str((hour % 12) or 12) + am_pm  # 转换小时为12小时制，并加上AM/PM信息
    end_hour = str(((hour + 1) % 12) or 12) + am_pm  # 计算结束小时的12小时制表示形式
    print("The happiest hour ever is at {}-{}, {} - {}, with a sentiment score of {:.2f}".format(
            month, day, start_hour, end_hour, max_sentiment))


    # Question 2
    happiest_day, happiest_day_index = calculate_q2(hour_sentiment_gathered)
    print("The happiest day ever is at {}-{}, with a total sentiment score of {:.2f}".format(
        happiest_day_index[0]+1, happiest_day_index[1]+1, happiest_day))


    # Question 3
    max_count, most_active_hour_index = calculate_q3(hour_count_gathered)
    max_count = int(max_count)
    month, day, hour = most_active_hour_index
    am_pm = "am" if hour < 12 else "pm"
    start_hour = str((hour % 12) or 12) + am_pm  # 转换小时为12小时制，并加上AM/PM信息
    end_hour = str(((hour + 1) % 12) or 12) + am_pm  # 计算结束小时的12小时制表示形式
    print("The most active hour ever is at {}-{}, {} - {}, had the most tweets(#{})".format(
            month, day, start_hour, end_hour, max_count))


    # Question 4
    most_active_day_count, most_active_day_index = calculate_q4(hour_count_gathered)
    print("The most active day ever is at {}-{}, had the most tweets(#{})".format(
        most_active_day_index[0]+1, most_active_day_index[1]+1, most_active_day_count))





