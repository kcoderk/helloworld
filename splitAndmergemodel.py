#-*- encoding:utf-8 -*-
from sys import argv
import os
def split():
    trunksize=1024*1024*70
    filename=0
    with open('train_model2.m','rb') as f:
        while True:
            trunk=f.read(trunksize)
            if not trunk:
                break
            filename+=1
            with open('modelpart'+str(filename),'wb') as f1:
                f1.write(trunk)
def merge():
    with open('train_model2.m','wb') as f:
        filename=0
        while True:
            filename+=1
            if not os.path.exists('modelpart'+str(filename)):
                break
            with open('modelpart'+str(filename),'rb') as f1:
                trunk = f1.read()
            f.write(trunk)
if __name__ =='__main__':
    if argv[1]=='split':
        split()
    if argv[1]=='merge':
        merge()
