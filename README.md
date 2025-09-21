# Privato

Privato is a SDK for building secure and privacy-focused applications. It provides tools and libraries to help developers create applications that analyze and redact personal identifiable information (PII).

Privato provides both an API and a web interface for easy interaction.

## Features

- PII Detection: Identify and classify various types of PII in text data.
- Redaction: Automatically redact sensitive information to protect user privacy.
- Customizable: Extend and customize the detection and redaction capabilities to fit specific needs.
- Easy Integration: Simple API for seamless integration into existing applications.
- Web Interface: User-friendly web interface for manual review and redaction.

## Installation
You can install Privato using pip:

```bash
pip install privato
```

## Usage
Here's a simple example of how to use Privato to detect and redact PII in text:

```py
from privato.core.redactor import Redactor

text = "John's email is john.doe@example.com and his phone number is (123) 456-7890."
redactor = Redactor()
redacted_text = redactor.redact_text(text)['text']
print(redacted_text)
```
This will output:
```
"<PERSON>'s email is <EMAIL_ADDRESS> and his phone number is <PHONE_NUMBER>."
```

## Web Interface
To run the web interface, use the following command:

```bash
uvicorn privato.app.main:app --reload
```

To start the frontend, navigate to the `privato/static` directory and run:

```bash
npm install
npm run dev
```

Then, open your browser and go to `http://localhost:5173`.

## Docs
For more detailed documentation, visit the [Privato Documentation](https://github.com/Mohammed-Saajid/privato).