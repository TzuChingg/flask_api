from msilib import Table
from app import app
from flaskext.mysql import MySQL


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

# SQL Table
# CREATE TABLE cdss(
#     Id int not null  AUTO_INCREMENT,
#     Timestamp Timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     Predict VARCHAR(10),
#     Patient VARCHAR(10),
#     Application_number VARCHAR(20),
#     Strain VARCHAR(256),
#     Bed VARCHAR(10),
#     Prediction int ,
#     PRIMARY KEY (Id)
# );