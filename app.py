from bson.objectid import ObjectId
from flask import Flask, json, render_template, url_for
import requests
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask import jsonify, request
from werkzeug.utils import redirect


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/blore_house"
mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _location = _json['location']
    _total_sqft = int(_json['total_sqft'])
    _bath = int(_json['bath'])
    _price_in_lacs = float(_json['price_in_lacs'])
    _bhk = int(_json['bhk'])
    _price_per_sqft = float(_json['price_per_sqft'])

    if _location and _total_sqft and _bath and _price_in_lacs and _bhk and _price_per_sqft and request.method == 'POST':
        id = mongo.db.area_prices.insert_one({'location': _location, 'total_sqft': _total_sqft, 'bath': _bath, 'price_in_lacs':_price_in_lacs, 'bhk': _bhk, 'price_per_sqft': _price_per_sqft})
        resp = jsonify("Location added successfully")
        resp.status_code = 200
        return resp

    else:
        return not_found()

@app.route('/locations')
def users():
    users = mongo.db.area_prices.find()
    resp = dumps(users)
    return resp

@app.route('/location/<id>')
def user(id):
    user = mongo.db.area_prices.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_user(id):
    mongo.db.area_prices.delete_one({'_id': ObjectId(id)})
    resp = jsonify("Location deleted successfully")
    resp.status_code = 200
    return redirect('/')
    return resp

@app.route('/update/<id>', methods=['POST', 'GET'])
def update_location(id):
    if request.method == 'POST':
        _id = id
        _location = request.form['location']
        _total_sqft = float(request.form['total_sqft'])
        _bath = int(request.form['bath'])
        _price_in_lacs = float(request.form['price_in_lacs'])
        _bhk = int(request.form['bhk'])
        _price_per_sqft = float(request.form['price_per_sqft'])

        if _location and _total_sqft and _bath and _price_in_lacs and _bhk and _price_per_sqft and request.method == 'POST':
            id = mongo.db.area_prices.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set':  {'location': _location, 'total_sqft': _total_sqft, 'bath': _bath, 'price_in_lacs': _price_in_lacs, 'bhk': _bhk, 'price_per_sqft': _price_per_sqft}})
            resp = jsonify("Location updated successfully")
            resp.status_code = 200
            return redirect('/')
            return resp
        else:
            return not_found()


@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename=filename), code=301)

# Frontend
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        req = requests.get('http://127.0.0.1:800/locations')
        data = json.loads(req.content)
        return render_template('index.html', data=data)
    elif request.method == 'POST':
        _location = request.form['location']
        _total_sqft = int(request.form['total_sqft'])
        _bath = int(request.form['bath'])
        _price_in_lacs = float(request.form['price_in_lacs'])
        _bhk = int(request.form['bhk'])
        _price_per_sqft = float(request.form['price_per_sqft'])
        if _location and _total_sqft and _bath and _price_in_lacs and _bhk and _price_per_sqft and request.method == 'POST':
            id = mongo.db.area_prices.insert_one({'location': _location, 'total_sqft': _total_sqft, 'bath': _bath, 'price_in_lacs': _price_in_lacs, 'bhk': _bhk, 'price_per_sqft': _price_per_sqft})
            resp = jsonify("Location added successfully")
            resp.status_code = 200
            return redirect('/')
        else:
            return not_found()
# End Frontend

@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status' : 404,
        'message' : 'Not Found '+ request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(port=800, debug=True)
