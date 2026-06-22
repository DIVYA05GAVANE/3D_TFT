# GDS Hierarchy Refresh

Standalone GDS files do not live-link to lower-hierarchy GDS files. When a leaf
layout such as `nfet_W6u_L5.gds` changes, any already-exported top GDS still
contains the old embedded cell geometry until it is refreshed and rewritten.

Use `scripts/refresh_gds_leaf_cells.py` to copy updated source cell geometry
into a standalone top GDS while preserving the existing parent references.

## Requirements

- Python 3
- `gdstk`
- Access to the target GDS and source leaf GDS files

The remote layout VM already has Python and `gdstk` installed.

## Common Remote Flow

From the local repo, copy the updated leaf and script to the remote workspace:

```sh
scp scripts/refresh_gds_leaf_cells.py \
  pdk/tft3d_platform/libs.ref/tft3d_macros/gds/nfet_W6u_L5.gds \
  vboxuser@100.115.20.54:/home/vboxuser/codex_tft3d_cdslib_ngspice_check_20260620/

scp pdk/tft3d_platform/libs.ref/tft3d_macros/gds/nfet_W6u_L5.gds \
  vboxuser@100.115.20.54:/home/vboxuser/codex_tft3d_cdslib_ngspice_check_20260620/tft3d_macros/gds/nfet_W6u_L5.gds
```

On the remote VM, refresh the folded final GDS:

```sh
cd /home/vboxuser/codex_tft3d_cdslib_ngspice_check_20260620

python3 refresh_gds_leaf_cells.py \
  --target tft3d_macros/gds/open3dstack_f5_decoder_compact_spice_dual_sided_with_sense_amp_precharge_col_driver_folded.gds \
  --source tft3d_macros/gds/nfet_W6u_L5.gds:nfet_W6u_L5 \
  --match-prefixed \
  --report reports/f5_folded_nfet_w6_leaf_refresh.json
```

Pull the refreshed final GDS and report back local:

```sh
scp vboxuser@100.115.20.54:/home/vboxuser/codex_tft3d_cdslib_ngspice_check_20260620/tft3d_macros/gds/open3dstack_f5_decoder_compact_spice_dual_sided_with_sense_amp_precharge_col_driver_folded.gds \
  pdk/tft3d_platform/libs.ref/tft3d_macros/gds/open3dstack_f5_decoder_compact_spice_dual_sided_with_sense_amp_precharge_col_driver_folded.gds

scp vboxuser@100.115.20.54:/home/vboxuser/codex_tft3d_cdslib_ngspice_check_20260620/reports/f5_folded_nfet_w6_leaf_refresh.json \
  pdk/tft3d_platform/libs.ref/tft3d_macros/gds/f5_folded_nfet_w6_leaf_refresh.json
```

## Why `--match-prefixed` Matters

The folded GDS may not contain a cell named exactly `nfet_W6u_L5`. Imported
children are often renamed with hierarchy prefixes, for example:

```text
col_dec__nfet_W6u_L5
decmap__nfet_W6u_L5
pch__nfet_W6u_L5
sa_w6__nfet_W6u_L5
sel__nfet_W6u_L5
```

`--match-prefixed` updates every target cell named either `SOURCE_CELL` or
`PREFIX__SOURCE_CELL`. Parent references are left intact, so the updated cell is
seen by all higher-level instances in the folded hierarchy.

## Refreshing More Cells

For a single known leaf, prefer explicit `--source`:

```sh
python3 scripts/refresh_gds_leaf_cells.py \
  --target pdk/tft3d_platform/libs.ref/tft3d_macros/gds/open3dstack_f5_decoder_compact_spice_dual_sided_with_sense_amp_precharge_col_driver_folded.gds \
  --source pdk/tft3d_platform/libs.ref/tft3d_macros/gds/nfet_W6u_L5.gds:nfet_W6u_L5 \
  --match-prefixed \
  --report pdk/tft3d_platform/libs.ref/tft3d_macros/gds/f5_folded_nfet_w6_leaf_refresh.json
```

To discover matching source cells from a directory:

```sh
python3 scripts/refresh_gds_leaf_cells.py \
  --target pdk/tft3d_platform/libs.ref/tft3d_macros/gds/open3dstack_f5_decoder_compact_spice_dual_sided_with_sense_amp_precharge_col_driver_folded.gds \
  --source-dir pdk/tft3d_platform/libs.ref/tft3d_macros/gds \
  --match-prefixed \
  --report pdk/tft3d_platform/libs.ref/tft3d_macros/gds/f5_folded_gds_hierarchy_refresh.json
```

Use `--source-dir` carefully: it refreshes every matching source top cell it can
find. For ECO work, explicit `--source` is safer.

## Outputs And Safety

The script:

- creates a timestamped backup next to the target GDS unless `--no-backup` is used
- reports the target hash before and after refresh
- reports each updated target cell
- reports direct parent cells and ancestor cells for each update
- preserves parent references, source reference transforms, labels, paths, and polygons

After refreshing, compare local and remote hashes:

```sh
sha256sum tft3d_macros/gds/open3dstack_f5_decoder_compact_spice_dual_sided_with_sense_amp_precharge_col_driver_folded.gds
```

On Windows:

```powershell
Get-FileHash pdk/tft3d_platform/libs.ref/tft3d_macros/gds/open3dstack_f5_decoder_compact_spice_dual_sided_with_sense_amp_precharge_col_driver_folded.gds -Algorithm SHA256
```

## Padframe Route ECOs

`padframe_to_macro_routes` is a top-level hierarchy route cell, not a leaf macro
that can be refreshed from `--source`. If a pad assignment changes, update this
route cell directly and audit it separately from the leaf-cell refresh.

For precharge/equalizer and sense-amplifier bottom-pad reroutes, keep the
wrapper mapping and GDS labels aligned:

```text
PAD_S08 eq
PAD_S09 pchg
PAD_S10 precharge
PAD_S11 vpre
PAD_S18 vdd_sense
PAD_S19 vdd_inv_sense
PAD_S20 vth_sense
PAD_S21 vss_sense
PAD_S22..PAD_S29 sense_out<0>..sense_out<7>
```

After editing the route cell, verify that every moved net has exactly one
connected route component, no component contains labels from two moved nets, and
all route endpoints overlap the intended padframe and macro pin metal. The
current audit report for that ECO is:

```text
pdk/tft3d_platform/libs.ref/tft3d_macros/gds/f5_precharge_opamp_bottom_pad_reroute.json
```

Older audit flows may only check internal route cells such as
`precharge_to_mux_routes` or `sl_mux_routes`; include `padframe_to_macro_routes`
when the ECO touches padframe-to-macro wiring.
