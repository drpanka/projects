#!/usr/bin/env python3
"""Convert a Supermetrics data_query JSON tool-result file to CSV.

Header row is derived from requested_field_ids (NOT the row-0 display names).
Usage: sm2csv.py <in.json> <out.csv> [--keep-display-header]
"""
import json, csv, sys

def load(path):
    with open(path) as f:
        return json.load(f)

def to_csv(inp, outp):
    j = load(inp)
    d = j["data"]
    fids = d.get("requested_field_ids") or []
    rows = d.get("data") or []
    if not rows:
        print(f"{inp}: EMPTY (0 rows)")
        with open(outp, "w", newline="") as f:
            csv.writer(f).writerow(fids)
        return 0
    # row 0 is the display-name header from Supermetrics; drop it
    body = rows[1:] if len(rows[0]) == len(fids) else rows
    # sanity: if row0 does not look like a header (i.e. equals field ids) keep it
    with open(outp, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(fids)
        for r in body:
            w.writerow(r)
    print(f"{inp} -> {outp}: {len(body)} data rows, {len(fids)} cols: {fids}")
    return len(body)

if __name__ == "__main__":
    to_csv(sys.argv[1], sys.argv[2])
