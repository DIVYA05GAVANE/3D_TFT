#!/usr/bin/env python3
"""Refresh embedded leaf cells in a standalone GDS from source leaf GDS files.

GDS references are internal to a stream file, so a top-level GDS will not update
itself when a lower-hierarchy source GDS changes. This script performs the
repeatable refresh step: for each source GDS, it replaces the contents of the
same-named cell inside the target GDS while preserving all parent references.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path

import gdstk


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def get_cell(lib: gdstk.Library, name: str) -> gdstk.Cell:
    for cell in lib.cells:
        if cell.name == name:
            return cell
    raise KeyError(name)


def cells_by_name(lib: gdstk.Library) -> dict[str, gdstk.Cell]:
    return {cell.name: cell for cell in lib.cells}


def source_top_cell(lib: gdstk.Library, source_path: Path, requested: str | None) -> gdstk.Cell:
    if requested:
        return get_cell(lib, requested)

    stem = source_path.stem
    for cell in lib.cells:
        if cell.name == stem:
            return cell

    tops = lib.top_level()
    if len(tops) == 1:
        return tops[0]

    names = ", ".join(sorted(cell.name for cell in tops))
    raise ValueError(f"{source_path}: cannot infer source top cell from top cells: {names}")


def clone_items(items):
    cloned = []
    for item in items:
        try:
            cloned.append(item.copy())
        except AttributeError:
            cloned.append(item)
    return cloned


def direct_parents(lib: gdstk.Library, child_name: str) -> list[dict[str, int | str]]:
    parents = []
    for cell in lib.cells:
        count = sum(1 for ref in cell.references if getattr(ref.cell, "name", ref.cell) == child_name)
        if count:
            parents.append({"cell": cell.name, "references": count})
    return sorted(parents, key=lambda item: str(item["cell"]))


def ancestors(lib: gdstk.Library, child_name: str) -> list[str]:
    graph = {
        cell.name: [getattr(ref.cell, "name", ref.cell) for ref in cell.references]
        for cell in lib.cells
    }
    result = []
    for cell in lib.cells:
        seen = set()
        stack = list(graph[cell.name])
        while stack:
            name = stack.pop()
            if name in seen:
                continue
            seen.add(name)
            stack.extend(graph.get(name, []))
        if child_name in seen:
            result.append(cell.name)
    return sorted(result)


def matching_target_cells(target_lib: gdstk.Library, source_name: str, match_prefixed: bool) -> list[gdstk.Cell]:
    matches = []
    for cell in target_lib.cells:
        if cell.name == source_name or (match_prefixed and cell.name.endswith("__" + source_name)):
            matches.append(cell)
    return sorted(matches, key=lambda cell: cell.name)


def ref_cell_name(ref: gdstk.Reference) -> str:
    return getattr(ref.cell, "name", ref.cell)


def clone_reference_for_target(
    source_ref: gdstk.Reference,
    target_ref_cell: gdstk.Cell,
) -> gdstk.Reference:
    if source_ref.repetition is not None and getattr(source_ref.repetition, "size", 0):
        raise ValueError("Array references are not supported by this refresh helper.")
    return gdstk.Reference(
        target_ref_cell,
        origin=tuple(source_ref.origin),
        rotation=source_ref.rotation,
        magnification=source_ref.magnification,
        x_reflection=source_ref.x_reflection,
    )


def mapped_reference_cell(
    target_cells: dict[str, gdstk.Cell],
    target_cell: gdstk.Cell,
    source_cell: gdstk.Cell,
    source_ref: gdstk.Reference,
    old_target_refs: list[gdstk.Reference],
    index: int,
) -> gdstk.Cell:
    source_ref_name = ref_cell_name(source_ref)
    prefix = ""
    if target_cell.name.endswith("__" + source_cell.name):
        prefix = target_cell.name[: -len(source_cell.name)]

    for candidate in (prefix + source_ref_name, source_ref_name):
        if candidate in target_cells:
            return target_cells[candidate]

    if len(old_target_refs) == len(source_cell.references):
        old_ref_name = ref_cell_name(old_target_refs[index])
        if old_ref_name in target_cells:
            return target_cells[old_ref_name]

    raise KeyError(
        f"{target_cell.name}: cannot map source reference {source_ref_name}; "
        f"tried {prefix + source_ref_name!r} and {source_ref_name!r}"
    )


def bbox_to_list(cell: gdstk.Cell):
    bbox = cell.bounding_box()
    if bbox is None:
        return None
    return [[float(x), float(y)] for x, y in bbox]


def refresh_cell(target_lib: gdstk.Library, target_cell: gdstk.Cell, source_cell: gdstk.Cell) -> dict:
    target_cells = cells_by_name(target_lib)
    old_target_refs = list(target_cell.references)
    before = {
        "target_cell": target_cell.name,
        "bbox": bbox_to_list(target_cell),
        "polygons": len(target_cell.polygons),
        "paths": len(target_cell.paths),
        "references": len(target_cell.references),
        "labels": len(target_cell.labels),
    }

    new_polygons = clone_items(source_cell.polygons)
    new_paths = clone_items(source_cell.paths)
    new_references = [
        clone_reference_for_target(
            ref,
            mapped_reference_cell(target_cells, target_cell, source_cell, ref, old_target_refs, index),
        )
        for index, ref in enumerate(source_cell.references)
    ]
    new_labels = clone_items(source_cell.labels)

    old_elements = (
        list(target_cell.polygons)
        + list(target_cell.paths)
        + list(target_cell.references)
        + list(target_cell.labels)
    )
    if old_elements:
        target_cell.remove(*old_elements)
    target_cell.add(*new_polygons, *new_paths, *new_references, *new_labels)

    after = {
        "target_cell": target_cell.name,
        "bbox": bbox_to_list(target_cell),
        "polygons": len(target_cell.polygons),
        "paths": len(target_cell.paths),
        "references": len(target_cell.references),
        "labels": len(target_cell.labels),
    }

    return {"source_cell": source_cell.name, "target_cell": target_cell.name, "before": before, "after": after}


def parse_source(spec: str) -> tuple[Path, str | None]:
    if ":" in spec:
        path, cell = spec.rsplit(":", 1)
        return Path(path), cell
    return Path(spec), None


def discover_sources(source_dirs: list[Path], target: Path, target_lib: gdstk.Library) -> list[str]:
    target_names = {cell.name for cell in target_lib.cells}
    target_resolved = target.resolve()
    discovered = []

    for source_dir in source_dirs:
        for source_path in sorted(source_dir.glob("*.gds")):
            if source_path.resolve() == target_resolved:
                continue
            source_lib = gdstk.read_gds(str(source_path))
            source_cell = source_top_cell(source_lib, source_path, None)
            if source_cell.name in target_names:
                discovered.append(f"{source_path}:{source_cell.name}")

    return discovered


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path, help="Standalone GDS to update in place.")
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Source leaf GDS, optionally SOURCE.gds:CELL_NAME. May be repeated.",
    )
    parser.add_argument(
        "--source-dir",
        action="append",
        default=[],
        type=Path,
        help="Discover matching source leaf GDS files from a directory. May be repeated.",
    )
    parser.add_argument(
        "--match-prefixed",
        action="store_true",
        help="Also refresh target cells named PREFIX__SOURCE_CELL.",
    )
    parser.add_argument("--report", type=Path, help="Optional JSON report path.")
    parser.add_argument("--no-backup", action="store_true", help="Skip timestamped .bak copy.")
    args = parser.parse_args()

    target = args.target
    target_before_hash = sha256(target)
    backup = None
    if not args.no_backup:
        backup = target.with_suffix(target.suffix + f".pre_leaf_refresh_{time.strftime('%Y%m%d_%H%M%S')}.bak")
        shutil.copy2(target, backup)

    target_lib = gdstk.read_gds(str(target))
    source_specs = list(args.source)
    source_specs.extend(discover_sources(args.source_dir, target, target_lib))
    if not source_specs:
        raise SystemExit("No source cells requested or discovered.")

    updates = []
    seen_cells = set()
    for source_spec in source_specs:
        source_path, requested_cell = parse_source(source_spec)
        source_lib = gdstk.read_gds(str(source_path))
        source_cell = source_top_cell(source_lib, source_path, requested_cell)
        if source_cell.name in seen_cells:
            continue
        seen_cells.add(source_cell.name)
        target_matches = matching_target_cells(target_lib, source_cell.name, args.match_prefixed)
        if not target_matches:
            raise KeyError(source_cell.name)
        for target_cell in target_matches:
            if target_cell.name in seen_cells:
                continue
            seen_cells.add(target_cell.name)
            parent_summary = direct_parents(target_lib, target_cell.name)
            ancestor_summary = ancestors(target_lib, target_cell.name)
            update = refresh_cell(target_lib, target_cell, source_cell)
            update.update(
                {
                    "source_gds": str(source_path),
                    "source_sha256": sha256(source_path),
                    "direct_parents": parent_summary,
                    "ancestor_cells": ancestor_summary,
                }
            )
            updates.append(update)

    target_lib.write_gds(str(target))
    report = {
        "target_gds": str(target),
        "backup_gds": str(backup) if backup else None,
        "target_sha256_before": target_before_hash,
        "target_sha256_after": sha256(target),
        "updates": updates,
        "status": "pass",
    }

    text = json.dumps(report, indent=2, sort_keys=True)
    if args.report:
        args.report.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
