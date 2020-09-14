#BSUB -J O1
#BSUB -q GW
#BSUB -n 10
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -a python 
#BSUB -R span[ptile=10]
python /share/home/yangsc/Documents/DownloadLIGOdata/downloadO1data.py
