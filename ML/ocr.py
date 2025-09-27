# import easyocr

# reader = easyocr.Reader(['en'], gpu=False, verbose=False)


# def run_ocr(image_path: str) -> str:
#     """
#     Run OCR on an image/PDF and return extracted text.
    
#     Args:
#         image_path (str): Path to the image or PDF.
#         min_confidence (float): Confidence threshold for filtering results.

#     Returns:
#         str: Combined extracted text.
#     """

#     print("OCR STARTED.......")
    
#     # Perform OCR
#     results = reader.readtext(image_path)

#     # Filter by confidence and join text
#     extracted_texts = [text for _, text, conf in results ]
#     combined_text = " ".join(extracted_texts)

#     print("OCR DONE.......")

#     return combined_text



# app/ocr.py
from paddleocr import PaddleOCR
from PIL import Image

# Initialize PaddleOCR
ocr = PaddleOCR(lang='en', use_angle_cls=True)

def run_ocr(image_path: str) -> str:
    """
    Run OCR on the given image file and return combined text.
    """
    results = ocr.ocr(image_path)  # returns a list of lists of boxes + texts
    
    for res in results:
        # Access JSON dict
        res_json = res.json  # this is a dict containing detection + recognition info
        rec_texts = res_json['res']['rec_texts']
        full_text = " ".join(rec_texts)
        print("Combined text:", full_text)

    return full_text

