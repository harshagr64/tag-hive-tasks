from flask import Flask, request
import sqlite3 as sql
application = Flask(__name__)


@application.route('/auth', methods=['POST'])
def auth():
    # try:
    token = request.form['token']
    con = sql.connect("database.db")
    cur = con.cursor()
    print(16, con, cur)
    querystring = "SELECT username from users where token = '{}' LIMIT 1".format(token)
    result = cur.execute(querystring)
    print(result)
    if result:
        username = result.fetchone()[0]
        print(querystring, result, username)
        con.close()
        return username
    else:
        return 'fail'


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5001)
