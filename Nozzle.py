# cadquery‑based parametric vortex‑cannon parts
# requires cadquery 2.x  (pip install cadquery)
# generates STEP files for the chamber body and screw‑in nozzle
# ---------------------------------------------------------------
# tuning parameters (millimetres)
chamber_inner_d      = 52.0     # matches 2″ loud‑speaker frame
chamber_length       = 50.0
wall_thickness       = 3.0

nozzle_exit_d        = 15.0     # D_o (throat)
conv_half_angle      = 10.0     # °
land_length          = nozzle_exit_d * 0.5

diff_total_angle     = 13.0     # °
diff_len_factor      = 2.5

thread_pitch         = 2.0
thread_length        = 8.0
clearance            = 0.2      # radial thread clearance
file_prefix          = "vortex_"

# ---------------------------------------------------------------
import cadquery as cq
import math

def build_chamber():
    outer_d = chamber_inner_d + 2 * wall_thickness
    body = (
        cq.Workplane("XY")
        .cylinder(chamber_length, outer_d / 2)
        .faces("<Z").workplane()
        .hole(chamber_inner_d)
    )
    # bore for nozzle male thread
    body = (
        body.faces(">Z[1]")
        .workplane()
        .cylinder(thread_length, chamber_inner_d / 2 + clearance)
    )
    return body

def build_nozzle():
    conv_len = (chamber_inner_d - nozzle_exit_d) / (2 * math.tan(math.radians(conv_half_angle)))
    diff_len = nozzle_exit_d * diff_len_factor
    total_len = thread_length + conv_len + land_length + diff_len

    # outer sleeve (with male thread region)
    outer = cq.Workplane("XY").cylinder(total_len, chamber_inner_d / 2)
    # optional chamfer on entry lip for printing ease
    outer = outer.edges("|Z and >Z[1]").chamfer(0.3)  # use '>Z[1]' to ensure edge exists

    # internal flow path profile
    pts = [
        (0, chamber_inner_d/2),
        (conv_len, nozzle_exit_d/2),
        (conv_len+land_length, nozzle_exit_d/2),
        (conv_len+land_length+diff_len, nozzle_exit_d/2 + diff_len*math.tan(math.radians(diff_total_angle/2)))
    ]
    flow = cq.Workplane("XZ").polyline(pts).close().revolve(360) q.Workplane("XZ").polyline(pts).close().revolve(360)

    nozzle = outer.cut(flow)
    return nozzle

if __name__ == "__main__":
    chamber = build_chamber()
    nozzle = build_nozzle()

    chamber_val = chamber.val()
    nozzle_val = nozzle.val()

    chamber_val.exportStep(file_prefix + "chamber.step")
    nozzle_val.exportStep(file_prefix + "nozzle.step")

    print("STEP files written: vortex_chamber.step, vortex_nozzle.step")
