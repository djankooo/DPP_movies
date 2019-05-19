import json

from flask import Flask, request, jsonify
from pip._vendor.msgpack.fallback import xrange

app = Flask(__name__)


class Customer(object):

    def __init__(self, customer_id, customer_name):
        self.customer_id = customer_id
        self.customer_name = customer_name


class Movie(object):

    def __init__(self, movie_id, movie_name):
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.customers = []

    def add_customers(self, customer_id, customer_name):
        self.customers.append(Customer(customer_id, customer_name))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/db/movies', methods=['GET'])
def getAllMovies():
    with open('data.json') as json_file:
        database = json.load(json_file)
        for p in database['movies']:
            print('Movie ID: ' + p['movie_id'])
            print('Movie Name: ' + p['movie_name'])
            for c in p['customers']:
                print('Customer ID: ' + c['customer_id'])
                print('Customer Name: ' + c['customer_name'])
    return jsonify(database)


@app.route('/db/movies/<movie_id>', methods=['GET'])
def getMovie(movie_id):
    with open('data.json') as json_file:
        database = json.load(json_file)
        for p in database['movies']:
            if p['movie_id'] == movie_id:
                return jsonify(p)


@app.route('/db/movies', methods=['POST'])
def createMovie():
    with open('data.json', 'r') as json_file:
        database = json.load(json_file)
    json_file.close()

    print(database)

    dat = Movie(
        request.json['id'],
        request.json['name'],
    )

    database['movies'].append(dat.__dict__)

    print(database)

    with open('data.json', 'w+') as json_file:
        json.dump(database, json_file, indent=4)
    json_file.close()

    return "Movie created"


@app.route('/db/movies/<movieID>', methods=['PUT', 'POST'])
def updateEmp(movieID):
    with open('data.json') as json_file:
        database = json.load(json_file)
        print(database)
        for p in database['movies']:
            if p['movie_id'] == movieID:
                print(movieID)
                p['movie_name'] = request.json['name']
        print(database)
    with open('data.json', 'w+') as json_file:
        json.dump(database, json_file, indent=4)
    json_file.close()

    return 'database updated'


@app.route('/db/movies/<movieID>', methods=['DELETE'])
def deleteEmp(movieID):
    with open('data.json') as json_file:
        database = json.load(json_file)
        db = database['movies']
        for i in xrange(len(db)):
            if db[i]["movie_id"] == movieID:
                db.pop(i)
                break
    with open('data.json', 'w+') as json_file:
        json.dump(database, json_file, indent=4)
    json_file.close()

    return 'movie deleted'


if __name__ == '__main__':
    app.run()
