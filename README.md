# Task Manager Application

A task manager application built with Flask, MongoDB, Flask-Login, and Socket.IO. This project demonstrates an advanced understanding of Python web development, real-time communication, and NoSQL database integration.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

The Task Manager application is designed to efficiently manage tasks with real-time updates. Users can register, log in, create, update, and delete tasks. The application leverages modern web technologies to provide a responsive and interactive user experience.

## Features

- **User Authentication**: Secure user registration and login functionality using Flask-Login.
- **Task Management**: Full CRUD (Create, Read, Update, Delete) operations for tasks.
- **Real-Time Updates**: Real-time task updates using Socket.IO.
- **Responsive Design**: Responsive and interactive frontend built with Bootstrap.
- **Comprehensive Documentation**: Clear and concise documentation for installation, usage, and contribution.

## Architecture

The application is structured as a monolithic Flask application with the following components:

- **Backend**: Flask framework with RESTful API endpoints.
- **Frontend**: HTML templates rendered by Flask with dynamic content updates via JavaScript and Socket.IO.
- **Database**: MongoDB for flexible and scalable data storage.
- **Real-Time Communication**: Socket.IO for real-time task updates.

## Installation

### Prerequisites

- Python 3.8+
- MongoDB
- Node.js (for Socket.IO)

### Steps

1. **Clone the repository**:
   ```sh
   git clone https://github.com/pn300/project-task-manager.git
   cd project-task-manager

2. **Set up a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt

4. **Set up the MongoDB database**
   - Ensure MongoDB is running on your machine.
   - Create a database named `taskmanager`

5. **Run the application:**
    ```sh
    python app.py

## Usage

1. **Register a new account.**
2. **Log in with your credentials.**
3. **Create, update, and delete tasks:**
   - Navigate to the Tasks page to manage your tasks.
   - Real-time updates will be reflected immediately.

## Contributing

Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Open a pull request.

Please ensure your code follows the project's coding standards and passes all tests. 
