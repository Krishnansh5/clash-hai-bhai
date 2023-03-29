from configparser import LegacyInterpolation
from datetime import date
import json
from operator import le
from time import time
import copy
#  print(len(dict))
# print(dict.keys())
def prettify_lec(i : int, dept : str):
    filename = "output.json"
    f = open(filename, 'r')
    dict = json.load(f)
    if  dict[dept][i]['tut'] != "None":
        time_string = dict[dept][i]['lec'] + ' '  +dict[dept][i]['tut']
    else:
        time_string = dict[dept][i]['lec']
    # print(time_string)
    lst = list(time_string)
    for i in lst:
        if i == '\n':
            lst.pop(lst.index(i))
        elif i == ',':
            lst.pop(lst.index(i))
        elif i in ['M','T', 'W', 'Th', 'F']:
            lst[lst.index(i)] = ' {} '.format(i)
        elif i == 'h':
            lst[lst.index(i) - 1] = ' Th '
            lst.pop(lst.index(i)) 
    strung = "".join(lst)
    strung_ =strung.split(' ')
    final = []
    for i in strung_:
        if i == '':
            continue
        elif len(i) == len('T09:00-10:00'):
            final.append(i[0])
            final.append(i[1:])
        else:
            final.append(i)
    
    for i in final:
        if len(i) == len('09:00-10:00'):
            final[final.index(i)] = i.split("-")

    for i in final:
        if len(i) == 2 and type(i) == list:
            final[final.index(i)] = ["".join(z.split(":")) for z in i]

    return final


def get_dict(i : int, dept : str):
    timestring = prettify_lec(i, dept)
    if (timestring == ['None']):
        return {}
    dates_indices = []
    # if (i == 7):
    #     print(timestring)
    for i in range(len(timestring)):
        if (len(timestring[i]) != 1):
        
            if (type(timestring[i]) != str):
                dates_indices.append(i)
        
    # print(dates_indices)
    dates_dict = {}
    for i in range(len(timestring)):
        # print(i)
        if i not in dates_indices:
            ind = next_date(i, dates_indices)
            # print(ind)
            try:
                dates_dict[timestring[i]] = timestring[dates_indices[ind]]
            except:
                print(timestring)
    
    return dates_dict
        
def next_date(i : int, dates_indices):
    for ctr in range(len(dates_indices)):
        if dates_indices[ctr] > i:
            return ctr

def get_fixed_json(path):
    filename = "output.json"
    f = open(filename, 'r')
    dict = json.load(f)
    new_dict = {}
    for dept in dict:
        new_dict[dept] = dict[dept]
        for i in range(len(dict[dept])):
            new_dict[dept][i]["timings"] = get_dict(i, dept)
    outfile = path
    f_o = open(outfile, "w")
    json.dump(new_dict, f_o)

epoch_dict = {
        "M" : 0,
        "T" : 1,
        "W" : 2,
        "Th" : 3,
        "F" : 4
    }
def return_since_epoch(time : str, day : str):
    time_int = int(time)
    return str(time_int + epoch_dict[day]*2400)

# def add_epoch_key(path):
#     for i in dict["courses"]:
#         timings = i["timings"]
#         timings_list = []
#         for day in timings:
#             start, stop = timings[day][0], timings[day][1]
#             if day in epoch_dict:
#                 timings_list.append([return_since_epoch(start, day), return_since_epoch(stop, day)])
#         print(timings_list)
#         i["timings_since_epoch"] = timings_list
#     filename = path
#     f = open(filename, 'w')
#     json.dump(dict, f)
#     f.close()

def add_epoch_key(filename):
    filename = filename
    f = open(filename, 'r')
    dict = json.load(f)
    f.close()
    
    for dept in dict:
        for i in range(len(dict[dept])):
            timings = dict[dept][i]["timings"]
            timings_list = []
            for day in timings:
                start, stop = timings[day][0], timings[day][1]
                if day in epoch_dict:
                    timings_list.append([return_since_epoch(start, day), return_since_epoch(stop, day)])
            # print(timings_list)
            dict[dept][i]["timings_since_epoch"] = timings_list
        f = open(filename, 'w')
        json.dump(dict, f)
        f.close()

