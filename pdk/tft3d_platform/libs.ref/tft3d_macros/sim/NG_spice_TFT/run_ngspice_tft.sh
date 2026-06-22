#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ngspice -b -o id_vds_tft_n1_ngspice.log id_vds_tft_n1_ngspice.sp
printf 'Wrote %s, %s, and %s
'   "id_vds_tft_n1_ngspice.log"   "id_vds_tft_n1_ngspice.dat"   "id_vds_tft_n1_ngspice.raw"
