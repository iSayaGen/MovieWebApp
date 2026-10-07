# 🎬 MovieWeb

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![OMDb API](https://img.shields.io/badge/API-OMDb-222222)](https://www.omdbapi.com/)

A modern Flask web application for creating and managing personal movie collections.

MovieWeb uses the **OMDb API** to automatically retrieve movie information such as posters, release years, and directors when a movie is added.

---

## 🎥 Features

- Create and manage users
- Create personal movie collections
- Search for movies through the OMDb API
- Automatically display movie posters
- Display release year and director
- Prevent duplicate movies within the same user's collection
- Remove movies from a collection
- User-friendly error and success messages
- Responsive, modern dark-themed interface
- SQLite database for local persistence
- Environment variables for API credentials

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Application logic |
| **Flask** | Web framework |
| **Flask-SQLAlchemy** | Database integration |
| **SQLAlchemy 2.0** | ORM and database queries |
| **SQLite** | Local database |
| **OMDb API** | Movie metadata |
| **Jinja2** | HTML templating |
| **HTML & CSS** | User interface |
| **python-dotenv** | Environment variable management |
| **Requests** | HTTP requests to OMDb |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- Python 3.x
- pip
- An [OMDb API key](https://www.omdbapi.com/apikey.aspx)

### 1. Clone the repository

```bash
git clone https://github.com/iSayaGen/MovieWebApp.git
cd MovieWebApp
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OMDB_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

Replace `your_api_key_here` with your OMDb API key.

The `.env` file is intentionally excluded from Git and should **never be committed**.

### 5. Run the application

```bash
python app.py
```

Then open the application in your browser at:

```text
http://127.0.0.1:5000
```

---

## 🎞️ How It Works

MovieWeb organizes movies into individual user collections.

### Add a movie

1. Create or select a user.
2. Enter a movie title.
3. MovieWeb sends the title to the OMDb API.
4. OMDb returns the available movie information.
5. MovieWeb stores the movie in the SQLite database.
6. The movie is displayed in the user's collection.

For example:

```text
Inception
    ↓
OMDb API
    ↓
┌─────────────────────────────┐
│ Title:    Inception         │
│ Year:     2010              │
│ Director: Christopher Nolan │
│ Poster:   [Poster URL]      │
└─────────────────────────────┘
    ↓
MovieWeb Database
```


---

## 📁 Project Structure

```text
MovieWebApp/
├── app.py                  # Flask application and routes
├── data_manager.py         # Database operations
├── models.py               # SQLAlchemy models
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── .gitignore
│
├── data/
│   └── movies.db           # Local SQLite database (not committed)
│
├── static/
│   └── style.css           # Application styling
│
└── templates/
    ├── base.html
    ├── index.html
    ├── movies.html
    ├── 404.html
    └── 500.html
```

---

## 🗄️ Database

MovieWeb uses **SQLite** with **Flask-SQLAlchemy**.

The database is created automatically when the application starts:

```python
with app.app_context():
    db.create_all()
```

The local database file is stored at:

```text
data/movies.db
```

The `data/` directory is ignored by Git so that local database files are not committed to the repository.

---

## 🔌 OMDb API

MovieWeb uses the **OMDb API** to retrieve movie information.

When a user enters a movie title, the application sends a request to OMDb and retrieves information such as:

- Movie title
- Release year
- Director
- Poster

The returned information is then stored in the local SQLite database.

The API endpoint used by the application is:

```text
https://www.omdbapi.com/
```

---

## ⚠️ Error Handling

MovieWeb includes custom error pages for common server errors:

- **404 — Page Not Found**
- **500 — Internal Server Error**

The application also handles common API and database errors and displays user-friendly flash messages instead of exposing technical error details.

---

## 🎨 Design

The interface uses a modern dark theme with:

- Responsive movie cards
- Movie posters
- User collection cards
- Styled forms and buttons
- Success and error notifications
- Empty-state screens
- Custom error pages
- Responsive layouts for smaller screens

The goal is to keep the interface simple while still making the application feel like a polished movie collection website.

---

## 📚 Project Context

MovieWeb was built as part of a Flask and SQLAlchemy learning project.

The project focuses on practicing:

- Flask routing
- Jinja2 templates
- Forms and POST requests
- SQLAlchemy 2.0 models
- Database CRUD operations
- External API integration
- Environment variables
- Error handling
- Git and GitHub workflows

---

## 📄 License

This project was created for educational purposes.