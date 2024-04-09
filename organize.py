#!/bin/python3

from localutils.misc import once
from datetime import datetime
import json
import sys
import os
import textwrap
import itertools

def name(datum):
    author = datum['author']
    if author['global_name'] != None :
        return author['global_name']
    return author['username']

def read_file(str_, alldata):
    try:
        data = json.loads(str_)
    except:
        print('hello', file=sys.stderr)
        print(str_, file=sys.stderr)
        raise ValueError
    for item in data:
        item['timestamp'] = datetime.fromisoformat(item['timestamp'])
        if int(item['id']) not in alldata:
            alldata[int(item['id'])] = item
    
def print_data(datum, last_user, all):
    repeat_user = True
    if datum['author']['username'] != last_user:
        print(f"\n{name(datum)} ({datum['author']['username']})")
        repeat_user = False
        last_user = datum['author']['username']
    wrap = []
    for line in datum['content'].splitlines():
        lines = textwrap.wrap(line, 50, replace_whitespace=False)
        if len(lines) > 0:
            lines[0] = (lines[0],)
        else:
            print("<no message text>")
        wrap.extend(lines)
    
    metadata = []
    if 'referenced_message' in datum:
        id_ = None
        try:
            id_ = int(datum['referenced_message']['id'])
        except TypeError:
            id_ = int(datum['message_reference']['message_id'])
        if id_ in all:
            old_msg = all[id_]
            p = name(old_msg)[:10] + ': ' + old_msg['content'][:15].replace('\n',' ')+'...'
        else:
            p = 'reply unknown'
        metadata.append(p)
    metadata.append(datetime.strftime(datum['timestamp'], '%d/%m/%Y, %H:%M UTC'))
    if datum['edited_timestamp'] != None:
        metadata.append('edited')
    if len(datum['attachments']) != 0:
        metadata.append('attachment')
    if len(datum['embeds']) != 0:
        metadata.append('embed')
    if 'reactions' in datum:
        reactions = [(reaction['emoji']['name'], reaction['count']) for reaction in datum['reactions']]
    else:
        reactions = None
    
        
    str_ = ''
    for line, md in itertools.zip_longest(wrap, metadata, fillvalue=''):
        if type(line) == tuple:
            str_ += f">>> {line[0].ljust(51)} {md}\n"
        else:
            str_ += f"    {line.ljust(51)} {md}\n"
    
    print(str_,end='')
    if reactions != None:
        for reaction in reactions:
            print(reaction[0]+str(reaction[1])+' ', end='')
        print()
    return last_user

def cut_line(line):
    line = line[21:-4]
    return line.replace('\\\"', '\"').replace('\\\\', '\\')

if __name__ == '__main__':
    har = sys.argv[1]
    alldatums = {}
    with open(har) as f:
        for line in f:
            if 'global_name' in line:
                line = cut_line(line)
                if line != None and line.startswith('['):
                    read_file(line, alldatums)
                
    datum_list = list(alldatums.values())
    datum_list.sort(key = lambda x: x['timestamp'])
    
    last_user = None
    for i in datum_list:
        last_user = print_data(i, last_user, alldatums)
