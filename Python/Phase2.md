# Phase 2: Core Data Structures — Interview Toolkit

> These structures appear in **60–70% of MAANG coding rounds**. Master them in order — each section builds on the last.

---

## Table of Contents

1. [Mental Model: How to Think About DS](#mental-model)
2. [Linear Structures](#linear-structures)
   - [Linked Lists](#linked-lists)
   - [Stacks](#stacks)
   - [Queues & Deques](#queues--deques)
3. [Non-Linear Structures](#non-linear-structures)
   - [Binary Trees](#binary-trees)
   - [Binary Search Trees (BST)](#binary-search-trees-bst)
   - [Heaps / Priority Queues](#heaps--priority-queues)
   - [Tries (Prefix Trees)](#tries-prefix-trees)
   - [Graphs](#graphs)
4. [Good-to-Know](#good-to-know)
   - [Monotonic Stack / Queue](#monotonic-stackqueue)
   - [Union-Find (Disjoint Set Union)](#union-find-disjoint-set-union)
5. [Complexity Cheatsheet](#complexity-cheatsheet)
6. [Pattern Recognition Guide](#pattern-recognition-guide)

---

## Mental Model

Before diving in, internalize this framework. Every data structure exists to answer a specific **access pattern question**:

| Question | Data Structure |
|---|---|
| "What came in most recently?" | Stack |
| "What came in first / oldest?" | Queue |
| "What is the current min/max?" | Heap |
| "Does this word start with...?" | Trie |
| "Which group does X belong to?" | Union-Find |
| "What are the neighbors of X?" | Graph |
| "Give me element at position N" | Array / Linked List |

When you see a problem, ask: **"What access pattern does this problem need?"** — that maps directly to the structure.

---

## Linear Structures

---

## Linked Lists

### What it is

A sequence of **nodes**, where each node holds a `value` and a `next` pointer (for singly linked) or both `next` and `prev` (for doubly linked). There is no contiguous memory — the list is scattered in the heap, stitched together by pointers.

```
Head
 ↓
[1 | next] → [2 | next] → [3 | next] → null
```

### Why interviewers love it

Linked list problems are almost entirely about **pointer manipulation under constraints**. Can you rearrange references without losing the chain? This tests whether you truly understand references vs. values — something that separates junior from senior engineers.

### Key Properties

| Property | Singly Linked | Doubly Linked |
|---|---|---|
| Access by index | O(n) | O(n) |
| Insert at head | O(1) | O(1) |
| Insert at tail | O(n) without tail ptr | O(1) with tail ptr |
| Delete a node (with ref) | O(1) | O(1) |
| Space per node | 1 pointer overhead | 2 pointer overhead |
| Traverse backward | ❌ | ✅ |

### The Node Structure

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### Core Techniques

#### 1. The Dummy Node Pattern
When your logic might need to touch the head node (like deleting it or inserting before it), always start with a sentinel dummy node. This eliminates null-check edge cases at the head.

```python
dummy = ListNode(0)
dummy.next = head
curr = dummy
# ... do operations ...
return dummy.next  # actual head may have changed
```

#### 2. Two Pointer / Fast-Slow Pointer (Floyd's Technique)
One pointer moves 1 step at a time, the other moves 2. This is the backbone of cycle detection and finding midpoints.

```python
slow, fast = head, head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# When fast reaches end, slow is at the middle
```

**Why it works for cycle detection:** If there is a cycle, fast will eventually "lap" slow and they will meet. If there is no cycle, fast reaches `None` first.

#### 3. Reversing a Linked List (In-Place)
The single most tested linked list operation. You need three pointers: `prev`, `curr`, `next_node`.

```python
def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next   # save before overwriting
        curr.next = prev        # reverse the pointer
        prev = curr             # advance prev
        curr = next_node        # advance curr
    return prev                 # prev is now the new head
```

**Trace through [1→2→3→null]:**
- Step 1: next=2, 1→null, prev=1, curr=2
- Step 2: next=3, 2→1, prev=2, curr=3
- Step 3: next=null, 3→2, prev=3, curr=null
- Return prev=3 → `[3→2→1→null]` ✅

### Problem Walkthroughs

#### Detect Cycle
```python
def hasCycle(head):
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

#### Merge Two Sorted Lists
Use a dummy node and always pick the smaller value. This is like the merge step in merge sort.

```python
def mergeTwoLists(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 if l1 else l2  # attach remainder
    return dummy.next
```

#### LRU Cache
This is the "boss" linked list problem. Uses a **doubly linked list + hashmap** combo. The list maintains access order (most recent at tail), the hashmap gives O(1) lookup.

```python
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}  # key -> node
        # Dummy head (LRU end) and tail (MRU end)
        self.head = ListNode(0)
        self.tail = ListNode(0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_tail(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        if key in self.cache:
            self._remove(self.cache[key])
            self._insert_at_tail(self.cache[key])
            return self.cache[key].val
        return -1

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = ListNode(value)
        node.key = key
        self.cache[key] = node
        self._insert_at_tail(node)
        if len(self.cache) > self.cap:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
```

### Common Mistakes

- **Losing the next pointer**: Always save `next_node = curr.next` before modifying `curr.next`
- **Off-by-one in fast/slow**: For finding the middle of an even-length list, decide whether you want the left or right middle and adjust your loop condition accordingly
- **Forgetting null checks**: `fast and fast.next` — always check both, because `fast.next` will throw if `fast` is null

---

## Stacks

### What it is

A **Last-In, First-Out (LIFO)** structure. Think of a stack of plates — you always add to the top and remove from the top.

```
push(3) → [1, 2, 3]  ← top
pop()   → returns 3, stack is [1, 2]
peek()  → returns 2, stack is [1, 2]
```

In Python, a regular list used with `.append()` and `.pop()` is a perfectly efficient stack (both O(1) amortized).

### Why interviewers love it

Stacks are the **"most recent state" machine**. Any time a problem involves tracking the last thing you saw, needing to go back to a previous state, or matching brackets/pairs — it's almost certainly a stack.

### The Core Mental Model

> **"I need to remember where I came from, so I can get back there."**

This is why stacks power: recursion (the call stack is literally a stack), undo functionality, expression evaluation, DFS, and parenthesis matching.

### Key Properties

| Operation | Time Complexity |
|---|---|
| Push | O(1) |
| Pop | O(1) |
| Peek (top) | O(1) |
| Search | O(n) |
| Space | O(n) |

### Problem Walkthroughs

#### Valid Parentheses
The canonical stack problem. Push open brackets onto the stack. When you see a close bracket, pop and verify it matches.

```python
def isValid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:             # it's a closing bracket
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)          # it's an opening bracket
    return not stack                    # stack must be empty at end
```

**Key insight**: The most recently seen open bracket must match the current close bracket. This is literally LIFO in action.

#### Daily Temperatures
"How many days until a warmer temperature?" — this is the **next greater element** pattern.

```python
def dailyTemperatures(temps):
    n = len(temps)
    result = [0] * n
    stack = []  # stores indices of unresolved days
    
    for i, temp in enumerate(temps):
        while stack and temps[stack[-1]] < temp:
            idx = stack.pop()
            result[idx] = i - idx   # days waited = distance
        stack.append(i)
    
    return result
```

**Why stack?** You push a day's index, waiting for a warmer day to come. When a warmer day arrives, you resolve all waiting days that are colder (inner while loop). The stack always maintains a **decreasing sequence of temperatures** from bottom to top (this is actually a Monotonic Stack — covered in Good-to-Know section).

#### Min Stack
Design a stack that returns the minimum in O(1). The trick: maintain a **parallel stack** that tracks the current minimum at each push level.

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []   # parallel min stack

    def push(self, val):
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]
```

**Key insight**: The min_stack stores "what is the minimum of everything currently in the main stack?" at every level. When you pop from main, pop from min_stack too — they stay in sync.

#### Evaluate Reverse Polish Notation
Process operands by pushing onto stack. When you hit an operator, pop two operands, compute, and push the result back.

```python
def evalRPN(tokens):
    stack = []
    ops = {'+', '-', '*', '/'}
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()  # b is top, a is below
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(int(a / b))  # truncate toward zero
        else:
            stack.append(int(token))
    return stack[0]
```

---

## Queues & Deques

### What it is

**Queue**: First-In, First-Out (FIFO). Like a real queue at a coffee shop — first person in line gets served first.

**Deque (Double-Ended Queue)**: Supports insert and delete from both ends in O(1). The most flexible linear structure.

```
Queue:  enqueue(3) → [1, 2, 3]   dequeue() → 1, queue is [2, 3]
Deque:  appendleft(0) → [0, 1, 2, 3]   pop() → 3, deque is [0, 1, 2]
```

In Python, always use `collections.deque` — regular lists have O(n) for `pop(0)`, but deque is O(1) for both ends.

```python
from collections import deque
q = deque()
q.append(1)       # enqueue right
q.appendleft(0)   # enqueue left
q.pop()           # dequeue right
q.popleft()       # dequeue left (standard queue behavior)
```

### Why interviewers love it

Queues power **BFS (Breadth-First Search)**, which is the primary tool for shortest path on unweighted graphs and level-order tree traversal. Deques are essential for **sliding window maximum** — one of the most elegant interview tricks.

### Key Properties

| Operation | Queue (deque) | Deque |
|---|---|---|
| Enqueue / Append | O(1) | O(1) both ends |
| Dequeue / Popleft | O(1) | O(1) both ends |
| Peek | O(1) | O(1) both ends |
| Search | O(n) | O(n) |

### Problem Walkthroughs

#### Sliding Window Maximum
Given array `nums` and window size `k`, return the max in each window as it slides right. Naive: O(nk). Optimal with monotonic deque: O(n).

```python
from collections import deque

def maxSlidingWindow(nums, k):
    dq = deque()  # stores indices, front is always the max of current window
    result = []
    
    for i, num in enumerate(nums):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Maintain decreasing order — remove smaller elements from back
        while dq and nums[dq[-1]] < num:
            dq.pop()
        
        dq.append(i)
        
        # Window is full
        if i >= k - 1:
            result.append(nums[dq[0]])  # front is always the max
    
    return result
```

**Key insight**: The deque stores indices in decreasing order of their values. The front is always the current window's maximum. This works because any element smaller than the current element can never be the maximum of any future window (since the current element is newer and larger).

#### Implement Queue Using Two Stacks
Classic puzzle — use two stacks to simulate FIFO.

```python
class MyQueue:
    def __init__(self):
        self.in_stack = []   # for push
        self.out_stack = []  # for pop/peek

    def push(self, x):
        self.in_stack.append(x)

    def _transfer(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def pop(self):
        self._transfer()
        return self.out_stack.pop()

    def peek(self):
        self._transfer()
        return self.out_stack[-1]

    def empty(self):
        return not self.in_stack and not self.out_stack
```

**Key insight**: Transfer only when `out_stack` is empty. Elements in `out_stack` are in reversed order (which is FIFO order). Amortized O(1) per operation.

#### Rotting Oranges (Multi-source BFS)
Grid problem — all rotten oranges spread simultaneously. This screams **BFS from multiple sources at once**.

```python
from collections import deque

def orangesRotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c, 0))   # (row, col, minutes)
            elif grid[r][c] == 1:
                fresh += 1
    
    minutes = 0
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    
    while q:
        r, c, mins = q.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                minutes = max(minutes, mins + 1)
                q.append((nr, nc, mins + 1))
    
    return minutes if fresh == 0 else -1
```

---

## Non-Linear Structures

---

## Binary Trees

### What it is

A **hierarchical structure** where each node has at most two children: a `left` child and a `right` child.

```
        1          ← Root
       / \
      2   3        ← Internal nodes
     / \
    4   5          ← Leaf nodes
```

Binary trees are the **most common interview topic** after arrays. They appear directly as problems and indirectly as the foundation for BSTs, heaps, tries, and segment trees.

### Node Structure

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Key Terminology

| Term | Meaning |
|---|---|
| Root | Top-most node, no parent |
| Leaf | Node with no children |
| Height | Longest path from root to leaf |
| Depth | Distance from root to a specific node |
| Balanced | Height difference between subtrees ≤ 1 |
| Complete | All levels filled except last, last filled left to right |
| Full | Every node has 0 or 2 children |
| Perfect | Full + all leaves at same level |

### The Four Traversals

These are the foundation of almost every tree problem. Memorize them cold.

```python
# Preorder: Root → Left → Right (useful for copying, serializing)
def preorder(root):
    if not root: return
    print(root.val)
    preorder(root.left)
    preorder(root.right)

# Inorder: Left → Root → Right (gives sorted order for BST!)
def inorder(root):
    if not root: return
    inorder(root.left)
    print(root.val)
    inorder(root.right)

# Postorder: Left → Right → Root (useful for deletion, computing subtree values)
def postorder(root):
    if not root: return
    postorder(root.left)
    postorder(root.right)
    print(root.val)

# Level-order (BFS): Level by level, left to right
from collections import deque
def levelorder(root):
    if not root: return []
    q, result = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):      # process exactly one level
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        result.append(level)
    return result
```

### The Recursive Pattern

Almost every tree problem follows this exact template:

```python
def solve(node):
    # Base case: empty node
    if not node:
        return <base_value>
    
    # Recurse on children
    left_result = solve(node.left)
    right_result = solve(node.right)
    
    # Combine results for current node
    return <combine(left_result, right_result, node.val)>
```

Your entire job is filling in what `<base_value>` and `<combine>` are.

### Problem Walkthroughs

#### Maximum Depth
```python
def maxDepth(root):
    if not root:
        return 0                                   # base: empty node has depth 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

#### Lowest Common Ancestor (LCA)
Given two nodes `p` and `q`, find their LCA. The LCA is the deepest node that has both `p` and `q` as descendants.

```python
def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root       # found one of them (or hit null)
    
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    
    if left and right:
        return root       # p and q are in different subtrees → current is LCA
    return left or right  # one subtree has both
```

**The logic**: If you find `p` on the left and `q` on the right (or vice versa), the current node is the LCA. If both are on the same side, return the non-null result (which itself already holds the answer from a deeper call).

#### Serialize / Deserialize Binary Tree
Encode a tree to string, decode back to identical tree. Use preorder with null markers.

```python
class Codec:
    def serialize(self, root):
        if not root:
            return "null,"
        return str(root.val) + "," + self.serialize(root.left) + self.serialize(root.right)

    def deserialize(self, data):
        vals = iter(data.split(","))
        
        def build():
            val = next(vals)
            if val == "null":
                return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
        
        return build()
```

---

## Binary Search Trees (BST)

### What it is

A binary tree with one additional invariant: **for every node, all values in its left subtree are less than it, and all values in its right subtree are greater than it.**

```
        5
       / \
      3   8
     / \   \
    1   4   9
```

This ordering property is what gives BST its power: you can search in O(log n) by going left (smaller) or right (larger) at each node.

### Key Properties

| Operation | Average (Balanced) | Worst (Skewed) |
|---|---|---|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Inorder traversal | O(n) | O(n) |

**Critical insight**: Inorder traversal of a BST yields elements in **sorted ascending order**. This is used constantly.

### Problem Walkthroughs

#### Validate BST
A node is valid only if it is within a range `(min, max)`. Pass these bounds down recursively.

```python
def isValidBST(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True
    if not (min_val < root.val < max_val):
        return False
    return (isValidBST(root.left, min_val, root.val) and
            isValidBST(root.right, root.val, max_val))
```

**Common mistake**: Checking only against immediate parent is wrong. A node in the right subtree must be greater than ALL ancestors on its left-side path, not just its direct parent.

#### Kth Smallest Element
Inorder traversal visits BST nodes in sorted order. Stop at the kth node.

```python
def kthSmallest(root, k):
    stack = []
    curr = root
    count = 0
    
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left       # go as far left as possible
        curr = stack.pop()
        count += 1
        if count == k:
            return curr.val
        curr = curr.right
```

---

## Heaps / Priority Queues

### What it is

A **complete binary tree** maintained with the heap property:
- **Min-heap**: Parent is always ≤ its children. The root is the minimum.
- **Max-heap**: Parent is always ≥ its children. The root is the maximum.

Internally stored as an array (not a tree object), where for node at index `i`:
- Left child: `2i + 1`
- Right child: `2i + 2`
- Parent: `(i - 1) // 2`

```
Min-heap:       1
               / \
              3   2
             / \
            5   4
Array: [1, 3, 2, 5, 4]
```

In Python, `heapq` is a **min-heap** by default. For max-heap, negate values.

```python
import heapq

heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
heapq.heappop(heap)      # returns 1 (minimum)

# Max-heap trick: negate values
heapq.heappush(heap, -val)
max_val = -heapq.heappop(heap)

# Build heap from list in O(n)
nums = [3, 1, 4, 1, 5]
heapq.heapify(nums)
```

### Key Properties

| Operation | Time |
|---|---|
| Get min/max (peek) | O(1) |
| Insert | O(log n) |
| Remove min/max | O(log n) |
| Build from array | O(n) |
| Search | O(n) |

### Problem Walkthroughs

#### Top K Frequent Elements
Count frequencies, then use a heap of size k.

```python
from collections import Counter
import heapq

def topKFrequent(nums, k):
    count = Counter(nums)
    # Min-heap of size k: if we see a more frequent element, pop the least frequent
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)   # remove least frequent
    return [num for freq, num in heap]
```

**Why min-heap for "top K largest"?** Counterintuitive but elegant: keep a min-heap of size k. The minimum in the heap is the k-th largest overall. Anything larger displaces it.

#### Merge K Sorted Lists
Use a heap to always extract the globally smallest current element across all lists.

```python
import heapq

def mergeKLists(lists):
    heap = []
    dummy = ListNode(0)
    curr = dummy
    
    # Push the head of each list
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next
```

#### Find Median from Data Stream
Maintain two heaps: a max-heap for the lower half, a min-heap for the upper half. Balance them so their sizes differ by at most 1.

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []   # max-heap (negate values) — lower half
        self.hi = []   # min-heap — upper half

    def addNum(self, num):
        heapq.heappush(self.lo, -num)         # push to lower half
        # Balance: top of lo must be ≤ top of hi
        if self.hi and (-self.lo[0]) > self.hi[0]:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # Size balance: lo can have at most 1 more than hi
        if len(self.lo) > len(self.hi) + 1:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        elif len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
```

---

## Tries (Prefix Trees)

### What it is

A tree where each node represents a character, and paths from root to nodes represent prefixes of stored words. Not stored as key-value pairs — the structure itself encodes the keys.

```
Words: ["cat", "car", "card", "care", "bat"]

        root
       /    \
      c      b
      |      |
      a      a
     / \     |
    t   r    t
        |
        d, e
```

### Why interviewers love it

Tries are the **correct** solution for any problem involving string prefix operations, autocomplete, or word search in a grid. They're one of the few structures where using anything else is objectively worse.

### Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}        # char → TrieNode
        self.is_end = False       # marks a complete word

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end   # must end at a complete word marker

    def startsWith(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True           # any node found is a valid prefix
```

### Key Properties

| Operation | Time |
|---|---|
| Insert | O(L) where L = word length |
| Search | O(L) |
| Prefix search (startsWith) | O(L) |
| Space | O(ALPHABET_SIZE × N × L) |

### When to Use a Trie

- Autocomplete / search suggestions
- Spell checking
- IP routing (longest prefix match)
- Word search in a grid (Word Search II uses Trie + DFS)
- Dictionary lookups with prefix queries

---

## Graphs

### What it is

A collection of **nodes (vertices)** connected by **edges**. The most general data structure — almost anything can be modeled as a graph.

```
Undirected Graph:      Directed Graph (DAG):
   A — B                  A → B
   |   |                  ↓   ↓
   C — D                  C → D
```

### Representations

```python
# Adjacency List (most common for interview problems)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']
}

# Adjacency Matrix (when you need O(1) edge lookup)
# matrix[i][j] = 1 means edge from i to j
matrix = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
]

# Implicit graph (grid problems — no explicit graph needed)
# Each cell (r, c) connects to (r±1, c) and (r, c±1)
```

### Graph Traversals

#### DFS (Depth-First Search) — Go Deep, Backtrack
```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

# Iterative DFS (using stack)
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
```

#### BFS (Breadth-First Search) — Level by Level
```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    q = deque([start])
    while q:
        node = q.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
```

**DFS vs BFS — when to use which:**

| Use DFS when... | Use BFS when... |
|---|---|
| Exploring all paths | Finding shortest path (unweighted) |
| Detecting cycles | Level-order processing |
| Topological sort | Multi-source spreading (e.g., rotting oranges) |
| Connected components | Nearest/closest node problems |

### Problem Walkthroughs

#### Number of Islands
Classic DFS/BFS on a grid. Each `'1'` you find, DFS to mark the entire island as visited.

```python
def numIslands(grid):
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'   # mark visited (in-place)
        dfs(r+1, c); dfs(r-1, c)
        dfs(r, c+1); dfs(r, c-1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count
```

#### Course Schedule (Cycle Detection in Directed Graph)
Can you complete all courses given prerequisites? This is asking: **is the graph a DAG (no cycles)?**

```python
def canFinish(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    # 0=unvisited, 1=visiting(in current path), 2=visited(safe)
    state = [0] * numCourses
    
    def has_cycle(node):
        if state[node] == 1: return True   # back edge = cycle
        if state[node] == 2: return False  # already safe
        state[node] = 1
        for neighbor in graph[node]:
            if has_cycle(neighbor):
                return True
        state[node] = 2
        return False
    
    for i in range(numCourses):
        if has_cycle(i):
            return False
    return True
```

#### Shortest Path (BFS — unweighted)
BFS naturally finds the shortest path because it explores level by level.

```python
from collections import deque

def shortestPath(graph, start, end):
    visited = {start}
    q = deque([(start, 0)])   # (node, distance)
    
    while q:
        node, dist = q.popleft()
        if node == end:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append((neighbor, dist + 1))
    
    return -1   # no path found
```

---

## Good-to-Know

---

## Monotonic Stack/Queue

### What it is

A stack (or deque) that is maintained in either **strictly increasing** or **strictly decreasing** order by removing violating elements before inserting. Not a separate data structure — it's a technique applied to a regular stack/deque.

### The Insight

When you push a new element and pop all smaller elements before it, those popped elements have found their **"next greater element"** (which is the current element being pushed). This makes it O(n) instead of O(n²) for a class of problems.

### Template

```python
stack = []  # stores indices
for i, num in enumerate(nums):
    # Maintain DECREASING order (pop smaller elements)
    while stack and nums[stack[-1]] < num:
        idx = stack.pop()
        # nums[idx]'s next greater element is num (at index i)
        answer[idx] = i
    stack.append(i)
```

### Key Problems

**Next Greater Element:**
```python
def nextGreaterElement(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result
```

**Largest Rectangle in Histogram:**
For each bar, find the first shorter bar to the left and right. That defines the maximum rectangle using this bar as the height.

```python
def largestRectangleArea(heights):
    stack = []   # stores indices of increasing heights
    max_area = 0
    heights.append(0)   # sentinel to flush the stack at end
    
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    
    return max_area
```

---

## Union-Find (Disjoint Set Union)

### What it is

A data structure that efficiently tracks which elements belong to the same **group (component)**. Supports two operations:
- `find(x)`: Which group does `x` belong to? (returns a representative/root)
- `union(x, y)`: Merge the groups of `x` and `y`

With **path compression** + **union by rank**, both operations become nearly O(1) amortized (technically O(α(n)) — the inverse Ackermann function, which is ≤ 4 for any practical input size).

### Implementation

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))   # each element is its own parent
        self.rank = [0] * n            # tree height estimate

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False   # already in same set
        # Union by rank: attach smaller tree under larger
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

### Problem Walkthroughs

#### Number of Connected Components
```python
def countComponents(n, edges):
    uf = UnionFind(n)
    components = n           # start with n isolated components
    for u, v in edges:
        if uf.union(u, v):
            components -= 1  # two components merged into one
    return components
```

#### Redundant Connection
Find the edge that creates the first cycle in an undirected graph.

```python
def findRedundantConnection(edges):
    uf = UnionFind(len(edges) + 1)
    for u, v in edges:
        if not uf.union(u, v):   # already connected → this edge is redundant
            return [u, v]
```

**When to prefer Union-Find over DFS for connectivity:**
- When you're processing edges one at a time and need dynamic updates
- When you need to check connectivity repeatedly
- When you don't need the actual path, just membership in the same component

---

## Complexity Cheatsheet

| Structure | Access | Search | Insert | Delete | Space |
|---|---|---|---|---|---|
| Linked List | O(n) | O(n) | O(1) at head | O(1) with ref | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Binary Tree | O(n) | O(n) | O(n) | O(n) | O(n) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Heap | O(1) min/max | O(n) | O(log n) | O(log n) | O(n) |
| Trie | — | O(L) | O(L) | O(L) | O(N×L×A) |
| Graph (adj list) | O(V+E) | O(V+E) | O(1) | O(V+E) | O(V+E) |
| Union-Find | — | O(α(n)) | O(α(n)) | — | O(n) |

`L` = string length, `A` = alphabet size, `V` = vertices, `E` = edges, `α` = inverse Ackermann

---

## Pattern Recognition Guide

When you see this in a problem → reach for this structure:

| Problem Signal | Structure / Technique |
|---|---|
| "K most frequent / largest / smallest" | Heap (size K) |
| "Shortest path" (unweighted) | BFS |
| "All paths / exists a path" | DFS |
| "Cycle detection" | DFS with color states OR Union-Find |
| "Group / connected components" | Union-Find or BFS/DFS |
| "Prefix / autocomplete / dictionary" | Trie |
| "Most recently seen" / "undo" | Stack |
| "Next greater/smaller element" | Monotonic Stack |
| "Sliding window max/min" | Monotonic Deque |
| "Level-order / by layer" | BFS + Queue |
| "Matching brackets / pairs" | Stack |
| "Sorted tree property" | BST + Inorder traversal |
| "Running median" | Two Heaps |
| "Ordered processing" | Queue |
| "LRU / access order" | Doubly Linked List + HashMap |
| "Dependency ordering" | Topological Sort (BFS/DFS on DAG) |
