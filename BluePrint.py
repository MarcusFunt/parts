import matplotlib.pyplot as plt

# Design parameters for blueprint
chamber_inner_d = 52.0
wall_thickness = 3.0
chamber_length = 50.0
nozzle_exit_d = 15.0
conv_half_angle = 10.0  # deg
land_length = nozzle_exit_d * 0.5  # 7.5 mm
diff_total_angle = 13.0  # deg
diff_len_factor = 2.5
thread_length = 8.0

import math
conv_len = (chamber_inner_d - nozzle_exit_d) / (2 * math.tan(math.radians(conv_half_angle)))
diff_len = nozzle_exit_d * diff_len_factor
diff_half_angle = diff_total_angle / 2

total_len = chamber_length + conv_len + land_length + diff_len

# Build profile coordinates (half section)
x = [0,
     chamber_length,
     chamber_length + conv_len,
     chamber_length + conv_len + land_length,
     chamber_length + conv_len + land_length + diff_len]
y = [chamber_inner_d/2 + wall_thickness,
     chamber_inner_d/2 + wall_thickness,
     nozzle_exit_d/2 + wall_thickness,
     nozzle_exit_d/2 + wall_thickness,
     nozzle_exit_d/2 + diff_len*math.tan(math.radians(diff_half_angle)) + wall_thickness]

# Inner wall path
xi = [0,
      chamber_length,
      chamber_length + conv_len,
      chamber_length + conv_len + land_length,
      chamber_length + conv_len + land_length + diff_len]
yi = [chamber_inner_d/2,
      chamber_inner_d/2,
      nozzle_exit_d/2,
      nozzle_exit_d/2,
      nozzle_exit_d/2 + diff_len*math.tan(math.radians(diff_half_angle))]

plt.figure(figsize=(10,3))
plt.plot(x, y, 'k', linewidth=2)
plt.plot(xi, yi, 'b', linewidth=2)
plt.plot(x, [-yy for yy in y], 'k', linewidth=2)
plt.plot(xi, [-yy for yy in yi], 'b', linewidth=2)

# Add thread region indication
plt.fill_between([chamber_length-thread_length, chamber_length], [chamber_inner_d/2,-chamber_inner_d/2], 
                 color='lightgrey', alpha=0.3)

# Annotations
plt.text(chamber_length/2, chamber_inner_d/2+4, f"Chamber {chamber_length} mm", ha='center')
plt.text(chamber_length+conv_len/2, nozzle_exit_d/2+4, f"Converging {conv_len:.1f} mm @10°", ha='center')
plt.text(chamber_length+conv_len+land_length/2, nozzle_exit_d/2+4, f"Land {land_length} mm", ha='center')
plt.text(chamber_length+conv_len+land_length+diff_len/2, 
         nozzle_exit_d/2+diff_len*math.tan(math.radians(diff_half_angle))+4,
         f"Diffuser {diff_len:.1f} mm @13°", ha='center')
plt.text(chamber_length+2, chamber_inner_d/2, "Thread region", rotation=90, va='top')

plt.title("Half‑section blueprint – Speaker‑driven Vortex Cannon")
plt.axis('equal')
plt.axis('off')
plt.tight_layout()
