from re import A, I
import pymysql
from app import app
from config import mysql
from flask import jsonify
import pandas as pd
from flask import flash, request
import json

@app.route('/create', methods=['POST'])
def create_user():
    try:        
        _json = request.json
        if  request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            # json 拆分匯入SQL
            sqlQuery = "INSERT INTO cdss(Predict, Patient, Application_number, Strain, Bed, Prediction) VALUES( %s, %s, %s, %s, %s, %s)" 
            bindData = ((i['Predict'], i['Patient'], i['Application_number'], i['Strain'], i['Bed'], i['Prediction']) for i in _json) 
            cursor.executemany(sqlQuery, bindData)
            conn.commit()

            respone = jsonify('User added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()     

@app.route('/createtxt', methods=['POST'])
def createtxt_user():
    try:        
        txt = request.get_data().decode("utf-8")
        txt = pd.DataFrame([i.split(',') for i in txt.split('\r\n')[1:]], columns=txt.split('\r')[0].split(','))
        _json = txt.to_json(orient="records") # 輸出 json 格式
        _json = json.loads(_json) #重新load json ，為了讓python 讀json檔
        if  request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            # json 拆分匯入SQL
            sqlQuery = "INSERT INTO cdss(Predict, Patient, Application_number, Strain, Bed, Prediction) VALUES( %s, %s, %s, %s, %s, %s)" 
            bindData = ((i['Predict'], i['Patient'], i['Application_number'], i['Strain'], i['Bed'], i['Prediction']) for i in _json) 
            cursor.executemany(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('User added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  
     
@app.route('/user')
def user():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM cdss")
        userRows = cursor.fetchall()
        respone = jsonify(userRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/user/<int:user_id>')
def user_details(user_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM cdss WHERE Patient =%s", user_id)
        userRow = cursor.fetchall()
        respone = jsonify(userRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        _json = request.json
        _Predict = _json['Predict']
        _Patient= _json['Patient']
        _Application_number = _json['Application_number']
        _Strain = _json['Strain']
        _Bed = _json['Bed']
        _Prediction = _json['Prediction']

        if _Predict and _Patient and _Application_number and _Strain and _Bed and _Prediction and request.method == 'PUT':			
            sqlQuery = ("UPDATE cdss SET Predict=%s, Patient=%s, Application_number=%s, Strain=%s, Bed=%s, Prediction=%s WHERE Id=%s")
            bindData = ( _Predict, _Patient, _Application_number, _Strain,_Bed, _Prediction, user_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('User updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM cdss WHERE id =%s", user_id)
		conn.commit()
		respone = jsonify('User deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()