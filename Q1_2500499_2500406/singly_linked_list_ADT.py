class Node:
    def __init__(self, data):
        self.data = data      # The actual value stored in this node
        self.next = None      # Pointer to the next node (None if last node)


class AugmentedLinkedList:
    """
    Augmented Singly Linked List with O(1) index-based access.

    This data structure combines a traditional singly linked list with a 
    hash map (dictionary) to enable constant-time access to any element
    by its index position.

    Key Components:
    - Linked list: Stores data as a chain of Node objects
    - Hash map (index_map): Maps integer indices to node references

    Time Complexities:
    - get(i):    O(1) - Direct hash map lookup
    - insert(i): O(1) best case (tail), O(n) worst case (index sync)
    - remove(i): O(1) best case (tail), O(n) worst case (index sync)
    """

    def __init__(self):
        """
        Initialize an empty augmented linked list.

        Attributes:
        - head: Points to the first node (None if list is empty)
        - tail: Points to the last node (enables O(1) append)
        - size: Number of elements currently in the list
        - index_map: Dictionary mapping index -> node reference
        """
        self.head = None
        self.tail = None
        self.size = 0
        self.index_map = {}  # Hash map for O(1) access: {index: Node}

    # ==================== INDEX MAP MANAGEMENT ====================

    def _rebuild_index_map(self):
        """
        Rebuild the entire index map by traversing the linked list.

        This method is called when a significant portion of indices
        need to be updated (e.g., insert/remove in first half of list).

        Algorithm:
        1. Clear existing mappings
        2. Traverse from head to tail
        3. Assign each node to its corresponding index

        Time Complexity: O(n) - Must visit every node once
        """
        self.index_map.clear()           # Remove all existing mappings
        current = self.head              # Start at the beginning
        idx = 0
        while current:                   # Traverse until end (None)
            self.index_map[idx] = current  # Map index to node reference
            current = current.next       # Move to next node
            idx += 1                     # Increment index counter

    def _update_indices_after_insert(self, start_index):
        """
        Update index mappings after a new element is inserted.

        When inserting at position i, all elements from i onwards
        shift to higher indices. This method synchronizes the hash map.

        Strategy Selection (Heuristic):
        - If start_index < size/2: Full rebuild (many indices affected)
        - If start_index >= size/2: Partial shift (fewer indices affected)

        Parameters:
        - start_index: Position where insertion occurred

        Time Complexity: O(n) worst case, O(n-i) for partial shift
        """
        if start_index < self.size // 2:
            # More than half the list affected - full rebuild is simpler
            self._rebuild_index_map()
        else:
            # Less than half affected - shift indices from end backwards
            # We go backwards to avoid overwriting values we still need
            for i in range(self.size - 1, start_index, -1):
                if i - 1 in self.index_map:
                    self.index_map[i] = self.index_map[i - 1]

    def _update_indices_after_remove(self, start_index):
        """
        Update index mappings after an element is removed.

        When removing at position i, all elements after i shift
        to lower indices. This method synchronizes the hash map.

        Strategy Selection (Heuristic):
        - If start_index < size/2: Full rebuild
        - If start_index >= size/2: Partial shift

        Parameters:
        - start_index: Position where removal occurred

        Time Complexity: O(n) worst case, O(n-i) for partial shift
        """
        if start_index < self.size // 2:
            # More than half affected - rebuild entire map
            self._rebuild_index_map()
        else:
            # Less than half affected - shift indices forward
            for i in range(start_index, self.size):
                if i + 1 in self.index_map:
                    self.index_map[i] = self.index_map[i + 1]
            # Clean up: remove the old last index (now invalid)
            if self.size in self.index_map:
                del self.index_map[self.size]

    # ==================== CORE OPERATIONS ====================

    def get(self, i):
        """
        Retrieve the data at position i.

        This is the key O(1) operation enabled by the hash map.
        Instead of traversing the linked list, we directly access
        the node through the index_map.

        Algorithm:
        1. Validate index bounds
        2. Look up node in hash map using index as key
        3. Return the node's data

        Parameters:
        - i: Index position (0-based)

        Returns:
        - Data stored at position i

        Raises:
        - IndexError: If i is out of bounds

        Time Complexity: O(1) - Hash map lookup is constant time
        """
        # Validate index is within valid range [0, size-1]
        if i < 0 or i >= self.size:
            raise IndexError(
                f"Index {i} out of bounds for list of size {self.size}")

        # Direct access: hash map lookup O(1) -> get node -> return data
        return self.index_map[i].data

    def insert(self, i, data):
        """
        Insert a new element with given data at position i.

        Three cases handled:
        1. Insert at head (i=0): New node becomes first element
        2. Insert at tail (i=size): New node becomes last element
        3. Insert in middle: New node inserted between existing nodes

        Parameters:
        - i: Index position where new element will be placed
        - data: Value to store in the new node

        Raises:
        - IndexError: If i is out of valid insert range [0, size]

        Time Complexity:
        - Best case O(1): Insert at tail (no index shifting)
        - Worst case O(n): Insert at head/middle (requires index sync)
        """
        # Validate index: insert allows [0, size] inclusive
        # (i=size means append at end)
        if i < 0 or i > self.size:
            raise IndexError(
                f"Insert index {i} out of bounds (valid range: 0-{self.size})")

        # Create new node with the given data
        new_node = Node(data)

        # CASE 1: Insert at head (i = 0)
        if i == 0:
            new_node.next = self.head    # New node points to old head
            self.head = new_node         # Update head to new node
            if self.size == 0:
                self.tail = new_node     # If list was empty, tail is also new node
            self.size += 1               # Increment size before updating indices
            self._update_indices_after_insert(0)  # Shift all indices
            self.index_map[0] = new_node          # Map index 0 to new node

        # CASE 2: Insert at tail (i = size, i.e., append)
        elif i == self.size:
            self.tail.next = new_node    # Old tail points to new node
            self.tail = new_node         # Update tail to new node
            self.size += 1               # Increment size
            # Simply add new mapping (no shifting needed)
            self.index_map[i] = new_node

        # CASE 3: Insert in middle (0 < i < size)
        else:
            # Get the node currently at position (i-1) using hash map - O(1)
            prev_node = self.index_map[i - 1]
            new_node.next = prev_node.next  # New node points to node that was at i
            prev_node.next = new_node       # Previous node now points to new node
            self.size += 1                  # Increment size before updating indices
            self._update_indices_after_insert(
                i)  # Shift indices from i onwards
            self.index_map[i] = new_node          # Map index i to new node

    def remove(self, i):
        """
        Remove and return the element at position i.

        Three cases handled:
        1. Remove head (i=0): Second element becomes new head
        2. Remove tail (i=size-1): Second-to-last becomes new tail
        3. Remove from middle: Bypass the removed node

        Parameters:
        - i: Index position of element to remove

        Returns:
        - Data from the removed node

        Raises:
        - IndexError: If i is out of bounds

        Time Complexity:
        - Best case O(1): Remove at tail (minimal index update)
        - Worst case O(n): Remove at head/middle (requires index sync)
        """
        # Validate index is within valid range [0, size-1]
        if i < 0 or i >= self.size:
            raise IndexError(
                f"Remove index {i} out of bounds for list of size {self.size}")

        # Get the node to be removed using hash map - O(1)
        removed_node = self.index_map[i]

        # CASE 1: Remove head (i = 0)
        if i == 0:
            self.head = self.head.next   # Head moves to second node
            if self.size == 1:
                self.tail = None         # List becomes empty
            self.size -= 1               # Decrement size BEFORE updating indices
            if self.size > 0:
                self._update_indices_after_remove(0)  # Shift all indices down
            else:
                self.index_map.clear()   # List is empty, clear all mappings

        # CASE 2 & 3: Remove from middle or tail (i > 0)
        else:
            # Get the node before the one being removed - O(1)
            prev_node = self.index_map[i - 1]
            prev_node.next = removed_node.next  # Bypass removed node

            # If removing tail, update tail pointer
            if i == self.size - 1:
                self.tail = prev_node    # Previous node is now the tail

            self.size -= 1               # Decrement size BEFORE updating indices
            self._update_indices_after_remove(
                i)  # Shift indices from i onwards

        # Return the data from removed node
        return removed_node.data

    # ==================== UTILITY METHODS ====================

    def get_values(self):
        """
        Helper method to visualize the list contents as a Python list.

        Traverses the linked list and collects all data values.
        Useful for debugging and testing.

        Returns:
        - List of all data values in order

        Time Complexity: O(n) - Must traverse entire list
        """
        values = []
        current = self.head
        while current:
            values.append(current.data)
            current = current.next
        return values


