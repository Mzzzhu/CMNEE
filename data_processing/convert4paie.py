from os import path
import os
import re
import json
import uuid
import random
import argparse
import numpy as np
from tqdm import tqdm
from typing import List, Optional, Dict, Union

random.seed(42)

convert2chinese = {
    "Experiment": "试验",
    "Manoeuvre": "演习",
    "Deploy": "部署",
    "Support": "支援",
    "Accident": "意外事故",
    "Exhibit": "展示",
    "Conflict": "冲突",
    "Injure": "伤亡",
    "Subject": "主体",
    "Equipment": "装备",
    "Date": "时间",
    "Location": "地点",
    "Area": "区域",
    "Content": "演习内容",
    "Militaryforce": "军事力量",
    "Object": "客体",
    "Materials": "物资",
    "Result": "事故后果",
    "Quantity": "数量",
}

def default_load_json(json_file_path, encoding='utf-8', **kwargs):
    with open(json_file_path, 'r', encoding=encoding) as fin:
        tmp_json = json.load(fin, **kwargs)
    return tmp_json

def split_chinese_string(sentence):
    result = []
    for char in sentence:
        if '\u4e00' <= char <= '\u9fff':
            result.extend(list(char))
        else:
            result.append(char)
    return result

def fetch_word(ipt):
    lst = []
    offset = 0
    text = ipt.lower()
    offset_add = [0]
    space_flag_list = []
    while len(text) > 0:
        match = re.match(r'[a-z]+', text)
        match2 = re.match(r'[0-9]+', text)
        match3 = re.match(r'�+', text)
        match5 = re.match(r'\u200b+', text)
        match4 = re.match(r'\s+', text)
        match6 = re.match(r'\\x+', text)
        if match:
            word = match.group(0)
            offset += len(word)
            offset_add.append(offset)
            lst.append(word)
            space_flag_list.append(0)
        elif match2:
            word = match2.group(0)
            offset += len(word)
            offset_add.append(offset)
            lst.append(word)
            space_flag_list.append(0)
        elif match4:
            word = match4.group(0)
            for i in range(len(word)):
                offset += 1
                offset_add.append(offset)
                lst.append(word[i])
                space_flag_list.append(1)
        elif match3:
            word = match3.group(0)
            for i in range(len(word)):
                offset += 1
                offset_add.append(offset)
                lst.append(word[i])
                space_flag_list.append(1)
        elif match5:
            word = match5.group(0)
            for i in range(len(word)):
                offset += 1
                offset_add.append(offset)
                lst.append(word[i])
                space_flag_list.append(1)
        elif match6:
            word = match6.group(0)
            for i in range(len(word)):
                offset += 1
                offset_add.append(offset)
                lst.append(word[i])
                space_flag_list.append(1)
        else:
            word = text[0:1]
            offset += 1
            offset_add.append(offset)
            lst.append(word)
            space_flag_list.append(0)
        text = text.replace(word, '', 1)
    return lst, offset_add, space_flag_list

def fetch_word_clean(ipt):
    lst = []
    s = ipt.lower()
    while len(s) > 0:
        match = re.match(r'[a-z]+', s)
        match2 = re.match(r'[0-9]+', s)
        if match:
            word = match.group(0)
        elif match2:
            word = match2.group(0)
        else:
            word = s[0:1]
        lst.append(word)
        s = s.replace(word, '', 1).strip(' ')
    return lst

def convert_offset(raw_s, raw_e, offset_add, space_flag_list,delete_flag):
    new_s = offset_add.index(raw_s)
    new_e = offset_add.index(raw_e)
    f_s = new_s - sum(space_flag_list[:new_s]) - sum(delete_flag[:new_s])
    f_e = new_e - sum(space_flag_list[:new_e]) - sum(delete_flag[:new_e])
    return f_s,f_e

def delete_xtoken(mys):
    sl = mys
    i = 0
    delete_list = []
    delete_flag = []
    while i < len(sl):
        s = sl[i]
        try:
            s = s.encode('raw_unicode_escape').decode('utf-8')
            i += 1
            delete_flag.append(0)
        except:
            sl.remove(s)
            delete_list.append(i)
            delete_flag.append(1)
    new_sl = []
    for i in range(len(sl)):
        if len(delete_list)>0:
            if i<delete_list[0] or i >len(delete_list):
                new_sl.append(sl[i])
                delete_flag.append(0)
        else:
            new_sl.append(sl[i])
    return new_sl, delete_list, delete_flag

def split_text(text):
    result_list = re.split(r'。', text.strip())

    sent_list = []
    for i in range(len(result_list) - 1):
        if result_list[i] is not None:
            sent_list.append((i, result_list[i]))
    return sent_list

def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or abs(value - array[idx-1]) < abs(value - array[idx])):
        return array[idx-1]
    else:
        return array[idx]


