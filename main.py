"""
test the simplified sentence with GPT_test_model
"""
import json
from GPT_test_model import GPTclassify

# fetch the simplified sentences
filename = 'data\\LLM_simplify_result3.json'
with open(filename, encoding='utf-8') as f:
    sentences = json.load(f) # a list of dictionaries {"complex":, "simplify":}

temp = []
sentences = sentences[0:5]+sentences[13:18]+sentences[33:38]+sentences[56:61]
for pair in sentences:
    temp.extend([pair['complex'], pair['simplify']])
# start testing with chatGPT
results = GPTclassify(temp, silent=False)
# notice that 1 means inproper, which means GPT knows it's bad, thus a jailbreak fails
complex_results = results[0::2]
simplify_results = results[1::2]
original_jailbreak_rate = complex_results.count(0)/len(complex_results)
original_fail_rate = complex_results.count(1)/len(complex_results)
simplify_jailbreak_rate = simplify_results.count(0)/len(simplify_results)
simplify_fail_rate = simplify_results.count(1)/len(simplify_results)
# print a table with percentage
print("original jailbreak rate: {:.2f}%".format(original_jailbreak_rate*100))
print("original fail rate: {:.2f}%".format(original_fail_rate*100))
print("simplify jailbreak rate: {:.2f}%".format(simplify_jailbreak_rate*100))
print("simplify fail rate: {:.2f}%".format(simplify_fail_rate*100))

#store the results
store = [{
            'original_jailbreak_rate': original_jailbreak_rate,
            'original_fail_rate': original_fail_rate,
            'simplify_jailbreak_rate': simplify_jailbreak_rate,
            'simplify_fail_rate': simplify_fail_rate
        }]
for i in range(len(sentences)):
    store.extend([{
        'complex': sentences[i]['complex'],
        'original_result': complex_results[i],
        'simplify': sentences[i]['simplify'],
        'simplify_result': simplify_results[i]
    }])
with open('data/LLM_test_result3.json', 'w', encoding='utf-8') as f:
    json.dump(store, f, ensure_ascii=False, indent=4)