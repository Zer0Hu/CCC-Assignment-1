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
    



    