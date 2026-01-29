# Luxury Shopping Website

A premium e-commerce platform built with Flask, featuring user authentication, product catalog, shopping cart, and order management.

## Features

- **User Authentication**: Secure login/registration system with password hashing
- **Product Catalog**: Browse luxury products with categories and search
- **Shopping Cart**: Add/remove items with real-time cart updates
- **Order Management**: Complete order processing with status tracking
- **Admin Panel**: Product management and order administration
- **Modern UI**: Responsive design with Tailwind CSS
- **SQL Database**: Azure SQL Database with SQLAlchemy ORM

## Installation

1. Clone the repository:
```bash
cd luxury-shopping
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Database Setup

This project uses an external SQL database for all data storage (recommended: **Azure SQL Database**).

### Required Environment Variable:

Set the `DATABASE_URL` environment variable with your database credentials:

```bash
DATABASE_URL=mssql+pyodbc://USERNAME:PASSWORD@luxurydatabase.database.windows.net:1433/luxurydb?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no
```

### Quick Start for Team Members:

1. **Clone the repository:**
```bash
git clone [your-repo-url]
cd luxuryshoppingwebsite-1
```

2. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set database connection:**
```powershell
# Option A: Environment variable (recommended)
$env:DATABASE_URL = "mssql+pyodbc://USERNAME:PASSWORD@luxurydatabase.database.windows.net:1433/luxurydb?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"

# Option B: Create .env file
echo DATABASE_URL=mssql+pyodbc://USERNAME:PASSWORD@luxurydatabase.database.windows.net:1433/luxurydb?driver=ODBC+Driver+18+for+SQL+Server\&Encrypt=yes\&TrustServerCertificate=no > .env
```

5. **Run the application:**
```bash
./venv/bin/python3 app.py
```

### Important Notes:

- **Never commit** `.env` file to GitHub (it's in .gitignore)
- **Share database credentials** securely with your team
- **All team members** will connect to the same database

The application will be available at `http://localhost:5000`

## Default Credentials

- **Admin**: username: `admin`, password: `admin123`
- **Regular User**: Register through the signup form

## Database

The application uses the database specified by `DATABASE_URL`. Tables are automatically created on first run. The database includes:

- Users table with authentication data
- Products table with inventory
- Shopping cart functionality
- Orders and order items tracking

## Project Structure

```
luxury-shopping/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage with product catalog
│   ├── login.html        # User login page
│   ├── register.html     # User registration page
│   ├── product.html      # Product detail page
│   ├── cart.html         # Shopping cart page
│   ├── orders.html       # User orders page
│   ├── admin.html        # Admin dashboard
│   └── add_product.html  # Add product form
└── .env.example         # Environment variables template
```

## Usage

1. **Browse Products**: Visit the homepage to see featured products
2. **Register/Login**: Create an account or login with existing credentials
3. **Add to Cart**: Click "Add to Cart" on any product
4. **Checkout**: Review cart items and place order
5. **Track Orders**: View order history and status in "Orders" section
6. **Admin Access**: Use admin credentials to manage products and orders

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: Azure SQL Database (recommended) with SQLAlchemy ORM
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Authentication**: Flask-WTF with password hashing
- **Icons**: Font Awesome
- **Images**: Unsplash placeholder images

## Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Session-based authentication
- Input validation and sanitization
- SQL injection prevention with SQLAlchemy ORM

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Feel free to modify and use according to your needs.
