from flask import Blueprint, request, jsonify
from datetime import datetime
from tabulate import tabulate
from babel.numbers import format_currency
import requests

bp = Blueprint("telegram_message", __name__)

@bp.route("/messageToTelegram", methods=["POST"])
def messageToTelegram():
    data = request.get_json()
    customer = data.get("customer", {})
    items = data.get("items", [])

    token = "7887654399:AAFpPsAFTYxT3NfPDFIvqUYpctlhfRYD794"
    chat_id = "1331584819"

    cart_list = [[i["title"], i["quantity"], f"${float(i['price']):.2f}"] for i in items]
    table = tabulate(cart_list, headers=["Item", "Qty", "Price"], tablefmt="grid")

    dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = (
        f"<b>✅ New Order Received</b>\n\n"
        f"<b>📅 Date:</b> {dateTime}\n"
        f"<b>👤 Name:</b> {customer.get('fullName')}\n"
        f"<b>📞 Phone:</b> {customer.get('number')}\n"
        f"<b>📧 Email:</b> {customer.get('email')}\n"
        f"<b>📍 Address:</b> {customer.get('address')}\n"
        f"<b>💳 Payment Method:</b> {customer.get('payMethod')}\n"
        f"<b>🚚 Delivery Method:</b> {customer.get('deliveryMethod')}\n\n"
        f"<pre>{table}</pre>\n\n"
        f"<b>💰 Total:</b> {format_currency(customer.get('totalAmount', 0), 'USD', locale='en_US')}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    r = requests.post(url, data=payload)
    print("Telegram Status:", r.status_code, "Response:", r.text)
    return {"message": "Telegram Sent"}, 200
