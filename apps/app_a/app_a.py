from flask import Flask, request
import requests
application = Flask(__name__)


@application.route('/hello')
def hello():
    return 'Hello there'


@application.route('/jobs', methods=['POST'])
def jobs():
    token = request.headers['Authorization']
    data = {"token": token}
    result = requests.post('http://app-b-service:80/auth', data=data)
    plain_result = result.text
    # print(16, result, type(result), dir(result), plain_result, plain_result)
    if plain_result == "density":
        return 'Jobs:\nTitle: Devops\nDescription: Awesome\n'
    else:
        return 'fail'


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)
