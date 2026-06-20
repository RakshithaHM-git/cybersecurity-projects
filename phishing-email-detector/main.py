import pandas as pd
import re
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

# ---------------------------------
# Feature Extraction Function
# ---------------------------------
def extract_features(text):
    text = str(text)

    # Feature 1: URL Count
    url_count = len(re.findall(r'http[s]?://', text))

    # Feature 2: Suspicious Keywords
    keywords = [
        'login', 'verify', 'urgent',
        'password', 'bank', 'account',
        'update', 'click', 'reward',
        'free', 'winner', 'prize'
    ]

    keyword_count = sum(
        1 for word in keywords
        if word in text.lower()
    )

    # Feature 3: Email Length
    text_length = len(text)

    # Feature 4: Exclamation Marks
    exclamation_count = text.count('!')

    # Feature 5: Digit Count
    digit_count = sum(c.isdigit() for c in text)

    return [
        url_count,
        keyword_count,
        text_length,
        exclamation_count,
        digit_count
    ]


# ---------------------------------
# Load Dataset
# ---------------------------------
data = pd.read_csv("dataset.csv")

# Convert labels
data['label'] = data['label'].map({
    'safe': 0,
    'phishing': 1
})

# ---------------------------------
# Feature Extraction
# ---------------------------------
X = data['text'].apply(extract_features).tolist()
y = data['label']

# ---------------------------------
# Train-Test Split
# ---------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

# ---------------------------------
# Train Model
# ---------------------------------
model = GaussianNB()
model.fit(X_train, y_train)

# ---------------------------------
# Predictions
# ---------------------------------
y_pred = model.predict(X_test)

# ---------------------------------
# Evaluation
# ---------------------------------
print("\n=== Phishing Email Detection Results ===\n")

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:\n")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# ---------------------------------
# Graphical Confusion Matrix
# ---------------------------------
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Safe", "Phishing"]
)

disp.plot()
plt.title("Phishing Email Detection")
plt.show()

# ---------------------------------
# User Email Prediction
# ---------------------------------
print("\n==============================")
print("TEST YOUR OWN EMAIL")
print("==============================")

new_email = input("\nEnter Email Text:\n")

new_features = [extract_features(new_email)]

prediction = model.predict(new_features)

if prediction[0] == 1:
    print("\n⚠️ Result: PHISHING EMAIL")
else:
    print("\n✅ Result: SAFE EMAIL")