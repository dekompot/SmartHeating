import random

def generate_fire_color():
    # Adjust these ranges to control the intensity of red, orange, and yellow
    red = random.randint(200, 255)
    green = random.randint(50, 150)
    blue = random.randint(0, 50)

    # Adjust this range to control the overall brightness
    brightness = random.randint(180, 255)

    # Create the RGB color
    color = (red, green, blue)

    # Adjust the brightness of the color
    color = tuple(min(c + brightness, 255) for c in color)

    return color


def visualize_fire(pixels, n_pixels):
    for i in range(n_pixels):
        pixels[i] = generate_fire_color()


# Example usage:
for _ in range(10):
    random_color = generate_fire_color()
    print(random_color)
