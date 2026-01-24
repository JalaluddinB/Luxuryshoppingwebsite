from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import openai
from google import genai
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, IntegerField, SelectField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'luxury_shopping_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///luxury_shopping.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.context_processor
def inject_user():
    user = None
    cart_count = 0
    user_id = session.get('user_id')
    if user_id is not None:
        user = User.query.get(user_id)
        cart_count = db.session.query(db.func.coalesce(db.func.sum(Cart.quantity), 0)).filter(Cart.user_id == user_id).scalar() or 0
    return {'user': user, 'cart_count': cart_count}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200))
    stock = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

class SiteSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Length(min=6, max=120)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[InputRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired(), NumberRange(min=0)])
    category = StringField('Category', validators=[InputRequired()])
    stock = IntegerField('Stock', validators=[InputRequired(), NumberRange(min=0)])
    image_url = StringField('Image URL', validators=[Length(max=200)])
    submit = SubmitField('Add Product')

class ConfigForm(FlaskForm):
    ai_provider = SelectField('AI Provider', choices=[('openai', 'OpenAI'), ('gemini', 'Google Gemini')], default='openai')
    openai_api_key = StringField('OpenAI API Key', validators=[Length(max=200)])
    gemini_api_key = StringField('Gemini API Key', validators=[Length(max=200)])
    submit = SubmitField('Save Settings')

