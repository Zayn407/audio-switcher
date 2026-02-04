from PIL import Image, ImageDraw

def create_icon():
    """Create a professional audio switcher icon"""
    sizes = [256, 128, 64, 48, 32, 16]
    images = []

    for size in sizes:
        # Create image with white background
        img = Image.new('RGBA', (size, size), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Scale factor
        scale = size / 256

        # Background circle
        padding = int(10 * scale)
        draw.ellipse([padding, padding, size - padding, size - padding],
                     fill=(41, 128, 185, 255))  # Blue background

        # Draw speaker icon (left side)
        center_y = size // 2
        speaker_left = int(size * 0.25)

        # Speaker body
        speaker_size = int(30 * scale)
        draw.rectangle(
            [speaker_left - speaker_size // 2, center_y - speaker_size // 2,
             speaker_left + speaker_size // 2, center_y + speaker_size // 2],
            fill=(255, 255, 255, 255),
            outline=(255, 255, 255, 255),
            width=max(2, int(3 * scale))
        )

        # Sound wave lines
        for i in range(3):
            offset = int((15 + i * 10) * scale)
            line_y = center_y - int(20 * scale) + offset
            draw.line(
                [speaker_left + speaker_size, line_y,
                 speaker_left + speaker_size + int(15 * scale), line_y],
                fill=(255, 255, 255, 255),
                width=max(2, int(3 * scale))
            )

        # Draw speaker icon (right side)
        speaker_right = int(size * 0.75)

        # Speaker body
        draw.rectangle(
            [speaker_right - speaker_size // 2, center_y - speaker_size // 2,
             speaker_right + speaker_size // 2, center_y + speaker_size // 2],
            fill=(255, 255, 255, 255),
            outline=(255, 255, 255, 255),
            width=max(2, int(3 * scale))
        )

        # Sound wave lines
        for i in range(3):
            offset = int((15 + i * 10) * scale)
            line_y = center_y - int(20 * scale) + offset
            draw.line(
                [speaker_right - speaker_size - int(15 * scale), line_y,
                 speaker_right - speaker_size, line_y],
                fill=(255, 255, 255, 255),
                width=max(2, int(3 * scale))
            )

        # Draw switching arrows in the middle
        center_x = size // 2
        arrow_size = int(20 * scale)
        arrow_width = max(2, int(4 * scale))

        # Right arrow (top)
        arrow_y_top = center_y - int(12 * scale)
        draw.line(
            [center_x - arrow_size, arrow_y_top, center_x + arrow_size, arrow_y_top],
            fill=(255, 193, 7, 255),  # Yellow
            width=arrow_width
        )
        # Arrow head
        draw.polygon([
            (center_x + arrow_size, arrow_y_top),
            (center_x + arrow_size - int(10 * scale), arrow_y_top - int(8 * scale)),
            (center_x + arrow_size - int(10 * scale), arrow_y_top + int(8 * scale))
        ], fill=(255, 193, 7, 255))

        # Left arrow (bottom)
        arrow_y_bottom = center_y + int(12 * scale)
        draw.line(
            [center_x + arrow_size, arrow_y_bottom, center_x - arrow_size, arrow_y_bottom],
            fill=(255, 193, 7, 255),
            width=arrow_width
        )
        # Arrow head
        draw.polygon([
            (center_x - arrow_size, arrow_y_bottom),
            (center_x - arrow_size + int(10 * scale), arrow_y_bottom - int(8 * scale)),
            (center_x - arrow_size + int(10 * scale), arrow_y_bottom + int(8 * scale))
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
