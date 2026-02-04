# INF1008 Assignment (Part 1)

## Team
- Chern Ze Hou (2303710) — Q2b
- Guo You Yan (2502970) — Q2a
- Ang Ben Rong (2503508) — Q3b
- Adil Hadi (2500499) — Q1
- Ng Jun Yang (2500406) — Q1
- Mohamad Danish Bin Mohammad (2501370) — Q3a

## Folder Structure
- `Q1_2500499_2500406/` — Singly linked list ADT with index map
- `Q2A_2502970/` — Order of growth algorithms (heap sort + subset sum)
- `Q2B_2303710/` — Recursion implementation (GSR analyzer)
- `Q3A_2501370/` — Sorting stability analysis (merge vs quick)
- `Q3B_2503508/` — Counting sort implementation and tests

## Questions Overview
### Q1: Singly Linked List ADT Implementation
Implements a singly linked list augmented with an index map (hash map) to enable O(1) access by index. The list supports `get`, `insert`, and `remove` while rebuilding or shifting indices to maintain correct index mappings.

### Q2a: Order of Growth
Two contrasting algorithms are implemented to demonstrate asymptotic growth:
- Carpark occupancy analyzer using Heap Sort (O(n log n)).
- Hawker food budget optimizer using exhaustive subset sum (O(2^n)).

### Q2b: Recursion Implementation
Implements an Overlapping Divide and Conquer approach to analyze HDB resale flat affordability using a Grant Support Ratio (GSR). The program demonstrates the recurrence `T(n) = 3T(n/2) + log n` with empirical complexity reporting.

### Q3a: Sorting Algorithm Analysis
Demonstrates stability in sorting by comparing Merge Sort (stable) and Quick Sort (unstable) on a large dataset, with validation checks for correctness and stability.

### Q3b: Sorting Algorithm Implementation and Proof
Implements Counting Sort (non-comparison-based) and provides testing/benchmarking scripts to validate correctness and illustrate performance under different value ranges.

## User Guide
All programs are in Python. Use `python3` (or `python` if your environment maps to Python 3).

### Q1: Singly Linked List ADT
- Run:
  - `python3 Q1_2500499_2500406/singly_linked_list_ADT.py`
- What it does:
  - Executes a built-in test sequence showing `insert`, `get`, and `remove` behavior and prints the list after each operation.

### Q2a: Order of Growth
#### Carpark Occupancy Analyzer (Heap Sort)
- Run:
  - `python3 Q2A_2502970/carpark_heapsort.py`
- What it does:
  - Menu-driven program for small tests, stress tests, scalability checks, and comparison-count analysis.

#### Hawker Budget Optimizer (Subset Sum)
- Run:
  - `python3 Q2A_2502970/hawker_subset_sum.py`
- What it does:
  - Menu-driven program for small verification and an exponential growth demonstration.

### Q2b: Recursion Implementation (GSR Analyzer)
- Requirements:
  - `pandas` installed (`pip install pandas`)
- Run:
  - `python3 Q2B_2303710/GSR_Analyzer.py`
- What it does:
  - Loads `Resale_Flat_Prices_Jan_2017_onwards.csv` and prompts for a town to compute peak GSR and complexity stats.

### Q3a: Sorting Stability Analysis
- Run:
  - `python3 Q3A_2501370/q3a.py`
- What it does:
  - Generates a large dataset and demonstrates stable vs unstable sorting, with verification checks.

### Q3b: Counting Sort
- Demo run:
  - `python3 Q3B_2503508/counting_sort.py`
- Test/benchmark run:
  - `python3 Q3B_2503508/counting_sort_test.py`
- What it does:
  - Demonstrates counting sort and benchmarks performance for different value ranges, including correctness checks.
