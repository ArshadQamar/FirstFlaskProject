# Social Networking Application

A simple social networking application built using Flask and SQLite. The application allows users to log in, send and receive messages, and view their message history.

## Features

- **User Authentication**: Secure login functionality where users can sign in with their credentials.
- **Messaging System**: Users can send and receive messages to/from other users and view their chat history.
- **Database**: Utilizes SQLite to store user and message data.
- **Responsive**: Basic HTML forms for messaging, displaying message history, and user login.

## Technologies Used

- **Flask**: Lightweight Python web framework for the backend.
- **SQLite**: Relational database used to store user and message data.
- **HTML**: Used for the front-end interface of the application.
- **Jinja2**: Templating engine for rendering dynamic HTML.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ArshadQamar/FirstFlaskProject/
   cd FirstFlaskProject


2. Set up a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Set up the database:
    - Ensure SQLite is available on your system.
    - The app automatically creates the necessary database tables on first run.

5. Run the application:
    ```bash
    flask run
    The app will be available at http://127.0.0.1:5000/.

## Usage
- **Login**: Users can log in using their username and password.
- **Messages**: Users can send messages to other users by entering their recipient's username and the message content. The sent message will appear in the chat history.
- **View Chat History**: Users can see their received messages displayed on the same page after sending messages.

## Contributing
If you want to contribute, feel free to fork the repository, create a branch, and submit a pull request with your changes.

## License
This project is open source and available under the MIT License.