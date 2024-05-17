import cv2

def draw_boxes_and_extract_insets(image_path, output_image_path, inset_paths, box_coords):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image: {image_path}")
        return

    insets = []

    for (x, y, w, h) in box_coords:
        # Extract the inset
        inset = image[y:y + h, x:x + w].copy()
        
        # Draw a red box on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # Draw a red box on the inset
        cv2.rectangle(inset, (0, 0), (w-1, h-1), (0, 0, 255), 2)
        
        insets.append(inset)

    # Save the image with boxes
    cv2.imwrite(output_image_path, image)

    # Save the insets
    for inset, inset_path in zip(insets, inset_paths):
        cv2.imwrite(inset_path, inset)

# Coordinates for the two boxes (x, y, width, height)
box_coords = [
    (350, 450, 100, 100),   # Coordinates for the first box
    (455, 275, 90, 90)  # Coordinates for the second box
]

# Process each image
image_files = ['gt.png', 'ours.png', 'nero.png']
output_files = ['gt_with_boxes.png', 'ours_with_boxes.png', 'nero_with_boxes.png']
inset_prefixes = ['gt_inset', 'ours_inset', 'nero_inset']

for img_file, out_file, prefix in zip(image_files, output_files, inset_prefixes):
    inset_paths = [f"{prefix}1.png", f"{prefix}2.png"]
    draw_boxes_and_extract_insets(img_file, out_file, inset_paths, box_coords)

print("Processing completed.")
