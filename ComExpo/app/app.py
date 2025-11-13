from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import text

app = Flask(__name__)

# Database configuration from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    try:
        # Test database connection
        # This is the corrected line
        db.session.execute(text("SELECT 1"))
        return {
            'status': 'healthy', 
            'database': 'connected',
            'app': 'Classroom Booking System'
        }, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('APP_PORT', 8000)), debug=True)