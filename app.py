import os
import random
import uuid
import json
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from twilio.rest import Client
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import logging
from config import Config
from db_utils import db
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
app.config['ALLOWED_EXTENSIONS'] = Config.ALLOWED_EXTENSIONS

# Ensure upload directory exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Twilio Credentials
ACCOUNT_SID = Config.TWILIO_ACCOUNT_SID
AUTH_TOKEN = Config.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = Config.TWILIO_PHONE_NUMBER

# WeatherAPI Key
WEATHER_API_KEY = Config.WEATHER_API_KEY

# AI Model
model = tf.keras.models.load_model("models\plant_disease_recog_model_pwp.keras")
with open("plant_disease.json", 'r') as file:
    plant_disease = json.load(file)

# Helper functions
def _check_access(template):
    if not session.get("verified"):
        flash("कृपया पहले लॉगिन करें", "danger")
        return redirect(url_for("login"))
    return render_template(template, name=session["name"])

def extract_features(image_path):
    image = tf.keras.utils.load_img(image_path, target_size=(160, 160))
    img_array = tf.keras.utils.img_to_array(image)
    return np.array([img_array])

def model_predict(image_path):
    features = extract_features(image_path)
    prediction = model.predict(features)
    return plant_disease[prediction.argmax()]

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            password = request.form.get("password")
            
            user = db.get_user_by_email(email)
            if user and check_password_hash(user["password"], password):
                session["user_id"] = str(user["_id"])
                session["name"] = user["name"]
                session["verified"] = True
                flash("सफलतापूर्वक लॉगिन किया गया!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("गलत ईमेल या पासवर्ड", "danger")
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash("लॉगिन करने में समस्या हुई। कृपया पुनः प्रयास करें।", "danger")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            
            if db.get_user_by_email(email):
                flash("यह ईमेल पहले से ही पंजीकृत है", "danger")
                return redirect(url_for("register"))
            
            hashed_password = generate_password_hash(password)
            user_data = {
                "name": name,
                "email": email,
                "password": hashed_password,
                "phone": "",
                "address": "",
                "farm_size": "",
                "crops": []
            }
            
            user_id = db.create_user(user_data)
            if user_id:
                flash("सफलतापूर्वक पंजीकृत किया गया! कृपया लॉगिन करें", "success")
                return redirect(url_for("login"))
            else:
                flash("पंजीकरण में समस्या हुई। कृपया पुनः प्रयास करें।", "danger")
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            flash("पंजीकरण में समस्या हुई। कृपया पुनः प्रयास करें।", "danger")
    
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("verified"):
        flash("कृपया पहले लॉगिन करें", "danger")
        return redirect(url_for("login"))
    
    user = db.get_user(session["user_id"])
    profile_picture = user.get("profile_picture", "") if user else ""
    
    return render_template("dashboard.html", 
                         name=session["name"],
                         profile_picture=profile_picture)

# Protected Routes
@app.route("/market")
def market():
    return _check_access("market.html")

@app.route("/irrigation")
def irrigation():
    return _check_access("irrigation.html")

@app.route("/tools")
def tools():
    return _check_access("tools.html")

@app.route("/seeds")
def seeds():
    return _check_access("seeds.html")

@app.route("/market1")
def market1():
    return _check_access("market1.html")

@app.route("/crop-advice")
def crop_advice():
    return _check_access("crop_advice.html")

@app.route("/home")
def ai_assistant():
    return _check_access("home.html")

@app.route("/equipment")
def equipment():
    return _check_access("equipment.html")

@app.route("/sugarcane")
def sugarcane():
    return _check_access("sugarcane.html")

@app.route("/rice")
def rice():
    return _check_access("rice.html")

@app.route("/wheat")
def wheat():
    return _check_access("wheat.html")

@app.route("/onion")
def onion():
    return _check_access("onion.html")

@app.route("/tomato")
def tomato():
    return _check_access("tomato.html")

@app.route("/potato")
def potato():
    return _check_access("potato.html")

@app.route("/cabbage")
def cabbage():
    return _check_access("cabbage.html")

@app.route("/ladii")
def ladii():
    return _check_access("ladii.html")

@app.route("/chilli")
def chilli():
    return _check_access("chilli.html")

@app.route("/garlic")
def garlic():
    return _check_access("garlic.html")

@app.route("/schemes")
def schemes():
    return _check_access("schemes.html")

@app.route("/about")
def about():
    try:
        team_members = [
            {
                'name': 'अथर्व पाटिल',
                'role': 'डॉक्यूमेंटेशन और रिपोर्ट',
                'bio': 'प्रोजेक्ट डॉक्यूमेंटेशन और रिपोर्टिंग में विशेषज्ञ',
                'image_url': 'team/atharv.jpg',
                'linkedin': 'https://linkedin.com/in/atharv',
                'twitter': 'https://twitter.com/atharv'
            },
            {
                'name': 'प्रणव चव्हाण',
                'role': 'फ्रंटएंड डेवलपर',
                'bio': 'यूजर इंटरफेस और वेब डिज़ाइन में विशेषज्ञ',
                'image_url': 'team/pranav.jpg',
                'linkedin': 'https://linkedin.com/in/pranav',
                'twitter': 'https://twitter.com/pranav'
            },
            {
                'name': 'करण घाटगे',
                'role': 'आईडिया और सिस्टम डेवलपमेंट',
                'bio': 'सिस्टम आर्किटेक्चर और प्रोजेक्ट प्लानिंग में विशेषज्ञ',
                'image_url': 'team/karan.jpg',
                'linkedin': 'https://linkedin.com/in/karan',
                'twitter': 'https://twitter.com/karan'
            },
            {
                'name': 'आर्य कुलकर्णी',
                'role': 'बैकएंड डेवलपर',
                'bio': 'सर्वर-साइड लॉजिक और डेटाबेस मैनेजमेंट में विशेषज्ञ',
                'image_url': 'team/aary.jpg',
                'linkedin': 'https://linkedin.com/in/aary',
                'twitter': 'https://twitter.com/aary'
            }
        ]
        
        return render_template('about.html', 
                             name=session.get('name'),
                             profile_picture=session.get('profile_picture'),
                             team_members=team_members)
    except Exception as e:
        logger.error(f"Error in about route: {str(e)}")
        return render_template('about.html', 
                             name=session.get('name'),
                             profile_picture=session.get('profile_picture'),
                             team_members=[])

@app.route("/developer-profile/<developer_id>")
def developer_profile(developer_id):
    try:
        developer = db.get_developer(developer_id)
        if not developer:
            flash("Developer not found", "danger")
            return redirect(url_for("about"))
        return render_template("developer_profile.html", 
                             developer=developer, 
                             name=session.get("name"))
    except Exception as e:
        logger.error(f"Error in developer profile: {str(e)}")
        flash("Error loading developer profile", "danger")
        return redirect(url_for("about"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("verified"):
        flash("कृपया पहले लॉगिन करें", "danger")
        return redirect(url_for("login"))
    
    try:
        user_id = session["user_id"]
        if request.method == "POST":
            updates = {
                "name": request.form.get("name"),
                "phone": request.form.get("phone"),
                "address": request.form.get("address"),
                "farm_size": request.form.get("farm_size"),
                "crops": request.form.get("crops", "").split(",")
            }
            
            if db.update_user(user_id, updates):
                session["name"] = updates["name"]
                flash("प्रोफाइल सफलतापूर्वक अपडेट की गई", "success")
            else:
                flash("प्रोफाइल अपडेट करने में समस्या हुई", "danger")
        
        user = db.get_user(user_id)
        if not user:
            flash("उपयोगकर्ता नहीं मिला", "danger")
            return redirect(url_for("login"))
        
        return render_template("profile.html", 
                            name=user.get("name", ""),
                            email=user.get("email", ""),
                            phone=user.get("phone", ""),
                            village=user.get("village", ""),
                            district=user.get("district", ""),
                            state=user.get("state", ""),
                            farm_size=user.get("farm_size", ""),
                            crops=user.get("crops", ""),
                            profile_picture=user.get("profile_picture", ""))
    except Exception as e:
        logger.error(f"Profile error: {str(e)}")
        flash("प्रोफाइल देखने में समस्या हुई", "danger")
        return redirect(url_for("login"))

@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    if not session.get("verified"):
        flash("कृपया पहले लॉगिन करें", "danger")
        return redirect(url_for("login"))
    
    if request.method == "POST":
        try:
            updates = {
                "name": request.form.get("name"),
                "phone": request.form.get("phone"),
                "village": request.form.get("village"),
                "district": request.form.get("district"),
                "state": request.form.get("state"),
                "farm_size": request.form.get("farm_size"),
                "crops": request.form.get("crops")
            }
            
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                if file and file.filename:
                    filename = secure_filename(f"{session['user_id']}_{file.filename}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pictures', filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    file.save(filepath)
                    updates['profile_picture'] = f"profile_pictures/{filename}"
            
            success = db.update_user(session["user_id"], updates)
            
            if success:
                flash("प्रोफाइल सफलतापूर्वक अपडेट हो गई", "success")
                session["name"] = updates["name"]
                return redirect(url_for("profile"))
            else:
                flash("प्रोफाइल अपडेट करने में त्रुटि हुई", "danger")
        except Exception as e:
            logger.error(f"Edit profile error: {str(e)}")
            flash("प्रोफाइल अपडेट करने में त्रुटि हुई", "danger")
    
    try:
        user = db.get_user(session["user_id"])
        return render_template("edit_profile.html", 
                             name=user.get("name", ""),
                             phone=user.get("phone", ""),
                             village=user.get("village", ""),
                             district=user.get("district", ""),
                             state=user.get("state", ""),
                             farm_size=user.get("farm_size", ""),
                             crops=user.get("crops", ""),
                             profile_picture=user.get("profile_picture", ""))
    except Exception as e:
        logger.error(f"Error loading edit profile: {str(e)}")
        flash("प्रोफाइल लोड करने में त्रुटि हुई", "danger")
        return redirect(url_for("profile"))

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("👋 आप सफलतापूर्वक लॉग आउट हो गए हैं", "success")
    return redirect(url_for("index"))

@app.route("/get-weather")
def get_weather():
    try:
        location = request.args.get("location")
        if not location:
            return jsonify({"error": "स्थान का पैरामीटर आवश्यक है"}), 400
            
        if ',' in location:
            lat, lon = location.split(',')
            location = f"{lat},{lon}"
            
        api_url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=3&lang=hi"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            logger.error(f"Weather API error: {response.status_code} - {response.text}")
            return jsonify({"error": "मौसम डेटा प्राप्त करने में विफल"}), 500
            
        data = response.json()
        
        if "error" in data:
            logger.error(f"Weather API error: {data['error']}")
            return jsonify({"error": data['error']['message']}), 500

        if not all(key in data for key in ['current', 'location', 'forecast']):
            logger.error("Missing required weather data fields")
            return jsonify({"error": "अमान्य मौसम डेटा प्रारूप"}), 500

        forecast_data = [{
            "date": day["date"],
            "maxtemp_c": day["day"]["maxtemp_c"],
            "mintemp_c": day["day"]["mintemp_c"],
            "avgtemp_c": day["day"]["avgtemp_c"],
            "condition": day["day"]["condition"]["text"],
            "icon": day["day"]["condition"]["icon"],
            "maxwind_kph": day["day"]["maxwind_kph"],
            "avghumidity": day["day"]["avghumidity"],
            "daily_chance_of_rain": day["day"]["daily_chance_of_rain"],
            "daily_chance_of_snow": day["day"]["daily_chance_of_snow"],
            "uv": day["day"]["uv"]
        } for day in data["forecast"]["forecastday"]]

        db.save_weather_data(location, data)

        return jsonify({
            "location": {
                "name": data["location"]["name"],
                "region": data["location"]["region"],
                "country": data["location"]["country"]
            },
            "current": {
                "temp_c": data["current"]["temp_c"],
                "condition": {
                    "text": data["current"]["condition"]["text"],
                    "icon": data["current"]["condition"]["icon"]
                },
                "wind_kph": data["current"]["wind_kph"],
                "humidity": data["current"]["humidity"],
                "feelslike_c": data["current"]["feelslike_c"],
                "uv": data["current"]["uv"]
            },
            "forecast": forecast_data
        })

    except Exception as e:
        logger.error(f"Weather API error: {str(e)}")
        return jsonify({"error": "मौसम डेटा प्राप्त करने में विफल"}), 500

@app.route("/uploadimages/<path:filename>")
def uploaded_images(filename):
    try:
        return send_from_directory(Config.UPLOAD_FOLDER, filename)
    except Exception as e:
        logger.error(f"Error serving image: {str(e)}")
        return "Image not found", 404

@app.route("/upload/", methods=["POST", "GET"])
def uploadimage():
    if not session.get("verified"):
        flash("कृपया पहले लॉगिन करें", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            if 'img' not in request.files:
                flash("कोई छवि नहीं मिली", "danger")
                return redirect("/home")
                
            image = request.files["img"]
            if image.filename == '':
                flash("कोई छवि नहीं चुनी गई", "danger")
                return redirect("/home")
                
            if not image.filename.lower().endswith(tuple(Config.ALLOWED_EXTENSIONS)):
                flash("अमान्य फ़ाइल प्रारूप। केवल PNG, JPG, JPEG फ़ाइलें स्वीकार्य हैं।", "danger")
                return redirect("/home")
            
            filename = f"temp_{uuid.uuid4().hex}_{image.filename}"
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            
            image.save(filepath)
            
            prediction = model_predict(filepath)
            
            db.save_disease_record(session["user_id"], filename, prediction)
            
            return render_template("home.html", 
                                result=True, 
                                imagepath=f"/uploadimages/{filename}", 
                                prediction=prediction, 
                                name=session.get("name"))
        except Exception as e:
            logger.error(f"Image upload error: {str(e)}")
            flash("छवि अपलोड करने में समस्या हुई", "danger")
            return redirect("/home")

    return redirect("/home")

if __name__ == "__main__":
    app.run(debug=True)
