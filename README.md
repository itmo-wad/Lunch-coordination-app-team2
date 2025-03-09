## "🍕 What's for Lunch?" – a simple and intuitive online tool for coordinating team lunch orders.

**Problem:** Coordinating lunch orders with colleagues is often chaotic and time-consuming. Teams waste time in chat discussions, struggle to reach consensus on menu choices, and often default to the same items due to decision fatigue.

**Solution:** A web-based lunch voting tool where team members can quickly vote on meal options within a set timeframe. The system helps teams make faster decisions about group lunch orders.

**Simplified cases:** A team needs to quickly decide on lunch options. They create a poll, vote within 30 minutes, and automatically get the winning choice. A team manager can access historical data to analyze lunch patterns and optimize food expenses based on team preferences.

## Technical section

For running this app you will need to install `Python 3` and `pip` on your operating system.<br><br>

With Python and pip installed, you will need to install `Flask`, `Flask-Login`, `Werkzeug`, `WTForms`, `Flask-SQLAlchemy`, `Flask-WTF`, `python-dotenv`.<br>
Install them with the following command:<br>
```
pip install -r requirements.txt
```

Also you need to configure the environment by copying `.env.example` and renaming it to `.env`, then editing the required parameters as desired:

| Parameter | Description |
|-----------|-------------|
| `SECRET_KEY` | Your super secret key for Flask sessions and security |
| `DB_URI` | Database connection string (for example: sqlite:///lunch_app.db) |


When you have everything installed, configured and running, just type
```
python app.py
```

The WebApp will run at `127.0.0.1:5000`. Use your browser to navigate to that address.
