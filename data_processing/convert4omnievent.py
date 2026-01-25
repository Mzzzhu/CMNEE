import os
import re
import json
import uuid
import jieba
import random
import argparse
import jsonlines

from tqdm import tqdm
from typing import List, Optional, Dict, Union

random.seed(42)


def generate_label2id_role2id(data_path: str) -> None:
    """Allocates an id for event types and roles within the event schema.

    Allocates an id for event types and roles within the event schema. The id of event types and roles start from 0.
    Finally, the correspondence of each event type/role and their id are stored in a dictionary and dumped into json
    files, in which the key of each element is the event type/role, and the value is their corresponding id.

    Args:
        data_path (`str`):
            A string indicating the path of the `duee_event_schema.json` schema file.
    """
    label2id, role2id = dict(NA=0), dict(NA=0)

    schema = list(jsonlines.open(data_path))
    for i, s in enumerate(schema):
        label2id[s["event_type"]] = i + 1
        for role in s["role_list"]:
            if role["role"] not in role2id:
                role2id[role["role"]] = len(role2id)

    io_dir = '/data/processed'.join("/".join(data_path.split("/")[:-1]).split('/data/original'))
    with open(os.path.join(io_dir, "label2id.json"), "w", encoding="utf-8") as f:
        json.dump(label2id, f, indent=4, ensure_ascii=False)

    with open(os.path.join(io_dir, "role2id.json"), "w", encoding="utf-8") as f:
        json.dump(role2id, f, indent=4, ensure_ascii=False)


def chinese_tokenizer(input_text: str,
                      tokenizer: Optional[str] = "jieba") -> List[str]:
    """Tokenizes the Chinese input sequence into tokens.

    Tokenizes the Chinese input sequence into tokens by calling the relevant packages. The function integrates four
    commonly-used tokenizers, including Jieba, LTP, THULAC, and HanLP. The tokenized tokens are stored as a list for
    return.

    Args:
        input_text (`str`):
            A string indicating the input text for tokenization.
        tokenizer (`str`, `optional`, defaults to "jieba"):
            A string indicating the tokenizer proposed to be utilized for the tokenization process, selected from
            "jieba", "ltp", "thulac", and "hanlp".

    Returns:
        token_list (`List[str]`):
            A list of strings representing the tokens within the given Chinese input sequence.
    """
    token_list = []
    if tokenizer == "jieba":
        token_list = jieba.lcut(input_text)

    # TODO: add other tokenizers
    if tokenizer == "ltp":
        raise NotImplementedError
    if tokenizer == "thulac":
        raise NotImplementedError
    if tokenizer == "hanlp":
        raise NotImplementedError

    return token_list


def re_tokenize(token_list: List[str],
                event: Dict) -> List[str]:
    trigger = event["trigger"]["text"]
    offset = event["trigger"]["offset"]

    start, brk1, brk2 = 0, -1, -1
    for i, t in enumerate(token_list):
        if brk1 == -1:
            if start <= offset[0] < start + len(t):
                brk1 = i
                if offset[1] <= start + len(t):
                    brk2 = i + 1
                    break
        else:
            if start <= offset[1] <= start + len(t):
                brk2 = i + 1
                break
        start += len(t)

    left = token_list[:brk1]
    middle = token_list[brk1:brk2]
    right = token_list[brk2:]

    middle_new = [token for token in re.split("(" + str(trigger) + ")", "".join(middle)) if token]

    return left + middle_new + right


def str_full_to_half(ustring: str) -> str:
    """Convert a full-width string to a half-width one.

    The corpus of some datasets contain full-width strings, which may bring about unexpected error for mapping the
    tokens to the original input sentence.

    Args:
        ustring(`str`):
            Original string.
    Returns:
        rstring (`str`):
            Output string with the full-width tokens converted
    """
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:   # full width space
            inside_code = 32
        elif 65281 <= inside_code <= 65374:    # full width char (exclude space)
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring

def default_load_json(json_file_path, encoding='utf-8', **kwargs):
    with open(json_file_path, 'r', encoding=encoding) as fin:
        tmp_json = json.load(fin, **kwargs)
    return tmp_json

