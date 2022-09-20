from flask import Blueprint, g, request, jsonify, make_response
import flask

__author__ = 'haiou'
CONN = Blueprint('conn', __name__)


@CONN.route('/import_status', methods=['post'])
def import_status():
    catalog = flask.request.values.get('catalog')
    status = flask.request.values.get('status')
    cookie1 = request.cookies.get('import_status')
    print('首次cookie1', cookie1)
    if int(status) == 0:
        if cookie1:
            if cookie1 == '0':
                print('cookie1', request.cookies.get('import_status'))
                return jsonify(status='fail', error_detail='有任务未完成')
            elif cookie1 == 1:
                resp = make_response('set_cookie')
                resp.set_cookie('import_status', '0')
                print('cookie2', request.cookies.get('import_status'))
                return jsonify(status='success', error_detail=None)
            else:
                return '输入错误'
        else:
            resp = make_response(jsonify(status='success', error_detail=None))
            resp.set_cookie('import_status', '0')
            print('cookie3', request.cookies.get('import_status'))
            return resp

    else:
        if cookie1 == '0':
            resp = make_response('import_status')
            resp.set_cookie('import_status', '1')
            print('cookie4', request.cookies.get('import_status'))
            return jsonify(status='success', error_detail=None)
        else:
            print('cookie5', request.cookies.get('import_status'))
            return jsonify(status='fail', error_detail='有任务未完成')
