# theme_selector/utils.py

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(
        max(0, min(255, rgb[0])),
        max(0, min(255, rgb[1])),
        max(0, min(255, rgb[2]))
    )

def lighten_hex_color(hex_color, percent):
    """Lighten a hex color by percentage."""
    rgb = hex_to_rgb(hex_color)
    rgb = tuple(int(c + (255 - c) * percent / 100) for c in rgb)
    return rgb_to_hex(rgb)

def darken_hex_color(hex_color, percent):
    """Darken a hex color by percentage."""
    rgb = hex_to_rgb(hex_color)
    rgb = tuple(int(c * (100 - percent) / 100) for c in rgb)
    return rgb_to_hex(rgb)
