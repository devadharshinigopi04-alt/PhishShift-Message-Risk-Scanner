# PhishShift Message Risk Scanner (ML-07)

A small Flask + machine-learning educational prototype for reviewing email/SMS text for possible phishing risk.

## Features
- Browser-based message input and scan result.
- TF-IDF text features with Logistic Regression.
- Basic suspicious-cue explanations.
- Uncertain/review band for model scores near the threshold.
- Synthetic demo dataset and training script.
- Health endpoint at `/health`.

## Requirements
- Python 3.10 or newer recommended.
- Internet is needed only to install Python packages; the scanner runs locally after setup.

## Run on Windows
Open a terminal in this project folder:

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python train_model.py
python app.py
```

Open http://127.0.0.1:5000 in your browser.

If activation is blocked in PowerShell, use Command Prompt (`cmd`) or run `.venv\Scripts\python.exe` directly.

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python train_model.py
python app.py
```

## Dataset and evaluation limitations
The included dataset is synthetic and intended only to demonstrate the pipeline. It is not representative of real phishing campaigns and its metrics must not be reported as real-world accuracy. Before a research or competition submission, collect a legally usable, documented dataset; record source and license; remove duplicate/near-duplicate templates; split by campaign/source group; and report precision, recall, F1, false-positive rate, false-negative rate, and robustness tests. The starter script uses a random split for a simple smoke test, not a rigorous campaign-held-out benchmark.

The displayed model score is an uncalibrated model output, not a reliable probability. The risk labels and keyword cues are decision support only, not a guarantee that a message is safe or malicious.

## Project structure
- `app.py` — Flask web app and scan logic
- `train_model.py` — builds demo data if needed, trains and evaluates model
- `data/sample_messages.csv` — synthetic educational examples (generated on first training run)
- `templates/index.html` — UI
- `static/style.css` — styling
- `requirements.txt` — Python dependencies

## Suggested report sections
1. Abstract
2. Problem statement and objectives
3. Existing system and proposed system
4. Dataset collection, license and preprocessing
5. Model design and evaluation methodology
6. Results and discussion
7. Limitations, ethics and future enhancement
8. Conclusion and references

## Safe use
Do not paste real credentials or sensitive messages into the demo. Do not automatically open or fetch suspicious URLs. Verify suspicious requests through an official website/app or a known contact channel.
