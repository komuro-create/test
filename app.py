from flask import Flask, make_response

app = Flask(__name__)

HTML = """<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>セキュリティ検査用デモアプリ</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 720px; margin: 48px auto; padding: 0 20px; line-height: 1.7; background: #f5f7fb; color: #182230; }
    main { background: white; border: 1px solid #dbe2ec; border-radius: 16px; padding: 28px; }
    h1 { margin-top: 0; }
    .ok { color: #157347; font-weight: 700; }
  </style>
</head>
<body>
  <main>
    <h1>セキュリティ検査用デモアプリ</h1>
    <p class="ok">公開前チェックの動作確認用ページです。</p>
    <p>HTTPS、セキュリティヘッダー、Cookie属性などの確認に使用できます。</p>
  </main>
</body>
</html>"""


@app.get("/")
def index():
    response = make_response(HTML)
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'unsafe-inline'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.set_cookie(
        "demo_session",
        "temporary-demo-value",
        secure=True,
        httponly=True,
        samesite="Lax",
        max_age=900,
    )
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
