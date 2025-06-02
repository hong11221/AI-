from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)
DATA_FILE = "routes.json"

@app.route("/")
def home():
    return "서버가 정상 작동 중입니다!"

@app.route("/map/<place>")
def map_view(place):
    if not os.path.exists(DATA_FILE):
        return render_template("map.html", place=place, routes=[])

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        all_routes = json.load(f)

    # ✅ JS에서 기대하는 구조 유지: { "user": ..., "route": [...] }
    matched_routes = [
        r for r in all_routes if any(place in addr for addr in r.get("route", []))
    ]

    return render_template("map.html", place=place, routes=matched_routes)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()
    if not data or "route" not in data or "user" not in data:
        return {"error": "Invalid data format"}, 400

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        all_routes = json.load(f)

    all_routes.append(data)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_routes, f, ensure_ascii=False, indent=2)

    return {"message": "경로 업로드 완료!"}

@app.route("/api/recommend/<place>")
def api_recommend(place):
    if not os.path.exists(DATA_FILE):
        return {"place": place, "matched_routes": []}, 200

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        all_routes = json.load(f)

    matched_routes = [
        r for r in all_routes if any(place in addr for addr in r.get("route", []))
    ]

    return {"place": place, "matched_routes": matched_routes}, 200

if __name__ == "__main__":
    print("🔥 Flask 앱 실행 시작!")
    app.run(debug=True)



if __name__ == '__main__':
    print("🔥 Flask 앱 실행 시작!")
    app.run(debug=True)