def _fallback_advisor_answer(user_question, products):
    q = (user_question or "").strip().lower()
    if not q:
        return None

    matched = None
    for p in products:
        name = (p.name or "").strip()
        if name and name.lower() in q:
            matched = p
            break

    wants_price = any(x in q for x in ["price", "cost", "how much"])
    wants_stock = any(x in q for x in ["how many", "stock", "available", "quantity", "in stock"])

    if matched:
        if wants_stock:
            return f"We currently have {matched.stock} {matched.name}(s) in stock."
        if wants_price:
            return f"The {matched.name} costs ${matched.price:.2f}. {matched.description}"
        return f"{matched.name}: ${matched.price:.2f}. {matched.description} (Category: {matched.category})"

    if wants_stock and products:
        lines = "\n".join([f"- {p.name}: {p.stock} in stock" for p in products[:5]])
        return f"Here is current stock for some items:\n{lines}"

    if wants_price and products:
        sample = products[:5]
        lines = "\n".join([f"- {p.name}: ${p.price:.2f}" for p in sample])
        return f"Here are some current prices from our catalog:\n{lines}"

    return None

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
        elif User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'error')
        else:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    product = Product.query.get_or_404(product_id)
    if product.stock <= 0:
        flash('This product is out of stock', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    cart_item = Cart.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
    
    if cart_item:
        if cart_item.quantity + 1 > product.stock:
            flash(f'Only {product.stock} left in stock for "{product.name}"', 'error')
            return redirect(url_for('cart'))
        cart_item.quantity += 1
        db.session.add(cart_item)
    else:
        cart_item = Cart(user_id=session['user_id'], product_id=product_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/remove_from_cart/<int:cart_id>')
def remove_from_cart(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id == session['user_id']:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart', 'info')
    
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart'))
    
    try:
        for item in cart_items:
            if item.product.stock < item.quantity:
                flash(f'Not enough stock for "{item.product.name}". Available: {item.product.stock}', 'error')
                return redirect(url_for('cart'))

        total = sum(item.product.price * item.quantity for item in cart_items)

        order = Order(user_id=session['user_id'], total_amount=total)
        db.session.add(order)
        db.session.flush()

        for item in cart_items:
            item.product.stock -= item.quantity
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            db.session.delete(item)

        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('index'))
    except Exception:
        db.session.rollback()
        flash('Checkout failed. Please try again.', 'error')
        return redirect(url_for('cart'))

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    orders = Order.query.all()
    
    # Handle Settings
    form = ConfigForm()
    if form.validate_on_submit():
        # Save provider
        provider_setting = SiteSetting.query.filter_by(key='ai_provider').first()
        if not provider_setting:
            provider_setting = SiteSetting(key='ai_provider')
            db.session.add(provider_setting)
        provider_setting.value = form.ai_provider.data
        
        # Save OpenAI Key
        openai_key_setting = SiteSetting.query.filter_by(key='openai_api_key').first()
        if not openai_key_setting:
            openai_key_setting = SiteSetting(key='openai_api_key')
            db.session.add(openai_key_setting)
        openai_key_setting.value = form.openai_api_key.data

        # Save Gemini Key
        gemini_key_setting = SiteSetting.query.filter_by(key='gemini_api_key').first()
        if not gemini_key_setting:
            gemini_key_setting = SiteSetting(key='gemini_api_key')
            db.session.add(gemini_key_setting)
        gemini_key_setting.value = form.gemini_api_key.data
        
        db.session.commit()
        flash('Settings updated successfully', 'success')
        return redirect(url_for('admin'))
    
    # Pre-populate form
    provider_setting = SiteSetting.query.filter_by(key='ai_provider').first()
    if provider_setting:
        form.ai_provider.data = provider_setting.value
        
    openai_key_setting = SiteSetting.query.filter_by(key='openai_api_key').first()
    if openai_key_setting:
        form.openai_api_key.data = openai_key_setting.value

    gemini_key_setting = SiteSetting.query.filter_by(key='gemini_api_key').first()
    if gemini_key_setting:
        form.gemini_api_key.data = gemini_key_setting.value
        
    return render_template('admin.html', products=products, orders=orders, form=form)

@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            stock=form.stock.data,
            image_url=form.image_url.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('add_product.html', form=form)

@app.route('/api/ask_advisor', methods=['POST'])
def ask_advisor():
    data = request.json
    user_question = data.get('question')
    client_api_key = data.get('api_key')
    client_provider = data.get('provider')
    
    if not user_question:
        return jsonify({'error': 'No question provided'}), 400
        
    # Get Provider (Client override or DB default)
    if app.debug and client_provider:
        provider = client_provider
    else:
        provider_setting = SiteSetting.query.filter_by(key='ai_provider').first()
        provider = provider_setting.value if provider_setting else 'openai'

    # Determine API Key: Client (Dev) > DB (Prod)
    final_api_key = None
    
    if app.debug and client_api_key:
        final_api_key = client_api_key
    else:
        # Fetch from DB based on provider
        if provider == 'gemini':
            key_setting = SiteSetting.query.filter_by(key='gemini_api_key').first()
        else:
            key_setting = SiteSetting.query.filter_by(key='openai_api_key').first()
            
        final_api_key = key_setting.value if key_setting else None
    
    if not final_api_key:
        return jsonify({'error': f'{provider.title()} Service not configured'}), 503
        
    try:
        # RAG: Retrieve all products
        products = Product.query.all()
        product_context = "\n".join([f"- {p.name}: ${p.price}. {p.description} (Category: {p.category})" for p in products])
        
        system_prompt = (
            "You are 'Lux', a sophisticated, polite, and helpful AI Advisor for a Luxury Shopping Website. "
            "Your persona is professional yet warm, embodying the elegance of the brand. "
            "You have access to the following product catalog:\n\n"
            f"{product_context}\n\n"
            "Answer the customer's question based on this catalog. "
            "Recommend products if they fit the user's needs. "
            "If the user asks about something not in the catalog, politely steer them back to our offerings. "
            "Keep your answers concise (under 150 words) unless detailed product info is requested."
        )

        answer = ""
        
        if provider == 'gemini':
            client = genai.Client(api_key=final_api_key, http_options={'api_version': 'v1alpha'})
            # Feed system prompt as first message effectively
            full_prompt = f"{system_prompt}\n\nUser Question: {user_question}"
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=full_prompt
            )
            answer = response.text
        else:
            client = openai.OpenAI(api_key=final_api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ]
            )
            answer = response.choices[0].message.content
            
        return jsonify({'answer': answer})
    except Exception as e:
        products = Product.query.all()
        fallback = _fallback_advisor_answer(user_question, products)
        if fallback:
            return jsonify({'answer': fallback, 'fallback': True})
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', email='admin@luxury.com', is_admin=True)
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            
            sample_products = [
                Product(name='Luxury Watch', description='Premium Swiss-made timepiece with gold plating', price=2500.00, category='Watches', image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400'),
                Product(name='Designer Handbag', description='Italian leather handbag with premium hardware', price=1800.00, category='Bags', image_url='https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400'),
                Product(name='Silk Scarf', description='100% pure silk scarf with exclusive designer print', price=350.00, category='Accessories', image_url='https://uk.silksilky.com/cdn/shop/files/1603004566_7c8e1b0d-c9e9-482a-9497-54e0a16fbd8c.jpg?v=1762889111&width=550'),
                Product(name='Leather Jacket', description='Genuine brown leather jacket with classic cut', price=1200.00, category='Clothing', image_url='https://images.unsplash.com/photo-1521223890158-f9f7c3d5d504?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'),
                Product(name='Diamond Ring', description='18k gold ring with brilliant cut diamond', price=5500.00, category='Jewelry', image_url='https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400'),
                Product(name='Premium Sunglasses', description='Designer sunglasses with UV protection', price=450.00, category='Accessories', image_url='https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400')
            ]
            
            for product in sample_products:
                db.session.add(product)
            
            db.session.commit()

        silk_scarf = Product.query.filter_by(name='Silk Scarf').first()
        if silk_scarf and silk_scarf.image_url != 'https://uk.silksilky.com/cdn/shop/files/1603004566_7c8e1b0d-c9e9-482a-9497-54e0a16fbd8c.jpg?v=1762889111&width=550':
            silk_scarf.image_url = 'https://uk.silksilky.com/cdn/shop/files/1603004566_7c8e1b0d-c9e9-482a-9497-54e0a16fbd8c.jpg?v=1762889111&width=550'
            db.session.commit()

        leather_jacket = Product.query.filter_by(name='Leather Jacket').first()
        if leather_jacket and leather_jacket.image_url != 'https://images.unsplash.com/photo-1521223890158-f9f7c3d5d504?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80':
            leather_jacket.image_url = 'https://images.unsplash.com/photo-1521223890158-f9f7c3d5d504?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'
            db.session.commit()
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
