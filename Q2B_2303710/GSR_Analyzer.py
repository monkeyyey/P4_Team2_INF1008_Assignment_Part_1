import pandas as pd
import math
import os
# Policy table sorted by date for Binary Search (O(lg m) complexity)
GRANT_POLICY_TABLE = [
    ("2017-01", 70000),  # Family Grant 50k + AHG 20k
    ("2019-09", 50000),
    ("2023-02", 70000),
    ("2024-08", 85000),
]

# Policy Change Dates
POLICY_DATES = ["2019-09", "2023-02", "2024-08"]
BASE_CASE_SIZE = 10
BRANCHING_FACTOR = 3
CSV_FILENAME = "Resale_Flat_Prices_Jan_2017_onwards.csv"
TARGET_FLAT_TYPE = "3 ROOM"


def demonstrate_complexity(n_values):
    # Updated header to reflect Total Theoretical Calls
    print("\n=== Proof of Time Complexity ===")
    print(f"{'n':>6} | {'Max Depth':>9} | {'Exp. Depth':>10} | {'Act. Calls':>10} | {'Theo. Calls':>12}")
    print("-" * 63)

    for n in n_values:
        # 1. Setup Data and Analyzer
        sample_data = [{'month': '2024-01', 'town': 'BUKIT PANJANG', 'flat_type': TARGET_FLAT_TYPE,
                        'lease_commence_date': 1980, 'resale_price': 500000}] * n

        analyzer = HDBGrantSupportAnalyzer()

        # 2. Run Actual Code
        analyzer.analyze(sample_data)

        # 3. Calculate Theoreticals
        # k = log2(n/10). We use max(0, ...) to handle n <= 10
        theoretical_height = max(0, math.ceil(math.log2(n / BASE_CASE_SIZE)))

        # Calculate Total Theoretical Calls using the Geometric Series: (a^(k+1) - 1) / (a - 1)
        # This counts every node in the tree (Internal + Leaves)
        theoretical_calls = (
            (BRANCHING_FACTOR**(theoretical_height + 1) - 1)
            / (BRANCHING_FACTOR - 1)
        )

        print(f"{n:6d} | {analyzer.max_depth:9d} | {theoretical_height:10d} | {analyzer.recursive_calls:10d} | {theoretical_calls:12.0f}")


def binary_search_grant(month_key):
    """Retrieves grant for a specific month using O(lg n) Binary Search."""
    low, high = 0, len(GRANT_POLICY_TABLE) - 1
    best_match = GRANT_POLICY_TABLE[0][1]
    while low <= high:
        mid = (low + high) // 2
        if GRANT_POLICY_TABLE[mid][0] <= month_key:
            best_match = GRANT_POLICY_TABLE[mid][1]
            low = mid + 1
        else:
            high = mid - 1
    return best_match


def find_policy_shock_index(data, start, end):
    """
    O(lg n): Binary Search to find the first index 
    where a major policy change or grant adjustment happened.
    """
    low, high = start, end
    shock_index = -1

    # We search for any of our critical policy dates in the current data segment
    while low <= high:
        mid = (low + high) // 2
        # If the transaction date matches a known policy change month
        if data[mid]['month'] in POLICY_DATES:
            shock_index = mid
            high = mid - 1  # Keep looking for the earliest shock in this range
        elif data[mid]['month'] < POLICY_DATES[0]:
            low = mid + 1
        else:
            high = mid - 1
    return shock_index

# --- 2. THE RECURSIVE ALGORITHM: T(n) = 3T(n/2) + lg n ---


