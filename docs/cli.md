# CLI Commands
This document provides an overview of the command-line interface (CLI) commands available in Privato for analyzing and redacting private data from images and documents.

## The `cli` Module
::: privato.cli.main

## Command Structure
Privato's CLI is built using Typer, which allows for easy command definition and argument parsing. The main CLI application is defined in `privato/cli/main.py`, and it includes subcommands for analysis and redaction.

## Available Commands
### 1. Analyze Command
- **Command**: `privato analyzer analyze`
- **Description**: Analyzes an image or a directory of images to detect private data such as signatures and faces.
- **Arguments**:
  - `--path`: Path to the image file or directory to be analyzed.
  - `--language`: (optional) Language code for text detection (default is "en").
  - `--hide-output`: (optional) If set, the output will not be printed to the console.
  - `--save-output`: (optional) If set, the analysis results will be saved to a JSON file.
  - `--output-path`: (optional) Path to save the output JSON file (default is None).

- **Example**:
  ```sh
    privato analyzer analyze --path path/to/your/image.jpg --language en --save-output --output-path path/to/save/results
  ```

### 2. Redact Command
- **Command**: `privato redactor redact`
- **Description**: Redacts private data from an image or a directory of images based on detected entities.
- **Arguments**:
    - `input_path`: Path to the image file or directory to be redacted.
    - `output_path`: Path to save the redacted image or directory of images.
    - `--language`: (optional) Language code for text detection (default is "en").

- **Example**:
  ```sh
    privato redactor redact input_path path/to/your/image.jpg output_path path/to/save/redacted_image.jpg --language en
  ```

## Help Command
To view the help message and see all available commands and options, you can run:
```sh
privato --help
```
This will display a list of all commands, their descriptions, and the arguments they accept.