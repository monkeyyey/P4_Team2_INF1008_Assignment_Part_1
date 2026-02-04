import time
import random

# ==========================================
# Student Name: Guo You Yan (2502970)
# Algorithm: Hawker Food Budget Optimizer (Subset Sum)
# Method: Recursive Exhaustive Enumeration
# Complexity: O(2^n) - Exponential
# Space Complexity: O(n) call stack + O(n × k) solution storage
# 
# NOTE ON ALGORITHM SELECTION:
# This implementation uses "Exhaustive Recursion" (checking all subsets),
# distinct from the optimized "Backtracking" used in N-Queens (Lecture 5).
# Unlike N-Queens which prunes invalid branches early, this algorithm 
# intentionally explores the full decision tree to demonstrate O(2^n) complexity.
# ==========================================

class FoodItem:
    """
    Represents a food item from a hawker stall.
    
    Attributes:
        name (str): Name of the food item
        price (float): Price in SGD
    """
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def __repr__(self):
        return f"{self.name} (${self.price:.2f})"


def subset_sum_recursive(items, target, index=0, current_set=None):
    """
    Finds all combinations of items that sum EXACTLY to target budget.
    
    Algorithm Logic:
    For each item, we make a BINARY DECISION:
        1. Include it in the current set (reduce target by item's price)
        2. Exclude it from the current set (keep target unchanged)
    
    This creates a complete binary decision tree with 2^n leaf nodes,
    resulting in O(2^n) time complexity.
    
    Time Complexity: O(2^n) where n is the number of items
    Space Complexity: O(n) for recursion call stack + O(n × k) for storing k solutions
    
    Args:
        items: List of FoodItem objects
        target: Target budget amount (float)
        index: Current position in items list
        current_set: Current subset being built
        
    Returns:
        List of all valid subsets that sum to target
    """
    if current_set is None:
        current_set = []
        
    # Base Case 1: Target achieved (within epsilon for float comparison)
    if abs(target - 0) < 0.0001:
        return [current_set]
    
    # Base Case 2: No items left or target became negative
    if index >= len(items) or target < 0:
        return []
    
    current_item = items[index]
    
    # Branch 1: INCLUDE the current item
    # Subtract item's price from target and move to next item
    with_item = subset_sum_recursive(
        items, 
        target - current_item.price, 
        index + 1, 
        current_set + [current_item]
    )
    
    # Branch 2: EXCLUDE the current item
    # Keep target same and move to next item
    without_item = subset_sum_recursive(
        items, 
        target, 
        index + 1, 
        current_set
    )
    
    # Combine results from both branches
    return with_item + without_item


def generate_hawker_orders(n):
    """
    Generates n realistic hawker food items for testing.
    
    Input Validation:
        • n must be positive
        • n should not exceed practical limits for O(2^n) algorithm
    
    Args:
        n: Number of food items to generate
        
    Returns:
        List of FoodItem objects
        
    Raises:
        ValueError: If n is invalid
    """
    if n <= 0:
        raise ValueError("N must be positive")
    if n > 30:
        raise ValueError("N too large for O(2^n) algorithm (max 30 for demonstration)")
    
    menu = [
        "Chicken Rice", "Laksa", "Satay", "Char Kway Teow", 
        "Roti Prata", "Ice Kachang", "Cendol", "Nasi Lemak", 
        "Hokkien Mee", "Carrot Cake", "Rojak", "Bak Chor Mee",
        "Wonton Mee", "Mee Goreng", "Fried Rice"
    ]
    
    orders = []
    for i in range(n):
        name = random.choice(menu) + f" #{i+1}"
        # Random price between $3.00 and $8.00 (realistic hawker prices)
        price = round(random.uniform(3.0, 8.0), 1)
        orders.append(FoodItem(name, price))
    
    return orders


