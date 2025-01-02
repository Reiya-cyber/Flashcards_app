# Web App for Basic Authentication Practice

This web app is developed to practice basic authentication coding and web app functionality. It allows you to explore the implementation of user authentication in a web application.

## Setup Instructions

To use this app, follow these steps:

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/Reiya-cyber/Flashcards_app.git
    cd Flashcards_app
    ```

2. Open the `website/__init__.py` file in a code editor.

3. Locate **line 21** and **line 22** in the file.

4. Replace the placeholder values with your Gmail address and Google app password:
    ```python
    # Example
    app.config['MAIL_USERNAME'] = 'your-gmail-address@gmail.com'  # Line 21
    app.config['MAIL_PASSWORD'] = 'your-google-app-password'  # Line 22
    ```

5. Save the file.

6. Run the application:
    ```bash
    python3 main.py
    ```

## Requirements

- Python 3.x
- flask
- flask_sqlalchemy
- flask_login
- flask_mail
- sqlalchemy
- werkzeug

## Notes

- Make sure you enable "Less secure app access" in your Google account settings to allow the app to log in.
- The Gmail address should be your full email (e.g., `your-email@gmail.com`).
- The Google app password can be generated from your Google account settings if you have two-factor authentication enabled.
