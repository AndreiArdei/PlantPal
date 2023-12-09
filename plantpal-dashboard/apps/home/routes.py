# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from collections import defaultdict

from decouple import config
from werkzeug.utils import secure_filename, redirect

from apps.clasifier import classify_image
from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
import sqlite3


@blueprint.route('/API/Plants')
@login_required
def plants():
    sql = '''
        SELECT Name, RequiredWater, RequiredLight
        FROM Plant
        ORDER BY Name;
    '''

    con = sqlite3.connect('identifier.sqlite')
    cur = con.cursor()

    return jsonify(
        [{"Name": name, "ReqWater": reqWater, "ReqLight": reqLight} for name, reqWater, reqLight in cur.execute(sql)])


@blueprint.route('/final', methods=['POST'])
@login_required
def finalPart():
    selection = request.form.get('selectUnkn')
    family = request.form.get('family')
    reqWater = request.form.get('reqWat')
    reqSun = request.form.get('reqSun')

    con = sqlite3.connect('identifier.sqlite')

    if selection is None:
        selection = family
        sql1 = '''
            INSERT INTO Plant (Name, RequiredWater, RequiredLight) 
            VALUES (?, ?, ?);
        '''
        cur = con.cursor()
        cur.execute(sql1, (family, reqWater, reqSun))

    sql = '''
        UPDATE PlantPal
        SET PlantID = (
            SELECT Plant.PlantID
            FROM Plant
            WHERE Name = ?
            LIMIT 1)
        WHERE PlantPalID = ?;
    '''

    cur = con.cursor()
    cur.execute(sql, (selection, 1))

    return redirect('/index.html')


@blueprint.route('/API/LastWater')
@login_required
def lastWater():
    plantID = request.args.get('plantID')

    if plantID is None:
        raise ValueError('Request did not provide plantID')

    sql = '''
        SELECT strftime('%s','now') - strftime('%s',s.MeasuredAt)
        FROM SensorData s
        WHERE (
            SELECT m.Data
            FROM SensorData m
            WHERE s.Data-m.Data > 0.5
              AND s.SensorName = 'LoadCell'
            ORDER BY m.MeasuredAt DESC
            )
            AND s.SensorName = 'LoadCell'
            AND s.PlantPalID = ?
        ORDER BY s.MeasuredAt DESC
        LIMIT 1;
        '''

    con = sqlite3.connect('identifier.sqlite')
    cur = con.cursor()

    return jsonify([{'time': time} for time in cur.execute(sql, (plantID,))])


@blueprint.route('/API/PlantCount')
@login_required
def plantCount():
    sql = \
        '''
        SELECT DISTINCT COUNT(PlantPalID)
        FROM PlantPal
    '''
    con = sqlite3.connect('identifier.sqlite')
    cur = con.cursor()

    return jsonify([{"PlantPals": plantPals} for plantPals in cur.execute(sql)])


@blueprint.route('/API/contCapacity')
@login_required
def containerCapacity():
    plantID = request.args.get('plantID', type=int)

    if plantID is None:
        raise ValueError('Request did not provide plantID')

    con = sqlite3.connect('identifier.sqlite')
    cur = con.cursor()

    sql = '''
        SELECT WaterVolume
        FROM PlantPal
        WHERE PlantPalID = ?
        LIMIT 1
    '''

    return jsonify([{"waterVolume": WaterVolume} for WaterVolume in cur.execute(sql, (plantID,))])


@blueprint.route('/API/historicalData')
@login_required
def historicalData():
    # time in seconds
    plantID = request.args.get('plantID', type=int)
    timespan = request.args.get('date', default=0, type=int)

    if plantID is None:
        raise ValueError('Request did not provide plantID')

    con = sqlite3.connect('identifier.sqlite')
    cur = con.cursor()

    sql = '''
        SELECT WaterAmount, WateredAt 
        FROM WaterHistory 
        WHERE PlantPalID = ? 
          '''

    if timespan == 0:
        sql += " ORDER BY WateredAt DESC"
        sql += " LIMIT 1"
        params = (plantID,)
    else:
        sql += "AND WateredAt >= (SELECT strftime(\'%s\',\'now\') - ?)"
        sql += " ORDER BY WateredAt DESC"
        params = (plantID, timespan)

    return jsonify([{"amount": amount, "time": time} for amount, time in cur.execute(sql, params).fetchall()])


@blueprint.route('/API/sensorName')
@login_required
def sensorNames():
    sql = '''
        SELECT DISTINCT SensorName
        FROM SensorData
        WHERE PlantPalID = ?
    '''

    con = sqlite3.connect('identifier.sqlite')
    cur = con.cursor()

    return jsonify([{'name': sensorName} for sensorName in cur.execute(sql, (1,))])


@blueprint.route('/API/sensorData')
@login_required
def sensorData():
    types = request.args.get('type', type=str)
    limit = request.args.get('limit', default=1, type=int)
    plantPalID = request.args.get('plantID', type=int)

    if plantPalID is None:
        raise ValueError("Request did not provide plantID")

    sql = \
        '''
        SELECT SensorName, Data, strftime('%s',MeasuredAt)
        FROM SensorData
        WHERE PlantPalID = ?
        '''
    if types is not None:
        params = (plantPalID, types, limit)
        sql += ' AND upper(SensorName) = upper(?) '
    else:
        params = (plantPalID, limit)

    sql += '''
        ORDER BY  MeasuredAt 
        LIMIT ?
    '''

    con = sqlite3.connect('identifier.sqlite')
    cur = con.cursor()

    results = defaultdict(list)
    for sensorName, data, time in cur.execute(sql, params).fetchall():
        results[sensorName].append({"value": data, "date": int(time)*1000})

    return results


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# ------- AI STUFF -------- #
@blueprint.route('/uploader', methods=['GET', 'POST'])
@login_required
def uploadFile():
    # check if the post request has the file part
    if 'photo' not in request.files:
        raise ValueError('No file part')

    file = request.files['photo']
    if file.filename == '':
        raise ValueError('No selected file')

    if fileAllowed(file.filename):
        filename = secure_filename(file.filename)
        file.save(filename)
        return redirect('/AI_Classify?name=' + filename)
    raise ValueError("File not allowed")


@blueprint.route('/API/classify')
@login_required
def classifier():
    filename = request.args.get('filename')
    return jsonify(classify_image(filename))


# Helper - Extract current page name from request
def get_segment(requests):
    try:

        segment = requests.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


def fileAllowed(filename):
    return filename.rsplit('.', 1)[1].lower() in config('ALLOWED_EXTENSIONS').split(',')