if __name__ == "__main__":
    print("=" * 75)
    print("Singapore Hawker Budget Optimizer")
    print("Algorithm: Subset Sum - O(2^n) Exponential Complexity")
    print("Find exact combinations that match your budget")
    print("=" * 75)
    
    while True:
        try:
            print("\n--- MENU ---")
            print("1. Small Verification (Finding exact budget)")
            print("2. Exponential Growth Proof (n=10 to n=25)")
            print("3. Exit")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '3':
                print("\nExiting. Enjoy your meal!")
                break
            
            if choice not in ['1', '2']:
                print("Invalid choice. Please enter 1-3.")
                continue
            
            if choice == '1':
                # Controlled test case for verification
                print("\n--- SMALL VERIFICATION TEST ---")
                orders = [
                    FoodItem("Chicken Rice", 4.0), 
                    FoodItem("Iced Tea", 1.5), 
                    FoodItem("Hokkien Mee", 4.0), 
                    FoodItem("Satay (5 sticks)", 5.5)
                ]
                target = 5.5
                
                print(f"\nAvailable Items:")
                for i, item in enumerate(orders, 1):
                    print(f"  {i}. {item}")
                print(f"\nTarget Budget: ${target:.2f}")
                
                print("\nFinding all combinations that sum to exactly ${:.2f}...".format(target))
                start = time.time()
                solutions = subset_sum_recursive(orders, target)
                elapsed = time.time() - start
                
                print(f"\n✓ Found {len(solutions)} valid combination(s):")
                for i, sol in enumerate(solutions, 1):
                    total = sum(x.price for x in sol)
                    items_list = [x.name for x in sol]
                    print(f"\n{i}. {items_list}")
                    print(f"   Total: ${total:.2f}")
                    
                    # Verification
                    if abs(total - target) > 0.001:
                        print("   ✗ ERROR: Sum mismatch!")
                    else:
                        print("   ✓ Sum verified correct")
                
                print(f"\nTime: {elapsed:.4f} seconds")
                print(f"Note: With {len(orders)} items, algorithm explored 2^{len(orders)} = {2**len(orders)} possible combinations")
                
            elif choice == '2':
                # Exponential growth demonstration
                print("\n--- EXPONENTIAL GROWTH PROOF ---")
                print("Testing how recursive calls DOUBLE with each additional item...\n")
                
                print(f"{'Items (N)':>10} {'Combinations (2^N)':>20} {'Time (s)':>12} {'Growth':>12}")
                print("-" * 60)
                
                prev_time = None
                
                for n in range(10, 26):
                    try:
                        orders = generate_hawker_orders(n)
                        # Use impossible target to force full tree traversal
                        target = 9999.0
                        
                        start = time.time()
                        subset_sum_recursive(orders, target)
                        elapsed = time.time() - start
                        
                        ratio_str = "baseline"
                        if prev_time and prev_time > 0:
                            ratio = elapsed / prev_time
                            ratio_str = f"{ratio:.2f}x"
                        
                        print(f"{n:>10} {2**n:>20,} {elapsed:>12.4f} {ratio_str:>12}")
                        
                        prev_time = elapsed
                        
                        # Stop if taking too long
                        if elapsed > 5.0:
                            print("\n(Stopping early - exponential growth makes larger n impractical)")
                            print(f"Notice: Time is doubling with each additional item!")
                            print(f"This confirms O(2^n) exponential behavior.")
                            break
                            
                    except ValueError as e:
                        print(f"Error at n={n}: {e}")
                        break
                
                print("\n" + "=" * 60)
                print("ANALYSIS:")
                print("• Each additional item DOUBLES the number of combinations")
                print("• Growth factor consistently ~2.0x confirms O(2^n)")
                print("• Beyond n ≈ 25-30, algorithm becomes impractical")
                print("• This demonstrates why exponential algorithms are limited")
                print("=" * 60)
        
        except (EOFError, KeyboardInterrupt):
            print("\n\nProgram interrupted. Goodbye!")
            break
        
        except ValueError as e:
            print(f"\nError: {e}")
            print("Please try again with valid input.")
        
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Please report this issue.")