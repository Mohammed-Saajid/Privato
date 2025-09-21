# API Reference

Privato provides a RESTful API for analyzing and redacting private data from images. This document outlines the available endpoints, request/response formats, and usage examples.

## The `api` Module

::: privato.app.main 

## API Endpoints
The API is accessible at the base URL `/api/v1`. Below are the primary endpoints:

### 1. Analyze Image
- **Endpoint**: `/analyze`

- **Method**: `POST`

- **Description**: Analyzes an image to detect private data such as signatures and faces.
- **Request**:
  - **Headers**: `Content-Type: multipart/form-data`
  - **Body**: 
    - `file`: The image file to be analyzed.
    - `language`: (optional) Language code for text detection (default is "en").
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: JSON object containing detected entities and their bounding boxes.

### 2. Redact Image
- **Endpoint**: `/redact`
- **Method**: `POST`
- **Description**: Redacts private data from an image based on detected entities.
- **Request**:
  - **Headers**: `Content-Type: multipart/form-data`
  - **Body**: 
    - `file`: The image file to be redacted.
    - `language`: (optional) Language code for text detection (default is "en").
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: The redacted image file.



