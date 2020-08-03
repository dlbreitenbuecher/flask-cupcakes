"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLCHEMY_ECHO'] = True

connect_db(app)

@app.route('/api/cupcakes')
def list_all_cupcakes():
    """ Return JSON about all cupcakes {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def list_single_cupcake(cupcake_id):
    """ Return JSON about a single cupcake {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()
    
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_single_cupcake():
    """ Create cupcake from form data & return it
    
    Return JSON to of newly created cupcake {cupcake: {flavor, size, rating, image}}"""

    flavor = request.json['flavor'] 
    size = request.json['size'] 
    rating = request.json['rating'] 
    image = request.json['image'] # TODO: is is RESTful practice to include the default URL here too

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    # confirm successful add; return with status code 201 CREATE
    return (jsonify(cupcake=serialized), 201)

