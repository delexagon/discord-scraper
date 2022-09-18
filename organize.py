#!/bin/python3

from datetime import datetime
import json
import os

def read_file(filename, alldata, timestrs):
    file = open(filename)
    data = json.load(file)
    [(alldata.append(item), timestrs.add(item['timestamp'])) for item in data if item['timestamp'] not in timestrs]
        
def get_timestamp(datum):
    timestr = datum['timestamp']
    strs = timestr.split('+')
    if strs[1] != '00:00':
        print(stderr, "failure: " + strs[1])
    try:
        return datetime.strptime(strs[0], '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return datetime.strptime(strs[0], '%Y-%m-%dT%H:%M:%S')

def sort_all(alldata):
    alldata.sort(key = get_timestamp)
    
def print_data(datum):
    print(datum['author']['username'] + " " + datum['id'] + ', ' + datum['timestamp'])
    print('>>> ' + datum['content'].replace('\n', '\n>>> '))
    a = False
    if datum['edited_timestamp'] != None:
        print('edited', end=' ')
        a = True
    if len(datum['attachments']) != 0:
        print('attachment', end=' ')
        a = True
    if len(datum['embeds']) != 0:
        print('embed', end=' ')
        a = True
    if 'referenced_message' in datum:
        try:
            print('reply to: ' + datum['referenced_message']['id'], end=' ')
        except TypeError:
            print('reply to: ' + datum['message_reference']['message_id'], end=' ')
        a = True
    if datum['type'] != 0:
        print('type: ' + str(datum['type']), end=' ')
        a = True
    if a:
        print()
    print()

alldatums = []
timestrs = {'sjjsiw'}
files = ['individual/'+f for f in os.listdir('individual') if os.path.isfile('individual/'+f)]
for f in files:
    if f[-1] == "2":
        read_file(f, alldatums, timestrs)
        
sort_all(alldatums)

for i in alldatums:
    print_data(i)
