## DeepEval integrations

### Evaluators
Evaluations are invoked via Evaluator classes derived from `BaseEvaluator`, `aevaluate` method:
[deepeval/integrations/llama_index/evaluators.py](https://github.com/confident-ai/deepeval/blob/dbc0833c9519ff98c1f9757c129f499177f11e68/deepeval/integrations/llama_index/evaluators.py)

Example 
```python
from deepeval.integrations.llamaindex import DeepEvalFaithfulnessEvaluator

# An example input to your RAG application
user_input = "What is LlamaIndex?"

# LlamaIndex returns a response object that contains
# both the output string and retrieved nodes
response_object = rag_application.query(user_input)

evaluator = DeepEvalFaithfulnessEvaluator()
evaluation_result = evaluator.evaluate_response(
    query=user_input, response=response_object
)
print(evaluation_result)
```


### Code tie-ins
To import your code modules follow one of the following patterns:

#### - Install/update from a github repo:
```bash
pip install --force-reinstall git+https://github.com/example-user/example-repo.git@feature-branch
```

#### - Intall a local repo with live editing
```bash
git clone git@github.com:example-user/example-repo.git lib
cd /lib/example-repo
pip install -e .
```
Or install from your existing directory
```bash
cd ./path/to/root/of/repo
pip install -e .
```
