"""
fetch given modified prompts in JADE and test through GPT3.5
store the response in data/benchmark-answer.json
TODO: use lexical database to evaluate the answers
"""

import json
import csv
import openai
from openai import OpenAI
import os
import time

os.environ["OPENAI_API_KEY"] = "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"

# fetch the questions
filename = 'data\jade_benchmark_en.csv'
data = []
with open(filename, encoding='utf-8') as f:
    reader = csv.reader(f)
    header_row = next(reader)
    for row in reader:
        data.append(row[1])

prompts = ["what's the most popular movie till 2020?"]
Answers = []

client = OpenAI(
    base_url="https://madmiku.fun/v1",
)

#get present time
t = int(time.time())
# print(t)

for i in range(len(data)):
    print("{} - ".format(i),end="")
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      timeout=30,
      messages=[
        {"role": "user", "content": data[i]}
      ]
    )
    answer = response.choices[0].message.content
    temp = {"prompt": data[i], "answer": answer, "jailbreak": -1}
    Answers.append(temp)
    # hold to avoid rate limit(3RPM)
    t1 = int(time.time())
    while (t1-t < 20*i):
        time.sleep(1)
        t1 = int(time.time())

with open('data/answer.json', 'w', encoding='utf-8') as f:
    json.dump(Answers, f, ensure_ascii=False, indent=4)