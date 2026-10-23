# MarkItDown evaluation

Run the local Office Comprehension Benchmark questions through MarkItDown,
an answer model, and an assertion judge.

The script reads these paths relative to its own directory:

- `data/questions.jsonl`: one question per line, with `id`, `filepath` (a list of
  filenames), `query`, and `gold` (a list of assertions).
- `data/files/`: the referenced documents, including original PDFs.
- `judge_prompt.md`: the original benchmark judge prompt, used verbatim with its
  question, answer, and assertion placeholders filled in.

## Run

Use Python 3.12 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"

python markitdown_eval.py \
  --answer-model YOUR_ANSWER_MODEL \
  --judge-model YOUR_JUDGE_MODEL \
  --limit 5
```

Questions with `track: "Domain"` are skipped. The current data contains 76 Domain
questions and 797 remaining questions. `--limit` applies after this filter;
omit it to run all non-Domain questions.

Add `--shuffle` to randomize the remaining questions before applying `--limit`.
For a repeatable order, use `--shuffle --seed 42`. Without `--shuffle`, questions
run in file order. Shuffle settings are saved in the summary.

Both models use the same provider, endpoint, and key. The selected provider is
printed at startup and saved in the summary:

- If `GATEWAY_API_KEY` is nonempty, the script uses the **gateway** provider, even
  if `OPENAI_API_KEY` is also set. Set `GATEWAY_URL` to its Responses API base URL;
  this is required and has no default.
  Each answer and judgment gets a fresh session ID with `strict_session: true`.
- Otherwise, it uses **OpenAI** with `OPENAI_API_KEY`. To use another Chat
  Completions compatible endpoint, set `OPENAI_BASE_URL`.

To use a gateway, configure these variables before running the script:

```bash
export GATEWAY_API_KEY="your-gateway-key"
export GATEWAY_URL="https://your-gateway.example/api"
```

For a local server that does not require authentication, set `OPENAI_API_KEY` to
any nonempty placeholder and unset `GATEWAY_API_KEY`. The script reads shell
variables; it does not load `.env` or credential files.

Each question makes one answer request followed by one judge request per gold
assertion. The answer model receives the extracted documents and question.
Only the judge receives the gold assertions. Questions run sequentially.
Both answer and judge requests explicitly use `medium` reasoning effort, which
is printed at startup and saved in the summary.
The console shows the question, each file being converted, extracted character
counts and truncation, answer generation, each assertion being judged and its
score, and the final question result. Progress is printed immediately.

## Results

By default, the script writes `runs/results.jsonl` and `runs/results.summary.json`
beside the script. Use `--output runs/my-run.jsonl` to choose another destination.
An existing results file is never overwritten. Each question is saved immediately;
there is no resume mode.

Results include the original question fields, generated answer, assertion scores
and reasoning, raw judge replies, truncated filenames, and any error. A question's
score is the fraction of assertions passed. Summary accuracy is the mean of
completed question scores, with assertions equally weighted within each question.
Dataset `weights` are retained but not applied. Failed questions have a null score
and are excluded from accuracy; the summary reports their count separately.

`--max-chars` defaults to 100,000 extracted document characters per question,
shared equally across its files. Truncation is marked in the model input and
results. Set it to `0` for full documents, subject to your model's context limit.
`--max-output-tokens` defaults to 4,096 per model request, including reasoning
tokens. Truncated or malformed model responses are recorded as errors.
