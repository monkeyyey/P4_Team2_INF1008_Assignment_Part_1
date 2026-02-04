import time
import random
import math

# ==========================================
# Student Name: Guo You Yan (2502970)
# Algorithm: Singapore Carpark Occupancy Analyzer using Heap Sort
# Complexity: O(n log n) - Linearithmic
# Space Complexity: O(1) auxiliary space (in-place sorting)
# ==========================================

class CarparkRecord:
    """
    Represents a single carpark sensor reading from LTA's real-time system.
    
    Attributes:
        carpark_id (str): Unique identifier for the carpark
        available_lots (int): Number of currently available parking lots
        total_lots (int): Total capacity of the carpark
        occupancy_rate (float): Percentage of occupied lots (0.0 to 1.0)
    """
    def __init__(self, carpark_id, available_lots, total_lots):
        self.carpark_id = carpark_id
        self.available_lots = available_lots
        self.total_lots = total_lots
        # Avoid division by zero
        if total_lots > 0:
            self.occupancy_rate = (total_lots - available_lots) / total_lots
        else:
            self.occupancy_rate = 0.0

    def __repr__(self):
        return f"[{self.carpark_id}] {self.available_lots}/{self.total_lots} ({self.occupancy_rate:.1%} full)"


def heapify(arr, n, i, comparisons):
    """
    Maintains the Max-Heap property for a subtree rooted at index i.
    
    This is the CORE operation that makes Heap Sort O(log n) per call.
    The heap is a complete binary tree where:
    - Parent at index i
    - Left child at index 2*i + 1
    - Right child at index 2*i + 2
    
    Time Complexity: O(log n) - traverses height of heap
    
    Args:
        arr: Array of CarparkRecord objects
        n: Size of heap to consider
        i: Index of root of subtree to heapify
        comparisons: List containing comparison count (mutable for tracking)
    """
    largest = i  # Initialize largest as root
    left = 2 * i + 1     # Left child index
    right = 2 * i + 2    # Right child index

    # Compare with left child
    if left < n:
        comparisons[0] += 1
        if arr[left].occupancy_rate > arr[largest].occupancy_rate:
            largest = left

    # Compare with right child
    if right < n:
        comparisons[0] += 1
        if arr[right].occupancy_rate > arr[largest].occupancy_rate:
            largest = right

    # If largest is not root, swap and recursively heapify affected subtree
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, comparisons)


def heap_sort_carparks(data):
    """
    Sorts carpark records by occupancy rate using Heap Sort algorithm.
    Returns records from FULLEST to EMPTIEST.
    
    WHY O(n log n)?
    ===============
    Step 1 - BUILD MAX HEAP: O(n)
        • Start from last non-leaf node (n//2 - 1)
        • Heapify all nodes moving upward
        • Although individual heapify is O(log n), total work is O(n)
        • This is proven by: Σ(h=0 to log n) of (n/2^(h+1)) * h = O(n)
    
    Step 2 - EXTRACT MAX (n times): O(n log n)
        • Swap root (max element) with last element: O(1)
        • Heapify the reduced heap: O(log n)
        • Repeat n times: n × O(log n) = O(n log n)
    
    TOTAL: O(n) + O(n log n) = O(n log n)
    
    SPACE COMPLEXITY: O(1) auxiliary space
        • Sorts in-place using only a constant amount of extra memory
        • Only uses variables for loop counters and swap operations
        • This is better than Merge Sort's O(n) space requirement
    
    Args:
        data: List of CarparkRecord objects
        
    Returns:
        Tuple of (sorted_data, comparison_count)
    """
    n = len(data)
    comparisons = [0]  # Use list to make it mutable for tracking

    # STEP 1: Build Max-Heap
    # Process all non-leaf nodes from bottom to top
    # Last non-leaf node is at index (n//2 - 1)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i, comparisons)

    # STEP 2: Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root (maximum) to end of array
        data[i], data[0] = data[0], data[i]
        
        # Call max heapify on the reduced heap
        heapify(data, i, 0, comparisons)
    
    # Array is now in ascending order (emptiest to fullest)
    # Reverse it to get descending order (fullest to emptiest)
    data.reverse()
    
    return data, comparisons[0]


