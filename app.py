import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


from flask import Flask, request, Response, render_template
import json
import os

app = Flask(__name__)
DATA_FILE = 'routes.json'

@app.route('/')
def home():
    return "서버가 정상 작동 중입니다!"

@app.route('/upload', methods=['POST'])
def upload_route():
    data = request.get_json()
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        routes = json.load(f)

    routes.append(data)

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(routes, f, ensure_ascii=False, indent=2)

    return Response(
        json.dumps({"message": "경로 업로드 완료!"}, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )

@app.route('/recommend/<place>')
def recommend(place):
    if not os.path.exists(DATA_FILE):
        return Response(
            json.dumps({"place": place, "routes": []}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        all_routes = json.load(f)

    recommended = [r["route"] for r in all_routes if place in r["route"]]

    return Response(
        json.dumps({"place": place, "routes": recommended}, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )

# ✅ 여기가 핵심!
@app.route('/map/<place>')
def map_view(place):
    if not os.path.exists(DATA_FILE):
        return render_template("map.html", place=place, routes=[])
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        all_routes = json.load(f)

    # ❗ 기존 조건: place in r["route"] → ❌
    # ✅ 수정된 조건: place in any(addr for addr in route)
    matched_routes = [r["route"] for r in all_routes if any(place in addr for addr in r["route"])]

    return render_template("map.html", place=place, routes=matched_routes)


if __name__ == '__main__':
    print("🔥 Flask 앱 실행 시작!")
    app.run(debug=True)