class HDBGrantSupportAnalyzer:
    def __init__(self):
        self.recursive_calls = 0
        self.max_depth = 0

    def analyze(self, data, current_depth=0):
        n = len(data)
        self.recursive_calls += 1
        # Track the deepest point reached in the tree
        self.max_depth = max(self.max_depth, current_depth)

        # --- BASE CASE ---
        if n <= BASE_CASE_SIZE:
            if n == 0:
                return 0

            sum_price = sum(t['resale_price'] for t in data)
            mean_price = sum_price / n

            grant_amount = binary_search_grant(data[n // 2]['month'])

            return mean_price / grant_amount

        # --- Basic Operation: f(n) = lg n ---
        # Search for a 'Policy Shock' index within the current timeframe
        shock_idx = find_policy_shock_index(data, 0, n - 1)

        shock_ratio = 0
        if shock_idx != -1:
            # If a shock exists, calculate the ratio EXACTLY at that policy transition
            grant = binary_search_grant(data[shock_idx]['month'])
            shock_ratio = data[shock_idx]['resale_price'] / grant

        # --- DIVIDE AND CONQUER 3*T(n/2) ---
        mid = n // 2
        q1 = n // 4
        q3 = q1 + mid  # Covers the middle 50% (25th to 75th percentile)

        first_half = self.analyze(data[:mid], current_depth + 1)
        second_half = self.analyze(data[mid:], current_depth + 1)
        boundary_sector = self.analyze(data[q1:q3], current_depth + 1)

        # Recurse back the maximum GSR found accross 3 segments including shock
        return max(first_half, second_half, boundary_sector, shock_ratio)

    def interpret_GSR(self, ratio):
        """Translates the peak Grant Support Ratio into buyer advice."""

        if ratio < 5.0:
            status = "Optimal Support (Low GSR)"
            advice = "Grant support is high. The downpayment barrier is minimal."
        elif 5.0 <= ratio < 8.0:
            status = "Decent Support (MODERATE GSR)"
            advice = "Healthy buffer. Expect to fund about half of the downpayment via CPF/Cash."
        elif 8.0 <= ratio < 10.0:
            status = "Mediocre Support (High GSR)"
            advice = "Relatively Expensive. Price growth has significantly outpaced grant support."
        else:
            status = "Low Support (Very High GSR)"
            advice = "Market Disconnect. Grant covers <10% of price. Significant cash/OA reserves required."

        return status, advice


# --- 3. MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # Usage with test data
    demonstrate_complexity([10, 40, 100, 160, 400, 500, 640, 3038])
    TOWNS = [
        "ANG MO KIO", "BEDOK", "BISHAN", "BUKIT BATOK", "BUKIT MERAH",
        "BUKIT PANJANG", "BUKIT TIMAH", "CENTRAL AREA", "CHOA CHU KANG",
        "CLEMENTI", "GEYLANG", "HOUGANG", "JURONG EAST", "JURONG WEST",
        "KALLANG/WHAMPOA", "MARINE PARADE", "PASIR RIS", "PUNGGOL",
        "QUEENSTOWN", "SEMBAWANG", "SENGKANG", "SERANGOON", "TAMPINES",
        "TOA PAYOH", "WOODLANDS", "YISHUN"
    ]

    print("\n=== HDB Grant Support Analyzer ===")
    for i, town in enumerate(TOWNS, 1):
        print(f"{i:2d}. {town}")

    try:
        choice = int(input("\nSelect town (1-26): "))
        if not (1 <= choice <= 26):
            raise ValueError
        selected_town = TOWNS[choice - 1]

        # Load data
        df = pd.read_csv(CSV_FILENAME)
        # Remove columns that aren't needed for GSR analysis
        columns_to_remove = [
            'block', 'street_name', 'storey_range',
            'floor_area_sqm', 'flat_model', 'remaining_lease'
        ]
        df_pruned = df.drop(columns=columns_to_remove)

        # Filter: 3 ROOM and specific Town
        df_town_filtered = df_pruned[(df_pruned['flat_type'] == TARGET_FLAT_TYPE) &
                                     (df_pruned['town'] == selected_town)].copy()

        # Sort chronologically (Crucial for n/2 splits to represent time sectors)
        df_town_filtered = df_town_filtered.sort_values('month')

        # Prepare for recursion
        data_list = df_town_filtered.to_dict('records')

        if data_list:
            analyzer = HDBGrantSupportAnalyzer()
            peak_GSR = analyzer.analyze(data_list)
            grant_support_status, message = analyzer.interpret_GSR(
                peak_GSR)
            print(
                f"\n[REPORT FOR {selected_town}]\n"
                f"Transactions: {len(data_list)}\n"
                f"Recursive Calls: {analyzer.recursive_calls}\n"
                f"Max Depth: {analyzer.max_depth}\n"
                f"Peak Grant Support Ratio (Mean Price / Grant): {peak_GSR:.4f}\n"
                f"Grant Support for {selected_town}: {grant_support_status}\n"
                f"Advice: {message}\n\n"
            )
        else:
            print(f"No data available for {selected_town}.")

    except (ValueError, IndexError):
        print("Invalid selection. Please run the script again.")
    except FileNotFoundError:
        print("CSV file not found. Ensure the dataset is in the script directory.")
