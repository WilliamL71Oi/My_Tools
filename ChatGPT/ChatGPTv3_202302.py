#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@author WilliamL71Oi
@date   2023/02/16
"""

import openai
from termcolor import colored
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters.terminal256 import Terminal256Formatter
from tenacity import retry, stop_after_attempt, wait_random


openai.api_key = "Yourkey"

# 使用说明
print('\n' + "ChatGPT脚本使用说明：")
print('1.该脚本支持多行输入(但不包括空行)；')
print('2.由于无需科学上网即可使用，所以等待答复的时间可能有点长；')
print('3.需要添加openai.api_key：注册ChatGPT后登陆https://platform.opanai.com可新建自己的key；')
print("4.输入两次回车后等待下即可看到回复；")
print("5.输入'quit'即可退出程序。" + '\n')


# 反复提交问题，这里指定提交6次,每次等待1-3秒。可根据自己情况修改。
@retry(stop=stop_after_attempt(6), wait=wait_random(min=1, max=3))
def chat(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=2500,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["Human:", "AI:"]
    )
    answer = response["choices"][0]["text"].strip()
    if len(answer) != 0:  # 避免返回空白
        return answer
    else:
        raise Exception


text = ""  # 设置一个字符串变量
turns = []  # 设置一个列表变量，turn指对话时的话轮

while True:  # 能够连续提问
    question1 = input(colored(">>>You: " + '\n', 'green'))
    # 定义一个函数convert_to_string()

    def convert_to_string():
        result = ""
        # 创建一个循环，当用户输入两次回车表示输入结束
        while True:
            line = input()
            if line:
                result += line
            else:
                line.strip() == ""   # 当用户输入两次回车时跳出循环
                break
        return result
    # 调用函数
    question = question1 + convert_to_string()
    # print(question)   #用于调试
    print(colored('Thinking...Please wait...' +'\n', 'cyan'))
    if len(question.strip()) == 0:  # 如果输入为空，提醒输入问题
        print(">>>ChatAI:please input your question!" + '\n')
    elif question.lower() == "quit":  # 如果输入为"quit"，程序终止
        print("\nChatAI: See You Next Time!")
        break
    else:
        prompt = text + "\n" + question
        if len(prompt) <= 2000:  # 避免撑爆。ChatGpt API最大处理1500个词左右: prompt+completion不能超过2048个token，约1500个自然词。
            result = chat(prompt)
        else:
            # 因为len(prompt)算的是字符数,2000这个字符数可以自己调整，估计不超过5000一般都可以。
            result = chat(prompt[-2000:])
        turns += [question] + [result]  # 只有这样迭代才能连续提问理解上下文
        print(colored(">>>ChatAI:", 'magenta'))

        # 调用 Pygments 的 highlight 方法，传入需要高亮显示的字符串以及需要使用的语言：
        highlighted_string = highlight(
            result, PythonLexer(), Terminal256Formatter(style="default"))
        # 显示最终结果
        print(highlighted_string, sep='\n')
        if len(turns) <= 6:  # 指定一定的话轮语境以保证对话的连续性，这里指定为6次。你可以根据实际情况修改。
            text = " ".join(turns)
        else:
            text = " ".join(turns[-6:])
