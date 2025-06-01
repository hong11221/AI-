import requests
import json

url = "http://127.0.0.1:5000/upload"

sample_data = [
    {
        "user": "hongd",
        "route": [
            "서울특별시 종로구 세종대로 110",
            "서울특별시 중구 을지로 50",
            "서울특별시 강남구 테헤란로 212"
        ]
    },
    {
        "user": "kim",
        "route": [
            "서울특별시 마포구 양화로 94",
            "서울특별시 용산구 이태원로 179",
            "서울특별시 성동구 왕십리로 125"
        ]
    },
    {
        "user": "lee",
        "route": [
            "서울특별시 송파구 올림픽로 300",
            "서울특별시 동작구 흑석로 105",
            "서울특별시 구로구 디지털로 300"
        ]
    }
]

for data in sample_data:
    res = requests.post(url, json=data)
    print("응답:", json.dumps(res.json(), ensure_ascii=False, indent=2))
