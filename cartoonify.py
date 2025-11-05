import cv2
import numpy as np

def cartoonify_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image from path: '{image_path}'")
        return

    # Resize image to width 600px (maintaining aspect ratio)
    height, width, _ = img.shape
    new_width = 600
    new_height = int((new_width / width) * height)
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Convert to grayscale and reduce noise
    gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.medianBlur(gray_img, 5)

    # Edge mask
    edges = cv2.adaptiveThreshold(
        gray_img, 
        255, 
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 
        9, 
        9
    )

    # Smooth colors (cartoon effect)
    color_img = resized_img
    for _ in range(7):
        color_img = cv2.bilateralFilter(color_img, d=9, sigmaColor=9, sigmaSpace=7)

    # Combine edges with color image
    cartoon_img = cv2.bitwise_and(color_img, color_img, mask=edges)

    # Show results
    cv2.imshow("Original Image", resized_img)
    cv2.imshow("Cartoon Image", cartoon_img)

    # Save output
    cv2.imwrite("cartoon_output.png", cartoon_img)
    print("\n✅ Cartoonified image saved as **cartoon_output.png**")

    print("Press any key to close windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    path = input("Enter the path to your image: ")
    cartoonify_image(path)
