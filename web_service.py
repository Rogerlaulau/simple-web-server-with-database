'''
This servers as the presentation layer

Route 1 - list customers with able to search by first name, last name and order by credit limit
Route 2 - list employees with able to search by first name, last name and order by last name
Route 3 - list orders with able to search by customer first name, last name and order by order date or customer last name
Route 4 - create new product

Features:
 - basic authorization
 - support 20 concurrent queries
 - support cross origin resource sharing
 - error handling e.g. requested URL not found

To run the web service:
python3 web_service.py
'''



from flask import Flask, request, jsonify, make_response
from flask.wrappers import Response
from flask_cors import CORS
from functools import wraps
from waitress import serve
import traceback
import connect_DB as dao

app = Flask(__name__)
CORS(app)

# Configuration
host = '0.0.0.0'
port = 8080
max_upload_size = 4096
threads = 20
cleanup_interval = 10
channel_timeout = 60
timeout_sec = 5

auth_username = 'rogerlau' 
auth_password = 'rogerlau'


#this is a HTTP Basic Authentication that is used for each endpoint
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == auth_username and auth.password == auth_password:
            return f(*args, **kwargs)
        return make_response('Could not verify\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated

@app.errorhandler(404)
def error_404(error):
    print(f'{error} - {request.url}')
    response = dict(status=0, message="404 Not Found")
    return jsonify(response), 404

@app.errorhandler(Exception)
def error_500(error):
    print(traceback.format_exc())
    response = {'status':0, 'message':str(error)}
    return response, 500


@app.route("/status",methods=["GET"])
def status():
    print(f'/status')
    result = {}
    result['status'] = 1
    result['data'] = "successful connection"
    return jsonify(result)


@app.route("/get_customer", methods=["POST"])
@auth_required
def get_customer():
    data = request.json
    print(f"/get_customer: {data}")

    response = dao.get_customers(data["last_name"], data["first_name"])

    result = {}
    result['status'] = 1
    result['data'] = response
    return jsonify(result)


@app.route("/get_employee", methods=["POST"])
@auth_required
def get_employee():
    data = request.json
    print(f"/get_employee: {data}")

    response = dao.get_employees(data["last_name"], data["first_name"])

    result = {}
    result['status'] = 1
    result['data'] = response
    return jsonify(result)


@app.route("/get_order", methods=["POST"])
@auth_required
def get_order():
    data = request.json
    print(f"/get_order: {data}")

    response = dao.get_orders(data["last_name"], data["first_name"])

    result = {}
    result['status'] = 1
    result['data'] = response
    return jsonify(result)


@app.route("/create_product", methods=["POST"])
@auth_required
def create_product():
    data = request.json
    print(f"/create_product: {data}")

    response = dao.create_product(
        data["product_code"], 
        data["product_name"],
        data["product_line"],
        data["product_scale"],
        data["product_vendor"],
        data["product_description"],
        data["quantity_in_stock"],
        data["buy_price"],
        data["msrp"]
    )

    result = {}
    result['status'] = 1
    result['data'] = response
    return jsonify(result)




if __name__ == '__main__':
    print(f'Web service started at port: {port}')
    serve(app, host=host, port=port, threads=threads, cleanup_interval=cleanup_interval, channel_timeout=channel_timeout) 