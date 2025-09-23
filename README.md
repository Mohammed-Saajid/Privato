# Privato

Privato is a SDK for building secure and privacy-focused applications. It provides tools and libraries to help developers create applications that analyze and redact personal identifiable information (PII).

Privato provides both an API, CLI and a web interface for easy interaction.

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
To run the Backend, use the following command:

```bash
privato api run
```

Then, open your browser and go to `http://127.0.0.1:8080`.


## Make Commands
- `make help`: List all available make commands.
- `make install`: Install the required dependencies.
- `make install-dev`: Install development dependencies.
- `make test`: Run the test suite.
- `make run`: Start the FastAPI Development server.
- `make clean`: Remove temporary files and directories.
- `make deploy`: Build and run the Docker container.
- `make down`: Stop and remove the Docker container.


## Docs
For more detailed documentation, visit the [Privato Documentation](https://mohammed-saajid.github.io/Privato/).