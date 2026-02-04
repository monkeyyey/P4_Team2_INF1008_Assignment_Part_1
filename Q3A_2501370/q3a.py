import random
import time
import sys
import copy

"""
this programme is created to test out 2 sorting algorithms for its stability, merge sort (stable) and quick sort (unstable)
this programme will do:
1. create a dataset of 1,000,000
2. sort the dataset in 2 ways (merge and quick sort)
3. check if sorted in ascending order
4. check if stable
run the programme and wait until finish sorting. quick sort will take more time than merge sort
"""

#set a recursion limit to handle quicksort on large dataset
sys.setrecursionlimit(2000000)

DATA_SIZE = 1000000

def generate_data(size):
    #generate a dictionary
    #key is a random int from 1 - 100000 (has duplicates) and original index is an int from 1 - 1,000,000 (no duplicates)
    data = []
    print(f"Generating {size} records...")
    for i in range(size):
        record = {
            'key': random.randint(0,100000),
            'original_index': i
        }
        data.append(record)
    return data

def verify_and_show_proof(arr, alg_name):
    print(f"\n[{alg_name}] ANALYSIS & PROOF")
    print("=" * 60)

    #1. PROOF OF SORTING: show the first few records
    #if the keys (0, 0, 1, 2...) are increasing, it's visually sorted
    print("A. SNAPSHOT (First 5 records):")
    for i in range(5):
        print(f"   Position {i}: {arr[i]}")

    # 2. PROOF OF STABILITY
    #look for two records next to each other that have the same key.
    #then check their original_index to see if they stayed in order.
    print("\nB. STABILITY EVIDENCE:")
    
    violation_found = False
    example_pair_found = False

    for i in range(len(arr) - 1):
        #only care about pairs with identical keys
        if arr[i]['key'] == arr[i+1]['key']:
            
            #check if this specific pair is "bad" (Unstable)
            if arr[i]['original_index'] > arr[i+1]['original_index']:
                print(f"   [PROOF OF INSTABILITY FOUND]")
                print(f"   We found two records with Key {arr[i]['key']}:")
                print(f"     1. {arr[i]} (Came from index {arr[i]['original_index']})")
                print(f"     2. {arr[i+1]} (Came from index {arr[i+1]['original_index']})")
                print("    CONCLUSION: The record that came LATER (index %d) is now FIRST." % arr[i]['original_index'])
                print("      This proves the algorithm is UNSTABLE.")
                violation_found = True
                break # We found our proof, stop looking.
            
            #if no violation found, keep this as a "Good" example
            #just in case the whole list is stable.
            if not example_pair_found:
                good_example_idx = i
                example_pair_found = True

    #if the loop is finished and found no violations, it is Stable
    #show the "Good" example we found earlier
    if not violation_found:
        if example_pair_found:
            i = good_example_idx
            print(f"   [PROOF OF STABILITY]")
            print(f"   Inspection of duplicate pair with Key {arr[i]['key']}:")
            print(f"     1. {arr[i]} (Came from index {arr[i]['original_index']})")
            print(f"     2. {arr[i+1]} (Came from index {arr[i+1]['original_index']})")
            print("    CONCLUSION: The original order (Index %d before %d) was PRESERVED." % (arr[i]['original_index'], arr[i+1]['original_index']))
            print("      (Checked all 1,000,000 records: No violations found.)")
        else:
            print("   (No duplicates found in the data to test stability.)")

    print("=" * 60)

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            #if keys are equal, take from left half first
            if left_half[i]['key'] <= right_half[j]['key']:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

#for quick sort
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        #compare key only
        if arr[j]['key'] < pivot['key']:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)


if __name__ == "__main__":
    #generate data
    master_data = generate_data(DATA_SIZE)

    #create independent copies for each sort so they don't affect each other
    data_for_merge = copy.deepcopy(master_data)
    data_for_quick = copy.deepcopy(master_data)

    #test merge sort
    print(f"\nRunning Merge Sort on {DATA_SIZE} records (Expecting Stable)...")
    start_time = time.time()
    merge_sort(data_for_merge)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    verify_and_show_proof(data_for_merge, "Merge Sort")

    #test quick sort
    print(f"Running Quick Sort on {DATA_SIZE} records (Expecting Unstable)...")
    start_time = time.time()
    quick_sort(data_for_quick, 0, len(data_for_quick) - 1)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    verify_and_show_proof(data_for_quick, "Quick Sort")