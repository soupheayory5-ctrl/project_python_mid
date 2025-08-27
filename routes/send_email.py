# routes/send_email.py
from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
from mail_config import mail   # ← FIX: import from mail_config, not ext_mail
from tabulate import tabulate
from babel.numbers import format_currency
from datetime import datetime

bp = Blueprint("send_email", __name__)

@bp.route("/sendEmail", methods=["POST"])
def send_email():
    try:
        data = request.get_json(force=True)
        customer = data["customer"]
        items = data["items"]

        # Build the table
        cart_list = [[i['title'], i['quantity'], f"${float(i['price']):.2f}"] for i in items]
        table = tabulate(cart_list, headers=["Item", "Qty", "Price"], tablefmt="grid")

        html_content = (
            f"<b>📅 Date:</b> {datetime.now():%d/%m/%Y %H:%M:%S}<br>"
            f"<b>👤 Name:</b> {customer.get('fullName')}<br>"
            f"<b>📞 Phone:</b> {customer.get('number')}<br>"
            f"<b>📧 Email:</b> {customer.get('email')}<br>"
            f"<b>📍 Address:</b> {customer.get('address')}<br>"
            f"<b>💳 Payment Method:</b> {customer.get('payMethod')}<br>"
            f"<b>🚚 Delivery Method:</b> {customer.get('deliveryMethod')}<br><br>"
            f"<pre>{table}</pre><br>"
            f"<b>💰 Total:</b> {format_currency(customer.get('totalAmount', 0), 'USD', locale='en_US')}<br><br>"
            "We will contact you soon!"
        )

        # sender will default to MAIL_DEFAULT_SENDER (or MAIL_USERNAME) from app config
        msg = Message(
            subject="✅ Your Order Confirmation",
            recipients=[customer["email"]],
            html=html_content,
        )

        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        current_app.logger.exception("Email send failed")
        return jsonify({"error": str(e)}), 500
