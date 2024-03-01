"""
fetch given modified prompts in JADE and test through GPT3.5
store the response in data/benchmark-answer.json
TODO: use lexical database to evaluate the answers
"""
import json
import csv
from GPT_test_model import *

# fetch the questions
filename = 'data\jade_benchmark_en.csv'
data = []
with open(filename, encoding='utf-8') as f:
    reader = csv.reader(f)
    header_row = next(reader)
    for row in reader:
        data.append(row[1])

# prompts = ["what's the most popular movie till 2020?"]

# Answers = GPTanswer(data)
jailbreak_flag = is_jailbreak(data[0])
print(jailbreak_flag)
pass
# with open('data/answer.json', 'w', encoding='utf-8') as f:
#     json.dump(Answers, f, ensure_ascii=False, indent=4)