def convert_cmnee_to_unified(data_path: str,
                            save_path: str,
                            dump: Optional[bool] = True) -> List[Dict[str, Union[str, List[Dict]]]]:

    lines = default_load_json(data_path)

    formatted_data = []

    error_split_num = 0
    for line in lines:
        events = line["event_list"]
        coref_arguments = line["coref_arguments"]
        if not events:
            continue
        doc_key = line["id"]
        raw_text = line["text"]

        s = re.sub(r'\\u.{4}', '�', raw_text.__repr__())
        text = eval(s)
        full_text_raw = split_chinese_string(text)
        full_text_2, offset_add, space_flag_list = fetch_word(text)
        text_clean0 = text.replace(" ", "").replace("\u3000", '').replace("\u200b", '').replace('�', '')
        text_clean, delete_list, delete_flag = delete_xtoken(list(text_clean0))
        mys = ''.join(text_clean)
        full_text = fetch_word_clean(mys)
        sentences = split_text(mys)

        if len(full_text)+sum(space_flag_list)+sum(delete_flag) == len(full_text_2):
            instance = dict()
            instance["id"] = doc_key
            instance["text"] = raw_text
            instance["full_text"] = full_text
            instance["event_list"] = []
            for event_id, event in enumerate(events):
                instance["event_list"].append({})
                event_type = convert2chinese[event['event_type']]
                instance["event_list"][event_id]["event_type"] = event_type
                event_trigger = {}

                raw_s = event['trigger']["offset"][0]
                raw_e = event['trigger']["offset"][1]
                event_trigger_start, event_trigger_end = convert_offset(raw_s,raw_e,offset_add,space_flag_list,delete_flag)
                event_trigger["text"] = event['trigger']["text"]
                event_trigger["offset"] = [event_trigger_start, event_trigger_end]
                instance["event_list"][event_id]["trigger"] = event_trigger
                try:
                    event_trigger["text"] == "".join(full_text[index] for index in range(event_trigger_start, event_trigger_end))
                except:
                    print("{}error, trigger is {}".format(text, event_trigger["text"]))

                event_args = list()
                for arg_info in event['arguments']:
                    evt_arg = dict()

                    if arg_info['offset'][0] in offset_add and arg_info['offset'][1] in offset_add:
                        raw_arg_s = arg_info['offset'][0]
                        raw_arg_e = arg_info['offset'][1]
                        evt_arg_start, evt_arg_end = convert_offset(raw_arg_s,raw_arg_e,offset_add,space_flag_list,delete_flag)
                        evt_arg['role'] = convert2chinese[arg_info['role']]
                        evt_arg['text'] = arg_info['text']
                        evt_arg["offset"] = [evt_arg_start, evt_arg_end]
                        event_args.append(evt_arg)
                        instance["event_list"][event_id]["arguments"] = event_args
                        try:
                            evt_arg['text'] == "".join(full_text[index] for index in range(evt_arg_start,evt_arg_end))
                        except:
                            print("{}error, arg is {}".format(text, evt_arg["text"]))
                    else:
                        print("Invalid arg {}!".format(arg_info))


            instance["coref_arguments"] = []
            for coref_arg_info in coref_arguments:
                coref_list = list()

                for coref_arg_s in coref_arg_info:
                    coref_arg = dict()
                    if coref_arg_s['offset'][0] in offset_add and coref_arg_s['offset'][1] in offset_add:
                        raw_coref_arg_s = coref_arg_s['offset'][0]
                        raw_coref_arg_e = coref_arg_s['offset'][1]
                        coref_arg_start, coref_arg_end = convert_offset(raw_coref_arg_s,raw_coref_arg_e,offset_add,space_flag_list,delete_flag)
                        coref_arg['text'] = coref_arg_s['text']
                        coref_arg["offset"] = [coref_arg_start, coref_arg_end]
                        coref_list.append(coref_arg)

                        try:
                            full_text[coref_arg_start:coref_arg_end] == full_text_raw[raw_coref_arg_s:raw_coref_arg_e]
                        except:
                            print("{}error, coref_arg is {}".format(text, coref_arg["text"]))
                    else:
                        print("Invalid coref_arg {}!".format(coref_arg_s))
                instance["coref_arguments"].append(coref_list)
            formatted_data.append(instance)
        else:
            error_split_num += 1
            # print("{} split error!".format(text))

    print("We get {}/{} instances for [{}].".format(len(formatted_data), len(lines), data_path))

    if dump:
        save_name = data_path.split("/")[-1].replace(".json", ".unified.jsonl")
        with open(os.path.join(save_path, save_name), 'w', encoding='utf-8') as f:
            for item in formatted_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return formatted_data



if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="CMNEE")
    arg_parser.add_argument("--data_dir", type=str, default="../dataset/cmnee")
    arg_parser.add_argument("--save_dir", type=str, default="../dataset/cmnee_paie")
    args = arg_parser.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "sample.json"), args.save_dir)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "train.json"), args.save_dir)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "valid.json"), args.save_dir)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "test.json"), args.save_dir)

