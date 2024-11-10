# DRF Library API Service

A simple API service for managing and borrowing books from a library.

## Features

### Book Management
- Create, Retrieve, List, Update, Delete books

### Borrowing Management
- Create, Retrieve, List, Update borrowings

### Payment Management
- List, Retirieve payments

### User Management
- Register a new user with an e-mail and password.
- Access basic user data.
- Obtain both access and refresh tokens for authentication.
- Use the refresh token to get a new access token.
- Check if your access token is still valid.  

### Stripe Payments Management
- Create stipe checkout payment session via stripe API
- Get redirects to *success* or *cancel* pages 

### Telegram Notification
- Send a notification to Telegram via a bot each time a new borrowings is created

### Additional Features 
- View the API documentation and schema via */api/doc/swagger/* or */api/doc/redoc/*.
- Access the admin panel at */admin/* to manage all the models.

## How to Launch the Project without Docker

### 1. Clone the Repository

```
git clone https://github.com/Meksim-fesh/drf-library.git
cd drf-library
```
### 2. Create and Activate Virtual Environment

```
python -m venv venv # Or python3 -m venv venv
source venv\Scripts\activate # Or source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Rename the `.env.example` file to `.env` and set your environment variables:

- For Telegram notification: *You need to create own telegram bot and obtain a token and own id.*
- For Stripe: *You need to create an account*
- For PostgreSQL: *You need to create a PostgreSQL local database*

```
SECRET_KEY=your-secret-key
DEBUG=True
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_USER_ID=your-telegram-user-id
STRIPE_API_KEY=your-stripe-api-key
POSTGRES_PASSWORD=your-db-password
POSTGRES_USER=your-db-user
POSTGRES_DB=your-db-db
POSTGRES_HOST=your-db-host
POSTGRES_PORT=your-db-port
```

### 5. Apply Migrations

```
python manage.py migrate
```

### 6. Create a Superuser

```
python manage.py createsuperuser
```

### 7. Run the Server

```
python manage.py runserver
```

### Using SQLite3

To use SQLite3 db you need to change following lines in `settings.py` file

from:

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
    }
}
```

to:

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

## How to Launch the Project With Docker

### 1. Go Through Steps 1-5 Above

### 2. Build the Container

```
docker-compose build
```

### 3. Start the Container

```
docker-compose up
```

## How to Gain an Access

### 1. Create User

Create regular user at */api/user/register/*

or create super user (admin) with the command from the above-mentioned Step 6:

```
python manage.py createsuperuser
```

### 2. Get Access Token

Go to */api/user/token/* to get an access token.

To use token you can download *ModHeader* extension for *Google Chrome*/*Opera* or *Modify Header Value* for *Firefox*

Example:

**Header Name**: Authorize

**Header Value**: Bearer your-token

By default, the access token has a short validity period (5 minutes). You can change this in `settings.py` file by modifying following line:

```
"ACCESS_TOKEN_LIFETIME": timedelta(minutes=5)
```

## License

This project is licensed under the MIT License.
