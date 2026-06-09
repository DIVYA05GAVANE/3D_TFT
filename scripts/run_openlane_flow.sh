#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
openlane_root=${OPENLANE_ROOT:-$HOME/OpenLane}
design_dir=${OPENLANE_DESIGN_DIR:-"$repo_root/openlane/tft3d_macro_layout"}
tag=${OPENLANE_TAG:-layout}
extra_args=${OPENLANE_EXTRA_ARGS:--no_lvs -no_drc -no_antennacheck}
pdk_root=${PDK_ROOT:-"$repo_root/pdk"}
pdk=${PDK:-tft3d_platform}
std_cell_library=${STD_CELL_LIBRARY:-tft3d_sc_t5}
macro_lib="$pdk_root/$pdk/libs.ref/tft3d_macros"

if [[ "$design_dir" != /* ]]; then
    design_dir="$repo_root/$design_dir"
fi

require_file() {
    if [[ ! -f "$1" ]]; then
        echo "missing required file: $1" >&2
        exit 1
    fi
}

require_glob() {
    local pattern=$1
    local matches=()
    shopt -s nullglob
    matches=($pattern)
    shopt -u nullglob
    if (( ${#matches[@]} == 0 )); then
        echo "missing required files matching: $pattern" >&2
        exit 1
    fi
}

require_file "$design_dir/config.tcl"
require_file "$pdk_root/$pdk/libs.tech/openlane/config.tcl"
require_file "$pdk_root/$pdk/libs.tech/openlane/$std_cell_library/config.tcl"
require_file "$pdk_root/$pdk/libs.ref/$std_cell_library/techlef/tft3d_platform.tlef"
require_file "$macro_lib/verilog/3d_tft_blackboxes.v"
require_file "$macro_lib/lib/3d_tft_placeholders.lib"
require_file "$macro_lib/spice/3d_tft_macros.spice"
require_file "$pdk_root/$pdk/libs.tech/ngspice/tft3d_platform.spice"
require_glob "$macro_lib/lef/*.lef"
require_glob "$macro_lib/gds/*.gds"

export PDK_ROOT="$pdk_root"
export PDK="$pdk"
export STD_CELL_LIBRARY="$std_cell_library"

if [[ -x /openlane/flow.tcl ]]; then
    cd /openlane
    # shellcheck disable=SC2086
    exec ./flow.tcl -design "$design_dir" -tag "$tag" -overwrite $extra_args
fi

if [[ ! -d "$openlane_root" ]]; then
    echo "OPENLANE_ROOT does not exist: $openlane_root" >&2
    exit 1
fi

image_tag=$(cd "$openlane_root" && python3 dependencies/get_tag.py)
platform=$(cd "$openlane_root" && python3 docker/current_platform.py)
image=${OPENLANE_IMAGE:-ghcr.io/the-openroad-project/openlane:${image_tag}-${platform}}

cd "$openlane_root"
exec docker run --rm \
    -v "$openlane_root:/openlane" \
    -v "$openlane_root/designs:/openlane/install" \
    -v "$HOME:$HOME" \
    -e PDK_ROOT="$PDK_ROOT" \
    -e PDK="$PDK" \
    -e STD_CELL_LIBRARY="$STD_CELL_LIBRARY" \
    --user "$(id -u):$(id -g)" \
    "$image" \
    bash -lc "cd /openlane && ./flow.tcl -design '$design_dir' -tag '$tag' -overwrite $extra_args"
