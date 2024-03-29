import time
import numpy
import re
from datetime import datetime

def read_file(file_path):
    f = open(file_path,"rb")
    for line in f:
        yield line.decode()
    
    f.close()
# lazy load, only load when the program needs to.
# Read in lines one by one to save memory.
# Cleaner, has a higher flexibility than normal .readline().
    


def extract_sentiment(line):
    # 检查该行是否包含 "sentiment" 字段
    if '"sentiment":' in line:
        # 找到 "sentiment" 字段后面的值
        start_index = line.index('"sentiment":') + len('"sentiment":')
        end_index = line.index(',', start_index)  
        sentiment_value_str = line[start_index:end_index].strip()  

        # 将sentiment转换为float
        try:
            sentiment_value = float(sentiment_value_str)
            return sentiment_value
        except ValueError:
            print("Error converting sentiment value to float:", sentiment_value_str)
            return None
    else:
        return None
    


def extract_created_at(line):
    # 用正则表达式从string中匹配创建时间
    match = re.search(r'"created_at":"([^"]+)"', line)
    if match:
        created_at_str = match.group(1)  # 获取匹配到的时间字符串
        # 提取月、日、小时
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
    


    