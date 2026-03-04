"""
LEGAL-DISCOVERY Domain Service (7777Hz)
Part of PARALEGAL-PI recursive network
Handles: Document analysis, exhibit organization, evidence extraction
"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-legal-discovery-7777hz')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///legal_discovery.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Fix Railway PostgreSQL URL
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace(
        'postgres://', 'postgresql://', 1
    )

db = SQLAlchemy(app)

# Import routes after db initialization
from routes import api
app.register_blueprint(api, url_prefix='/api')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'domain': 'legal_discovery',
        'frequency': '7777Hz',
        'capabilities': [
            'document_analysis',
            'exhibit_organization',
            'evidence_extraction',
            'police_report_analysis'
        ]
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 7777))
    app.run(host='0.0.0.0', port=port, debug=True)
