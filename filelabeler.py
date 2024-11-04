import subprocess
import argparse
from PIL import Image, ImageDraw, ImageFont
import os

def load_font(font_path, font_size):
    """
    Load the specified font; if unavailable, fall back to the default font.
    """
    try:
        return ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font at {font_path} not found. Using default font.")
        return ImageFont.load_default()

def calculate_text_position(draw, text, font, image_width, image_height):
    """
    Calculate the position to center the text on the image.
    """
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2
    return x, y

def calculate_appropriate_font_size(text, max_width, max_height, font_path="/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"):
    """
    Calculate the maximum font size that allows the text to fit within the specified dimensions.
    """
    font_size = 200  # Start with a large font size, based on label height
    while font_size > 0:
        font = ImageFont.truetype(font_path, font_size)
        # Create a temporary image to calculate the text size
        temp_image = Image.new("RGB", (max_width, max_height))
        draw = ImageDraw.Draw(temp_image)
        
        # Get text bounding box
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Check if text fits within label dimensions
        if text_width <= max_width and text_height <= max_height:
            return font_size  # Return the largest font size that fits

        # Reduce font size and try again
        font_size -= 1

    return font_size  # Return the smallest font size if no fitting size is found

def create_label_image(text, font_size=None, width=900, height=300):
    """
    Create a label image with centered text and save it to a file in /tmp.
    """
    #filename = "/tmp/label.png"  # Save image to /tmp directory
    filename = "./label.png"
    # Calculate font size if not specified
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"
    if font_size is None:
        font_size = calculate_appropriate_font_size(text, width, height, font_path)

    # Load the calculated or specified font size
    font = load_font(font_path, font_size)

    # Create the label image and draw text
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Calculate text position and draw text
    x, y = calculate_text_position(draw, text, font, width, height)
    draw.text((x, y), text, fill="black", font=font)
    
    # Flip the image horizontally to correct the mirrored output
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Save the image
    image.save(filename)
    return filename

def find_dymo_printer():
    """
    Find the first printer with "DYMO" in its name using the lpstat command.
    """
    try:
        result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "DYMO" in line:
                return line.split()[1]  # Return the printer name
    except subprocess.CalledProcessError:
        print("Failed to retrieve printer list.")
    return None

def print_label(filename, printer_name=None):
    """
    Send the label image file to the printer using the 'lpr' command.
    """
    # Find a default DYMO printer if none is specified
    if not printer_name:
        printer_name = find_dymo_printer()
        if printer_name:
            print(f"No printer specified. Using DYMO printer: {printer_name}")
        else:
            print("No DYMO printer found. Please specify a printer.")
            return

    # Define the print command
    command = ["lpr", filename]
    if printer_name:
        command.extend(["-P", printer_name])  # Specify the printer name
    
    try:
        subprocess.run(command, check=True)
        print("Label printed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to print label:", e)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Print a label with specified text.")
    parser.add_argument("text", type=str, help="Text to print on the label")
    parser.add_argument("--font_size", type=int, help="Font size for the label text")
    parser.add_argument("--printer", type=str, help="Optional printer name")
    args = parser.parse_args()

    # Create and print the label
    label_image = create_label_image(args.text, args.font_size)
    print_label(label_image, args.printer)

    # Clean up the label image file from /tmp
    if os.path.exists(label_image):
        os.remove(label_image)

if __name__ == "__main__":
    main()
