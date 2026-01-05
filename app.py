from flask import Flask, render_template, request # Added 'request'
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta # NEW: To handle calendar logic

app = Flask(__name__)

# CONFIGURATION
# This creates the database file in your 'database' folder
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database', 'naqsh.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the Database
db = SQLAlchemy(app)

# ------------------------------------
# DATABASE MODELS (The Blueprint)
# ------------------------------------
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Storing image filename like 'deluxe.jpg'
    image = db.Column(db.String(100), nullable=False, default='default.jpg') 
    # Capacity logic
    capacity = db.Column(db.Integer, nullable=False)
    # Pricing logic (Integers are safer than Floats for currency)
    price_weekday = db.Column(db.Integer, nullable=False)
    price_weekend = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Room {self.name}>'

# ------------------------------------
# ROUTES ( The Pages)
# ------------------------------------

@app.route('/')
def home():
    # 1. Fetch all rooms from the database
    rooms = Room.query.all()
    
    # 2. Send the room data to the HTML template
    return render_template('home.html', rooms=rooms)

@app.route('/availability', methods=['GET', 'POST'])
def availability():
    # If user just visits the page (GET), show the empty form
    if request.method == 'GET':
        return render_template('availability.html')
    
    # If user submitted the form (POST), calculate prices
    if request.method == 'POST':
        # 1. Get data from the HTML form
        checkin_str = request.form.get('checkin')
        checkout_str = request.form.get('checkout')
        
        # 2. Convert text "2026-01-01" into a Date Object
        checkin_date = datetime.strptime(checkin_str, '%Y-%m-%d')
        checkout_date = datetime.strptime(checkout_str, '%Y-%m-%d')
        
        # 3. Calculate Logic
        duration = checkout_date - checkin_date
        total_nights = duration.days
        
        if total_nights <= 0:
            return "Error: Check-out must be after Check-in"

        # 4. Weekend vs Weekday Logic
        # We need to loop through EVERY night of the stay
        weekend_nights = 0
        weekday_nights = 0
        
        current_date = checkin_date
        for i in range(total_nights):
            # .weekday() returns 0=Monday, 1=Tuesday ... 4=Friday, 5=Saturday, 6=Sunday
            # We treat Friday (4) and Saturday (5) as "Resort Weekend" pricing
            if current_date.weekday() in [4, 5]: 
                weekend_nights += 1
            else:
                weekday_nights += 1
            
            # Move to next day
            current_date += timedelta(days=1)

        # 5. Calculate Price for EVERY Room in Database
        available_rooms = []
        all_rooms = Room.query.all()
        
        for room in all_rooms:
            cost = (room.price_weekday * weekday_nights) + (room.price_weekend * weekend_nights)
            
            room_result = {
                'room_name': room.name,
                # ADD THIS LINE BELOW:
                'image': room.image, 
                'capacity': room.capacity,
                'total_price': cost,
                'weekend_nights': weekend_nights
            }
            available_rooms.append(room_result)
        
        # 6. Send results back to the same page
        return render_template('availability.html', results=available_rooms, nights=total_nights, checkin=checkin_str, checkout=checkout_str)

@app.route('/setup')
def setup():
    # TEMPORARY ROUTE: Run this once to create the DB and add rooms
    with app.app_context():
        db.create_all()
        
        # Check if rooms exist, if not, add them
        if Room.query.count() == 0:
            # ROOM 1: Deluxe Garden
            r1 = Room(
                name="Deluxe Garden Room",
                image="deluxe_garden.jpg",
                capacity=2,
                price_weekday=1600,
                price_weekend=2200,
                description="Perfect for couples. Garden view with strong privacy."
            )
            # ROOM 2: Premium Valley
            r2 = Room(
                name="Premium Room (Valley View)",
                image="premium_valley.jpg",
                capacity=2,
                price_weekday=2000,
                price_weekend=2600,
                description="Breathtaking valley views. Our most popular choice."
            )
            # ROOM 3: Family Suite
            r3 = Room(
                name="Family Suite (4 Pax)",
                image="family_suite.jpg",
                capacity=4,
                price_weekday=3000,
                price_weekend=3500,
                description="Spacious setup for families or groups of friends."
            )
            
            db.session.add_all([r1, r2, r3])
            db.session.commit()
            return "Database Created and Rooms Added!"
        
        return "Database already exists."

@app.route('/gallery')
def gallery():
    # We are pretending we have more images by repeating the ones we have.
    # In a real app, we would scan a folder or ask the database.
    photos = [
        {'src': 'deluxe.jpg', 'caption': 'Deluxe Room Interiors'},
        {'src': 'premium.jpg', 'caption': 'Valley View from Bed'},
        {'src': 'suite.jpg', 'caption': 'Family Suite Space'},
        {'src': 'default.jpg', 'caption': 'Resort Exterior'},
        {'src': 'deluxe.jpg', 'caption': 'Cozy Corners'}, # Repeating for demo
        {'src': 'premium.jpg', 'caption': 'Sunrise Views'} # Repeating for demo
    ]
    return render_template('gallery.html', photos=photos)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/corporate')
def corporate():
    return render_template('corporate.html')

if __name__ == '__main__':
    app.run(debug=True)