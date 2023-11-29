from flask import Flask, render_template, jsonify, request, flash, redirect
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, register_user, load_users_from_db, get_user_by_id, get_user_by_username, load_coffee_from_db, add_to_cart, get_cart, delete_cart_item, load_applications_from_db, create_order, clear_cart, get_user_orders
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

jobs = load_jobs_from_db()
users = load_users_from_db()
coffee = load_coffee_from_db()



class User(UserMixin):
  def __init__(self, user_id, username, email, user_role):
      self.id = user_id
      self.username = username
      self.email = email
      self.user_role = user_role

@login_manager.user_loader
def load_user(user_id):
  # Load user from the database based on user_id
  user_data = get_user_by_id(user_id)
  if user_data:
      return User(user_data['user_id'], user_data['username'], user_data['email'], user_data['user_role'])
  return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Validate user credentials
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = get_user_by_username(username)
        if user_data and user_data['password'] == password:
            user = User(user_data['user_id'], user_data['username'], user_data['email'], user_data['user_role'])
            login_user(user)

            # Check if the user is an admin and redirect accordingly
            if user.user_role == '1':
                return redirect('/admin/dashboard')
            else:
                return redirect('/dashboard')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    print("Current User:", current_user)

    # Load the cart items for the current user using the get_cart function
    cart_items = get_cart(current_user.id)

    # Fetch additional details for each coffee item in the cart
    detailed_cart_items = []
    for cart_item in cart_items:
        # Assuming load_coffee_from_db returns a list, use [0] to get the first item
        coffee_item = load_coffee_from_db(cart_item['coffee_id'])[0]

        detailed_cart_item = {
            'cart_id': cart_item['cart_id'],
            'coffee_name': coffee_item['coffee_name'],
            'price': coffee_item['price'],
            'quantity': cart_item['quantity'],
            'image_url': coffee_item['image_url']
        }
        detailed_cart_items.append(detailed_cart_item)
    return render_template('dashboard.html', user=current_user, cart_items=detailed_cart_items)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Check if the current user is an admin
    if current_user.user_role != '1':
        return render_template('error.html', message='Permission denied.')

    # Fetch data for the admin dashboard
    coffee_data = load_coffee_from_db()
    job_data = load_jobs_from_db()
    applications_data = load_applications_from_db()
    users_data = load_users_from_db()

    return render_template('admin_dashboard.html', user=current_user, coffee_data=coffee_data, job_data=job_data, applications_data=applications_data, users_data=users_data)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Logout successful!', 'success')
  return render_template('login.html')

@app.route("/")
def hello_world():
  return render_template("home.html", jobs=jobs, company_name='Sangrai Kopi')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
  
@app.route('/career')
def career():
    return render_template('career.html', jobs=jobs)

@app.route('/coffee', methods=['GET', 'POST'])
def coffee_page():
    if request.method == 'POST':
        if current_user.is_authenticated:
            coffee_id = request.form.get('coffee_id')
            quantity = int(request.form.get('quantity', 1))  # Default to 1 if quantity is not provided
            # Add the selected coffee to the user's shopping cart
            add_to_cart(current_user.id, coffee_id, quantity)

            flash(f'Successfully added {quantity} item(s) to your cart!', 'success')

            # Redirect to the coffee page or the cart page
            return redirect('/coffee')

        else:
            flash('You must be logged in to add items to your cart. Please log in or register.', 'warning')
            return redirect('/coffee')

    return render_template('coffee.html', coffee=coffee)


@app.route('/add_to_cart/<int:coffee_id>/<int:quantity>', methods=['GET', 'POST'])
@login_required
def add_to_cart_route(coffee_id, quantity):
    if request.method == 'POST':
        user_id = current_user.id
        add_to_cart(user_id, coffee_id, quantity)
        flash('Item added to cart successfully!', 'success')
        return redirect('/coffee')

    # Handle GET request if needed (e.g., show information about the added item)
    return render_template('add_to_cart.html', coffee_id=coffee_id, quantity=quantity)

@app.route('/delete_cart_item/<int:cart_item_id>', methods=['POST'])
@login_required
def delete_cart_item_route(cart_item_id):
    # Call a function to delete the item from the cart based on the cart_item_id
    delete_cart_item(current_user.id, cart_item_id)
    flash('Item removed from your cart!', 'success')

    # Redirect to the dashboard page to show the updated cart
    return redirect('/dashboard')

@app.route("/api/job/<job_id>")
def show_job_json(job_id):
  job = load_job_from_db(job_id)
  return jsonify(job)

@app.route("/jobs/<job_id>")
def show_job(job_id):
  job = load_job_from_db(job_id)
  if not job:
    return "Not Found"
  return render_template("jobpage.html", job=job)

@app.route("/jobs/<job_id>/apply", methods=['post'])
def apply_for_job(job_id):
  data = request.form
  job = load_job_from_db(job_id)
  add_application_to_db(job_id, data)
  return render_template('application_submitted.html', application=data, job=job)
  

@app.route('/register', methods=['post'])
def register_user_route():
  data = request.form
  register_user(data)
  return render_template('registration_success.html')



@app.route('/order')
@login_required
def order():
    # Get the current user's cart items
    cart_items = get_cart(current_user.id)

    try:
        # Replace 'coffee_id' and 'quantity' with the actual keys in your cart_items dictionary
      total_amount = sum(cart_item['quantity'] * load_coffee_from_db(cart_item['coffee_id'])[0]['price'] for cart_item in cart_items)
        # Create an order in the database
        
      order_data = {
            'user_id': current_user.id,
            'order_date': datetime.now(),
            'total_amount': total_amount
        }
      create_order(order_data)

        # Clear the user's cart
      clear_cart(current_user.id)

      return render_template('order_success.html', total_amount=total_amount)
    except Exception as e:
        # Handle the exception, you can print or log the error for debugging
        print(f"Error in order route: {e}")
        return render_template('order_failure.html')



@app.route('/orders')
@login_required
def orders():
    # Get all orders for the current user
    user_orders = get_user_orders(current_user.id)

    return render_template('orders.html', user_orders=user_orders)

        


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)