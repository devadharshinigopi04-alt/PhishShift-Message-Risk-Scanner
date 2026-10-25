from pathlib import Path
import re
import joblib
from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.joblib"

app = Flask(__name__)
_model = None

def get_model():
    global _model
    if _model is None and MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    return _model

def extract_cues(message):
    text = message.lower()
    cues = []
    patterns = [
        (r"\b(urgent|immediately|within 24 hours|act now|final warning)\b", "Urgency or time pressure"),
        (r"\b(verify|confirm|update|validate)\b.{0,45}\b(account|password|identity|details|payment)\b", "Request to verify sensitive information"),
        (r"\b(password|one[- ]time password|otp|pin|bank details|credit card)\b", "Sensitive credential or payment wording"),
        (r"https?://|www\.", "URL included in the message"),
        (r"\b(suspended|locked|blocked|terminated)\b", "Threat of account restriction"),
        (r"\b(prize|winner|claim your reward|free gift)\b", "Unexpected reward wording"),
    ]
    for pattern, label in patterns:
        if re.search(pattern, text):
            cues.append(label)
    return cues

def scan_message(message):
    model = get_model()
    if model is None:
        return {"label": "Model not trained", "risk": "Unavailable", "confidence": None,
                "cues": extract_cues(message),
                "explanation": "Run python train_model.py first to create the local model."}
    probabilities = model.predict_proba([message])[0]
    classes = list(model.classes_)
    phishing_index = classes.index("phishing")
    score = float(probabilities[phishing_index])
    # These thresholds are configurable starter values, not a guarantee of real-world safety.
    if 0.40 <= score <= 0.60:
        label, risk = "Needs review", "Uncertain"
    elif score > 0.60:
        label, risk = "Likely phishing", "High"
    else:
        label, risk = "Likely legitimate", "Lower"
    cues = extract_cues(message)
    explanation = ("Potentially suspicious text patterns were found." if cues
                   else "No listed keyword cues were found; this does not prove the message is safe.")
    return {"label": label, "risk": risk, "confidence": round(score * 100, 1),
            "cues": cues, "explanation": explanation}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    message = ""
    if request.method == "POST":
        message = request.form.get("message", "").strip()[:10000]
        if message:
            result = scan_message(message)
    return render_template("index.html", result=result, message=message)

@app.route("/health")
def health():
    return {"status": "ok", "model_ready": MODEL_PATH.exists()}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
