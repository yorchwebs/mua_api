# MUA API

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Flask Version](https://img.shields.io/badge/flask-3.1-blue.svg)](https://flask.palletsprojects.com/)
[![Postman Docs](https://img.shields.io/badge/docs-Postman-orange?logo=postman)](https://documenter.getpostman.com/view/your-doc-id)

A simple and robust Flask API to handle newsletter subscriptions with MailerLite and contact form submissions via SMTP.

---

## Features

- **Newsletter Subscription:** `/subscribe` endpoint to add users to a MailerLite mailing list.
- **Contact Form:** `/contact` endpoint to send contact form data via SMTP.
- **Validation:** Uses Pydantic for request data validation.
- **Configuration:** Manages settings with `python-decouple` for easy environment-based configuration.
- **CORS Support:** Enabled globally for development.
- **Containerization:** Docker support for easy deployment.

---

## CORS Configuration

CORS is currently enabled for all origins (`*`) to simplify local development.
**⚠️ In production, this should be restricted** to the specific domain(s) that will consume the API — for example:

```python
from flask_cors import CORS

CORS(app, origins=["https://yourfrontenddomain.com"])
This helps prevent unauthorized cross-origin requests and improves your API’s security.

Getting Started
Prerequisites
Python 3.12+
```

Docker (optional, for containerized deployment)

---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/mua-api.git
cd mua-api
```

### Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements-dev.txt
```

### Configuration

Create a .env file in the root of the project and add the following environment variables:

```bash
# MailerLite Configuration
MAILERLITE_API_KEY=your_mailerlite_api_key
MAILERLITE_GROUP_ID=your_mailerlite_group_id

# SMTP Configuration
SMTP_HOST=your_smtp_host
SMTP_PORT=your_smtp_port
SMTP_USER=your_smtp_user
SMTP_PASSWORD=your_smtp_password
SMTP_FROM=your_smtp_from_address
SMTP_TO=your_smtp_to_address
```
---

## Email Setup Guide

You can configure the API to send emails using Gmail SMTP or a custom domain.

### 🔹 Using Gmail
- Go to your Google Account → Security section.

- Enable 2-Step Verification (required to use App Passwords).

- Generate an App Password for “Mail”.

- Use the following configuration in your .env file:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_generated_app_password
SMTP_FROM=your_email@gmail.com
SMTP_TO=destination_email@example.com
```

**⚠️ Regular Gmail passwords won’t work — App Passwords are required.**

---

### 🔹 Using a Custom Domain (e.g., via your hosting provider)

- Locate your domain’s email service settings (e.g., Zoho, Outlook, Namecheap, Hostinger, etc.).

- Obtain the SMTP details (host, port, username, and password).

- Add SPF and DKIM records to your DNS for better deliverability.

- Update your .env file with your domain’s details, for example:

```bash
SMTP_HOST=mail.yourdomain.com
SMTP_PORT=587
SMTP_USER=contact@yourdomain.com
SMTP_PASSWORD=your_password
SMTP_FROM=contact@yourdomain.com
SMTP_TO=support@yourdomain.com
```

- Running the Application
- Local Development
- Run the application in development mode:

```bash
python run.py
```

The application will be available at:

```bash
http://127.0.0.1:5000
```

---

## Production with Docker

Build the Docker image

```bash
# Copiar código
docker build -t mua-api .
```

Run the Docker container

```bash
# Copiar código
docker run -p 8080:8080 --env-file .env mua-api
```

The application will be available at:

```bash
# Copiar código
http://0.0.0.0:8080
```

---

## API Endpoints

/subscribe

Method: POST

Description: Subscribes a user to the MailerLite mailing list.

Request Body:

```json
{
  "email": "user@example.com"
}
```

Responses:

**200 OK:** Subscription successful.

**422 Unprocessable Entity:** Invalid input data.

**400 Bad Request:** Error from MailerLite API.

---

/contact

Method: POST

Description: Sends a contact form submission via SMTP.

Request Body:

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "123-456-7890",
  "message": "This is a test message."
}
```

Responses:

**200 OK:** Email sent successfully.

**400 Bad Request:** Missing required fields.

**500 Internal Server Error:** Error sending the email.

---

## Postman API Documentation

Interactive API documentation is available via Postman:

[![Postman Docs](https://img.shields.io/badge/docs-Postman-orange?logo=postman)](https://documenter.getpostman.com/view/your-doc-id)

This documentation includes:

- Example requests and responses.

- The ability to test endpoints directly.

- A “Run in Postman” button for easy import.

---

## Testing
To run the test suite, use the following command:

```bash
# Copiar código
pytest
```

---

## Dependencies

Production:

- Flask

- Flask-Cors

- gunicorn

- pydantic

- python-decouple

- requests

Development

- pytest

and all production dependencies.

See requirements-prod.txt and requirements-dev.txt for details.
