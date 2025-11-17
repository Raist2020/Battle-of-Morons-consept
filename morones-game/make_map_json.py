import json
import os

# Настройки
MAP_FILENAME = "map_bg.png"  # твой PNG-файл карты
OUTPUT_HTML = "map.html"
OUTPUT_JSON = "cells.json"

# Если есть старый JSON, загружаем
if os.path.exists(OUTPUT_JSON):
    with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
        cells = json.load(f)
else:
    cells = []

# Генерация HTML
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Game of Morons Map Editor</title>
<style>
  body {{
    margin: 0;
    padding: 0;
  }}
  #map-container {{
    position: relative;
    width: 100%;
    max-width: 1920px;
    aspect-ratio: 1920 / 1009;
    margin: auto;
    background: url('{MAP_FILENAME}') no-repeat center center;
    background-size: cover;
  }}
  .cell {{
    position: absolute;
    border: 2px solid rgba(255,0,0,0.3);
    background-color: rgba(255,0,0,0.1);
    cursor: move;
  }}
</style>
</head>
<body>
<div id="map-container"></div>

<script>
let cells = {json.dumps(cells, indent=2)};
const container = document.getElementById("map-container");

function createCellElement(cell) {{
    const el = document.createElement("div");
    el.className = "cell";
    el.style.top = cell.top + "%";
    el.style.left = cell.left + "%";
    el.style.width = cell.width + "%";
    el.style.height = cell.height + "%";
    el.draggable = true;
    el.onclick = () => {{
        alert("Cell ID: " + cell.id);
    }};
    // Drag
    let offsetX, offsetY;
    el.addEventListener("mousedown", e => {{
        offsetX = e.offsetX;
        offsetY = e.offsetY;
        function moveHandler(ev) {{
            const rect = container.getBoundingClientRect();
            let left = ((ev.clientX - rect.left - offsetX) / rect.width) * 100;
            let top = ((ev.clientY - rect.top - offsetY) / rect.height) * 100;
            if(left < 0) left = 0;
            if(top < 0) top = 0;
            if(left + cell.width > 100) left = 100 - cell.width;
            if(top + cell.height > 100) top = 100 - cell.height;
            cell.left = left;
            cell.top = top;
            el.style.left = left + "%";
            el.style.top = top + "%";
        }}
        function upHandler() {{
            document.removeEventListener("mousemove", moveHandler);
            document.removeEventListener("mouseup", upHandler);
            saveCells();
        }}
        document.addEventListener("mousemove", moveHandler);
        document.addEventListener("mouseup", upHandler);
    }});
    container.appendChild(el);
}}

function saveCells() {{
    fetch("save_cells.py", {{
        method: "POST",
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify(cells)
    }});
}}

// Создаём элементы
cells.forEach(cell => createCellElement(cell));

// Добавление новых клеток по клику
container.addEventListener("dblclick", e => {{
    const rect = container.getBoundingClientRect();
    const width = 5;  // размер квадрата в процентах
    const height = 5;
    const left = ((e.clientX - rect.left) / rect.width) * 100 - width/2;
    const top = ((e.clientY - rect.top) / rect.height) * 100 - height/2;
    const newCell = {{
        id: cells.length + 1,
        top: top < 0 ? 0 : top,
        left: left < 0 ? 0 : left,
        width: width,
        height: height
    }};
    cells.push(newCell);
    createCellElement(newCell);
    saveCells();
}});
</script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML с картой создан: {OUTPUT_HTML}")
print(f"JSON для клеток: {OUTPUT_JSON}")

