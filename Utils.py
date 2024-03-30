import time
import numpy as np
import re
import os
from datetime import datetime

def read_file(rank, size,file_path):
    f_size = os.path.getsize(file_path)
    # 每个node读一样的size的file， 把整个file平均分成size份
    bytes_per_node = f_size // size
    chunk_start = rank * bytes_per_node
    bytes_readed = 0 # 当前node已经读了多少byte，初始值为0


    f = open(file_path,"rb")
    f.seek(chunk_start,0) #找到当前node开始读的地方
    for line in f:

        # 如果一行在中间被分开了怎么办？
        # 方案：除了rank0, 其他rank都不读第一行，让前一个rank读
        if rank == 0 or bytes_readed > 0:
            yield line.decode()
    
        bytes_readed += len(line)

        if bytes_readed >= bytes_per_node:
            break

    f.close()
# lazy load, only load when the program needs to.
# Read in lines one by one to save memory.
# Cleaner, has a higher flexibility than normal .readline().
    


def extract_sentiment(line):
    # 查找匹配的sentiment
    match = re.search(r'"sentiment":(-?\d+(\.\d+)?)', line)
    if match:
        try:
            # 尝试将匹配到的string转换为float
            sentiment = float(match.group(1))
            return sentiment
        except ValueError:
            # 如果无法转换为float，则返回 None
            # 所以如果sentiment不是数字， ignore
            # ！！(所以我没有考虑sentiment不是float的情况，据说有些sentiment后面跟的是个dictionary)！！
            return None
    else:
        return None
    


def extract_created_at(line):
    # 用正则表达式从string中匹配创建时间
    match = re.search(r'"created_at":"([^"]+)"', line)
    if match:
        created_at_str = match.group(1)  # 获取匹配到的string
        # 提取month, day, hour
        date_time_match = re.match(r'\d{4}-\d{2}-\d{2}T(\d{2}):', created_at_str)
        if date_time_match:
            month = int(created_at_str[5:7])
            day = int(created_at_str[8:10])
            hour = int(date_time_match.group(1))
            return month, day, hour
        else:
            return None
    else:
        return None
    
def calculate_q1(hour_sentiment):
    max_sentiment = 0  # 初始设为0
    happiest_hour_index = None  # 最快乐的小时的index

    
    for month in range(hour_sentiment.shape[0]):
        for day in range(hour_sentiment.shape[1]):
            for hour in range(hour_sentiment.shape[2]):
                sentiment = hour_sentiment[month, day, hour]
                # 如果当前小时的sentiment大于max_sentiment，则更新max_sentiment和index
                if sentiment > max_sentiment:
                    max_sentiment = sentiment
                    happiest_hour_index = (month + 1, day + 1, hour)

    return max_sentiment, happiest_hour_index


def calculate_q2(hour_sentiment):
    # 将第三维度（小时）的值加起来，得到每天的total sentiment
    day_sentiment_total = np.sum(hour_sentiment, axis=2)
    
    # 找到sentiment最大的一天和对应的index
    happiest_day = np.max(day_sentiment_total)
    happiest_day_index = np.unravel_index(np.argmax(day_sentiment_total), day_sentiment_total.shape)
    
    return happiest_day, happiest_day_index


def calculate_q3(hour_count):
    max_count = 0  # 初始设为0
    most_active_hour_index = None  # 最active的小时的index

    
    for month in range(hour_count.shape[0]):
        for day in range(hour_count.shape[1]):
            for hour in range(hour_count.shape[2]):
                count = hour_count[month, day, hour]
                # 如果当前小时的count大于max_count，则更新max_count和index
                if count > max_count:
                    max_count = count                    
                    most_active_hour_index = (month + 1, day + 1, hour)

    return max_count, most_active_hour_index


def calculate_q4(hour_count):
     # 将第三维度（小时）的值加起来，得到每天的total counts
    day_count_total = np.sum(hour_count, axis=2)
    
    # 找到tweets count最大的一天和对应的index
    most_active_day_count = np.max(day_count_total)
    most_active_day_index = np.unravel_index(np.argmax(day_count_total), day_count_total.shape)
    
    return most_active_day_count, most_active_day_index


    