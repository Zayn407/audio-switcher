from PIL import Image, ImageDraw

def create_icon():
    """Create a simple and recognizable audio switcher icon"""
    sizes = [256, 128, 64, 48, 32, 16]
    images = []

    for size in sizes:
        # Create image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        scale = size / 256

        # Draw a bold circular background
        padding = int(8 * scale)
        # Gradient-like effect with two circles
        draw.ellipse([padding, padding, size - padding, size - padding],
                     fill=(52, 152, 219, 255))  # Bright blue

        # Draw large bold "A ⇄ B" symbol
        center_x = size // 2
        center_y = size // 2

        # Font size simulation with rectangles for A and B
        letter_size = int(40 * scale)
        letter_thick = max(3, int(8 * scale))

        # Letter A (left side)
        a_x = int(size * 0.25)
        # A triangle
        a_points = [
            (a_x, center_y + letter_size // 2),
            (a_x - letter_size // 2, center_y + letter_size // 2),
            (a_x, center_y - letter_size // 2)
        ]
        draw.polygon(a_points, fill=(255, 255, 255, 255))
        # A horizontal bar
        draw.rectangle([
            a_x - letter_size // 3, center_y,
            a_x + letter_thick, center_y + letter_thick
        ], fill=(52, 152, 219, 255))

        # Letter B (right side)
        b_x = int(size * 0.75)
        # B vertical line
        draw.rectangle([
            b_x - letter_size // 2, center_y - letter_size // 2,
            b_x - letter_size // 2 + letter_thick, center_y + letter_size // 2
        ], fill=(255, 255, 255, 255))
        # B top bump
        draw.ellipse([
            b_x - letter_size // 2, center_y - letter_size // 2,
            b_x + letter_size // 4, center_y
        ], fill=(255, 255, 255, 255))
        # B bottom bump
        draw.ellipse([
            b_x - letter_size // 2, center_y - letter_thick // 2,
            b_x + letter_size // 4, center_y + letter_size // 2
        ], fill=(255, 255, 255, 255))

        # Draw BOLD double arrow in center
        arrow_y = center_y
        arrow_left = int(size * 0.38)
        arrow_right = int(size * 0.62)
        arrow_thick = max(3, int(8 * scale))

        # Horizontal line
        draw.rectangle([
            arrow_left, arrow_y - arrow_thick // 2,
            arrow_right, arrow_y + arrow_thick // 2
        ], fill=(255, 193, 7, 255))

        # Left arrow head (pointing left)
        arrow_head_size = int(15 * scale)
        draw.polygon([
            (arrow_left, arrow_y),
            (arrow_left + arrow_head_size, arrow_y - arrow_head_size),
            (arrow_left + arrow_head_size, arrow_y + arrow_head_size)
        ], fill=(255, 193, 7, 255))

        # Right arrow head (pointing right)
        draw.polygon([
            (arrow_right, arrow_y),
            (arrow_right - arrow_head_size, arrow_y - arrow_head_size),
            (arrow_right - arrow_head_size, arrow_y + arrow_head_size)
        ], fill=(255, 193, 7, 255))

        images.append(img)

    # Save as ICO file with multiple sizes
    images[0].save('icon.ico', format='ICO', sizes=[(s, s) for s in sizes])
    print("Icon created: icon.ico")

    # Also save as PNG for preview
    images[0].save('icon_preview.png', format='PNG')
    print("Preview created: icon_preview.png")

if __name__ == "__main__":
    create_icon()
