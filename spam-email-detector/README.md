# 📧 Spam Email Detector

A machine learning web app that predicts whether an email is **Spam** or
**Not Spam**, built with **scikit-learn** (TF-IDF + Naive Bayes) and a
**Streamlit** front end with a styled animated background.

---

## 🗂️ Project structure

```
spam-email-detector/
├── app.py                  # Streamlit web app (the UI)
├── train_model.py          # Trains the ML model and saves it
├── generate_dataset.py     # Generates the labeled email dataset
├── data/
│   └── spam_dataset.csv    # Training data (email text + label)
├── model/
│   ├── spam_classifier.pkl # Trained model (created by train_model.py)
│   └── vectorizer.pkl      # TF-IDF vectorizer (created by train_model.py)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## ▶️ Run it locally in VS Code

1. **Unzip** this project and open the folder in VS Code.

2. **Create a virtual environment** (recommended) and activate it:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Retrain the model.** A trained model is already included
   in `model/`, so you can skip this — but if you want to regenerate the
   dataset or retrain from scratch:
   ```bash
   python generate_dataset.py
   python train_model.py
   ```

5. **Run the app**:
   ```bash
   streamlit run app.py
   ```

   Your browser will open automatically at `http://localhost:8501`.
   Paste any email text into the box and click **Predict** to see if it's
   spam.

---

## 🌍 Deploy it for free (Streamlit Community Cloud)

This is the easiest way to get a public link that "everyone can use."

1. **Create a GitHub repository** and push this whole project folder to it
   (make sure `data/`, `model/`, `app.py`, `train_model.py`, and
   `requirements.txt` are all included).

   ```bash
   git init
   git add .
   git commit -m "Spam email detector project"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```

2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in
   with your GitHub account.

3. Click **"New app"**, then select:
   - **Repository:** the repo you just pushed
   - **Branch:** `main`
   - **Main file path:** `app.py`

4. Click **Deploy**. Streamlit Cloud will install everything from
   `requirements.txt` and launch your app automatically.

5. You'll get a public URL like:
   ```
   https://<your-app-name>.streamlit.app
   ```
   Share this link with your teacher and classmates — anyone can open it
   and try the detector, no installation needed.

> Note: if `model/*.pkl` files aren't present for any reason, `app.py` will
> automatically train the model on first load using `data/spam_dataset.csv`,
> so deployment works even from a fresh clone.

---

## 🧠 How it works

1. **Dataset** (`generate_dataset.py`): builds a labeled set of realistic
   spam and legitimate ("ham") emails covering common patterns — prize
   scams, phishing, fake loans, work-from-home schemes, alongside normal
   emails like meeting reminders, invoices, and personal messages.

2. **Feature extraction**: `TfidfVectorizer` converts email text into
   numeric features based on word/phrase importance (unigrams + bigrams).

3. **Model**: a `MultinomialNB` (Naive Bayes) classifier — a fast,
   well-proven algorithm for text classification tasks like spam
   detection.

4. **App** (`app.py`): loads the trained model, lets the user paste an
   email, and shows the prediction (Spam / Not Spam) along with a
   confidence percentage for each class.

---

## ✏️ Ideas to extend the project (optional, for extra credit)

- Swap in a real-world public dataset (e.g. the SMS Spam Collection or
  Enron spam dataset) for even broader coverage.
- Try a different model (Logistic Regression, SVM) and compare accuracy.
- Add a file-upload option so users can upload a `.txt` or `.eml` file.
- Show the top keywords that pushed the prediction toward spam/ham.
- Add a feedback button so users can correct wrong predictions, and log
  those to improve the dataset later.
