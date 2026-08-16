import os

def make_info_card(output_path="info-card.svg"):
    # Neofetch-style info card
    # Each line fades and slides in on a short stagger
    static_mode = os.environ.get("STATIC", "0") == "1"

    svg_width = 490
    svg_height = 300

    content = [
        {"key": "Now", "value": "AI Product Manager &amp; Founder @ Maahir &amp; Co."},
        {"key": "Prev", "value": "Hackathon Team Leader @ Royal Technosoft"},
        {"key": "Stack", "value": "Python, LLMs, Computer Vision (YOLOv8)"},
        {"key": "Highlights", "value": "Built NyAI (Legal AI Assistant)"},
        {"key": "Seeking", "value": "Remote collaboration with early-stage AI startups"}
    ]

    title = "Maahirrrr@github"
    os_name = "GitHub Profile OS"
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
        '  <style>',
        '    .text { font-family: monospace; font-size: 14px; fill: #c9d1d9; }',
        '    .key { fill: #58a6ff; font-weight: bold; }',
        '    .title { fill: #7ee787; font-weight: bold; }',
        '    .separator { fill: #8b949e; }'
    ]

    if not static_mode:
        svg.append('    @keyframes slideIn {')
        svg.append('      0% { opacity: 0; transform: translateX(-10px); }')
        svg.append('      100% { opacity: 1; transform: translateX(0); }')
        svg.append('    }')
        svg.append('    .animated { opacity: 0; animation: slideIn 0.5s forwards; }')
    else:
        svg.append('    .animated { opacity: 1; }')

    svg.append('  </style>')
    svg.append('  <g class="text">')

    line_height = 24
    y = 30
    delay_step = 0.2
    
    def animate_style(index):
        if static_mode:
            return ""
        return f' style="animation-delay: {index * delay_step}s"'

    # Title
    svg.append(f'    <text x="20" y="{y}" class="animated"<animate_style>><tspan class="title">{title}</tspan><tspan class="separator">-------------------</tspan></text>'.replace("<animate_style>", animate_style(0)))
    y += line_height
    
    svg.append(f'    <text x="20" y="{y}" class="animated"<animate_style>>OS: {os_name}</text>'.replace("<animate_style>", animate_style(1)))
    y += line_height
    
    for i, item in enumerate(content):
        svg.append(f'    <text x="20" y="{y}" class="animated"<animate_style>><tspan class="key">{item["key"]}</tspan><tspan class="separator">:</tspan> {item["value"]}</text>'.replace("<animate_style>", animate_style(i+2)))
        y += line_height

    # Color blocks
    y += line_height
    colors = ['#ff7b72', '#ffa657', '#3fb950', '#79c0ff', '#a5d6ff', '#d2a8ff']
    color_blocks = ""
    for j, color in enumerate(colors):
        color_blocks += f'<rect x="{20 + j*20}" y="{y-12}" width="20" height="15" fill="{color}" />'
    
    svg.append(f'    <g class="animated"<animate_style>>{color_blocks}</g>'.replace("<animate_style>", animate_style(len(content)+2)))

    svg.append('  </g>')
    svg.append('</svg>')

    with open(output_path, "w") as f:
        f.write("\n".join(svg))
    print(f"Generated {output_path}")

if __name__ == "__main__":
    make_info_card()
