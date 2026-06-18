from flask import Flask,jsonify
from models import db ,TokenBlocklist
from auth_routes import auth_bp
from flask_migrate import Migrate 
import config
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from extensions import jwt, limiter
from flasgger import Swagger
import logging
from flask import request
import os 
###for testing purpose we had unlimit the user 
load_dotenv()

app = Flask(__name__)
app.config.from_object(config.Config)
jwt.init_app(app)
limiter.init_app(app)
##for logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# swagger = Swagger(app) ##it is only doing the basic tasks not doing authentication so we will do next step in it
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Campus Management API",
        "description": "Campus API Documentation",
        "version": "1.0"
    },

    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter JWT Token as: Bearer <your_token>"
        }
    }
}

swagger = Swagger(
    app,
    config=swagger_config,
    template=swagger_template
)
##just put /apidocs after url 




app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)

app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):

    jti = jwt_payload["jti"]

    token = TokenBlocklist.query.filter_by(
        jti=jti
    ).first()

    return token is not None
# app.config.from_object(config)

db.init_app(app)
migrate = Migrate(app, db)

# import routes
from routes.student_routes import student_bp
from routes.department_routes import department_bp

app.register_blueprint(student_bp)
app.register_blueprint(department_bp)
app.register_blueprint(
    auth_bp,
    url_prefix="/api/v1/auth"
)
@app.route('/')
def  welcome_topage():
    return "WELCOME TO THE CAMPUS DB"


## not found
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested URL does not exist"
    }), 404

## for the bad request
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad Request",
        "message": "Invalid input provided"
    }), 400

## method not found 
@app.errorhandler(405)
def method_not_found_request(error):
    return jsonify({
        "error": "Method Not Found",
        "message": "Invalid input provided"
    }), 405

##server error
@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "Something went wrong on the server"
    }), 500

###handle sqlalchemy error 
@app.errorhandler(IntegrityError)
def handle_db_error(error):

    db.session.rollback()

    return jsonify({
        "error": "Database Error",
        "message": "Duplicate or invalid data entry"
    }), 400

@app.before_request
def log_request():

    logging.info(
        f"{request.method} {request.path}"
    )

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    # as migration all do this now 

    # app.run(host="0.0.0.0", port=5000,debug=True ,use_reloader = False)
    ##
    ##
    ##atual server looks like app.run(debug=True ,use_reloader = False)
    # app.run(host="0.0.0.0", port=5000,debug=True)
    #to use render we ahve to do this
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )