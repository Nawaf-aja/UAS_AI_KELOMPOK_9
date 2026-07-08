# AI Klasifikasi Topik Keluhan Pelanggan Perbankan

Project UAS Artificial Intelligence topik 10: klasifikasi topik keluhan pelanggan perbankan dengan evaluasi model Supervised Learning, yaitu Naive Bayes vs Logistic Regression.

## Fitur

- Dataset utama dibaca dari `data/complaints.csv.zip` (CFPB Consumer Complaint Database).
- Subset olahan untuk training disimpan otomatis ke `data/processed_banking_complaints.csv`.
- Dataset dipetakan ulang menjadi kategori bisnis perbankan yang lebih jelas dan lebih seimbang: `account_management`, `account_closure`, `card_dispute`, `credit_reporting`, `fees_interest`, `fraud_scam`, `loan_mortgage`, dan `payment_transfer`.
- Preprocessing NLP: case folding, cleaning, stopword removal, dan stemming Sastrawi jika tersedia.
- TF-IDF custom untuk mengubah teks menjadi vektor numerik.
- Dua model supervised learning:
  - Multinomial Naive Bayes
  - Logistic Regression multiclass
- Evaluasi Accuracy, Precision, Recall, F1-Score, dan confusion matrix.
- Rekomendasi penanganan berbasis rule-based expert system.
- Web AI lokal berbasis Python standard library di `web_app.py`.
- Streamlit app di `app.py`.
- API JSON `POST /predict`.

## Struktur Repository

```text
data/       Dataset mentah ZIP dan subset hasil proses
models/     File model hasil training
src/        Kode sumber AI modular
notebooks/  Catatan eksperimen
reports/    Metrik evaluasi dan confusion matrix
docs/       Dokumen penjelasan Word
```

## Cara Menjalankan

### 1. Instalasi

Clone project ini atau salin folder project, lalu masuk ke folder project:

```bash
cd "artifial intelegent"
```

Jika ingin menjalankan versi Streamlit, install dependency:

```bash
pip install -r requirements.txt
```

Versi web lokal `web_app.py` tidak membutuhkan dependency tambahan selain Python dan NumPy yang dipakai model.

### 2. Dataset Lokal atau API

Default-nya training membaca dataset olahan lokal dari:

```text
data/processed_banking_complaints.csv
```

File mentah besar `complaints.csv.zip` tidak wajib ada di repo. Jika file mentah tersedia, kode juga bisa membangun ulang subset dari:

```text
data/complaints.csv.zip
```

Jika ingin memakai dataset dari API, jalankan repo dataset API:

```bash
git clone https://github.com/zulisiadmin/api-dataset-banking.git
cd api-dataset-banking
python api_server.py
```

Lalu di folder project AI, set URL API:

PowerShell:

```powershell
$env:DATA_API_URL="http://127.0.0.1:8765/complaints"
python -m src.train --print
```

CMD:

```cmd
set DATA_API_URL=http://127.0.0.1:8765/complaints
python -m src.train --print
```

Linux/macOS:

```bash
export DATA_API_URL="http://127.0.0.1:8765/complaints"
python -m src.train --print
```

Jika `DATA_API_URL` tidak diset, sistem otomatis kembali memakai dataset lokal.

Jika API dataset sudah kamu deploy, pakai URL deploy:

```powershell
$env:DATA_API_URL="https://nama-aplikasi-kamu.onrender.com/complaints"
python -m src.train --print
```

### 3. Training

Training model:

```bash
python -m src.train --print
```

### 4. Menjalankan Web AI

Web AI tanpa dependency tambahan:

```bash
python web_app.py
```

Buka:

```text
http://127.0.0.1:8501
```

Streamlit:

```bash
pip install -r requirements.txt
streamlit run app.py
```

### 5. Deploy ke Streamlit Cloud

Saat membuat app di Streamlit Cloud, pilih main file:

```text
streamlit_app.py
```

atau:

```text
app.py
```

Jangan pilih `web_app.py` sebagai main file Streamlit Cloud. File `web_app.py` adalah server lokal berbasis Python standard library. Jika terlanjur memilih `web_app.py`, versi terbaru sudah diberi fallback agar tetap mengarah ke UI Streamlit.

## API Docs

Endpoint:

```text
POST /predict
Content-Type: application/json
```

Request:

```json
{
  "text": "My transfer failed but my balance was deducted",
  "model": "logistic_regression"
}
```

Response sukses `200`:

```json
{
  "status": 200,
  "model": "logistic_regression",
  "prediction": "payment_transfer",
  "confidence": 0.84,
  "top_predictions": [
    {"label": "payment_transfer", "confidence": 0.84}
  ],
  "recommendation": {
    "priority": "High",
    "target_unit": "Payment Operation / Transaction Support",
    "sla": "1-3 hari kerja"
  }
}
```

Response gagal `400`:

```json
{
  "status": 400,
  "error": "Teks keluhan tidak boleh kosong."
}
```

## Architecture Diagram

```text
Input Layer
  -> Web UI / Streamlit / API JSON
Preprocessing
  -> case folding, cleaning, stopword removal, stemming
Feature Extraction
  -> TF-IDF
Inference
  -> Naive Bayes atau Logistic Regression
Output
  -> kategori keluhan, confidence score, top predictions
Expert System
  -> prioritas, divisi tujuan, SLA, dan langkah penanganan
```

## Referensi

- scikit-learn documentation: TfidfVectorizer, MultinomialNB, LogisticRegression.
- PySastrawi: Indonesian stemmer.
- CFPB Consumer Complaint Database: sumber dataset komplain finansial.
