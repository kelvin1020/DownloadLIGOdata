#!/usr/bin/env python
# coding: utf-8
"""
Nov 24, Shucheng Yang

"""


from abc import ABCMeta, abstractmethod
from gwosc.datasets import find_datasets, run_segment
from gwosc.locate import get_run_urls, get_event_urls
import logging
from multiprocessing import Pool
import os
import re
import time



from json.decoder import JSONDecodeError

def datasets2sample_rate(datasets):
    """从数据集名中提取采样率"""
    if datasets.find("16KHZ") != -1:
        return 16384
    elif datasets.find("4KHZ") != -1:
        return 4096
    elif datasets == "O1":
        return 4096
    else:
        print("Please check your input?")
        return None

class AbstractGetdata(metaclass=ABCMeta):
    """下载数据的抽象类"""
    def __init__(self, datasets, dirname = None):
        """初始化，创建下载文件夹，文件夹名称若为空，则默认为数据库名称database"""
        self.datasets = datasets
        
        if dirname:
            self.dirname  = dirname
        else:
            self.dirname = datasets

        if not os.path.exists(self.dirname):
            os.system("mkdir " + self.dirname)
        
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename=self.dirname + '/download.log', level=logging.INFO) 
        logging.info("Created Directory" + self.dirname)

    def __down__(self, url):
        """根据网址下载数据"""
        try:
            os.system("wget -P " + self.dirname + '/ --no-check-certificate '+ url)
            return 1
        except ValueError as e:
            logging.info(e)

    @abstractmethod
    def download(self):
        pass

class getspan(AbstractGetdata):
    """下载运行数据，继承自AbstractGetdata"""
    def __init__(self, datasets, dirname = None):
        super().__init__(datasets, dirname)

    def __downWhichDetector__(self, detector):
        """下载某次运行某一探测器的全部数据，并行"""
        try:
            urls = get_run_urls(self.datasets, detector, self.start, self.end)  #获取数据段网址

            #检查某一数据段是否已下载，删除重复网址
            pattern = re.compile(detector[0] + '-.*.hdf5')  
            urls_reduced = []
            for url in urls:
            # for url in urls[0:2]: #测试                
                if not os.path.exists(self.dirname + '/' + pattern.search(url).group()): #如果未下载，则加入精简url列表
                    urls_reduced.append(url)

            with Pool() as pool:
                result = pool.map(self.__down__, urls_reduced)  #并行下载
        except JSONDecodeError:
            logging.info(detector + " data not exits in " + self.datasets)

    def download(self):
        """下载某次运行所有探测器的全部数据"""
        self.sample_rate = datasets2sample_rate(self.datasets)
        self.start, self.end = run_segment(self.datasets)      #查询数据段起始时刻start、结束时刻end
        
        self.__downWhichDetector__("H1")
        self.__downWhichDetector__("L1")        
        self.__downWhichDetector__("V1")        

class getevent(AbstractGetdata):
    """docstring for getdata"""
    def __init__(self, arg):
        super(AbstractGetdata, self).__init__()
        self.arg = arg
        

if __name__ == '__main__':
    #下载运行数据测试
    run_set = find_datasets(type='run') #运行数据集
    print(run_set)
    datasets = input("Please choose a datasets: ")

    test = getspan(datasets)
    test.download()


