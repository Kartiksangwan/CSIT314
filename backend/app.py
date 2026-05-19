from flask import Flask
from flask_cors import CORS
from database import db
from routes.auth import auth_bp
from routes.candidates import candidates_bp
from routes.employers import employers_bp
from routes.jobs import jobs_bp
from routes.search import search_bp
from routes.messages import messages_bp
from routes.bookmarks import bookmarks_bp
from routes.offers import offers_bp
from routes.recommendations import recommendations_bp

app = Flask(__name__)

# Config
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/talent_matching'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, supports_credentials=True)

db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(candidates_bp, url_prefix='/api/candidates')
app.register_blueprint(employers_bp, url_prefix='/api/employers')
app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
app.register_blueprint(search_bp, url_prefix='/api/search')
app.register_blueprint(messages_bp, url_prefix='/api/messages')
app.register_blueprint(bookmarks_bp, url_prefix='/api/bookmarks')
app.register_blueprint(offers_bp, url_prefix='/api/offers')
app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')

@app.route('/')
def index():
    return {'message': 'Talent Matching API is running'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
