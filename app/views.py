from flask import Flask, request, jsonify, render_template, session, \
    make_response
from .models import Promo_code, db
from . import promoapp
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import geopy.distance
import random
import string
geolocator = Nominatim()

@promoapp.route('/', methods=['GET'])
def index():
    """
    This endpoint will return the API documentation
    """
    return render_template('index.html')

@promoapp.route('/generate_code', methods=['POST'])
def generate():
    """This end point is for generating a promo code"""

    data = request.json
    code = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))

    promo_code = Promo_code.query.filter_by(code=code).first()
    if promo_code is None:
        promo_code = Promo_code(code=code,
                                event=data['event'],
                                expiry_date=datetime.utcnow() + timedelta(days=2),
                                status='active',
                                price=data['price'],
                                radius=data['radius'])
        db.session.add(promo_code)
        db.session.commit()
        return jsonify({'code': promo_code.code,
                        'date now': datetime.utcnow() + timedelta(days=2),
                        'status': 'pass',
                        'message': 'promo code generated successfully'
                        }), 201
    return jsonify({'status': 'fail',
                    'message': 'Promo code already exists'
                    }), 200

@promoapp.route('/promo_code/<int:id>', methods=['PUT'])
def deactivate(id):
    """This end point is for deactivating a promo code"""

    promo_code = Promo_code.query.filter_by(id=id).first()
    if promo_code is not None:
        promo_code2 = Promo_code.query.filter_by(id=id, status='active').first()
        if promo_code2 is not None:
            promo_code.status = 'deactivated'
            db.session.commit()
            return jsonify({'status': 'pass', 'message': 'promo_code deactivated'}), 201
        return jsonify({'status': 'fail', 'message': 'code is already inactive'})
    return jsonify({'status': 'fail',
                    'message': 'code doesnot exist'}), 404

@promoapp.route('/all_promo_codes', methods=['GET'])
def view_promo_codes():
    """This end point is for viewing all promo codes"""

    results = []
    promo_codes = Promo_code.query.filter_by().all()
    for codes in promo_codes:
        result = {
            'id': codes.id,
            'code': codes.code,
            'event': codes.event,
            'status': codes.status,
            'price': codes.price
        }
        results.append(result)
        if datetime.utcnow() > codes.expiry_date:
            codes.status = 'expired'
    if len(results) > 0:
        return jsonify({'promo_codes': results,
                        'count': str(len(results)),
                        'status': 'pass',
                        'message': 'promo codes found'
                        }), 200
    return jsonify({'count': '0','status': 'fail',
                    'message': 'no promo codes found'
                    }), 404

@promoapp.route('/active_promo_codes', methods=['GET'])
def view_active_promo_codes():
    """This end point is for viewing all active promo codes"""

    results = []
    promo_codes = Promo_code.query.filter_by(status='active').all()
    for codes in promo_codes:
        result = {
            'id': codes.id,
            'code': codes.code,
            'event': codes.event,
            'status': codes.status,
            'price': codes.price
        }
        results.append(result)
    if len(results) > 0:
        return jsonify({'promo_codes': results,
                        'count': str(len(results)),
                        'status': 'pass',
                        'message': 'active promo codes found'
                        }), 200
    return jsonify({'count': '0','status': 'fail',
                    'message': 'no active promo codes found'
                    }), 404

@promoapp.route('/test_validity', methods=['POST'])
def test_validity():
    """This end point is to test the validity of a promo code"""

    data = request.json
    promo_code = Promo_code.query.filter_by(code=data['code']).first()
    if promo_code is not None:
        origin = Promo_code.query.filter_by(event=data['origin']).first()
        destination = Promo_code.query.filter_by(event=data['destination']).first()

        try:
            origin_distance = geolocator.geocode(data['origin'])
            origin_distance_codes = (origin_distance.latitude, origin_distance.longitude)

            destination_distance = geolocator.geocode(data['destination'])
            destination_distance_codes = (destination_distance.latitude, destination_distance.longitude)

            event = geolocator.geocode(promo_code.event)
            event_codes = (event.latitude, event.longitude)

            event_origin_distance = geopy.distance.vincenty(origin_distance_codes, event_codes).km
            event_destination_distance = geopy.distance.vincenty(destination_distance_codes, event_codes).km

            if origin or destination is not None or \
                event_origin_distance < promo_code.radius or \
                event_destination_distance < promo_code.radius:
                return jsonify({'promo_code details': dict(id=promo_code.id,
                                                       code=promo_code.code,
                                                       event=promo_code.event,
                                                       expiry_data=promo_code.expiry_date,
                                                       status=promo_code.status,
                                                       price=promo_code.price),
                            'polyline':data['destination'] + data['origin']}), 200
            return jsonify({'status':'fail', 'message':'Promo code is not valid'}),400
        except:
            return jsonify({"Error with the location entered"})

    return jsonify({'status': 'fail',
                    'message': 'code doesnot exist'}), 404
