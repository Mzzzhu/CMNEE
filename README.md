# CMNEE
Source code and dataset for LREC-COLING 2024 paper: "[**CMNEE: A Large-Scale Document-Level Event Extraction Dataset based on Open-Source Chinese Military News**](http://export.arxiv.org/abs/2404.12242)"
will be released.

CMNEE can be downloaded from https://drive.google.com/drive/folders/1nfKiSsu88oBeykUSYm7NGn4Q50_2GPS1?usp=sharing.

# Overview
CMNEE is a large-scale, document-level open-source Chinese Military News Event Extraction dataset. It contains **17,000** documents and **29,223** events, which are all manually annotated based on a pre-defined schema for the military domain including 8 event types and 11 argument role types.

# About CMNEE
## Relevant Competition
CMNEE was used to support a competition "[Joint Extraction of Specific Domain Multi-Events Information](https://www.datafountain.cn/competitions/987)" held by Laboratory for Big Data and Decision, National University of Defense Technology. Although the formal competition has ended, the evaluation has been reopened to drive related research forward. The competition tasks will remain open for sustained benchmarking, and everyone is welcome to participate in the challenge. The competition organizers will continue to monitor the leaderboard results to select outstanding teams.

Note that in order to facilitate the organisation and advancement of the competition, there are 3 main differences between CMNEE (evaluated in our paper) and [FNDEE](https://www.datafountain.cn/competitions/987/datasets) (released in the competition platform):
+ Data split: FNDEE was divided into five subsets, which can be found in the introduction to the competition. CMNEE was divided into train, valid and test set.
+ Test label: Test sets of FNDEE have no label information.
+ Evaluation method: CMNEE used common metrics (Precision, Recall and F1-score) to evalute systematically while FNDEE used the average of Trigger F1-score, argument F1-score and overlapping argument F1-score to evaluate. Detailed information can be found in our paper and the competition website.


## Data format
```
{
         //"id": unique id for each instance
        "id": "114",
         //"text": document text contains event information
        "text": "6月13日，美国海军两架海军战斗机在执行飞行训练任务中发生相撞事故，导致一名飞行员死亡。 这两架飞机分别是来自法隆海军航空基地第13战斗机混合中队的F-5两座战斗机和来自驻扎在弗吉尼亚州奥西纳基地第15攻击战斗机中队的的F/A-18C单座战斗机，这两架飞机在法隆海军航空基地东部约80公里处相撞。 美海军表示，F-5战斗机飞行员在直升机的营救下已经安全撤离，F/A-18C战斗机的飞行员在此次的事故中死亡。发生相撞事故的原因目前还不清楚，美海军正在全力调查。", 
        //"event_list": a list for annotated events, each item is a dict for an event, non-event is []
        "event_list":[   
            { 
                //"event_type": predefined event type
                "event_type": "Manoeuvre", 
                //"trigger": the annotated event trigger
                "trigger":{ 
                    // "text": trigger text
                    "text": "执行", 
                    // "offset": the chinese character offset of the trigger
                    "offset": [18,20]
                },
                //"arguments": the annotated event arguments of the event, a dict
                "arguments":[
                    { 
                        //"role": the annotated argument role
                        "role": "Subject",
                        // "text": argument text
                        "text": "美国海军",
                        //"offset":the chinese character offset of the argument
                        "offset": [6,10]
                    }, 
                    {
                        "role": "Content",
                        "text": "飞行训练任务",
                        "offset": [20,26]
                    }, 
                    {
                        "role": "Date",
                        "text": "6月13日",
                        "offset": [0,5]
                    }
                ]
            },
            { 
                "event_type": "Accident",
                "trigger":{  
                    "text": "相撞",  
                    "offset": [29,31] 
                },
                "arguments":[
                    {  
                        "role": "Subject",
                        "text": "F-5两座战斗机",
                        "offset": [74,82]
                    }, 
                    {  
                        "role": "Subject",
                        "text": " F/A-18C单座战斗机",
                        "offset": [110,122]
                    }, 
                    {
                        "role": "Location",
                        "text": "法隆海军航空基地东部约80公里",
                        "offset": [129,144]
                    }, 
                    {
                        "role": "Date",
                        "text": "6月13日",
                        "offset": [0,5]
                    },
                    {
                        "role": "Result",
                        "text": "一名飞行员死亡",
                        "offset": [36,43]
                    }
                ]
            },
            {
                "event_type": "Injure", 
                "trigger":{  
                    "text": "死亡",  
                    "offset": [200,202] 
                },
                "arguments":[
                    {  
                        "role": "Subject",
                        "text": "F/A-18C战斗机的飞行员",
                        "offset": [179,193]
                    }, 
                    {  
                        "role": "Quantity",
                        "text": "一名",
                        "offset": [36,38]
                    }, 
                    {
                        "role": "Location",
                        "text": "法隆海军航空基地东部约80公里",
                        "offset": [129,144]
                    }, 
                    {
                        "role": "Date",
                        "text": "6月13日",
                        "offset": [0,5]
                    }
                ]
            }
        ]
//"coref_arguments": the coref-arguments list of the instance, each sub-list refers to the same object in the text
 "coref_arguments":[   
    [
        {
            "text": "美国海军",
            "offset": [6,10]
        },
        {
            "text": "美海军",
            "offset": [149,152]
        },
        {
            "text": "美海军",
            "offset": [219,222]
        }
    ],
    [
        {
            "text": "F-5两座战斗机",
            "offset": [74,82]
        },
        {
            "text": "F-5战斗机",
            "offset": [155,161]
        }
    ],
    [
        {
            "text": "F/A-18C单座战斗机",
            "offset": [110,122]
        },
        {
            "text": "F/A-18C战斗机",
            "offset": [179,182]
        }
    ]
 ]
}
```

# Evaluation
## Baselines
1. [DCFEE-O & DCFEE-M](https://aclanthology.org/P18-4009.pdf)
2. [GreedyDec & Doc2EDAG](https://arxiv.org/pdf/1904.07535)
3. [DEPPN](https://aclanthology.org/2021.acl-long.492.pdf)
4. [BERT+CRF](https://arxiv.org/pdf/2309.14258)
5. [EEQA](https://arxiv.org/pdf/2004.13625)
6. [TEXT2EVENT](https://arxiv.org/pdf/2106.09232)
7. [PAIE](https://arxiv.org/pdf/2202.12109)

Relevant processed data can be found from: https://drive.google.com/drive/folders/1I8LZFlqbOiKU0068pPszOmyD2XWOHDKf?usp=sharing.
Except for BERT+CRF and TEXT2EVENT, which we reproduced via [Omnievent](https://github.com/THU-KEG/OmniEvent), a comprehensive, fair, and easy-to-use toolkit for event understanding, other models were implemented through their relevant original repository.

# Citation
If CMNEE is helpful to your research, please consider citing the relevant paper. Thank you.
```
@misc{zhu2024cmnee,
    title={CMNEE: A Large-Scale Document-Level Event Extraction Dataset based on Open-Source Chinese Military News},
    author={Mengna Zhu and Zijie Xu and Kaisheng Zeng and Kaiming Xiao and Mao Wang and Wenjun Ke and Hongbin Huang},
    year={2024},
    eprint={2404.12242},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```
