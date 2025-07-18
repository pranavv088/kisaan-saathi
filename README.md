# Plant Disease Recognition System

A Flask-based web application that helps farmers identify plant diseases using machine learning. The system provides real-time disease detection, weather information, and agricultural advice.

## Features

- Plant disease detection using machine learning
- User authentication and profile management
- Weather information and forecasts
- Crop-specific advice and information
- Agricultural market information
- Irrigation guidance
- Government schemes information

## Setup Instructions

1. Clone the repository:



2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```
SECRET_KEY=your_secret_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_number
WEATHER_API_KEY=your_weather_api_key
```

5. Run the application:
```bash
python app.py
```

## Project Structure

- `app.py` - Main application file
- `config.py` - Configuration settings
- `db_utils.py` - Database utilities
- `models/` - Machine learning models
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `requirements.txt` - Python dependencies

## Technologies Used

- Flask (Python web framework)
- TensorFlow (Machine learning)
- MongoDB (Database)
- Twilio (SMS notifications)
- WeatherAPI (Weather information)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

#
