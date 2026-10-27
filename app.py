import json
import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# بيانات الأبواب المحدثة لتناسب الألعاب التفاعلية الثلاث
DOORS = [
    {
        "id": 1,
        "title": "1. Kapı: Büyülü Orman",
        "type": "puzzle",
        "unlocked": True
    },
    {
        "id": 2,
        "title": "2. Kapı: Hafıza Mağarası",
        "type": "memory",
        "unlocked": False
    },
    {
        "id": 3,
        "title": "3. Kapı: Rün Tapınağı",
        "type": "runes",
        "unlocked": False
    }
]

# 1. الواجهة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# 2. فحص حالة الخدمة (Health Check)
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "Gizemli Dünyalar Game"}), 200

# 3. جلب قائمة الأبواب
@app.route('/api/doors', methods=['GET'])
def get_doors():
    return jsonify(DOORS), 200

# 4. التحقق من حل اللغز وفتح الباب التالي
@app.route('/api/check-door', methods=['POST'])
def check_door():
    data = request.get_json() or {}
    door_id = data.get("door_id")
    
    door = next((d for d in DOORS if d["id"] == door_id), None)
    
    if not door:
        return jsonify({"success": False, "message": "Geçersiz kapı!"}), 400

    if not door["unlocked"]:
        return jsonify({"success": False, "message": "Bu kapı henüz kilitli!"}), 403

    # عند إكمال اللغز التفاعلي بنجاح
    next_door = next((d for d in DOORS if d["id"] == door_id + 1), None)
    if next_door:
        next_door["unlocked"] = True
        msg = f"{door_id}. Kapı tamamlandı! Sonraki kapının kilidi açıldı! 🔓"
    else:
        msg = "Tebrikler! Tüm bulmacaları çözdünüz ve Gizemli Dünyaları tamamladınız! 🎉"

    return jsonify({"success": True, "message": msg}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)