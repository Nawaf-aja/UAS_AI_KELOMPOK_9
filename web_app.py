import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.predict import predict_topic


HTML = """<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Klasifikasi Keluhan Perbankan</title>
  <style>
    :root { color-scheme: light; font-family: Inter, Segoe UI, Arial, sans-serif; }
    body { margin: 0; background: #f6f8fb; color: #172033; }
    header { background: #0f766e; color: white; padding: 28px clamp(18px, 5vw, 64px); }
    main { max-width: 980px; margin: 0 auto; padding: 24px clamp(16px, 4vw, 40px); }
    h1 { margin: 0 0 8px; font-size: clamp(26px, 5vw, 42px); letter-spacing: 0; }
    .subtitle { margin: 0; max-width: 760px; line-height: 1.6; }
    .panel { background: white; border: 1px solid #dbe3ef; border-radius: 8px; padding: 20px; margin-top: 18px; box-shadow: 0 8px 22px rgba(23, 32, 51, .06); }
    label { display: block; font-weight: 700; margin-bottom: 8px; }
    textarea, select { width: 100%; box-sizing: border-box; border: 1px solid #b9c5d6; border-radius: 6px; font: inherit; padding: 12px; background: white; }
    textarea { min-height: 150px; resize: vertical; }
    button { margin-top: 14px; border: 0; border-radius: 6px; background: #0f766e; color: white; font-weight: 700; padding: 12px 18px; cursor: pointer; }
    button:disabled { opacity: .65; cursor: progress; }
    .result { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
    .metric { border: 1px solid #dbe3ef; border-radius: 8px; padding: 14px; background: #fbfcfe; }
    .metric span { display: block; color: #64748b; font-size: 13px; margin-bottom: 6px; }
    .recommendation { line-height: 1.55; }
    .recommendation ul { margin: 8px 0 0 20px; padding: 0; }
    pre { white-space: pre-wrap; background: #101827; color: #e2e8f0; padding: 14px; border-radius: 8px; overflow:auto; }
  </style>
</head>
<body>
  <header>
    <h1>AI Klasifikasi Keluhan Pelanggan Perbankan</h1>
    <p class="subtitle">Masukkan teks keluhan, pilih model, lalu sistem akan mengklasifikasikan topik keluhan menggunakan pipeline NLP, TF-IDF, dan supervised learning.</p>
  </header>
  <main>
    <section class="panel">
      <label for="complaint">Teks keluhan</label>
      <textarea id="complaint">Transfer BI Fast gagal tetapi saldo saya terpotong dan penerima belum menerima dana.</textarea>
      <label for="model" style="margin-top: 14px;">Model</label>
      <select id="model">
        <option value="">Model terbaik otomatis</option>
        <option value="naive_bayes">Naive Bayes</option>
        <option value="logistic_regression">Logistic Regression</option>
      </select>
      <button id="predict">Prediksi Topik</button>
    </section>
    <section class="panel" id="output" hidden>
      <div class="result">
        <div class="metric"><span>Prediksi</span><strong id="label"></strong></div>
        <div class="metric"><span>Confidence</span><strong id="confidence"></strong></div>
        <div class="metric"><span>Model</span><strong id="usedModel"></strong></div>
        <div class="metric"><span>Prioritas</span><strong id="priority"></strong></div>
        <div class="metric"><span>Divisi Tujuan</span><strong id="unit"></strong></div>
        <div class="metric"><span>SLA</span><strong id="sla"></strong></div>
      </div>
      <h2>Rekomendasi Penanganan</h2>
      <div class="recommendation">
        <p id="summary"></p>
        <p id="note"></p>
        <strong>Langkah awal:</strong>
        <ul id="actions"></ul>
      </div>
      <h2>Response JSON</h2>
      <pre id="json"></pre>
    </section>
  </main>
  <script>
    const btn = document.getElementById('predict');
    btn.addEventListener('click', async () => {
      btn.disabled = true;
      btn.textContent = 'Memproses...';
      const payload = {
        text: document.getElementById('complaint').value,
        model: document.getElementById('model').value || null
      };
      try {
        const res = await fetch('/predict', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        document.getElementById('output').hidden = false;
        document.getElementById('label').textContent = data.prediction || data.error;
        document.getElementById('confidence').textContent = data.confidence ? Math.round(data.confidence * 100) + '%' : '-';
        document.getElementById('usedModel').textContent = data.model || '-';
        const rec = data.recommendation || {};
        document.getElementById('priority').textContent = rec.priority || '-';
        document.getElementById('unit').textContent = rec.target_unit || '-';
        document.getElementById('sla').textContent = rec.sla || '-';
        document.getElementById('summary').textContent = rec.summary || '-';
        document.getElementById('note').textContent = rec.confidence_note || '';
        const actions = document.getElementById('actions');
        actions.innerHTML = '';
        (rec.actions || []).forEach((action) => {
          const item = document.createElement('li');
          item.textContent = action;
          actions.appendChild(item);
        });
        document.getElementById('json').textContent = JSON.stringify(data, null, 2);
      } finally {
        btn.disabled = false;
        btn.textContent = 'Prediksi Topik';
      }
    });
  </script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            data = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if parsed.path == "/predict":
            params = parse_qs(parsed.query)
            text = params.get("text", [""])[0]
            model = params.get("model", [None])[0]
            payload = predict_topic(text, model)
            self._send_json(payload, payload.get("status", 200))
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != "/predict":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(body or "{}")
            result = predict_topic(payload.get("text", ""), payload.get("model"))
            self._send_json(result, result.get("status", 200))
        except Exception as exc:
            self._send_json({"status": 400, "error": f"Payload JSON tidak valid: {exc}"}, 400)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8501), Handler)
    print("Web AI berjalan di http://127.0.0.1:8501")
    server.serve_forever()


if __name__ == "__main__":
    if "streamlit" in sys.modules:
        import app  # noqa: F401
    else:
        main()
