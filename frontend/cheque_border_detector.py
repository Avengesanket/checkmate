import cv2
import os

def detect_and_crop_cheque_borders(image_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(image_folder):
        if filename.endswith(".png"):
            image = cv2.imread(os.path.join(image_folder, filename))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 30, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            largest_contour = max(contours, key=cv2.contourArea, default=None)
            if largest_contour is not None:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cheque = image[y:y + h, x:x + w]
                if w > 300 and h > 100:
                    cv2.imwrite(os.path.join(output_folder, f"cropped_{filename}"), cheque)