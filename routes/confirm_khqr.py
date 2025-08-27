from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

bp = Blueprint("confirm_khqr", __name__)

@bp.route("/confirmKHQR", methods=["POST"])
def confirm_khqr():
    try:
        file = request.files["slip"]
        payload = request.form["payload"]  # if needed
        filename = secure_filename(file.filename)
        save_dir = os.path.join("static", "payments")
        os.makedirs(save_dir, exist_ok=True)
        file.save(os.path.join(save_dir, filename))
        print("✅ KHQR slip received:", filename)
        return jsonify({"message": "Slip received"}), 200
    except Exception as e:
        print("❌ KHQR error:", str(e))
        return jsonify({"error": str(e)}), 500
