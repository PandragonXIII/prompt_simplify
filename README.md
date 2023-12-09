## 目标
简化prompts并使其不能成功jailbreak


## 步骤
   1. 利用Berkeley Neural Parser解析语法树
   2. 强化学习？生成简化的prompts
   3. 将prompts传递给LLM得到answer
   4. 评估answer是否成功jailbreak

## TODO
-[x]: 部署Berkeley Neural Parser
```
pip install benepar
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
python -m spacy download en_core_web_md
```
-[ ]: 看强化学习