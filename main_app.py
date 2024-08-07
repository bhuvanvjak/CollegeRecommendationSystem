from flask import Flask, render_template
from usapp import app as usa_bp
from canadaap import app as canada_bp
from japanapp import app as japan_bp
from ukaap import app as  uk_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(usa_bp, url_prefix='/usa')
app.register_blueprint(canada_bp)
app.register_blueprint(japan_bp, url_prefix='/japan')
app.register_blueprint(uk_bp, url_prefix='/uk')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)