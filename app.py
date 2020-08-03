'''Flask app for Cupcakes'''

from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLCHEMY_ECHO'] = True

connect_db(app)

@app.route('/api/cupcakes')
def list_all_cupcakes():
    ''' Return JSON about all cupcakes {cupcakes: [{id, flavor, size, rating, image}, ...]}'''

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def list_single_cupcake(cupcake_id):
    ''' Return JSON about a single cupcake {cupcake: {id, flavor, size, rating, image}}'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()
    
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_single_cupcake():
    ''' Create cupcake from form data.
    Return JSON of newly created cupcake {cupcake: {flavor, size, rating, image}}.'''

    flavor = request.json['flavor'] 
    size = request.json['size'] 
    rating = request.json['rating'] 
    image = request.json['image'] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)
    # CODE REVIEW - ADDRESSED: bug. write a test that will fail, fix bug,
    # BUG: what happens when we create a cupcake but uses default, test that defaults are used
    # evaluate test for more pessimistic cases (how to handle when something goes wrong)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    ''' Update cupcake; assume entire cupcake object is passed. 
    Return JSON of updated cupcake as {cupcake: {id, flavor, size, rating, image}}.'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # Collect new properties
    cupcake.flavor = request.json['flavor'] 
    cupcake.size = request.json['size'] 
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']
    # TODO - How can we update only the 'new'/different values compared with the instance we already have?

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    ''' Delete a cupcake. 
    Return JSON of deleted cupcake as {message: "Deleted"}.'''

    # Get and delete cupcake
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({'message': 'Deleted'})