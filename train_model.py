from pathlib import Path
import csv
import random
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sample_messages.csv"
MODEL_PATH = BASE_DIR / "model.joblib"

PHISHING_TEMPLATES = [
    "Urgent: your account will be suspended. Verify your details immediately at {url}",
    "Final warning: confirm your password to restore access: {url}",
    "Your payment failed. Update your bank details now at {url}",
    "You are a winner. Claim your free gift before it expires: {url}",
    "Unusual sign-in detected. Validate your identity using {url}",
    "Your mailbox is full. Login to increase storage: {url}",
    "Your package is on hold. Pay the small fee here: {url}",
    "Action required within 24 hours or your account will be locked: {url}",
    "Payroll information needs confirmation. Open {url} to verify your account",
    "Your subscription is terminated unless you update payment details at {url}",
]
LEGIT_TEMPLATES = [
    "Reminder: your team meeting is scheduled for {day} at {time}.",
    "Your library book is due on {day}. Please return it at the desk.",
    "The project report is available in the course portal. Contact your teacher with questions.",
    "Thanks for your order. Your receipt is available in your account order history.",
    "Your appointment is confirmed for {day} at {time}. Call the clinic if you need to reschedule.",
    "The monthly newsletter is ready to read on our official website.",
    "Your document was shared with you by a colleague. Review it when convenient.",
    "The campus event starts at {time} in the main auditorium.",
    "Your requested password reset was initiated. If this was not you, visit the official app directly.",
    "Your payment receipt has been generated. You can view it in the official application.",
]
URLS = ["http://verify-example.invalid/login", "https://secure-check.invalid/account",
        "http://billing-alert.invalid/pay", "https://claim-prize.invalid/reward"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Friday", "15 October", "next week"]
TIMES = ["9:00 AM", "2:30 PM", "11:15 AM", "4:00 PM"]

def create_sample_data():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(200):
        template = PHISHING_TEMPLATES[i % len(PHISHING_TEMPLATES)]
        rows.append({"message_id": f"SYN-P-{i+1:04}", "channel": "email_or_sms",
                     "message": template.format(url=URLS[i % len(URLS)]),
                     "label": "phishing", "campaign_group": f"synthetic-phish-{i % 10}",
                     "source": "synthetic educational example"})
        template = LEGIT_TEMPLATES[i % len(LEGIT_TEMPLATES)]
        rows.append({"message_id": f"SYN-L-{i+1:04}", "channel": "email_or_sms",
                     "message": template.format(day=DAYS[i % len(DAYS)], time=TIMES[i % len(TIMES)]),
                     "label": "legitimate", "campaign_group": f"synthetic-legit-{i % 10}",
                     "source": "synthetic educational example"})
    with DATA_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return rows

def main():
    if DATA_PATH.exists():
        with DATA_PATH.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    else:
        rows = create_sample_data()
    texts = [r["message"] for r in rows]
    labels = [r["label"] for r in rows]
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.25, random_state=42, stratify=labels
    )
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True, max_features=12000)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print("IMPORTANT: This is a synthetic demo dataset, not a real-world performance benchmark.")
    print(f"Test accuracy on random split: {accuracy_score(y_test, pred):.3f}")
    print("Classification report:")
    print(classification_report(y_test, pred, zero_division=0))
    print("Confusion matrix (labels order: legitimate, phishing):")
    print(confusion_matrix(y_test, pred, labels=["legitimate", "phishing"]))
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to: {MODEL_PATH}")

if __name__ == "__main__":
    main()
