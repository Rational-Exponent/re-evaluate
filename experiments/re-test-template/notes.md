## DeepEval integrations

### Evaluators
Evaluations can be performed per individual metric or in bulk using the `evaluate` function.

For example, see `experiments/re-test-template/step_4_eval.ipynb`:
```python
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric


metric = AnswerRelevancyMetric(threshold=0.5)
test_cases = [LLMTestCase(
    input=response.get("question"),
    actual_output=response.get("response")
) for response in qa_data.get("eval-questions")]

score_data = evaluate(test_cases, [metric])
scores = [r.metrics_data[0].score for r in score_data.test_results]
print(scores)
```


### Code tie-ins
Follow this method to integrate your code into the eval test harness:
1. Import your module code using one of the methods below
2. `import` your module into the test code file:
- For example: `experiments/re-test-template/step_3_test.ipynb`
3. Mock out security featuers
4. Save results of completions together with the relevant Q/T pair.

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