def convert_cmnee_to_unified(data_path: str,
                            save_path: str,
                            dump: Optional[bool] = True,
                            tokenizer: Optional[str] = "jieba") -> List[Dict[str, Union[str, List[Dict]]]]:
    """Converts the DuEE 1.0 dataset to the unified format.

    Extracts the information from the original DuEE 1.0 dataset and convert the format to a unified OpenEE dataset. The
    tokens not annotated as triggers are also regarded as negative triggers. The converted dataset is written to a json
    file.

    Args:
        data_path (`str`):
            A string representing the path of the original DuEE 1.0 dataset.
        dump (`bool`, `optional`, defaults to `True`):
            A boolean variable indicating whether or not to write the manipulated dataset into a json file.
        tokenizer (`str`, `optional`, defaults to `jieba`):
            A string indicating the tokenizer proposed to be utilized for the tokenization process, selected from
            "jieba", "ltp", "thulac", and "hanlp".

    Returns:
        formatted_data (`List[Dict[str, Union[str, List[Dict]]]]`):
            A list of dictionary indicating the manipulated dataset of DuEE 1.0 after converting its format into a
            unified OpenEE dataset.
    """
    fndee_data = default_load_json(data_path)

    formatted_data = []
    # error_annotations = []

    for sent_id, sent in enumerate(tqdm(fndee_data)):
        instance = dict()

        instance["id"] = sent["id"]
        instance["text"] = sent["text"]

        # tokens = chinese_tokenizer(instance["text"], tokenizer)

        instance["events"] = list()
        instance["negative_triggers"] = list()
        events_in_sen = list()

        trigger_list = []
        for event in sent["event_list"]:
            event["argument"] = list()
            for arg in event["arguments"]:
                role = arg["role"]
                arg_start = arg["offset"][0]
                arg_end = arg["offset"][1]
                event["argument"].append({"id": str(uuid.UUID(int=random.getrandbits(128))).replace("-", ""),
                                          "role": role, "mentions": [
                        {"mention_id": str(uuid.UUID(int=random.getrandbits(128))).replace("-", ""),
                         "mention": arg["text"],
                         "position": [arg_start, arg_end]}]})
            events_in_sen.append(event)
            trigger_list.append(event["trigger"]["text"])
            # if event["trigger"]["text"] not in tokens:
            #     print("trigger not in tokens", event["trigger"]["text"])
            #     tokens = re_tokenize(tokens, event)

        for e in events_in_sen:
            event = dict()
            event["type"] = e["event_type"]
            event["triggers"] = []

            char_start = e["trigger"]["offset"][0]
            char_end = e["trigger"]["offset"][1]
            e["id"] = str(uuid.UUID(int=random.getrandbits(128))).replace("-", "")

            event["triggers"].append({
                "id": "{}-{}".format(instance["id"], e["id"]),
                "trigger_word": e["trigger"]["text"],
                "position": [char_start, char_end],
                "arguments": e["argument"]
            })

            # if e["trigger"]["text"] not in tokens:
            #     print("e[trigger][text]", e["trigger"]["text"])
            #     print("tokens",tokens)

            assert instance["text"][char_start:char_end] == e["trigger"]["text"]
            # assert e["trigger"]["text"] in tokens
            for arg in e["argument"]:
                for a in arg["mentions"]:
                    assert instance["text"][a["position"][0]: a["position"][1]] == a["mention"]

            instance["events"].append(event)

        # negative triggers
        start = 0
        tokens = chinese_tokenizer(instance["text"], tokenizer)
        for token in tokens:
            char_start = start
            char_end = char_start + len(token)
            start = char_end

            if token not in trigger_list:
                negative = token
                instance["negative_triggers"].append({
                    "id": "{}-{}".format(instance["id"], str(uuid.uuid4()).replace("-", "")),
                    "trigger_word": negative,
                    "position": [char_start, char_end]
                })
                assert instance["text"][char_start:char_end] == negative
        formatted_data.append(instance)

    print("We get {}/{} instances for [{}].".format(len(formatted_data), len(fndee_data), data_path))

    # Change full punctuations into half.
    for line in formatted_data:
        line["text"] = str_full_to_half(line["text"])
        if "events" in line.keys():
            for event in line["events"]:
                for trigger in event["triggers"]:
                    trigger["trigger_word"] = str_full_to_half(trigger["trigger_word"])
                    for argument in trigger["arguments"]:
                        for mention in argument["mentions"]:
                            mention["mention"] = str_full_to_half(mention["mention"])
            for trigger in line["negative_triggers"]:
                trigger["trigger_word"] = str_full_to_half(trigger["trigger_word"])
        else:
            for trigger in line["candidates"]:
                trigger["trigger_word"] = str_full_to_half(trigger["trigger_word"])

    if dump:
        save_name = data_path.split("/")[-1].replace(".json", ".unified.jsonl")
        with open(os.path.join(save_path, save_name), 'w', encoding='utf-8') as f:
            for item in formatted_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return formatted_data


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="CMNEE")
    arg_parser.add_argument("--data_dir", type=str, default="../dataset/cmnee")
    arg_parser.add_argument("--save_dir", type=str, default="../dataset/cmnee_omnievent")
    args = arg_parser.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "sample.json"), args.save_dir)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "train.json"), args.save_dir)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "valid.json"), args.save_dir)
    convert_cmnee_to_unified(os.path.join(args.data_dir, "test.json"), args.save_dir)
