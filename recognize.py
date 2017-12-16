#-*- encoding:utf-8 -*-
import numpy as np
import cv2
from PIL import Image
from sklearn.externals import joblib
from PIL import Image
import cv2
import pandas as pd
class captcha():
    def __init__(self,captcha):
        self.model="train_model2.m"
        self.captcha=captcha
    def getPoint(self,x,y,data,subdata=None):
        a=[0,-1,0,1,0,-2,0,2,0,-3,0,3,0,-4,0,4,0,-5,0,5]
        b=[1,0,-1,0,2,0,-2,0,3,0,-3,0,4,0,-4,0,5,0,-5,0]
        width,height=data.shape
        if subdata is None:
            subdata=[]
        if x>5 and y<height-5 and y>5 and x<width-5:
            for i in range(20):
                if data[x+a[i]][y+b[i]]==1:
                    subdata.append((x+a[i],y+b[i]))
                    data[x+a[i]][y+b[i]]=2
                    self.getPoint(x+a[i],y+b[i],data,subdata)
        subdata.append((x,y))

    def getcell(self,data):
        list1=[]
        index=0
        flag=True
        for y in range(data.shape[1]):
            for x in range(data.shape[0]):
                if data[x][y]==1:
                    if list1:
                        for i in range(len(list1)):
                            if (x,y) in list1[i]:
                                flag=False
                    if not flag:
                        continue
                    list1.append([])
                    self.getPoint(x,y,data,list1[index])#调用流水算法
                    index+=1
                else :
                    continue
        allimg=[]
        for index in range(len(list1)):
            l=list1[index][0][0]
            t=list1[index][0][1]
            r=list1[index][0][0]
            b=list1[index][0][1]
            for i in list1[index]:
                x=i[0]
                y=i[1]
                l=min(l,x)
                t=min(t,y)
                r=max(r,x)
                b=max(b,y)
            w=r-l+1
            h=b-t+1
            if (w*h <8):#去除小色块
                continue
            img0=np.zeros([w,h])#创建全0矩阵
            for x,y in list1[index]:
                img0[x-l][y-t]=1
            img0[img0<1]=255
            img1=Image.fromarray(img0)
            img1=img1.convert('RGB')
            allimg.append(img1)
        return allimg
    def readimg(self,imgfile):
        img=cv2.imread(imgfile,2)
        data=np.array(img)
        data[data<235]=1
        data[data>235]=255
        return data
    def recognize(self,allimg):
        clf = joblib.load(self.model)
        a=[]
        for img in allimg:
            img=img.resize((30,30))
            img.save('1.png')
            img=cv2.imread('1.png',2)
            data=img.flatten()
            data[data>1]=0
            a.append(data)
        data=pd.DataFrame(a)
        captcha=clf.predict(data)
        return ''.join(captcha)
    def main(self):
        data = self.readimg(self.captcha)#'captcha1.png'
        allimg=self.getcell(data)
        print self.recognize(allimg)
if __name__=="__main__":
    cap=captcha('test1.png')
    cap.main()
