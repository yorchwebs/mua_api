# MUA API

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Flask Version](https://img.shields.io/badge/flask-3.1-blue.svg)](https://flask.palletsprojects.com/)
[![Postman Docs](https://img.shields.io/badge/docs-Postman-orange?logo=postman)](https://documenter.getpostman.com/view/33534242/2sB3WtrySp)

A simple and robust Flask API to handle newsletter subscriptions with MailerLite and contact form submissions via SMTP.

---

## Features

- **Newsletter Subscription:** `/subscribe` endpoint to add users to a MailerLite mailing list.
- **Contact Form:** `/contact` endpoint to send contact form data via SMTP.
- **Validation:** Uses Pydantic for request data validation.
- **Configuration:** Manages settings with `python-decouple` for easy environment-based configuration.
- **Containerization:** Docker support for easy deployment.
- **Testing:** Comprehensive test suite using `pytest`.

---

## Getting Started

### Prerequisites

- Python 3.12+
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yorchwebs/mua-api.git
    cd mua_api
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements-dev.txt
    ```

---

## CORS Configuration

CORS is currently enabled for all origins (`*`) to simplify local development.
**⚠️ In production, this should be restricted** to the specific domain(s) that will consume the API— for example:

```python
CORS(app, origins=["https://yourfrontenddomain.com"])
```

---

### Configuration

Create a `.env` file in the root of the project and add the following environment variables:

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
