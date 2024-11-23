from flask import Flask, render_template, send_from_directory
import os
import mysql.connector

app = Flask(__name__)

UPLOAD_FOLDER = './papers/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'whatever your username is',
    'password': 'whatever your password is',
    'database': 'scientific_journal'
}

@app.route('/')
def index():
    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Fetch file data from the database
    cursor.execute("SELECT Title, Authors,Link FROM journals")
    files = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    # Serve the file for download
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
