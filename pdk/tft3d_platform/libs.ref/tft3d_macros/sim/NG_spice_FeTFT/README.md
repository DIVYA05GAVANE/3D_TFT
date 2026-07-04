# NG_spice_FeTFT

This folder contains the native stock-ngspice FeTFT/FeFET model include.

- `fetft_nf1_vds0p1_ngspice.inc`: FeTFT/FeFET HVT/LVT table model translated
  from the original HSPICE Verilog-A/table behavior for ngspice.

The include uses the `Vd = 0.1 V` Id-Vg conductance-table slice and supports
Monte Carlo parameters for switching voltage, current scale, HVT/LVT Vg shift,
HVT/LVT scale, and HVT/LVT table tilt.

Monte Carlo simulation decks live in `../NG_spice_MonteCarlo`.
