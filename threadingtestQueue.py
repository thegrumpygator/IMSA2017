# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 17:18:01 2018

@author: brian
"""
import pandas as pd
from os import listdir
from os.path import isfile, join
import datetime

from queue import Queue
from threading import Thread

class doitWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        while True:
            file = self.queue.get()
            DoIt(file)
            self.queue.task_done()

#Function to fix the time (string)
def fixTime(df):
    '''This function takes the dataframe as an argument and 
    converts the string Lap Time column to be a datetime
    and then converts the datetime column to be a float.
    The function then returns the dataframe with those two
    columns appended to the right'''
    
    # TODO: Check to make sure that the 'Lap Time' column
    #       exists.
    # TODO: Check to make sure that the 'Lap Time' column
    #       is the right format
    
    df = df.assign(dtLapTime = pd.to_datetime('0:0:' + df['Lap Time'] + '0',
                                             exact = False, errors = 'ignore',
                                             format = "%H:%M:%S.%f").apply(lambda x: x.time()))
    df = df.assign(fLapTime = df.dtLapTime.apply(lambda x: ((x.hour * 60 + x.minute) * 60 + x.second) * 1000000 + x.microsecond) / 1000000)
    return df

def readIMSAFile(filename):
    df = pd.read_csv(filename)
    return fixTime(df)

def getFileList(mypath):
    return [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]


def getRowWithFastLap(df):
    return df.loc[df['fLapTime'].idxmin()]

def DoIt(mySingleFile):
    colsToKeep = ['Car', 'Class', 'Driver', 'Lap', 'dtLapTime', 'fLapTime']
    a = readIMSAFile(mySingleFile)[colsToKeep]
    b = getRowWithFastLap(a)
    b.loc['file'] = mySingleFile
    

## Main
def main():
    t0 = datetime.datetime.now()
    myFilesPath = "C:\\Users\\gator\\Documents\\GitHub\\IMSA2017\\LapData\\2018"
    for file in getFileList(myFilesPath):
        c.append(DoIt(file))
    pd.DataFrame(c).to_csv('test.csv')
    print(datetime.datetime.now() - t0)
    
if __name__ == '__main__':
   main()