from gwosc.datasets import run_segment
from gwosc.locate import get_urls
from multiprocessing import Pool
import os
import time
import re
#URL
#e.g. https://www.gw-openscience.org/archive/data/S6/967835648/L-L1_LOSC_4_V1-968650752-4096.hdf5

dirname = "O1"

start, end = run_segment(dirname)
timespan = range(start, end, 4096)                     #每段4096s

runlist = timespan[0:10]
# runlist = timespan[0:]

print("O1, start = {0}, end = {1}".format(start, end))

if not os.path.exists(dirname) : os.system("mkdir " + dirname), print(dirname + " created!")

pattern1 = re.compile('H-.*.hdf5')  
pattern2 = re.compile('L-.*.hdf5')  

def downHSpan(i):
    try:
        url1 = get_urls("H1", i, i+4096)[0]
        if not os.path.exists( dirname  + '/' + pattern1.search(url1).group() ): #若不存在文件，则下载
            os.system("wget -P" + dirname + '/ '+ url1)
        return 1        

    except Exception as e:
        with open(dirname + "/log.txt", 'a') as f:
            print(time.asctime() + ' ' + str(e), file = f)
        return 0 


def downLSpan(i):
    try:
        url2 = get_urls("L1", i, i+4096)[0]
        if not os.path.exists( dirname  + '/' + pattern2.search(url2).group() ):
            os.system("wget -P" + dirname + '/ '+ url2)
        return 1        

    except Exception as e:
        with open(dirname + "/log.txt", 'a') as f:
            print(time.asctime() + ' ' + str(e), file = f)
        return 0 


with Pool() as pool:
    result1 = pool.map(downHSpan, runlist)
    result2 = pool.map(downLSpan, runlist)

with open(dirname + "/run_result.txt", 'w') as f:
    print(result1, file = f)
    print(result2, file = f)    