import __future__
import os
import sys

from flask import jsonify, Blueprint, request, render_template

import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, status_response_ok, status_response_fail
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

from modules import cluster_handler

cluster = Blueprint('cluster', __name__)


@cluster.route('/clusters', methods=['GET'])
def clusters_show():
    return render_template("cluster.html", items=cluster_handler.list())


@cluster.route('/cluster', methods=['GET', 'POST', 'DELETE'])
def cluster_operation():
    logger.info("action="+request.method)
    if request.method == 'GET':  # TODO
        return jsonify({"cluster": "get"})
    elif request.method == 'POST':
        if "name" not in request.form or "daemon_url" not in request.form:
            logger.warn("cluster post without enough data")
            status_response_fail["error"] = "cluster operation post without enough data"
            status_response_fail["data"] = jsonify(request.form)
            return jsonify(status_response_fail)
        else:
            logger.debug(request.form['name'])
            logger.debug(request.form['daemon_url'])
            if cluster_handler.create(name=request.form['name'],
                                   daemon_url=request.form['daemon_url']):
                logger.debug("cluster POST successfully")
                return jsonify(status_response_ok)
            else:
                logger.debug("cluster POST failed")
                return jsonify(status_response_fail)
    elif request.method == 'DELETE':
        if "id" not in request.form or not request.form["id"]:
            logger.warn("cluster operation post without enough data")
            status_response_fail["error"] = "cluster delete without " \
                                          "enough data"
            status_response_fail["data"] = jsonify(request.form)
            return jsonify(status_response_fail)
        else:
            logger.debug(request.form["id"])
            logger.debug("cluster delete with id="+request.form["id"])
            if cluster_handler.delete(id=request.form["id"]):
                return jsonify(status_response_ok)
            else:
                return jsonify(status_response_fail)
    else:
        status_response_fail["error"] = "unknown operation method"
        status_response_fail["data"] = jsonify(request.form)
        return jsonify(status_response_fail)
