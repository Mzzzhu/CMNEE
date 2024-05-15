# CMNEE
LREC-COLING 2024的文章"[**CMNEE: A Large-Scale Document-Level Event Extraction Dataset based on Open-Source Chinese Military News**](http://export.arxiv.org/abs/2404.12242)"的数据和代码将会在近期公布。

CMNEE下载地址：https://drive.google.com/drive/folders/1nfKiSsu88oBeykUSYm7NGn4Q50_2GPS1?usp=sharing

# 概况
CMNEE是一个大规模的、基于文档标注的开源中文军事新闻事件抽取数据集。该数据集包含**17,000**份文档和**29,223**个事件，所有事件均基于预定义的军事领域模式人工标注，包括8种事件类型和11种论元角色。

# 数据集介绍
## 相关竞赛
CMNEE用于支撑**国防科技大学大数据与决策实验室**举办的第二届全国大数据与计算智能挑战赛“[领域多事件信息联合抽取](https://www.datafountain.cn/competitions/987)”赛题。该赛题已于2023年8月圆满结束，近期已经开放长期评测，赛事主办方将持续关注榜单结果以遴选优秀团队建立合作。

需要说明的是，为方便赛事的组织和开展，用于支撑赛题的FNDEE和论文中的CMNEE虽然数据完全一致，但主要有三点不同：
+ 数据划分：FNDEE划分为5个数据集，具体划分方式可参考网页信息；CMNEE划分为训练集、验证集和测试集。
+ 测试集信息：FNDEE的测试集均不包含标签信息。
+ 评测方式：CMNEE采用常见的准确率(Precision)、召回率(Recall)、F1分数(F1-score)以进行系统性的评估，FNDEE中考虑了交织论元的F1分数，此外为便于排名，最终的评测分数是触发词F1、普通论元F1和交织论元F1的均值。
具体信息及示例可参考网页说明。

## 数据格式
```
{
         // "id": 事件文本唯一标识
        "id": "114",
         // "text": 事件文本（string）
        "text": "6月13日，美国海军两架海军战斗机在执行飞行训练任务中发生相撞事故，导致一名飞行员死亡。 这两架飞机分别是来自法隆海军航空基地第13战斗机混合中队的F-5两座战斗机和来自驻扎在弗吉尼亚州奥西纳基地第15攻击战斗机中队的的F/A-18C单座战斗机，这两架飞机在法隆海军航空基地东部约80公里处相撞。 美海军表示，F-5战斗机飞行员在直升机的营救下已经安全撤离，F/A-18C战斗机的飞行员在此次的事故中死亡。发生相撞事故的原因目前还不清楚，美海军正在全力调查。", 
        // "event_list":标注的事件提及列表。该列表包含多条独立的事件提及字典（dict），每条独立的事件提及仅包含一种事件类型及该类型相应的事件论元。非事件样本的"event_list"为[]
        "event_list":[   
            { 
                // "event_type":标注的事件类型
                "event_type": "Manoeuvre", 
                // "trigger":标注的事件触发词
                "trigger":{ 
                    // "text":事件触发词文本，下同
                    "text": "执行", 
                    // "offset":触发词在事件文本中的偏移量，索引从0开始，[18,20]表示原始文本中第18个字符开始，左闭右开
                    "offset": [18,20]
                },
                // "arguments":标注的事件论元和论元角色的列表（list），列表中每个元素是一个字典（dict）
                "arguments":[
                    { 
                        // "role":标注的论元角色类型，下同
                        "role": "Subject",
                        // "text": 事件论元文本，下同
                        "text": "美国海军",
                        // "offset":事件论元在事件文本中偏移量，下同
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
// " coref_arguments ": 该事件样本的共指列表。该列表包含多个子列表，每个子列表包含若干指代同一个对象的文本，用 "text" 与 "offset"标注。当某个预测结果论元和标注结果论元的 "role"字段一致，而"text"字段或者"offset"字段不一致时，如果该预测结果论元的"text"字段以及"offset"字段和标注结果在同一个" coref_arguments "子列表中，也算该论元预测正确。如果当前事件样本没有共指的对象，" coref_arguments "为[]
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

# CMNEE评估
## 基线模型
1. [DCFEE-O & DCFEE-M](https://aclanthology.org/P18-4009.pdf)
2. [GreedyDec & Doc2EDAG](https://arxiv.org/pdf/1904.07535)
3. [DEPPN](https://aclanthology.org/2021.acl-long.492.pdf)
4. [BERT+CRF](https://arxiv.org/pdf/2309.14258)
5. [EEQA](https://arxiv.org/pdf/2004.13625)
6. [TEXT2EVENT](https://arxiv.org/pdf/2106.09232)
7. [PAIE](https://arxiv.org/pdf/2202.12109)

# 引用说明
如果CMNEE对您的研究有所帮助，请考虑引用相关文章。
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
