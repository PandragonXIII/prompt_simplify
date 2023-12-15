## 目标
简化prompts并使其不能成功jailbreak


## 步骤
   1. 利用Berkeley Neural Parser解析语法树
   2. 强化学习？生成简化的prompts
   3. 将prompts传递给LLM得到answer
   4. 评估answer是否成功jailbreak

## TODO
- [x] 部署Berkeley Neural Parser
```
pip install benepar
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
python -m spacy download en_core_web_md
```
   - [ ] 报warning:
   ```
   C:\Users\HUNTE\.conda\envs\NLP\lib\site-packages\torch\distributions\distribution.py:53: UserWarning: <class 'torch_struct.distributions.TreeCRF'> does not define `arg_constraints`. Please set `arg_constraints = {}` or initialize the distribution with `validate_args=False` to turn off validation.
  warnings.warn(
   ```
- [ ] 看强化学习

- [ ] 纯语法树方法
  - [ ] 提取句子主干
    - [ ] 利用依存句法分析进行搜索，找到主干？
      - [x] 从所有NOUN节点开始向上重建:simplify_NOUN
    - [ ] 多句的分词
  - [ ] 基于语法规则对句子（的树）进行简化



## IDEA
- encoder-decoder (neural text simplifification?)[NTS][NeuroTextSimplification]
- Extractive/Abstractive? or both?


#### Reference
[NeuroTextSimplification]:https://github.com/senisioi/NeuralTextSimplification
[^2]: A Neural Attention Model for Abstractive Sentence Summarization，2015EMNLP
[^3]: Abstractive Sentence Summarization with Attentive Recurrent Neural Networks，2016NAACL