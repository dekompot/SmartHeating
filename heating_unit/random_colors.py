import random

def generate_fire_color():
    # Adjust these ranges to control the intensity of red, orange, and yellow
    red = random.randint(200, 255)
    green = random.randint(0, 100)
    blue = random.randint(0, 25)

    # Create the RGB color
    color = (red, green, blue)

    return color


def visualize_fire(pixels, n_pixels):
    for i in range(n_pixels):
        pixels[i] = generate_fire_color()
    pixels.show()

'''
# Example usage:
for _ in range(10):
    random_color = generate_fire_color()
    print(random_color)'''
