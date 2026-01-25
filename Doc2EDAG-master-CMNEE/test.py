import re

# file_path = r'D:\python\text-summary\LDA主题分类\1.txt'
# with open(file_path, "r", encoding='utf-8') as f:  # 打开文件
#     text = f.read()  # 读取文件
def split_chinese_string(sentence):
    result = []
    for char in sentence:
        if '\u4e00' <= char <= '\u9fff':
            result.extend(list(char))
        else:
            result.append(char)
    return result


text = "俄罗斯国防副部长表示，俄罗斯将利用计算机建模展示在欧洲部署北约和美国的导弹防御系统将如何危及俄罗斯的安全。 美国打算在2020年完成四个阶段的导弹防御系统部署，俄罗斯则认为该系统会削弱该国的核威慑力。5月3日召开的莫斯科讨论会上，国防副部长称，俄罗斯将利用计算机建模成果演示北约导弹防御设施的危害。 美国与北约高级官员，非北约的欧洲国家也将受邀参加本次研讨会，预计超过50个国家的代表将出席会议。美方表示尚未看到邀请函，但愿意参加。 "
# 按照逗号分隔，#字符切割
result_list = re.split(r'。', text.strip())
print(result_list)
print(len(result_list))
sent_list = []
for i in range(len(result_list)-1):
    if result_list[i] is not None:
        sent_list.append((i, result_list[i]))
print(sent_list)

split_text = split_chinese_string(text)
print(split_text)
print(split_text[59:64])
# 按照逗号和句号拆分，两个字符以上切割需要放在 [ ] 中
# result_list = re.split(r'[，。]', text)
# 按照 ，。和空白字符切割
# result_list = re.split(r'[，。\s]', text)

# 使用括号捕获分组，默认保留分割符
# result_list = re.split(r'([，。])', text)

# 不想保留分隔符，以（?:...）的形式指定，不知道哪里问题，下面代码未实现
# result_list = re.split(r'(?:！[，。])', text)
# print(result_list)
