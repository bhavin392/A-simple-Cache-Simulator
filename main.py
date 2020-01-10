import tkinter as tk
from tkinter import filedialog
import numpy as np
import sys
import os
import math
def hitOrMiss(addr):
    storeAddr= addr # store the address into the local variable
    offset=int(math.log(blockSize, 2)) # calculating offset
    indexValue = int(math.log(cacheSize / (associativity * blockSize), 2))  # calculating index
    # addrLength = np.uint32(storeAddr) # converting address length to 32

    addrLength=32
    tag = addrLength - offset - indexValue # getting tag value 
    flag1 = int(('1' * tag + '0' * indexValue + '0' * offset), 2)# select tag value and make 0 for index and offset  
    tag = (storeAddr & flag1) >> (indexValue + offset)  # shif the tag
    flag2 = int(('0' * indexValue + '1' * indexValue+ '0' * offset), 2)# select index value and make 0 for tag and offset
    index = (storeAddr & flag2) >> (offset)  # shift the index

    if associativity==1: # check for associativity if 1 direct mapping
        if tag == cacheArray[index]:
            return 1;# if equal return  1 that means set so compare tag
        else:
            cacheArray[index]= tag # assign tag
            return 0;
    else: # 4 way set
        if tag in cacheArray[index]: # if tag value is in cache array
            store = cacheArray[index].index(tag)# store into a temporary variable
            lruArray[index][store] = max(lruArray[index]) + 1 # give the maximum value 
            return 1
        else:
            if 0 in cacheArray[index]: # if cache array is empty assign a tag value
                store = cacheArray[index].index(0) # assign a tag value
                cacheArray[index][store]= tag
                lruArray[index][store] = max(lruArray[index]) + 1 # give the maximum value 
            else: #if not empty get the least recently used index and replace it 
                lru = min(lruArray[index])  # get least recently used index
                temp1 = lruArray[index].index(lru) # store into temporary variable
                cacheArray[index][temp1] = tag # assign new tag
                lruArray[index][temp1] = max(lruArray[index]) + 1 # give maximum value
            return 0
def combinedCache(unified):
    hits = 0;# initialize hit and miss
    miss = 0;

    for addr in unified:
        if hitOrMiss(addr) is 1:  # call a function for hit or miss

            hits += 1  # increment hits
        else:

            miss = miss + 1  # increment misses
    return hits, miss

def InstructionCache(inst):
   
    misses = 0
    hits = 0
    for addr in inst:
        if hitOrMiss(addr) is 1:  # call a function for hit or miss
            hits += 1  # increment hits
        else:
            misses = misses + 1  # increment misses
    return hits, misses
  
def DataCache(dataAdr):
    misses = 0
    hits = 0
    for addr in dataAdr:
        if hitOrMiss(addr) is 1:  # call a function for hit or miss
            hits += 1  # increment hits
        else:
            misses = misses + 1  # increment misses
    return hits, misses
root= tk.Tk()
root.withdraw()
filepath =filedialog.askopenfilename(filetypes = (("trace files","*.din"),("out files",".out")))
file=open(filepath)
file_path = file.name
ext= os.path.splitext(file_path)
print(ext[1])
readData=file.readlines()
print("Enter the inputs in following order: cache size only integer(no kb),block size, associativity, cache type=1 for combined and 0 for split")
print("for example: python main.py 32 8 1 0")
cacheSize= int(sys.argv[1]) #multiply by 1024 to convert into KB
cacheSize = cacheSize*1024
blockSize = int(sys.argv[2]) #For block size
associativity= int(sys.argv[3]) #for associativity
cacheType= int(sys.argv[4]) #for cache type 1 for combined and 0 for split

 
# read line and split data and other intialization
cacheArray = [[0] * associativity] * int(cacheSize / (blockSize * associativity))  #declaring list for cache array 
lruArray = [[0] * associativity] * int(cacheSize / (blockSize * associativity))  # declaring list for lru
instr=[] # declaring list for seperate instruction and data cache
data=[]
combined=[] # declaring list for combined cache
count= 0; # intializing count to limit the iterations # can be commented to see full data
def switch(i):
    switcher={
    0:data.append(addr),
    1:data.append(addr),
    2:instr.append(addr)
    }
    return switcher.get(i,combined.append(addr))


for read in readData:
    split = read.split(' ')
    
   
    if ext[1] ==".din":
        label = int(split[0], 10) 
        addr = int(split[1], 16) # convert hexadecimal to decimal
        switch(label)
        
            
    else:
        addr = int(data[2], 16)
        data.append(addr)
        if count == 4000000:  # limiting the iteration to 4 million as mentioned in the question
            break
if (ext[1]==".din"):
    if cacheType == 0:
        hitsinstr,missesinstr=  InstructionCache(instr)
        print("Number of Instruction fetches "+ str(len(instr)))
        print("Number of instrHits " + str(hitsinstr))
        print("Number of instrMisses " + str(missesinstr))
        hitsdata,missesdata= DataCache(data)
        print("Number of Data Fetches"+str(len(data)))
        print("Number of dataHits " + str(hitsdata))
        print("Number of dataMisses " + str(missesdata))
    else :
        hits,misses=  combinedCache(combined)
        print("Number of fetches"+str(len(combined)))
        print("Number of Hits " + str(hits))
        print("Number of Misses " + str(misses))



