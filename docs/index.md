# Welcome to Privato's Documentation

This documentation provides comprehensive information about Privato, a python package designed to identify and redact personally identifiable information (PII) from data.

## Overview
Privato is a powerful tool that leverages various techniques to detect and redact sensitive information from various data formats. It is built using Python on top of Microsoft Presidio and utilizes various Open Source machine learning models for accurate PII detection.
The package is designed to be easy to use and integrate into existing workflows, making it an ideal choice for developers and companies looking to enhance their data privacy practices.

For ease of use, Privato offers both a Command-Line Interface (CLI) and a RESTful API. This allows users to choose the method that best fits their needs, whether they prefer to work directly from the terminal or integrate Privato's capabilities into their applications via API calls.

## Features
- **Analysis**: Identify PII in text using a combination of pattern matching, machine learning models, and custom recognizers.
- **Redaction**: Remove or mask identified PII from text to protect sensitive information.


## Installation
To install Privato, ensure you have Python 3.11+ and Uv (Python Package Manager) installed. You can then install the package using the following command:

```sh
pip install privato
```
