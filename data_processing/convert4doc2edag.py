import argparse
import re
import os
import json
import uuid
import random
import jsonlines

from tqdm import tqdm
from typing import List, Optional, Dict, Union

event_schema = {
    "Experiment":["Subject", "Equipment", "Date", "Location"],
    "Manoeuvre":["Subject", "Date","Area", "Content"],
    "Deploy":["Subject", "Militaryforce", "Date", "Location"],
    "Support":["Subject", "Object", "Materials", "Date"],
    "Accident":["Subject", "Date", "Location", "Result"],
    "Exhibit":["Subject", "Equipment", "Date", "Location"],
    "Conflict":["Subject", "Object", "Date", "Location"],
    "Injure":["Subject", "Quantity", "Date", "Location"],
}

def default_load_json(json_file_path, encoding='utf-8', **kwargs):
    with open(json_file_path, 'r', encoding=encoding) as fin:
        tmp_json = json.load(fin, **kwargs)
    return tmp_json

def split_text(text):
    result_list = re.split(r'。', text)
    sent_list = []
    sent_len = []
    len_sum = 0
    for i in range(len(result_list)):
        if i > 0:
            len_sum = len_sum + len(result_list[i-1])+1
        sent_list.append(result_list[i])
        sent_len.append(len_sum)
        # len_sum = len_sum + len(result_list[i])
    return sent_list, sent_len

def old_offset2new_offset(old_offset, sent_len, sent, arg_text):
    char_raw_start = old_offset[0]
    char_raw_end = old_offset[1]
    if char_raw_start < sent_len[-1]:  
        for i in range(len(sent_len)):
            if char_raw_start >= sent_len[i] and char_raw_end<sent_len[i+1]:
                char_new_start = char_raw_start - sent_len[i]
                char_new_end = char_raw_end - sent_len[i]
                try:
                    assert sent[i][char_new_start:char_new_end] == arg_text
                except:
                    print("{}error1".format(sent))
                new_offset = [i, char_new_start, char_new_end]
                break
            else:
                new_offset = None
    else:
        char_new_start = char_raw_start - sent_len[-1]
        char_new_end = char_raw_end - sent_len[-1]
        try:
            assert sent[len(sent_len)-1][char_new_start:char_new_end] == arg_text
        except:
            print("{}error2".format(sent))
        new_offset = [len(sent_len)-1, char_new_start, char_new_end]

    return new_offset

def coref_arg2ann_dranges(coref_arg, sent_len, sent):
    ann_valid_dranges = []
    coref_arg_num = 0
    coref_text_list = []
    for coref_arg_list in coref_arg:
        for coref_list in coref_arg_list:
            coref_text = coref_list["text"]
            coref_text_list.append(coref_text)
    coref_text_set = list(set(coref_text_list))
    coref2drange = dict([(key, []) for key in coref_text_set])
    for coref_arg_list in coref_arg:
        for coref_list in coref_arg_list:
            coref_arg_num += 1
            oldoffset = coref_list["offset"]
            coref_text = coref_list["text"]
            if oldoffset[0] < sent_len[-1]:
                for i in range(len(sent_len)):
                    if oldoffset[0]>sent_len[i] and oldoffset[1]<sent_len[i+1]:
                        char_new_start = oldoffset[0] - sent_len[i]
                        char_new_end = oldoffset[1] - sent_len[i]
                        newoffset = [i, char_new_start, char_new_end]
                        try:
                            assert sent[i][char_new_start:char_new_end]==coref_text
                        except:
                            print("{}error3".format(sent))
                        ann_valid_dranges.append(newoffset)
                        coref2drange[coref_text].append(newoffset)
            else:
                char_new_start = oldoffset[0] - sent_len[-1]
                char_new_end = oldoffset[1] - sent_len[-1]
                newoffset = [len(sent_len)-1, char_new_start, char_new_end]
                try:
                    assert sent[len(sent_len)-1][char_new_start:char_new_end] == coref_text
                except:
                    print("{}error4,{}".format(sent,coref_text))
                ann_valid_dranges.append(newoffset)
                coref2drange[coref_text].append(newoffset)
    # print(coref_arg_num)
    # print(len(ann_valid_dranges))
    return ann_valid_dranges, coref2drange

