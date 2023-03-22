from datetime import datetime
import json
import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

from invokes import invoke_http
from os import environ

app = Flask(__name__)
CORS(app)

payment_URL = environ.get('payment_URL') or "http://localhost:5005/pay"
read_booking_URL = environ.get('read_booking_URL') or"http://localhost:5002/read_booking"
update_booking_URL = environ.get('update_booking_URL') or "http://localhost:5002/update_booking"
email_URL = environ.get('email_URL') or "http://localhost:5008/sendVerificationEmail"


# @app.route("/getBookingInfo/", methods=['GET'])
# def get_booking_info():
#     booking_id = request.args.get('booking_id')

#     bookingInfo = invoke_http(read_booking_URL + "?booking_id=" + booking_id, method='GET')

#     return bookingInfo


@app.route("/new_payment", methods=['POST'])
def new_payment():
    # retrieve post request from stripe payment intent form
    data = request.get_json()
    app.logger.info(data)
    if ('order_id' in data.keys()):
        order_id = data['order_id']

        data['amount'] = int(float(data['amount']) * 100)
        # get booking
        # bookingInfo = invoke_http(read_booking_URL + '?booking_id=' + booking_id, method='GET')
        # app.logger.info(bookingInfo)
        
        # dummy to input payment price
        # data['price'] = int(float(bookingInfo['price']) * 100)


    # call stripe wrapper microservice
    
    app.logger.info(data)
    payment_intent = invoke_http(payment_URL, method='POST', json=data)
    # r = requests.request("POST", payment_URL, json = data)
    app.logger.info(payment_intent)

    if ('success' in payment_intent.keys()):
        success_data = {
            'order_id': payment_intent['order_id'],
            'payment_status': "Paid",
            'payment_id': payment_intent['payment_id']
        }
        app.logger.info(success_data)
        # update_paymentstatus = invoke_http(
        #     update_booking_URL, method='PUT', json=success_data)
        # app.logger.info(update_paymentstatus)

        # email microservice data
        # email_data = {
        #     "username": data['username'],
        #     "booking_id": data['booking_id'],
        #     "email": data["email"],
        #     "price": format(bookingInfo['price'],'.2f'),
        # }

        # app.logger.info(email_data)

        # call email microservice (POST)
        # invoke_email = invoke_http(email_URL, method='POST', json=email_data)
        # app.logger.info(invoke_email)

        # call email microservice (AMQP)
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking.email",
    #                                     body=json.dumps(email_data),properties=pika.BasicProperties(delivery_mode=2))



    # # invoke error log if encounter code 500 error from stripe_wrapper (Invalid Status)
    # if 'error' in payment_intent.keys() or ('code' in payment_intent.keys() and payment_intent['code'] == 500):
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking.error",
    #                                      body=json.dumps({'error_data': payment_intent, 'errorOrigin': 'stripe', 'datetime': str(datetime.datetime.now())}), properties=pika.BasicProperties(delivery_mode=2))

    return payment_intent


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
