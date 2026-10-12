import cadquery as cq
import math

in_w = 23.0
in_l = 53.0
wall = 2.0
out_w = in_w + wall * 2
out_l = in_l + wall * 2
out_h = 12.0

bottom = cq.Workplane("XY").box(out_w, out_l, out_h).faces(">Z").shell(-wall)

usb_cut = cq.Workplane("XZ").workplane(offset=out_l/2).center(0, out_h/2 - wall).box(9, 5, wall * 4)
bottom = bottom.cut(usb_cut)

lid = cq.Workplane("XY").box(out_w, out_l, wall).translate((0, 0, out_h/2 + wall/2))

pts = []
spacing = 4.5
r = 2.0
dy = spacing * math.sqrt(3) / 2

for row in range(-10, 11):
    for col in range(-4, 5):
        x = col * spacing + (spacing / 2 if row % 2 != 0 else 0)
        y = row * dy
        if abs(x) < in_w / 2 - 1 and abs(y) < in_l / 2 - 1:
            pts.append((x, y))

lid = lid.faces(">Z").workplane().pushPoints(pts).polygon(6, r * 2).cutThruAll()

cq.exporters.export(bottom, "pico2w_bottom.stl")
cq.exporters.export(lid, "pico2w_hex_lid.stl")

assembly = cq.Assembly()
assembly.add(bottom, name="bottom_case", color=cq.Color(0.2, 0.2, 0.2, 1.0))
assembly.add(lid, name="hex_lid", color=cq.Color(0.0, 0.5, 0.8, 1.0))

if "show_object" in locals():
    show_object(assembly)