def convert_cmnee_to_unified(data_path: str,
                            save_path: str,
                            dump: Optional[bool] = True) -> List[List[Dict]]:

    fndee_data = default_load_json(data_path)

    formatted_data = []
    # error_annotations = []
    delect_arg = 0
    data_num = 0
    non_event_num = 0

    for sent_id, sent in enumerate(tqdm(fndee_data)):
        data_num += 1
        instance = []

        instance.append(sent["id"])
        instance.append(dict())
        sents, sent_len = split_text(sent["text"])#add_real_sent_info
        instance[1]["sentences"] = sents
        coref_arg = sent["coref_arguments"]
        instance[1]["ann_valid_mspans"] = []
        instance[1]["ann_valid_dranges"], corefarg2drange = coref_arg2ann_dranges(coref_arg, sent_len, sents)
        coref_arg_text = list(corefarg2drange.keys())
        instance[1]["ann_mspan2dranges"] = {}
        instance[1]["ann_mspan2guess_field"] = {}
        instance[1]["recguid_eventname_eventdict_list"] = []

        if len(sent["event_list"])>0:
            event_id = 0
            for event in sent["event_list"]:
                event_type = event["event_type"]
                role_list = event_schema[event_type]
                role2arg = dict([(k, None) for k in role_list])
                event_info = [event_id, event_type, role2arg]
                instance[1]["recguid_eventname_eventdict_list"].append(event_info)
                multi_arg_i = 0
                role2multi_arg = dict([(k, []) for k in role_list])
                for arg in event["arguments"]:
                    role = arg["role"]
                    arg_text = arg["text"]
                    arg_start = arg["offset"][0]
                    arg_end = arg["offset"][1]
                    oldoffset = [arg_start, arg_end]
                    dranges = old_offset2new_offset(oldoffset, sent_len, sents, arg_text)
                    if dranges is not None:
                        # break
                        instance[1]["ann_valid_mspans"].append(arg_text)
                        #add coref_argument_info
                        if arg_text in coref_arg_text:
                            # try:
                            #     assert dranges in corefarg2drange[arg_text]
                            # except:
                            #     print("{}error".format(instance[0]))
                            if dranges in corefarg2drange[arg_text]:
                                instance[1]["ann_mspan2dranges"][arg_text] = corefarg2drange[arg_text]
                            else:
                                instance[1]["ann_mspan2dranges"][arg_text] = corefarg2drange[arg_text]+[dranges]
                        else:
                            instance[1]["ann_mspan2dranges"][arg_text] = [dranges]
                        instance[1]["ann_mspan2guess_field"][arg_text] = role

                        if role2arg[role] is None:
                            instance[1]["recguid_eventname_eventdict_list"][event_id][2][role] = arg_text
                        else:
                            instance[1]["recguid_eventname_eventdict_list"].append([event_id+1,event_type, {}])
                            instance[1]["recguid_eventname_eventdict_list"][event_id+1][2] = instance[1]["recguid_eventname_eventdict_list"][event_id][2].copy()
                            instance[1]["recguid_eventname_eventdict_list"][event_id+1][2][role] = arg_text
                            event_id += 1
                    else:
                        delect_arg += 1
                event_id += 1

            formatted_data.append(instance)
        else:
            non_event_num += 1

    print("We get {}/{} instances for [{}].".format(len(formatted_data), len(fndee_data), data_path))
    print("non-event num is {}".format(non_event_num))
    print("delect_arg{}".format(delect_arg))
    print("datanum is {}".format(data_num))

    if dump:
        save_name = data_path.split("/")[-1].replace(".json", ".unified.jsonl")

        with open(os.path.join(save_path, save_name), 'w', encoding='utf-8') as f:
            f.write(json.dumps(formatted_data, ensure_ascii=False, indent =4) + "\n")

    return formatted_data


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="CMNEE")
    arg_parser.add_argument("--data_dir", type=str, default="../dataset/cmnee")
    arg_parser.add_argument("--save_dir", type=str, default="../dataset/cmnee_doc2edag")
    args = arg_parser.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "sample.json"), args.save_dir)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "train.json"), args.save_dir)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "valid.json"), args.save_dir)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "test.json"), args.save_dir)