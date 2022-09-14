# from ast import pattern
# 从日志中提取数据并写到excel中，log已更新，请参考最新脚本
import re
from nbformat import write
import pandas as pd
import csv
import os

path = "../../third_party/xntp/sender/"

files = os.listdir(path)
flowNum = len(files)
rateRecord = "Rateof"+str(flowNum)+"flows.xlsx"
burstSizeRecord = "BurstSizeof"+str(flowNum)+"flows.xlsx"

rateWriter = pd.ExcelWriter(rateRecord)
burstWriter = pd.ExcelWriter(burstSizeRecord)

# XDEBUG("BurstRate: %lf, RecvRate: %lf, Rate,: %lf, Stalling: %lf, Time: %lf", token.rate(), token.recvRate(),sender_->rate_, sender_->stalling_, time::currentSecond());
# XDEBUG("BurstSize: %zu",queue_.size());
for filename in files:
    with open(path+filename, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        f.close()
    # 读完一个文件中的数据
    rates = []
    bursts = []
    for line in lines:
        string = str(line)
        regex = r".*: (.*), .*: (.*), .*: (.*), .*: (.*), .*: (.*)"
        # regex = r".*update (.*) at time (.*) unsmoothed (.*)"
        rate = re.search(regex, line)
        regex2 = r"BurstSize: (.*)"
        burst = re.search(regex2,line)
        if(rate):
            rates.append([rate.group(5), float(rate.group(1))*8/1024/1024, float(rate.group(2))
                        * 8/1024/1024, float(rate.group(3))*8/1024/1024, rate.group(4)])
        if(burst):
            bursts.append([burst.group(1)])
            
    rateData = pd.DataFrame(rates)
    rateData.to_excel(rateWriter, sheet_name=filename, header=[
                    "Time", "BurstRate", "RecvRate", "Rate", "Stalling"])
    burstData = pd.DataFrame(bursts)
    burstData.to_excel(burstWriter,header=["BurstSize"])


burstWriter.save()
burstWriter.close()

rateWriter.save()
rateWriter.close()
