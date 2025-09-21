# Quickstart Guide
Welcome to Privato! This quickstart guide will help you get up and running with the Privato application, which is designed to analyze and redact private data from images and documents.
## Prerequisites
Before you begin, ensure you have the following prerequisites installed:

- Python 3.11 or higher

- pip (Python package installer)

- uv (Python package manager)

## Installation
To install Privato, you can use pip. Open your terminal and run the following command:

```sh

pip install privato

```


## Running the Application
Once installed, you can start the Privato application using the command line interface (CLI). Open your terminal and run:

```sh

privato --help

```

This command will display the available commands and options for using Privato.

## Analyzing an Image

To analyze an image for Personally Identifiable Information (PII), use the following command:

```sh
privato analyzer analyze --file path/to/your/image.jpg --language en
```

## Redacting an Image

To redact Personally Identifiable Information (PII) from an image, use the following command:

```sh
privato redactor redact --file path/to/your/image.jpg --language en --output path/to/save/redacted_image.jpg
```