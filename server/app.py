#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>' , methods=['PATCH'])
def patch_bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        data = request.form
        new_name = data.get('name')
        if new_name:
            bakery.name = new_name
            db.session.commit()
            return make_response(bakery.to_dict()),200
        else:
            return make_response({'error':'Not found'},404)
    else:
        return make_response ({'error':'bakery not found'},404)
    

@app.route('/baked_goods', methods=['POST'])
def create_baked_goods():
    data = request.form
    name = data.get('name')
    price = data.get('price')
    bakery_id = data.get('bakery_id')
    if not name or not price or not bakery_id:
        return make_response({'error': 'Missing field'}, 404)
    new_baked_goods = BakedGood(name= name, price = price, bakery_id=bakery_id)
    db.session.add(new_baked_goods)
    db.session.commit()
    return make_response(new_baked_goods.to_dict(), 201)
@app.route('/baked_goods/<int:id>',methods=['DELETE'])
def delete_baked_goods(id):
    baked_goods = BakedGood.query.filter_by(id=id).first()
    if baked_goods:
        db.session.delete(baked_goods)
        db.session.commit()
        return make_response({'message':f'baked goods with id {id} successfully deleted'},200)
    else:
        return make_response({'error':'Baked goods not found'},404)
    
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)