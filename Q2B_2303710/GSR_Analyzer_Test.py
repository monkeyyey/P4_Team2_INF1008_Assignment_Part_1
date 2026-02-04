# gsr_test_harness.py
import os
import pandas as pd

from GSR_Analyzer import (
    binary_search_grant,
    find_policy_shock_index,
    HDBGrantSupportAnalyzer,
    CSV_FILENAME,
    TARGET_FLAT_TYPE,
)

TOWNS = [
    "ANG MO KIO", "BEDOK", "BISHAN", "BUKIT BATOK", "BUKIT MERAH",
    "BUKIT PANJANG", "BUKIT TIMAH", "CENTRAL AREA", "CHOA CHU KANG",
    "CLEMENTI", "GEYLANG", "HOUGANG", "JURONG EAST", "JURONG WEST",
    "KALLANG/WHAMPOA", "MARINE PARADE", "PASIR RIS", "PUNGGOL",
    "QUEENSTOWN", "SEMBAWANG", "SENGKANG", "SERANGOON", "TAMPINES",
    "TOA PAYOH", "WOODLANDS", "YISHUN"
]


def print_table(title, rows, headers):
    print(f"\n=== {title} ===")
    widths = [len(h) for h in headers]
    for r in rows:
        for i, val in enumerate(r):
            widths[i] = max(widths[i], len(str(val)))

    fmt = " | ".join("{:<" + str(w) + "}" for w in widths)
    print(fmt.format(*headers))
    print("-" * (sum(widths) + 3 * (len(widths) - 1)))
    for r in rows:
        print(fmt.format(*r))


def unit_tests():
    # --- binary_search_grant tests ---
    months = ["2016-12", "2017-01", "2018-05", "2019-09",
              "2020-01", "2023-02", "2024-07", "2024-08", "2025-01"]
    expected = [70000, 70000, 70000, 50000, 50000, 70000, 70000, 85000, 85000]
    rows = []
    for m, exp in zip(months, expected):
        got = binary_search_grant(m)
        rows.append([m, exp, got, "PASS" if got == exp else "FAIL"])
    print_table("Unit Test: binary_search_grant", rows,
                ["month", "expected", "got", "result"])

    # --- find_policy_shock_index tests ---
    # Case 1: shock exists at index 1
    data1 = [{"month": "2019-08"}, {"month": "2019-09"}, {"month": "2019-10"}]
    got1 = find_policy_shock_index(data1, 0, len(data1) - 1)

    # Case 2: no shock in range
    data2 = [{"month": "2018-01"}, {"month": "2018-02"}, {"month": "2018-03"}]
    got2 = find_policy_shock_index(data2, 0, len(data2) - 1)

    rows2 = [
        ["shock present", 1, got1, "PASS" if got1 == 1 else "FAIL"],
        ["no shock", -1, got2, "PASS" if got2 == -1 else "FAIL"],
    ]
    print_table("Unit Test: find_policy_shock_index", rows2,
                ["case", "expected", "got", "result"])


def recursion_correctness_tests():
    analyzer = HDBGrantSupportAnalyzer()

    # Base case n=10
    base_data = [{"month": "2024-01", "resale_price": 500000}] * 10
    got_base = analyzer.analyze(base_data)
    expected_base = 500000 / 70000  # 2024-01 grant
    rows = [["base case (n=10)", f"{expected_base:.10f}", f"{got_base:.10f}",
             "PASS" if abs(got_base - expected_base) < 1e-9 else "FAIL"]]

    print_table("Correctness Test: analyze()", rows, [
                "test", "expected", "got", "result"])


def end_to_end_real_csv(sample_towns=("BUKIT PANJANG", "WOODLANDS", "TOA PAYOH")):
    if not os.path.exists(CSV_FILENAME):
        print(f"\n[SKIP] CSV not found: {CSV_FILENAME}")
        return

    df = pd.read_csv(CSV_FILENAME)

    rows = []
    for town in sample_towns:
        df_town = df[(df["flat_type"] == TARGET_FLAT_TYPE)
                     & (df["town"] == town)].copy()
        df_town = df_town.sort_values("month")
        data_list = df_town.to_dict("records")

        if not data_list:
            rows.append([town, 0, "-", "-", "-", "No data"])
            continue

        analyzer = HDBGrantSupportAnalyzer()
        peak = analyzer.analyze(data_list)
        status, advice = analyzer.interpret_GSR(peak)

        rows.append([town, len(data_list), analyzer.recursive_calls,
                    analyzer.max_depth, f"{peak:.4f}", status])

    print_table("End-to-End Sample Town Results", rows,
                ["town", "transactions", "calls", "max_depth", "peak_GSR", "status"])


if __name__ == "__main__":
    unit_tests()
    recursion_correctness_tests()

    # Change towns here if you want different ones
    end_to_end_real_csv(sample_towns=(
        "BUKIT PANJANG", "WOODLANDS", "TOA PAYOH"))
