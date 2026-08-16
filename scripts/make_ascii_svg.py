import os
from PIL import Image

RAMP = " .`:-=+*cs#%@"

def make_ascii_svg(input_path="source-prepped.png", output_path="avi-ascii.svg"):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Please run prep_photo.py first.")
        return

    img = Image.open(input_path)
    # Resize to ~100x53
    # Font aspect ratio is roughly 2:1 (height is 2x width), so we adjust height
    new_width = 100
    aspect_ratio = img.height / img.width
    new_height = int(new_width * aspect_ratio * 0.5)
    img = img.resize((new_width, new_height))
    img = img.convert("L")

    pixels = img.load()
    
    # Generate SVG
    svg_width = 800
    svg_height = new_height * 14 + 40
    
    char_width = 8
    char_height = 14
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
        '  <style>',
        '    .ascii { font-family: monospace; font-size: 14px; fill: #8b949e; white-space: pre; }',
        '    .cursor { fill: #8b949e; }',
        '  </style>',
        '  <defs>'
    ]

    # Create clip paths for each row
    for row in range(new_height):
        delay = row * 0.05
        duration = 0.5
        svg.append(f'    <clipPath id="clip-{row}">')
        svg.append(f'      <rect x="0" y="{row * char_height}" width="0" height="{char_height}">')
        svg.append(f'        <animate attributeName="width" from="0" to="{new_width * char_width}" begin="{delay}s" dur="{duration}s" fill="freeze" />')
        svg.append(f'      </rect>')
        svg.append(f'    </clipPath>')
    svg.append('  </defs>')

    svg.append('  <g class="ascii">')
    for y in range(new_height):
        line = ""
        for x in range(new_width):
            # inverted ramp: bright (sparse) -> dark (dense)
            brightness = pixels[x, y]
            # brightness is 0-255. 255 is white (sparse)
            # RAMP index: 0 is sparse, len-1 is dense
            ramp_idx = int((255 - brightness) / 255 * (len(RAMP) - 1))
            line += RAMP[ramp_idx]
        
        # Escape XML chars just in case (though RAMP doesn't have < or >)
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        svg.append(f'    <text x="0" y="{y * char_height + 12}" clip-path="url(#clip-{y})">{line}</text>')
        
        # Cursor animation
        delay = y * 0.05
        duration = 0.5
        svg.append(f'    <rect class="cursor" x="0" y="{y * char_height + 2}" width="{char_width}" height="{char_height-2}" opacity="0">')
        svg.append(f'      <animate attributeName="x" from="0" to="{new_width * char_width}" begin="{delay}s" dur="{duration}s" fill="freeze" />')
        # cursor is visible only during typing
        svg.append(f'      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.99;1" begin="{delay}s" dur="{duration}s" fill="freeze" />')
        svg.append(f'    </rect>')
        
    svg.append('  </g>')
    svg.append('</svg>')

    with open(output_path, "w") as f:
        f.write("\n".join(svg))
    print(f"Generated {output_path}")

if __name__ == "__main__":
    make_ascii_svg()
