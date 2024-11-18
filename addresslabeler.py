import sys
import argparse
import os
from PIL import Image, ImageDraw, ImageFont
import subprocess

def load_courier_font(font_size):
    """
    Load the Courier font; if unavailable, fallback to default.
    """
    font_path = "/usr/share/fonts/msttcorefonts/Courier_New.ttf"
    try:
        return ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Courier font not found. Using default font.")
        return ImageFont.load_default()

def create_label_image(address, font_size=60, width=900, height=300):
    """
    Create a label image for an address and save it to a file in /tmp.
    """
    filename = "/tmp/address_label.png"
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Load the Courier font
    font = load_courier_font(font_size)

    # Set margin
    margin_left = 10
    margin_top = 10

    # Draw each line of the address starting at the top-left corner
    address_lines = address.split("\n")
    y = margin_top
    line_spacing = 10  # Additional spacing between lines
    for line in address_lines:
        draw.text((margin_left, y), line, fill="black", font=font)
        y += font_size + line_spacing  # Use font_size directly for line height

    # Save the image
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
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
    if not printer_name:
        printer_name = find_dymo_printer()
        if printer_name:
            print(f"Using DYMO printer: {printer_name}")
        else:
            print("No DYMO printer found. Please specify a printer.")
            return

    command = ["lpr", filename]
    if printer_name:
        command.extend(["-P", printer_name])
    try:
        subprocess.run(command, check=True)
        print("Label printed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to print label:", e)

def parse_addresses(input_text):
    """
    Parse addresses from the input text, splitting on blank lines.
    """
    return [address.strip() for address in input_text.split("\n\n") if address.strip()]

def main():
    parser = argparse.ArgumentParser(description="Print address labels using a DYMO printer.")
    parser.add_argument("file", nargs="?", help="Path to a file containing addresses. If not provided, reads from stdin.")
    parser.add_argument("--printer", type=str, help="Optional printer name")
    args = parser.parse_args()

    # Read input from file or stdin
    if args.file:
        with open(args.file, "r") as f:
            input_text = f.read()
    else:
        input_text = sys.stdin.read()

    # Parse addresses
    addresses = parse_addresses(input_text)

    # Create and print a label for each address
    for address in addresses:
        label_image = create_label_image(address)
        print_label(label_image, args.printer)

        # Clean up the label image file
        if os.path.exists(label_image):
            os.remove(label_image)

if __name__ == "__main__":
    main()
