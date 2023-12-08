## 目标
简化prompts并使其不能成功jailbreak


## 步骤
   1. 利用Berkeley Neural Parser解析语法树
   2. 强化学习？生成简化的prompts
   3. 将prompts传递给LLM得到answer
   4. 评估answer是否成功jailbreak

## TODO
-[ ]: 部署Berkeley Neural Parser
-[ ]: 看强化学习