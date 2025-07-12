# Half‑section blueprint for the latest round‑speaker vortex cannon
import matplotlib.pyplot as plt, math

# === Design parameters (mm) ===
ch_inner = 52.0          # chamber inner Ø
wall     = 3.0           # wall thickness
L_ch     = 50.0          # chamber length

D_exit   = 15.0          # throat Ø
ang_conv = 10.0          # converging half‑angle (deg)
land_L   = 0.5 * D_exit  # land length
ang_diff = 13.0          # total diffuser angle (deg)
diff_k   = 2.5           # diffuser length = k·D_exit

thread_L = 8.0           # thread engagement length

# === Derived ===
conv_L  = (ch_inner - D_exit) / (2 * math.tan(math.radians(ang_conv)))
diff_L  = D_exit * diff_k
diff_half = ang_diff / 2

# outer & inner profiles
X = [0, L_ch, L_ch+conv_L, L_ch+conv_L+land_L, L_ch+conv_L+land_L+diff_L]
Y = [ch_inner/2+wall, ch_inner/2+wall, D_exit/2+wall,
     D_exit/2+wall, D_exit/2+diff_L*math.tan(math.radians(diff_half))+wall]

Xi = [0, L_ch, L_ch+conv_L, L_ch+conv_L+land_L, L_ch+conv_L+land_L+diff_L]
Yi = [ch_inner/2, ch_inner/2, D_exit/2, D_exit/2,
      D_exit/2+diff_L*math.tan(math.radians(diff_half))]

plt.figure(figsize=(10,3))
plt.plot(X,  Y,  'k', lw=2)
plt.plot(Xi, Yi, 'b', lw=2)
plt.plot(X,  [-y for y in Y],  'k', lw=2)
plt.plot(Xi, [-y for y in Yi], 'b', lw=2)

# thread shading
plt.fill_between([L_ch-thread_L, L_ch], [ch_inner/2,-ch_inner/2], color='lightgrey', alpha=0.3)

# labels
plt.text(L_ch/2, ch_inner/2+4, f"Chamber {L_ch} mm", ha='center')
plt.text(L_ch+conv_L/2, D_exit/2+4, f"Converging {conv_L:.1f} mm @{ang_conv}°", ha='center')
plt.text(L_ch+conv_L+land_L/2, D_exit/2+4, f"Land {land_L:.1f} mm", ha='center')
plt.text(L_ch+conv_L+land_L+diff_L/2,
         D_exit/2+diff_L*math.tan(math.radians(diff_half))+4,
         f"Diffuser {diff_L:.1f} mm @{ang_diff}°", ha='center')
plt.text(L_ch+2, ch_inner/2, "Thread\nregion", rotation=90, va='top', ha='left')

plt.title("Half‑section blueprint – Speaker‑driven Vortex Cannon")
plt.axis('equal'); plt.axis('off'); plt.tight_layout()
