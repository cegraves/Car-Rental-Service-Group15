from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/car_rental'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 1. Categories Table
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(50), nullable=False)

# 2. Vehicles Table
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('vehicles', lazy=True))

# 3. Users Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)  # SUID
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# 4. Bookings Table
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    pickup_date = db.Column(db.String(20), nullable=False)
    return_date = db.Column(db.String(20), nullable=False)
    
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))

# 5. Payments Table
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Completed')

# Home Route
@app.route('/')
def index():
    selected_category = request.args.get('category')
    if selected_category:
        vehicles = Vehicle.query.join(Category).filter(Category.name == selected_category).all()
    else:
        vehicles = Vehicle.query.all()
    return render_template('carRentalIndex.html', vehicles=vehicles, selected_category=selected_category)

# Booking Route
@app.route('/book', methods=['POST'])
def book():
    vehicle_id = request.form.get('vehicle_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    suid_input = request.form.get('suid')  
    pickup_date = request.form.get('pickup_date')
    return_date = request.form.get('return_date')
    
    if suid_input:
        suid_input = suid_input.strip()
    
    # 1. Validate email domain
    if not email or not email.endswith('@syr.edu'):
        return "Error: You must use a valid @syr.edu email address to rent a vehicle.", 400
        
    # 2. Validate SUID format
    if not suid_input or not suid_input.isdigit() or len(suid_input) != 9:
        return f"Error: SUID must be a valid 9-digit number. (Received: '{suid_input}')", 400
    
    suid_int = int(suid_input)
    
    # 3. Check if vehicle is already booked for overlapping dates
    overlapping_booking = Booking.query.filter(
        Booking.vehicle_id == vehicle_id,
        Booking.pickup_date <= return_date,
        Booking.return_date >= pickup_date
    ).first()

    if overlapping_booking:
        return "Error: Sorry, this vehicle is already booked for some or all of those dates. Please choose different dates or another vehicle.", 400

    # 4. Check or create user
    user = User.query.filter_by(id=suid_int).first()
    if not user:
        user = User(id=suid_int, first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
        db.session.commit()
    
    # 5. Save the booking
    new_booking = Booking(
        user_id=user.id,  
        vehicle_id=vehicle_id, 
        pickup_date=pickup_date, 
        return_date=return_date
    )
    db.session.add(new_booking)
    db.session.commit()
    
    return redirect(url_for('index'))
"""
THIS CREATES DB TABLES AND SEEDS VEHICLE AND CATEGORY TABLES WITH STANDARD DATA UPON RUNNING THE APPLICATION

with app.app_context():
    db.create_all()
    
    # 1. Seed categories if empty
    if Category.query.count() == 0:
        categories_data = [
            Category(id=1, name='SUV'),
            Category(id=2, name='Sedan'),
            Category(id=3, name='Truck'),
            Category(id=4, name='Electric')
        ]
        db.session.bulk_save_objects(categories_data)
        db.session.commit()

    # 2. Seed normal, everyday vehicles if empty
    if Vehicle.query.count() == 0:
        vehicles_data = [
            # SUVs (Category 1)
            Vehicle(id=1, name='Toyota RAV4', price=45.00, category_id=1, image='https://images.unsplash.com/photo-1590362891991-f776e747a588?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=2, name='Ford Explorer', price=65.00, category_id=1, image='https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=3, name='Honda CR-V', price=48.00, category_id=1, image='https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=4, name='Subaru Outback', price=50.00, category_id=1, image='https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=5, name='Nissan Rogue', price=46.00, category_id=1, image='https://images.unsplash.com/photo-1553440569-bcc63803a83d?auto=format&fit=crop&w=800&q=80'),
            
            # Sedans (Category 2)
            Vehicle(id=6, name='Toyota Camry', price=35.00, category_id=2, image='https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=7, name='Honda Accord', price=38.00, category_id=2, image='https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=8, name='Hyundai Elantra', price=30.00, category_id=2, image='https://images.unsplash.com/photo-1541899481282-d53bffe3c351?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=9, name='Nissan Altima', price=34.00, category_id=2, image='https://images.unsplash.com/photo-1550355291-bbee04a92027?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=10, name='Chevrolet Malibu', price=33.00, category_id=2, image='https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80'),
            
            # Trucks (Category 3)
            Vehicle(id=11, name='Ford F-150', price=80.00, category_id=3, image='https://images.unsplash.com/photo-1563720222812-516ddb07e8ef?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=12, name='Chevrolet Silverado', price=78.00, category_id=3, image='https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=13, name='Ram 1500', price=82.00, category_id=3, image='https://images.unsplash.com/photo-1551830822-33d4e3b33560?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=14, name='Toyota Tacoma', price=65.00, category_id=3, image='https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=15, name='Ford Ranger', price=60.00, category_id=3, image='https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=800&q=80'),
            
            # Electric / Practical EVs (Category 4)
            Vehicle(id=16, name='Chevrolet Bolt EV', price=40.00, category_id=4, image='https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=17, name='Nissan Leaf', price=38.00, category_id=4, image='https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=18, name='Hyundai Kona Electric', price=45.00, category_id=4, image='https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=19, name='Volkswagen ID.4', price=52.00, category_id=4, image='https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=800&q=80'),
            Vehicle(id=20, name='Kia Niro EV', price=48.00, category_id=4, image='https://images.unsplash.com/photo-1617814076668-80928e469502?auto=format&fit=crop&w=800&q=80')
        ]
        db.session.bulk_save_objects(vehicles_data)
        db.session.commit()
"""
if __name__ == '__main__':
    app.run(debug=True)