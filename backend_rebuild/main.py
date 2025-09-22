from app import create_app
from flask_cors import CORS
from flask import jsonify, g
from libs.utils import auth_required

app=create_app()


@app.route('/')
def hello():
    return 'howdy'

@app.route('/protected', methods=['GET'])
@auth_required
def protected():
    return jsonify({
        "message": "You have access!",
        "firebase_id": g.firebase_id
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