# ==================== TEST FUNCTION ====================

def test():
    """
    Test function demonstrating the augmented linked list operations.

    Corrected version: inserts first to populate the list,
    then performs get and remove operations.
    """
    ll = AugmentedLinkedList()

    print("#================INSERT======================")
    print("ll.insert(0, 10)")
    ll.insert(0, 10)                    # List: [10]
    print(f"  Array: {ll.get_values()}\n")

    print("ll.insert(1, 20)")
    ll.insert(1, 20)                    # List: [10, 20]
    print(f"  Array: {ll.get_values()}\n")

    print("ll.insert(0, 5)")
    ll.insert(0, 5)                     # List: [5, 10, 20]
    print(f"  Array: {ll.get_values()}\n")

    print("ll.insert(2, 15)")
    ll.insert(2, 15)                    # List: [5, 10, 15, 20]
    print(f"  Array: {ll.get_values()}\n")

    print("#==================GET========================")
    print("ll.get(0)")
    result = ll.get(0)
    print(f"  Returns: {result}")
    print(f"  Array: {ll.get_values()}\n")

    print("ll.get(2)")
    result = ll.get(2)
    print(f"  Returns: {result}")
    print(f"  Array: {ll.get_values()}\n")

    print("ll.get(3)")
    result = ll.get(3)
    print(f"  Returns: {result}")
    print(f"  Array: {ll.get_values()}\n")

    print("#==================REMOVE======================")
    print("ll.remove(2)")
    removed = ll.remove(2)              # Removes 15, List: [5, 10, 20]
    print(f"  Removed: {removed}")
    print(f"  Array: {ll.get_values()}\n")

    print("ll.remove(0)")
    removed = ll.remove(0)              # Removes 5, List: [10, 20]
    print(f"  Removed: {removed}")
    print(f"  Array: {ll.get_values()}\n")


if __name__ == "__main__":
    test()
