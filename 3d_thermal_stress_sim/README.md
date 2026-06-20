# Repeated Stack Thermal and Stress Limit Study

This folder keeps the small replication package for the FeFET/TFT repeated-stack screening run.

The workflow used was:

1. Run the electrical model and map macro power into 3D-ICE floorplans.
2. Generate repeated FeFET/TFT stack orders for 3D-ICE.
3. Run 3D-ICE at 27 C ambient and collect peak/average tier temperatures.
4. Feed the converged peak temperature into the stress screening model.
5. Generate Gmsh, Elmer `.sif`, and ParaView `.vtu` artifacts for selected stacks.
6. Sweep stack count until thermal, stress, or warpage criteria fail.

The archived sweep used these criteria:

- Temperature limit: 85 C
- Stress failure ratio limit: 1.0
- Warpage limit: 50 um
- Handle substrate: 500 um Si
- Thermal grid: 4000 um cells for fast stack-count screening

## Files

- `scripts/stack_limit_driver.py`: self-contained Python controller for the stack-count sweep.
- `inputs/fefet_tier.flp`: FeFET-tier floorplan and mapped power input.
- `inputs/tft_tier.flp`: TFT-tier floorplan and mapped power input.
- `results/stack_limit_sweep.csv`: archived sweep data from the remote run.
- `results/summary.json`: archived machine-readable summary.
- `results/elmer_validation.json`: representative Elmer validation notes.
- `results/tool_versions.txt`: tool versions from the remote run.
- `plots/stack_limit_summary.png`: archived summary plot.

Generated rerun outputs are written to `generated/`, `thermal_runs/`, and `mechanical/`.

## Rerun

Install or provide:

- Python 3 with `numpy`, `meshio`, and `matplotlib`
- 3D-ICE 4.0 emulator
- Gmsh
- Optional: Docker image `eperera/elmerfem` for ElmerSolver validation

Example:

```bash
cd 3d_thermal_stress_sim
python3 -m pip install numpy meshio matplotlib
export THREEDICE=/path/to/3D-ICE-Emulator
python3 scripts/stack_limit_driver.py \
  --pairs 1,2,4,8,16,32,64,128,256,512,1024 \
  --thermal-cell-um 4000
```

To run representative Elmer cases as part of the sweep, add:

```bash
--run-elmer
```

## Scaling Limit Found

For both stack orders, the largest simulated safe point was 512 repeated FeFET/TFT pairs.

At 512 pairs:

- `fefet_on_tft`: peak temperature 48.827 C, stress ratio 0.994, warpage 16.49 um
- `tft_on_fefet`: peak temperature 48.788 C, stress ratio 0.994, warpage 16.50 um

The first simulated failure was 1024 pairs.

At 1024 pairs:

- `fefet_on_tft`: peak temperature 106.399 C, stress ratio 1.501
- `tft_on_fefet`: peak temperature 106.326 C, stress ratio 1.500

The failure is from both thermal limit and stress limit. Warpage was not the limiting condition once the 500 um Si handle substrate was included.

## What Is Still Missing

This is a screening model, not signoff.

- FeFET/array cells are still physical-only in the discovered SPICE bundle. Their power is placeholder workload power.
- The TFT behavioral model is temperature-insensitive, so the ngspice to 3D-ICE to ngspice loop converges structurally but does not yet change TFT power with local temperature.
- Residual film stress, CTE, modulus, adhesion, fracture, and yield values are assumed from literature-like screening values, not measured process data.
- 3D-ICE uses a coarse 4000 um thermal grid for the wide stack sweep. The 512 to 1024 pair bracket should be refined with smaller cells.
- Elmer is used as a generated FEM handoff and representative validation. Full wafer/chip boundary conditions, vias, interconnect density, bonding defects, and package constraints are not yet modeled.

To improve accuracy, add temperature-dependent FeFET/TFT compact models, measured film stress/material data, real operating workloads, refined thermal cells near the failure bracket, and calibrated Elmer boundary conditions.
