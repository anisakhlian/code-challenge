from flask import Blueprint, request, abort, g, current_app, jsonify
from models import db_session, PgDocument

documents_mod = Blueprint('documents', __name__)


@documents_mod.route('', methods=['POST'])
def create():
    request_data = request.get_json()
    documents = PgDocument.query.order_by('order').all()
    params = {
        'title': request_data.get('title', ''),
        'body': request_data.get('body', ''),
    }
    if documents:
        params['order'] = documents[-1].order + 1
    document = PgDocument(**params)
    db_session.add(document)
    db_session.commit()

    return jsonify({'data': document.serialize()}), 201


@documents_mod.route('', methods=['GET'])
def collection():
    is_trashed = request.args.get('is_trashed')
    trash_filter = PgDocument.deleted_at.is_(None)
    if is_trashed == 'true':
        trash_filter = PgDocument.deleted_at.isnot(None)

    is_pinned = request.args.get('is_pinned')
    pin_filter = None
    if is_pinned == 'true':
        pin_filter = PgDocument.is_pinned.is_(True)

    documents = PgDocument.query.filter(trash_filter)

    if pin_filter:
        documents = documents.filter(pin_filter)

    allowed_ordered_bys = {
        'title asc': PgDocument.title.asc(),
        'title desc': PgDocument.title.desc(),
    }
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    order_by = allowed_ordered_bys.get(f'{sort} {direction}')

    if order_by is not None:
        documents = documents.order_by(order_by)

    documents = documents.all()

    custom = request.args.get('custom')
    if custom:
        documents = PgDocument.query.order_by('order').all()

    if not documents:
        return jsonify({'data': []}), 200

    for i, document in enumerate(documents):
        documents[i] = document.serialize()

    return jsonify({'data': documents}), 200


@documents_mod.route('/<string:document_id>', methods=['PATCH'])
def update(document_id):
    document = PgDocument.query.get(document_id)
    if not document:
        abort(404, "resource not found")

    request_data = request.get_json()
    order = request_data.get('order')

    if order is not None:
        if order > document.order:
            documents = PgDocument.query.order_by('order').all()
            if order > documents[-1].order:
                abort(400, "order is out of range")
            for i in range(document.order, order):
                prev_document = PgDocument.query.filter(PgDocument.order == i+1).one()
                setattr(prev_document, 'order', i)
        elif order < document.order:
            for i in range(order, document.order):
                prev_document = PgDocument.query.filter(PgDocument.order == i).one()
                setattr(prev_document, 'order', i+1)
        setattr(document, 'order', order)
    else:
        for field in request_data.keys():
            setattr(document, field, request_data[field])

    db_session.add(document)
    db_session.commit()

    return jsonify({'data': document.serialize()}), 200


@documents_mod.route('/<string:document_id>', methods=['DELETE'])
def delete(document_id):
    document = PgDocument.query.get(document_id)
    if not document:
        abort(404, "resource not found")
    documents = PgDocument.query.order_by('order').all()
    for i in range(document.order, documents[-1].order):
        prev_document = PgDocument.query.filter(PgDocument.order == i + 1).one()
        setattr(prev_document, 'order', i)

    db_session.delete(document)
    db_session.commit()

    return jsonify({'message': 'OK'}), 200
