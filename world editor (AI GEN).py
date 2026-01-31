import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# ---------------- CONFIG ----------------
TILE_SIZE = 40
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, "Resources")
LEVEL_DIR = os.path.join(RESOURCES_DIR, "Levels")
TEXTURE_DIR = os.path.join(RESOURCES_DIR, "Textures")
# ----------------------------------------

class WorldMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG World Maker")

        # State
        self.tile_size = TILE_SIZE
        self.current_tile = 0
        self.textures = {}  # idx -> ImageTk.PhotoImage
        self.world = {}     # (x,y) -> tile index
        self.mode = "paint" # "paint" or "scroll"
        self.offset_x = 0
        self.offset_y = 0

        # UI
        self.create_ui()
        self.load_textures()
        self.draw_grid()

        # Drag state
        self.dragging = False
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    # ---------------- UI ----------------
    def create_ui(self):
        # Top scrollable texture bar
        self.texture_canvas = tk.Canvas(self.root, height=60, bg="lightgray")
        self.texture_scroll = tk.Scrollbar(self.root, orient="horizontal", command=self.texture_canvas.xview)
        self.texture_canvas.configure(xscrollcommand=self.texture_scroll.set)
        self.texture_canvas.pack(fill="x")
        self.texture_scroll.pack(fill="x")
        self.texture_frame = tk.Frame(self.texture_canvas)
        self.texture_canvas.create_window((0,0), window=self.texture_frame, anchor="nw")
        self.texture_frame.bind("<Configure>", lambda e: self.texture_canvas.configure(scrollregion=self.texture_canvas.bbox("all")))

        # Canvas for world
        self.canvas = tk.Canvas(self.root, width=800, height=540, bg="black")
        self.canvas.pack()

        # Tools
        tools_frame = tk.Frame(self.root, bg="lightgray")
        tools_frame.pack(side="bottom", fill="x")

        self.paint_btn = tk.Button(tools_frame, text="Paint Tool", command=lambda: self.set_mode("paint"))
        self.paint_btn.pack(side="left", padx=5, pady=5)

        self.scroll_btn = tk.Button(tools_frame, text="Scroll Tool", command=lambda: self.set_mode("scroll"))
        self.scroll_btn.pack(side="left", padx=5, pady=5)

        self.zoom_in_btn = tk.Button(tools_frame, text="Zoom +", command=lambda: self.zoom(1.2))
        self.zoom_in_btn.pack(side="left", padx=5, pady=5)

        self.zoom_out_btn = tk.Button(tools_frame, text="Zoom -", command=lambda: self.zoom(0.8))
        self.zoom_out_btn.pack(side="left", padx=5, pady=5)

        self.save_btn = tk.Button(tools_frame, text="Save", command=self.save_level)
        self.save_btn.pack(side="left", padx=5, pady=5)

        self.open_btn = tk.Button(tools_frame, text="Open", command=self.open_level)
        self.open_btn.pack(side="left", padx=5, pady=5)

        self.clear_btn = tk.Button(tools_frame, text="Clear", command=self.clear_level)
        self.clear_btn.pack(side="left", padx=5, pady=5)

    # ---------------- MODE ----------------
    def set_mode(self, mode):
        self.mode = mode

    # ---------------- TEXTURES ----------------
    def load_textures(self):
        self.textures.clear()
        for widget in self.texture_frame.winfo_children():
            widget.destroy()

        if not os.path.exists(TEXTURE_DIR):
            os.makedirs(TEXTURE_DIR)

        files = sorted([f for f in os.listdir(TEXTURE_DIR) if f.lower().endswith(".png")])
        for idx, file_name in enumerate(files):
            path = os.path.join(TEXTURE_DIR, file_name)
            img = Image.open(path).resize((self.tile_size, self.tile_size))
            photo = ImageTk.PhotoImage(img)
            self.textures[idx] = photo

            btn = tk.Button(self.texture_frame, image=photo, command=lambda i=idx: self.select_tile(i))
            btn.image = photo
            btn.pack(side="left", padx=2, pady=2)

    def select_tile(self, tile_id):
        self.current_tile = tile_id

    # ---------------- GRID ----------------
    def draw_grid(self):
        self.canvas.delete("all")
        for (x, y), tile in self.world.items():
            px = x * self.tile_size + self.offset_x
            py = y * self.tile_size + self.offset_y
            if tile in self.textures:
                self.canvas.create_image(px, py, image=self.textures[tile], anchor="nw")
            else:
                self.canvas.create_rectangle(px, py, px+self.tile_size, py+self.tile_size, fill="gray")
            self.canvas.create_rectangle(px, py, px+self.tile_size, py+self.tile_size, outline="black")

    def on_click(self, event):
        self.dragging = (event.x, event.y)
        if self.mode == "paint":
            self.paint_at(event.x, event.y)

    def on_drag(self, event):
        if self.mode == "paint":
            self.paint_at(event.x, event.y)
        elif self.mode == "scroll":
            dx = event.x - self.dragging[0]
            dy = event.y - self.dragging[1]
            self.offset_x += dx
            self.offset_y += dy
            self.dragging = (event.x, event.y)
            self.draw_grid()

    def paint_at(self, x, y):
        grid_x = int((x - self.offset_x) // self.tile_size)
        grid_y = int((y - self.offset_y) // self.tile_size)
        self.world[(grid_x, grid_y)] = self.current_tile
        self.draw_grid()

    # ---------------- ZOOM ----------------
    def zoom(self, factor):
        self.tile_size = max(5, min(200, int(self.tile_size * factor)))
        self.load_textures()
        self.draw_grid()

    # ---------------- FILE OPERATIONS ----------------
    def save_level(self):
        if not self.world:
            messagebox.showwarning("Empty", "Nothing drawn!")
            return

        if not os.path.exists(LEVEL_DIR):
            os.makedirs(LEVEL_DIR)

        file_path = filedialog.asksaveasfilename(
            initialdir=LEVEL_DIR,
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if not file_path:
            return

        xs = [x for x, y in self.world.keys()]
        ys = [y for x, y in self.world.keys()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        grid = [[0 for _ in range(width)] for _ in range(height)]
        for (x, y), val in self.world.items():
            val = min(val, len(self.textures)-1)
            grid[y - min_y][x - min_x] = val

        with open(file_path, "w") as f:
            for row in grid:
                line = "".join(str(tile) for tile in row)
                f.write(line + "\n")

        messagebox.showinfo("Saved", "Level saved successfully!")

    def open_level(self):
        if not os.path.exists(LEVEL_DIR):
            os.makedirs(LEVEL_DIR)

        file_path = filedialog.askopenfilename(
            initialdir=LEVEL_DIR,
            filetypes=[("Text Files", "*.txt")]
        )
        if not file_path:
            return

        self.world.clear()
        with open(file_path, "r") as f:
            lines = f.readlines()
        for y, line in enumerate(lines):
            line = line.strip()
            for x, ch in enumerate(line):
                try:
                    tile = int(ch)
                except ValueError:
                    tile = 0
                tile = min(tile, len(self.textures)-1)
                self.world[(x, y)] = tile
        self.draw_grid()

    def clear_level(self):
        self.world.clear()
        self.draw_grid()


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = WorldMaker(root)
    root.mainloop()
