# from ast import pattern
import re
from nbformat import write
import pandas as pd
import csv
import os

path = "./burstRateData/"

files = os.listdir(path)
flowNum = len(files)
excelname = "./Rateof"+str(flowNum)+"flows.xlsx"
ntosendname = "./ntosendof"+str(flowNum)+"flows.xlsx"

writer = pd.ExcelWriter(excelname)
writer_ntosend = pd.ExcelWriter(ntosendname)

# XDEBUG("BurstRate: %lf, RecvRate: %lf, Rate,: %lf, Stalling: %lf, Time: %lf", token.rate(), token.recvRate(),sender_->rate_, sender_->stalling_, time::currentSecond());
for filename in files:
    with open(path+filename, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        f.close()
    # 读完一个文件中的数据
    data = []
    ntosend = []
    for line in lines:
        string = str(line)
        regex = r".*: (.*), .*: (.*), .*: (.*), .*: (.*), .*: (.*)"
        # regex = r".*update (.*) at time (.*) unsmoothed (.*)"
        mysearch = re.search(regex, line)
        regex2 = r"time: (.*), bytes number: (.*)"
        mysearch2 = re.search(regex2,line)
        if(mysearch):
            data.append([mysearch.group(5), float(mysearch.group(1))*8/1024/1024, float(mysearch.group(2))
                        * 8/1024/1024, float(mysearch.group(3))*8/1024/1024, mysearch.group(4)])
        if(mysearch2):
            ntosend.append([mysearch2.group(1),mysearch2.group(2)])
            
    pdData = pd.DataFrame(data)
    pdData.to_excel(writer, sheet_name=filename, header=[
                    "Time", "BurstRate", "RecvRate", "Rate", "Stalling"])
    ntosend = pd.DataFrame(ntosend)
    ntosend.to_excel(writer_ntosend,header=["Time", "ntosend"])


writer.save()
writer.close()

writer_ntosend.save()
writer_ntosend.close()