def generate_realistic_data(n):
    """
    Generates n realistic Singapore carpark records for testing.
    
    Input Validation:
        • n must be positive
        • n must not exceed system limits (10 million)
    
    Args:
        n: Number of carpark records to generate
        
    Returns:
        List of CarparkRecord objects
        
    Raises:
        ValueError: If n is invalid
    """
    if n <= 0:
        raise ValueError(f"Input size must be positive. Received {n}.")
    if n > 10000000:
        raise ValueError("Size too large for system limit (max 10 million).")

    locations = ["Jurong", "Tampines", "Woodlands", "Bedok", "Yishun", 
                 "Ang Mo Kio", "Toa Payoh", "Clementi", "Bukit Batok"]
    types = ["HDB", "Mall", "Office"]
    data = []
    
    for i in range(n):
        loc = random.choice(locations)
        typ = random.choice(types)
        carpark_id = f"{loc}-{typ}-{i:05d}"
        
        # Realistic capacity ranges by type
        if typ == "HDB":
            total = random.randint(100, 300)
        elif typ == "Mall":
            total = random.randint(500, 1500)
        else:  # Office
            total = random.randint(200, 800)
        
        # Simulate peak hour occupancy (70-95% full)
        available = random.randint(int(total * 0.05), int(total * 0.30))
        
        data.append(CarparkRecord(carpark_id, available, total))
    
    return data


def verify_sort_correctness(data):
    """
    Verifies that data is sorted in descending order by occupancy rate.
    
    Args:
        data: List of CarparkRecord objects
        
    Returns:
        Boolean indicating if data is correctly sorted
    """
    for i in range(len(data) - 1):
        if data[i].occupancy_rate < data[i+1].occupancy_rate:
            return False
    return True


