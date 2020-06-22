import json

from flask import jsonify, request

from app.model_factory import ModelFactory


def datatable_search():
    args = request.values.get("args")
    if args:
        args = json.loads(args)
    else:
        args = {}

    data = ModelFactory.customer.datatable_search(args)

    customers = []
    for customer in data['customers']:
        cust_dict = customer.row2dict()
        cust_dict['address'] = customer.address.row2dict()
        cust_dict['address']['city'] = customer.address.city.row2dict()
        cust_dict['address']['city']['country'] = customer.address.city.country.row2dict()
        customers.append(cust_dict)

    response = {
        'draw':  args.get('draw'),
        'recordsTotal': data['records_total'],
        'recordsFiltered': data['records_filtered'],
        'data': customers,
    }
    return jsonify(response)
