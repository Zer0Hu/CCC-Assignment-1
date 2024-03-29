import time
from datetime import datetime

def read_file(file_path):
    f = open(file_path,"rb")
    for line in f:
        yield line.decode()
    
    f.close()
# lazy load, only load when the program needs to.
# Read in lines one by one to save memory.
# Cleaner, has a higher flexibility than normal .readline().
    


def extract_sentiment(tweet):
    sentiment_score = tweet.get("sentiment")
    if sentiment_score is not None:
        sentiment_score = float(sentiment_score)
    else:
        return None
    


def extract_created_at(tweet):
    
    # 获取 "created_at" 字段的值
    created_at = tweet.get('data', {}).get('created_at', None)
    
    # 如果存在 "created_at" 字段，提取月份、日期和小时信息
    if created_at is not None:
        # 将字符串日期时间信息转换为datetime对象
        created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # 提取月份、日期和小时信息
        month = created_at_dt.month
        day = created_at_dt.day
        hour = created_at_dt.hour
        
        return month, day, hour
    else:
        return None