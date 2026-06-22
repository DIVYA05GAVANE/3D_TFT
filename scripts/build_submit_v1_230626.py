#!/usr/bin/env python3
"""Build the compact Open3DStack submit GDS.

The folded source keeps a full north/top pad row and places the standalone test
fixtures high in the wrapper.  This export removes the unused top pads, keeps the
test fixtures plus the marked SRAM array, and tightens the wrapper/frame height.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import gdstk


ROOT = Path(__file__).resolve().parents[1]
GDS_DIR = ROOT / "pdk/tft3d_platform/libs.ref/tft3d_macros/gds"
SOURCE_GDS = GDS_DIR / "open3dstack_f5_decoder_compact_spice_dual_sided_with_sense_amp_precharge_col_driver_folded.gds"
OUTPUT_GDS = GDS_DIR / "submit_v1_230626.gds"
REPORT_JSON = GDS_DIR / "submit_v1_230626_report.json"

TOP_CELL = "open3dstack_f5_decoder_compact_spice_dual_sided_top"
PADFRAME_CELL = "open3dstack_padframe"
WRAPPER_CELL = "open3dstack_user_project_wrapper"
ROUTE_CELL = "padframe_to_macro_routes"

FRAME_W = 20_000.0
FRAME_H = 21_850.0
WRAPPER_X = 557.5
WRAPPER_Y = 1_000.0
WRAPPER_W = 18_000.0
WRAPPER_H = 20_550.0
TEST_BLOCK_Y = 14_550.0

KEEP_E_MAX = 19
KEEP_W_MAX = 30

VWL_P_NET = "vwl_p_wl_driver"
VWL_P_PAD_X = 736.0
VWL_P_PAD_LEFT_X = 65.0
VWL_P_PAD_Y = 1404.762
VWL_P_BUS_Y = 3350.0
VWL_P_LEFT_TRUNK_X = 2050.0
VWL_P_RIGHT_TRUNK_X = 17450.0
VWL_P_LEFT_PIN_X = 5859.11
VWL_P_RIGHT_PIN_X = 13535.89
VWL_P_PIN_YS = (
    3479.021,
    3779.021,
    4079.021,
    4379.021,
    4679.021,
    4979.021,
    5279.021,
    5579.021,
)


def bbox_tuple(bbox):
    if bbox is None:
        return None
    return [
        [round(float(bbox[0][0]), 3), round(float(bbox[0][1]), 3)],
        [round(float(bbox[1][0]), 3), round(float(bbox[1][1]), 3)],
    ]


def add_outline(cell: gdstk.Cell, x0: float, y0: float, x1: float, y1: float, width: float, layer: int, datatype: int) -> None:
    cell.add(gdstk.rectangle((x0, y0), (x1, y0 + width), layer=layer, datatype=datatype))
    cell.add(gdstk.rectangle((x0, y1 - width), (x1, y1), layer=layer, datatype=datatype))
    cell.add(gdstk.rectangle((x0, y0), (x0 + width, y1), layer=layer, datatype=datatype))
    cell.add(gdstk.rectangle((x1 - width, y0), (x1, y1), layer=layer, datatype=datatype))


def label_is_kept(label: gdstk.Label) -> bool:
    text = label.text
    if text.startswith("PAD_S"):
        return True
    if text.startswith("PAD_E"):
        return int(text.removeprefix("PAD_E")) <= KEEP_E_MAX
    if text.startswith("PAD_W"):
        return int(text.removeprefix("PAD_W")) <= KEEP_W_MAX
    return not text.startswith("PAD_N")


def is_removed_pad_polygon(poly: gdstk.Polygon) -> bool:
    if (poly.layer, poly.datatype) in {(150, 5), (152, 5)}:
        return True
    bbox = poly.bounding_box()
    if bbox is None:
        return False
    (x0, y0), (x1, _y1) = bbox

    # Unused north/top row.
    if y0 >= 23_000.0:
        return True

    # Unused upper right-side pads: PAD_E20..PAD_E42.
    if x0 >= 19_800.0 and y0 >= 9_450.0:
        return True

    # Unused upper left-side pads: PAD_W31..PAD_W42.
    if x1 <= 200.0 and y0 >= 14_450.0:
        return True

    return False


def compact_padframe(cell: gdstk.Cell) -> dict[str, int]:
    before_polys = len(cell.polygons)
    before_labels = len(cell.labels)
    removed_polys = [poly for poly in cell.polygons if is_removed_pad_polygon(poly)]
    removed_labels = [label for label in cell.labels if not label_is_kept(label)]
    cell.remove(*removed_polys, *removed_labels)

    add_outline(cell, 0.0, 0.0, FRAME_W, FRAME_H, 10.0, 150, 5)
    add_outline(
        cell,
        WRAPPER_X,
        WRAPPER_Y,
        WRAPPER_X + WRAPPER_W,
        WRAPPER_Y + WRAPPER_H,
        20.0,
        152,
        5,
    )
    return {
        "polygons_before": before_polys,
        "polygons_after": len(cell.polygons),
        "labels_before": before_labels,
        "labels_after": len(cell.labels),
    }


def is_test_ref(ref: gdstk.Reference) -> bool:
    name = ref.cell.name if isinstance(ref.cell, gdstk.Cell) else str(ref.cell)
    return name == "stack_sram_marked_right_array" or name.startswith("test_fixture_")


def compact_wrapper(cell: gdstk.Cell) -> dict[str, object]:
    before_polys = len(cell.polygons)
    moved: dict[str, tuple[float, float]] = {}

    test_refs = [ref for ref in cell.references if is_test_ref(ref)]
    old_y_min = min(ref.bounding_box()[0][1] for ref in test_refs if ref.bounding_box() is not None)
    dy = TEST_BLOCK_Y - old_y_min

    for ref in test_refs:
        old_origin = tuple(ref.origin)
        ref.origin = (ref.origin[0], ref.origin[1] + dy)
        name = ref.cell.name if isinstance(ref.cell, gdstk.Cell) else str(ref.cell)
        moved[name] = (round(float(old_origin[1]), 3), round(float(ref.origin[1]), 3))

    old_outlines = [poly for poly in cell.polygons if (poly.layer, poly.datatype) == (152, 5)]
    cell.remove(*old_outlines)
    add_outline(cell, 0.0, 0.0, WRAPPER_W, WRAPPER_H, 20.0, 152, 5)

    return {
        "polygons_before": before_polys,
        "polygons_after": len(cell.polygons),
        "test_ref_count": len(test_refs),
        "test_block_old_y_min": round(float(old_y_min), 3),
        "test_block_new_y_min": round(float(TEST_BLOCK_Y), 3),
        "test_block_shift_y": round(float(dy), 3),
        "moved_refs": moved,
    }


def pad_label_counts(cell: gdstk.Cell) -> dict[str, int]:
    counts = {"S": 0, "E": 0, "N": 0, "W": 0}
    for label in cell.labels:
        text = label.text
        if text.startswith("PAD_") and len(text) >= 5:
            side = text[4]
            if side in counts:
                counts[side] += 1
    return counts


def refs_bbox(refs: list[gdstk.Reference]):
    bboxes = [ref.bounding_box() for ref in refs]
    bboxes = [bbox for bbox in bboxes if bbox is not None]
    if not bboxes:
        return None
    return (
        (min(bbox[0][0] for bbox in bboxes), min(bbox[0][1] for bbox in bboxes)),
        (max(bbox[1][0] for bbox in bboxes), max(bbox[1][1] for bbox in bboxes)),
    )


def bbox_of_polygons(polygons: list[gdstk.Polygon]):
    bboxes = [poly.bounding_box() for poly in polygons]
    bboxes = [bbox for bbox in bboxes if bbox is not None]
    if not bboxes:
        return None
    return (
        (min(bbox[0][0] for bbox in bboxes), min(bbox[0][1] for bbox in bboxes)),
        (max(bbox[1][0] for bbox in bboxes), max(bbox[1][1] for bbox in bboxes)),
    )


def rect(cell: gdstk.Cell, x0: float, y0: float, x1: float, y1: float, layer: int, datatype: int = 0) -> None:
    cell.add(gdstk.rectangle((x0, y0), (x1, y1), layer=layer, datatype=datatype))


def wire_h(cell: gdstk.Cell, x0: float, x1: float, y: float, layer: int, width: float = 4.0) -> None:
    rect(cell, min(x0, x1), y - width / 2, max(x0, x1), y + width / 2, layer)


def wire_v(cell: gdstk.Cell, x: float, y0: float, y1: float, layer: int, width: float = 4.0) -> None:
    rect(cell, x - width / 2, min(y0, y1), x + width / 2, max(y0, y1), layer)


def metal_square(cell: gdstk.Cell, x: float, y: float, layer: int, size: float = 6.0) -> None:
    rect(cell, x - size / 2, y - size / 2, x + size / 2, y + size / 2, layer)


def via_stack(cell: gdstk.Cell, x: float, y: float) -> None:
    metal_square(cell, x, y, 8)
    rect(cell, x - 2.0, y - 2.0, x + 2.0, y + 2.0, 9)
    metal_square(cell, x, y, 10)


def bboxes_touch(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return (
        a[0] <= b[2] + 1e-6
        and b[0] <= a[2] + 1e-6
        and a[1] <= b[3] + 1e-6
        and b[1] <= a[3] + 1e-6
    )


def route_layers_connect(a: tuple[int, int], b: tuple[int, int]) -> bool:
    if a == b:
        return True
    return 9 in {a[0], b[0]} and {a[0], b[0]} <= {8, 9, 10}


def route_component_polygons(cell: gdstk.Cell, net_name: str) -> list[gdstk.Polygon]:
    shapes: list[dict[str, object]] = []
    for index, poly in enumerate(cell.polygons):
        bbox = poly.bounding_box()
        if bbox is None:
            continue
        shapes.append(
            {
                "index": index,
                "poly": poly,
                "layer": poly.layer,
                "datatype": poly.datatype,
                "bbox": (
                    float(bbox[0][0]),
                    float(bbox[0][1]),
                    float(bbox[1][0]),
                    float(bbox[1][1]),
                ),
            }
        )

    parent = list(range(len(shapes)))
    rank = [0] * len(shapes)

    def find(item: int) -> int:
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(a: int, b: int) -> None:
        root_a = find(a)
        root_b = find(b)
        if root_a == root_b:
            return
        if rank[root_a] < rank[root_b]:
            root_a, root_b = root_b, root_a
        parent[root_b] = root_a
        if rank[root_a] == rank[root_b]:
            rank[root_a] += 1

    buckets: dict[tuple[int, int], list[int]] = defaultdict(list)
    bucket_size = 200.0
    for index, shape in enumerate(shapes):
        x0, y0, x1, y1 = shape["bbox"]
        for gx in range(math.floor(x0 / bucket_size), math.floor(x1 / bucket_size) + 1):
            for gy in range(math.floor(y0 / bucket_size), math.floor(y1 / bucket_size) + 1):
                buckets[(gx, gy)].append(index)

    seen: set[tuple[int, int]] = set()
    for indexes in buckets.values():
        for offset, left in enumerate(indexes):
            for right in indexes[offset + 1 :]:
                key = (min(left, right), max(left, right))
                if key in seen:
                    continue
                seen.add(key)
                left_shape = shapes[left]
                right_shape = shapes[right]
                if route_layers_connect(
                    (left_shape["layer"], left_shape["datatype"]),
                    (right_shape["layer"], right_shape["datatype"]),
                ) and bboxes_touch(left_shape["bbox"], right_shape["bbox"]):
                    union(left, right)

    roots: set[int] = set()
    for label in cell.labels:
        if label.text != net_name:
            continue
        lx, ly = float(label.origin[0]), float(label.origin[1])
        for index, shape in enumerate(shapes):
            if shape["layer"] != label.layer:
                continue
            x0, y0, x1, y1 = shape["bbox"]
            if x0 - 1e-6 <= lx <= x1 + 1e-6 and y0 - 1e-6 <= ly <= y1 + 1e-6:
                roots.add(find(index))

    if not roots:
        raise RuntimeError(f"Could not find connected route component for {net_name}")

    return [shape["poly"] for index, shape in enumerate(shapes) if find(index) in roots]


def add_vwl_p_wl_driver_route(cell: gdstk.Cell) -> dict[str, object]:
    before_polygons = len(cell.polygons)
    before_labels = len(cell.labels)
    removed_polygons = route_component_polygons(cell, VWL_P_NET)
    removed_labels = [label for label in cell.labels if label.text == VWL_P_NET]
    removed_bbox = bbox_of_polygons(removed_polygons)
    removed_layer_counts = Counter((poly.layer, poly.datatype) for poly in removed_polygons)
    cell.remove(*removed_polygons, *removed_labels)

    wire_h(cell, VWL_P_PAD_LEFT_X, VWL_P_PAD_X, VWL_P_PAD_Y, 10)
    metal_square(cell, VWL_P_PAD_LEFT_X, VWL_P_PAD_Y, 10)
    via_stack(cell, VWL_P_PAD_X, VWL_P_PAD_Y)
    wire_v(cell, VWL_P_PAD_X, VWL_P_PAD_Y, VWL_P_BUS_Y, 8)
    via_stack(cell, VWL_P_PAD_X, VWL_P_BUS_Y)
    wire_h(cell, VWL_P_PAD_X, VWL_P_RIGHT_TRUNK_X, VWL_P_BUS_Y, 10)
    via_stack(cell, VWL_P_LEFT_TRUNK_X, VWL_P_BUS_Y)
    via_stack(cell, VWL_P_RIGHT_TRUNK_X, VWL_P_BUS_Y)
    wire_v(cell, VWL_P_LEFT_TRUNK_X, VWL_P_BUS_Y, max(VWL_P_PIN_YS), 8)
    wire_v(cell, VWL_P_RIGHT_TRUNK_X, VWL_P_BUS_Y, max(VWL_P_PIN_YS), 8)

    labels = [(VWL_P_PAD_X, VWL_P_PAD_Y)]
    for pin_y in VWL_P_PIN_YS:
        via_stack(cell, VWL_P_LEFT_TRUNK_X, pin_y)
        wire_h(cell, VWL_P_LEFT_TRUNK_X, VWL_P_LEFT_PIN_X, pin_y, 10)
        metal_square(cell, VWL_P_LEFT_PIN_X, pin_y, 10)
        labels.append((VWL_P_LEFT_PIN_X, pin_y))

        via_stack(cell, VWL_P_RIGHT_TRUNK_X, pin_y)
        wire_h(cell, VWL_P_RIGHT_PIN_X, VWL_P_RIGHT_TRUNK_X, pin_y, 10)
        metal_square(cell, VWL_P_RIGHT_PIN_X, pin_y, 10)
        labels.append((VWL_P_RIGHT_PIN_X, pin_y))

    for x, y in labels:
        cell.add(gdstk.Label(VWL_P_NET, (x, y), layer=10, texttype=0))

    added_polygons = cell.polygons[before_polygons - len(removed_polygons) :]
    added_bbox = bbox_of_polygons(added_polygons)
    added_layer_counts = Counter((poly.layer, poly.datatype) for poly in added_polygons)
    return {
        "removed_polygons": len(removed_polygons),
        "removed_labels": len(removed_labels),
        "removed_bbox_um": bbox_tuple(removed_bbox),
        "removed_layer_counts": {f"{layer}/{datatype}": count for (layer, datatype), count in sorted(removed_layer_counts.items())},
        "added_polygons": len(added_polygons),
        "added_labels": len(labels),
        "added_bbox_um": bbox_tuple(added_bbox),
        "added_layer_counts": {f"{layer}/{datatype}": count for (layer, datatype), count in sorted(added_layer_counts.items())},
        "bus_y_um": VWL_P_BUS_Y,
        "left_trunk_x_um": VWL_P_LEFT_TRUNK_X,
        "right_trunk_x_um": VWL_P_RIGHT_TRUNK_X,
        "pin_y_um": [round(pin_y, 3) for pin_y in VWL_P_PIN_YS],
        "polygons_before": before_polygons,
        "polygons_after": len(cell.polygons),
        "labels_before": before_labels,
        "labels_after": len(cell.labels),
    }


def main() -> None:
    lib = gdstk.read_gds(str(SOURCE_GDS))
    cells = {cell.name: cell for cell in lib.cells}

    padframe = cells[PADFRAME_CELL]
    wrapper = cells[WRAPPER_CELL]
    top = cells[TOP_CELL]
    routes = cells[ROUTE_CELL]

    padframe_report = compact_padframe(padframe)
    wrapper_report = compact_wrapper(wrapper)
    vwl_p_route_report = add_vwl_p_wl_driver_route(routes)
    test_refs = [ref for ref in wrapper.references if is_test_ref(ref)]
    test_block_wrapper_bbox = refs_bbox(test_refs)
    test_block_top_bbox = (
        (
            test_block_wrapper_bbox[0][0] + WRAPPER_X,
            test_block_wrapper_bbox[0][1] + WRAPPER_Y,
        ),
        (
            test_block_wrapper_bbox[1][0] + WRAPPER_X,
            test_block_wrapper_bbox[1][1] + WRAPPER_Y,
        ),
    )
    routes_bbox = routes.bounding_box()

    lib.write_gds(str(OUTPUT_GDS))

    report = {
        "source_gds": str(SOURCE_GDS),
        "output_gds": str(OUTPUT_GDS),
        "output_bytes": OUTPUT_GDS.stat().st_size,
        "cells_after": len(lib.cells),
        "top_cells_after": [cell.name for cell in lib.top_level()],
        "padframe": padframe_report,
        "wrapper": wrapper_report,
        "vwl_p_wl_driver_reroute": vwl_p_route_report,
        "pad_labels_after": pad_label_counts(padframe),
        "top_bbox_um": bbox_tuple(top.bounding_box()),
        "padframe_bbox_um": bbox_tuple(padframe.bounding_box()),
        "wrapper_bbox_um": bbox_tuple(wrapper.bounding_box()),
        "padframe_routes_bbox_um": bbox_tuple(routes_bbox),
        "test_block_wrapper_bbox_um": bbox_tuple(test_block_wrapper_bbox),
        "test_block_top_bbox_um": bbox_tuple(test_block_top_bbox),
        "route_to_test_vertical_gap_um": round(float(test_block_top_bbox[0][1] - routes_bbox[1][1]), 3),
        "kept_test_refs": sorted(
            ref.cell.name if isinstance(ref.cell, gdstk.Cell) else str(ref.cell)
            for ref in test_refs
        ),
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Wrote {OUTPUT_GDS}")
    print(f"Wrote {REPORT_JSON}")


if __name__ == "__main__":
    main()
