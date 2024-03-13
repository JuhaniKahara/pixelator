import sys
from PIL import Image
import numpy as np

def convert_image(input_filename, columns, rows, num_colors):
    # Open the image
    image = Image.open(input_filename)
    image = image.convert('L')  # Convert to grayscale

    # Calculate cell width and height
    width, height = image.size
    cell_width = width // columns
    cell_height = height // rows

    # Initialize the output matrix to be printed
    matrix = np.zeros((rows, columns), dtype=int)

    # Create a new image for the output
    output_image = Image.new('L', (width, height))

    # Define the shades of gray
    shades = np.linspace(0, 255, num_colors, dtype=int)

    # Define the range of grayscale values (0 to 255) and quantize into N levels
    quant_levels = np.linspace(0, 255, num_colors, endpoint=False)

    # Process each cell
    for i in range(columns):
        for j in range(rows):
            # Calculate the bounds of the cell
            left = i * cell_width
            upper = j * cell_height
            right = (i + 1) * cell_width
            bottom = (j + 1) * cell_height

            # Crop the cell from the original image
            cell = image.crop((left, upper, right, bottom))

            # Calculate the average brightness of the cell
            avg_brightness = np.mean(cell)

            # Find the closest shade of gray
            closest_shade = min(shades, key=lambda x: abs(x - avg_brightness))

            # Create a new cell with the closest shade of gray
            new_cell = Image.new('L', (cell_width, cell_height), int(closest_shade))

            # Paste the new cell into the output image
            output_image.paste(new_cell, (left, upper))

            # Save the quantized shade to matrix
            quantized_value = np.searchsorted(quant_levels, avg_brightness, side='right') - 1
            matrix[j, i] = quantized_value

    # Save or display the output image
    output_filename = 'output_' + input_filename
    output_image.save(output_filename)
    output_image.show()

    # Convert the matrix to a string for printing
    matrix_str = ""
    for row in matrix:
        for val in row:
            matrix_str += f"{val:2d} "  # Adjust formatting as needed
        matrix_str += "\n"

    # Save the matrix to a text file
    with open("output_matrix.txt", "w") as f:
        f.write(matrix_str)

    print("Matrix saved to output_matrix.txt")

def main():
    if len(sys.argv) != 5:
        print("Usage: python pixelator.py <filename> <columns> <rows> <num_colors>")
        sys.exit(1)

    input_filename = sys.argv[1]
    columns = int(sys.argv[2])
    rows = int(sys.argv[3])
    num_colors = int(sys.argv[4])

    convert_image(input_filename, columns, rows, num_colors)

if __name__ == "__main__":
    main()
