## Models
Privato utilizes pre-trained machine learning models to enhance its ability to detect and redact sensitive information from images. The models used in Privato are based on the YOLO (You Only Look Once) architecture, which is known for its speed and accuracy in object detection tasks.

### Available Models

1. **Signature Detection Model**: This model is trained to identify handwritten signatures in images. It is particularly useful for redacting signatures from scanned documents or images containing personal information. 
Link to the model repository: [YOLOv8 Signature Detector](https://huggingface.co/tech4humans/yolov8s-signature-detector)


2. **Face Detection Model**: This model is designed to detect human faces in images. It can be used to redact faces from photographs or any images where privacy needs to be maintained.
Link to the model repository: [YOLOv8 Face Detector](https://huggingface.co/arnabdhar/YOLOv8-Face-Detection)

### Model Files
The model files are stored in the `privato/ml/model` directory and include:
- `signature_model.onnx`: The ONNX format file for the signature detection model.
- `face_model.pt`: The PyTorch format file for the face detection model.

### Loading Models
Privato automatically loads these models when the application is initialized. The models are integrated into the image analysis and redaction processes, allowing users to easily detect and redact signatures and faces from images.

### Custom Models
While Privato comes with pre-trained models for signature and face detection, users can also integrate their own custom models if needed. This can be done by modifying the `inference.py` file in the `privato/ml` directory to load and utilize the custom models as per the user's requirements.