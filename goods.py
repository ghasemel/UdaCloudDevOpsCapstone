
import uuid
from http.client import BAD_REQUEST, CREATED, OK, NOT_FOUND, INTERNAL_SERVER_ERROR

from app import app, db, request, jsonify, log
from models import Goods




@app.route('/health')
def health_status():
    return {"status": "OK"}


@app.route('/api/v1/goods', methods=['POST'])
def add():
    """ add a new merchandise """
    if request.method == 'POST':
        try:
            merchandise = request.json
            log.info(f"add merchandise: {merchandise}")

            new_merchandise = Goods(
                name=merchandise["name"],
                description=merchandise["description"],
                stock=merchandise["stock"],
                price=merchandise["price"]
            )
            log.debug(f"json merchandise successfully decoded to object: {new_merchandise.json()}")

            db.session.add(new_merchandise)
            log.debug("merchandise successfully added to session")

            db.session.commit()

            log.debug(f"add merchandise with id: {new_merchandise.id}")

            return new_merchandise.json(), CREATED
        except Exception as e:
            log.error(e)
            return {'response': 'internal error'}, INTERNAL_SERVER_ERROR


@app.route('/api/v1/goods/<merchandise_id>')
def get(merchandise_id):
    try:
        uuid.UUID(str(merchandise_id))
    except ValueError:
        return {'response': f'invalid id: {merchandise_id}'}, BAD_REQUEST

    try:
        log.info(f"get merchandise with id {merchandise_id}")
        merchandise = Goods.query.filter_by(id=merchandise_id).first()

        if merchandise is None:
            return '', NOT_FOUND

        return merchandise.json(), OK

    except Exception as e:
        log.error(e)
        return {'response': 'internal error'}, INTERNAL_SERVER_ERROR


@app.route('/api/v1/goods/<merchandise_id>', methods=['DELETE'])
def delete(merchandise_id):
    try:
        uuid.UUID(str(merchandise_id))
    except ValueError:
        return {'response': f'invalid id: {merchandise_id}'}, BAD_REQUEST

    try:
        log.info(f"delete merchandise with id {merchandise_id}")
        merchandise = Goods.query.filter_by(id=merchandise_id).first()
        if merchandise is None:
            return '', NOT_FOUND

        db.session.delete(merchandise)
        db.session.commit()

        return '', OK
    except Exception as e:
        log.error(e)
        return {'response': 'internal error'}, INTERNAL_SERVER_ERROR


@app.route('/api/v1/goods/<merchandise_id>', methods=['PUT'])
def update(merchandise_id):
    try:
        uuid.UUID(str(merchandise_id))
    except ValueError:
        return {'response': f'invalid id: {merchandise_id}'}, BAD_REQUEST

    try:
        req_body = request.json
        log.debug(f"insert merchandise: {req_body}")

        log.info(f"update merchandise with id {merchandise_id}")
        merchandise = Goods.query.filter_by(id=merchandise_id).first()
        if merchandise is None:
            return '', NOT_FOUND

        merchandise.name = req_body["name"]
        merchandise.description = req_body["description"]
        merchandise.stock = req_body["stock"]
        merchandise.price = req_body["price"]

        db.session.commit()

        return '', OK
    except Exception as e:
        log.error(e)
        return {'response': 'internal error'}, INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