# ==========================================
# Main Menu - Interactive Testing Interface
# ==========================================
if __name__ == "__main__":
    print("=" * 75)
    print("Singapore LTA Carpark Occupancy Analyzer")
    print("Algorithm: Heap Sort - O(n log n) Complexity")
    print("Real-time ranking to help drivers find parking during peak hours")
    print("=" * 75)
    
    while True:
        print("\n--- MENU ---")
        print("1. Small Test & Correctness Verification")
        print("2. Stress Test (100,000 records)")
        print("3. Scalability Test (Prove O(n log n) growth)")
        print("4. Comparison Count Analysis")
        print("5. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            # Small test with correctness verification
            try:
                print("\n--- SMALL TEST: 20 Carparks ---")
                data = generate_realistic_data(20)
                
                print("Analyzing 20 carparks...")
                start = time.time()
                sorted_data, comparisons = heap_sort_carparks(data.copy())
                elapsed = time.time() - start
                
                # Automated correctness check
                print("\n[CORRECTNESS VERIFICATION]")
                is_sorted = verify_sort_correctness(sorted_data)
                print(f"✓ Sort order correct (descending): {is_sorted}")
                
                if not is_sorted:
                    print("✗ ERROR: Data is not sorted correctly!")
                    continue
                
                print(f"✓ Comparisons made: {comparisons}")
                print(f"✓ Time: {elapsed:.4f} seconds")
                
                print("\nTop 5 Fullest Carparks (drivers should avoid):")
                for i, record in enumerate(sorted_data[:5], 1):
                    print(f"  {i}. {record}")
                
                print("\nBottom 5 Emptiest Carparks (best options):")
                for i, record in enumerate(sorted_data[-5:], 1):
                    print(f"  {i}. {record}")
                    
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '2':
            # Stress test with 100,000 records
            print("\n--- STRESS TEST: 100,000 Carpark Records ---")
            print("Generating 100,000 realistic records...")
            
            data = generate_realistic_data(100000)
            print(f"Generated {len(data):,} records")
            
            print("\nSorting...")
            start = time.time()
            sorted_data, comparisons = heap_sort_carparks(data)
            elapsed = time.time() - start
            
            print(f"\n✓ Sorted {len(sorted_data):,} records in {elapsed:.4f} seconds")
            print(f"  Average: {(elapsed/len(sorted_data))*1e6:.2f} microseconds per record")
            print(f"  Total comparisons: {comparisons:,}")
            
            # Verify correctness
            is_sorted = verify_sort_correctness(sorted_data)
            print(f"  Correctness check: {'PASSED' if is_sorted else 'FAILED'}")
            
            print("\nTop 5 Most Congested Carparks:")
            for i, record in enumerate(sorted_data[:5], 1):
                print(f"  {i}. {record}")
            
            # Theoretical comparison
            theoretical = len(data) * math.log2(len(data))
            print(f"\nTheoretical O(n log n) operations: {theoretical:,.0f}")
            print(f"Actual comparisons: {comparisons:,}")
            print(f"Ratio (actual/theoretical): {comparisons/theoretical:.2f}x")
            print("(Heap Sort typically does ~2× n log n comparisons)")
            
        elif choice == '3':
            # Scalability test to prove O(n log n)
            print("\n--- SCALABILITY TEST: Prove O(n log n) Growth ---")
            print("Testing how time scales as input doubles...\n")
            
            sizes = [10000, 20000, 40000, 80000]
            print(f"{'Size':>10} {'Time (s)':>12} {'Ratio':>10} {'Expected':>12} {'Match?':>10}")
            print("-" * 65)
            
            prev_time = None
            
            for size in sizes:
                # Run 3 times and use median to reduce noise
                times = []
                for run in range(3):
                    data = generate_realistic_data(size)
                    start = time.time()
                    heap_sort_carparks(data)
                    times.append(time.time() - start)
                
                times.sort()
                elapsed = times[1]  # Median time
                
                if prev_time:
                    measured_ratio = elapsed / prev_time
                    
                    # CORRECT FORMULA for O(n log n):
                    # When n doubles: T(2n)/T(n) = (2n log 2n)/(n log n)
                    #                            = 2 × (log n + log 2)/log n
                    #                            = 2 × (1 + 1/log₂ n)
                    log_n = math.log2(size / 2)  # Previous size's log
                    theoretical_ratio = 2 * (1 + 1/log_n)
                    
                    # Check if within 15% of expected
                    diff_pct = abs(measured_ratio - theoretical_ratio) / theoretical_ratio * 100
                    match = "✓" if diff_pct < 15 else "✗"
                    
                    print(f"{size:>10,} {elapsed:>12.4f} {measured_ratio:>10.2f}x {theoretical_ratio:>12.2f}x {match:>10}")
                else:
                    print(f"{size:>10,} {elapsed:>12.4f} {'--':>10} {'baseline':>12} {'--':>10}")
                
                prev_time = elapsed
            
            print("\n" + "="*65)
            print("ANALYSIS:")
            print("• For O(n log n), when n doubles: ratio ≈ 2 × (1 + 1/log₂ n)")
            print("• Expected ratios decrease: ~2.18x → 2.16x → 2.14x → 2.13x")
            print("• Ratios should converge toward 2.0 as n increases")
            print("• ✓ indicates measured ratio within 15% of theoretical")
            print("="*65)
            
        elif choice == '4':
            # Comparison count analysis
            print("\n--- COMPARISON COUNT ANALYSIS ---")
            print("Analyzing how comparisons scale with input size...\n")
            
            sizes = [100, 500, 1000, 5000, 10000]
            print(f"{'Size (n)':>12} {'Comparisons':>15} {'n*log₂(n)':>15} {'Ratio':>10}")
            print("-" * 55)
            
            for size in sizes:
                data = generate_realistic_data(size)
                _, comparisons = heap_sort_carparks(data)
                
                theoretical = size * math.log2(size)
                ratio = comparisons / theoretical
                
                print(f"{size:>12,} {comparisons:>15,} {theoretical:>15,.0f} {ratio:>10.2f}x")
            
            print("\n" + "="*55)
            print("EXPLANATION:")
            print("• Heap Sort comparisons are typically ~2 × n log₂ n")
            print("• The ratio of ~2.0x confirms our O(n log n) analysis")
            print("• This is consistent with theoretical Heap Sort behavior")
            print("="*55)
            
        elif choice == '5':
            print("\nExiting. Drive safely!")
            break
            
        else:
            print("Invalid choice. Please enter 1-5.")