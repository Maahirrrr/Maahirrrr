import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap_svg(input_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, "r") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    
    # We want to arrange them into 53 columns by 7 rows
    # Actually, github graph is column-major.
    # Group by week (every 7 days)
    weeks = [days[i:i+7] for i in range(0, len(days), 7)]
    
    box_size = 12
    gap = 4
    
    svg_width = len(weeks) * (box_size + gap) + 40
    svg_height = 7 * (box_size + gap) + 60
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
        '  <style>',
        '    @keyframes slideDown {',
        '      0% { opacity: 0; transform: translateY(-10px); }',
        '      100% { opacity: 1; transform: translateY(0); }',
        '    }',
        '    .box { opacity: 0; animation: slideDown 0.5s forwards; }',
        '    .text { font-family: monospace; font-size: 12px; fill: #8b949e; }',
        '  </style>',
        '  <g transform="translate(20, 20)">'
    ]
    
    for col_idx, week in enumerate(weeks):
        for row_idx, day in enumerate(week):
            level = day.get("level", 0)
            # Cap level at length of palette - 1
            color = PALETTE[min(level, len(PALETTE)-1)]
            
            x = col_idx * (box_size + gap)
            y = row_idx * (box_size + gap)
            
            # Diagonal slide-down stagger
            # delay based on x + y
            delay = (col_idx + row_idx) * 0.02
            
            svg.append(f'    <rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" style="animation-delay: {delay}s" />')

    # Legend
    legend_y = 7 * (box_size + gap) + 10
    svg.append(f'    <text x="0" y="{legend_y + 10}" class="text">Less</text>')
    
    for i, color in enumerate(PALETTE[:5]):
        x = 40 + i * (box_size + gap)
        svg.append(f'    <rect x="{x}" y="{legend_y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" />')
        
    svg.append(f'    <text x="{40 + 5 * (box_size + gap) + 5}" y="{legend_y + 10}" class="text">More</text>')

    svg.append('  </g>')
    svg.append('</svg>')
    
    with open(output_path, "w") as f:
        f.write("\n".join(svg))
        
    print(f"Generated {output_path}")

if __name__ == "__main__":
    render_heatmap_svg()
