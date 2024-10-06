# DynamicLearningApp

## Introduction

DynamicLearningApp is a Flask-based web application designed to help users manage and view saved tiles with rich content. This application leverages advanced technologies such as LangChain and integrates various APIs to provide a seamless and interactive user experience.

## Features

- **User-Friendly Interface:** Built with Tailwind CSS for a responsive and modern design.
- **Dynamic Content Management:** Easily add, view, and manage content tiles.
- **Keyword Highlighting:** Automatically detects and highlights keywords within entries.
- **Address Management:** Allows users to input and manage their address information via a popup modal.
- **Extensible Architecture:** Easily integrable with other libraries and services through LangChain.

## Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/DynamicLearningApp.git
cd DynamicLearningApp
```

### 2. Create a New Branch

It's good practice to create a new branch for your work to keep the main branch clean.

```bash
git checkout -b your-feature-branch
```

### 3. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 4. Install Requirements

Install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

To run the application locally:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Navigate to `http://localhost:5000` in your web browser to access the application.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with clear messages.
4. Push your branch to your forked repository.
5. Create a pull request detailing your changes.

## License
This project is licensed under the [MIT License](LICENSE).

