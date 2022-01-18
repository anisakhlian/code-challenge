from flask import Blueprint, request, abort, g, current_app, jsonify
from models import db_session, PgDocument

documents_mod = Blueprint('documents', __name__)


@documents_mod.route('', methods=['POST'])
def create():
    request_data = request.get_json()

    parent_id = request_data.get('parent_id')
    if parent_id:
        parent_document = PgDocument.query.get(parent_id)
        if not parent_document:
            abort(404, "resource not found")

    document = PgDocument(
        title=request_data.get('title', ''),
        body=request_data.get('body', ''),
        parent_id=parent_id
    )
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

    documents = PgDocument.query \
        .filter(PgDocument.parent_id.is_(None)) \
        .filter(trash_filter)

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
    parent_id = request_data.get('parent_id')
    if parent_id:
        parent_document = PgDocument.query.get(parent_id)
        if not parent_document:
            abort(404, "resource not found")

    for field in request_data.keys():
        setattr(document, field, request_data[field])

    db_session.add(document)
    db_session.commit()

    if 'deleted_at' in request_data and document.children:
        _propagate_delete_status(document, request_data.get('deleted_at'))

    return jsonify({'data': document.serialize()}), 200


@documents_mod.route('/<string:document_id>', methods=['DELETE'])
def delete(document_id):
    document = PgDocument.query.get(document_id)
    if not document:
        abort(404, "resource not found")

    db_session.delete(document)
    db_session.commit()

    return jsonify({'message': 'OK'}), 200
