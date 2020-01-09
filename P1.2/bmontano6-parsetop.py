#!/usr/bin/env python
import csv
f50 = open('bmontano6-top-50.txt', 'w')
fht = open('bmontano6-top-1ht.txt', 'w')
htcount=0
fcount=0

with open('top-1m.csv', 'rb') as csvfile:
    for row in csvfile.readlines():
        if htcount < 100000:
            array = row.split(',')
            first_item=array[1]
            fht.write(first_item)
            htcount+=1
        if fcount < 50:
            f50.write(first_item)
            fcount+=1
