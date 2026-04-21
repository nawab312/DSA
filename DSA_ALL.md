# FAANG DevOps/SRE LeetCode Prep — 6-Month Roadmap

> **Target**: FAANG DevOps / SRE roles  
> **Duration**: 6 months (~180 days)  
> **Total problems**: ~200  
> **Daily target**: 1–2 problems/day  

---

## Why DSA matters for DevOps/SRE at FAANG

FAANG SRE/DevOps interviews include the same coding rounds as SWE — you will be asked to solve LeetCode-style problems on a whiteboard or live editor. Additionally, expect system design questions focused on reliability, scalability, and distributed systems.

---

## Difficulty Legend

- 🟢 Easy
- 🟡 Medium
- 🔴 Hard

---

## Phase 1 — Foundations (Month 1)
*Arrays, Hashing, Strings, Two Pointers, Sliding Window*

> These cover ~40% of interview questions. Master these before moving on.

### Arrays & Hashing

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 1 | Two Sum | 🟢 Easy | Hash map lookups — log parsing |
| 217 | Contains Duplicate | 🟢 Easy | Deduplication in pipelines |
| 242 | Valid Anagram | 🟢 Easy | String comparison fundamentals |
| 347 | Top K Frequent Elements | 🟡 Medium | Top-N metrics, alert aggregation |
| 238 | Product of Array Except Self | 🟡 Medium | Array manipulation |
| 49 | Group Anagrams | 🟡 Medium | Grouping/bucketing log events |
| 128 | Longest Consecutive Sequence | 🟡 Medium | Time-series gap detection |
| 36 | Valid Sudoku | 🟡 Medium | Constraint validation |

### Two Pointers

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 125 | Valid Palindrome | 🟢 Easy | String validation |
| 167 | Two Sum II | 🟢 Easy | Sorted data scanning |
| 15 | 3Sum | 🟡 Medium | Multi-condition matching |
| 11 | Container With Most Water | 🟡 Medium | Resource optimization thinking |
| 42 | Trapping Rain Water | 🔴 Hard | Capacity planning metaphor |

### Sliding Window

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 121 | Best Time to Buy and Sell Stock | 🟢 Easy | Time-window analysis |
| 3 | Longest Substring Without Repeating Chars | 🟡 Medium | Stream deduplication |
| 424 | Longest Repeating Character Replacement | 🟡 Medium | Rolling window metrics |
| 567 | Permutation in String | 🟡 Medium | Pattern matching in logs |
| 76 | Minimum Window Substring | 🔴 Hard | Log pattern search |
| 239 | Sliding Window Maximum | 🔴 Hard | Moving average for monitoring |

### Strings

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 20 | Valid Parentheses | 🟢 Easy | Config/YAML/JSON validation |
| 271 | Encode and Decode Strings | 🟡 Medium | Serialization (CI/CD artifacts) |
| 5 | Longest Palindromic Substring | 🟡 Medium | Pattern recognition |
| 438 | Find All Anagrams in a String | 🟡 Medium | Log keyword matching |

---

## Phase 2 — Core Data Structures (Month 2)
*Linked Lists, Stacks, Queues, Binary Search*

> Foundational for understanding OS internals, schedulers, and queuing systems.

### Linked Lists

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 206 | Reverse Linked List | 🟢 Easy | Pointer fundamentals |
| 21 | Merge Two Sorted Lists | 🟢 Easy | Merging sorted log streams |
| 141 | Linked List Cycle | 🟢 Easy | Deadlock/cycle detection |
| 143 | Reorder List | 🟡 Medium | List manipulation |
| 19 | Remove Nth Node From End | 🟡 Medium | Sliding references |
| 142 | Linked List Cycle II | 🟡 Medium | Find entry point of cycle |
| 23 | Merge K Sorted Lists | 🔴 Hard | Merging K log streams (very common) |

### Stack & Queue

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 155 | Min Stack | 🟢 Easy | O(1) min-tracking for metrics |
| 150 | Evaluate Reverse Polish Notation | 🟡 Medium | Expression parsing |
| 22 | Generate Parentheses | 🟡 Medium | Recursive config generation |
| 739 | Daily Temperatures | 🟡 Medium | Next-event detection |
| 853 | Car Fleet | 🟡 Medium | Rate-limiting queues |
| 84 | Largest Rectangle in Histogram | 🔴 Hard | Resource utilization peaks |

### Binary Search

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 704 | Binary Search | 🟢 Easy | Efficient log lookup |
| 74 | Search a 2D Matrix | 🟡 Medium | Multi-dimensional indexing |
| 875 | Koko Eating Bananas | 🟡 Medium | Rate/threshold optimization |
| 153 | Find Minimum in Rotated Sorted Array | 🟡 Medium | Shifted data detection |
| 33 | Search in Rotated Sorted Array | 🟡 Medium | Searching in partitioned datasets |
| 981 | Time Based Key-Value Store | 🟡 Medium | Versioned config stores |
| 4 | Median of Two Sorted Arrays | 🔴 Hard | Percentile latency calculation |

---

## Phase 3 — Trees & Graphs (Month 3)
*Binary Trees, BSTs, Tries, Graph BFS/DFS*

> Critical for network topology, dependency graphs, and service meshes.

### Binary Trees

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 226 | Invert Binary Tree | 🟢 Easy | Tree transformation |
| 104 | Maximum Depth of Binary Tree | 🟢 Easy | Hierarchy depth |
| 543 | Diameter of Binary Tree | 🟢 Easy | Network path length |
| 110 | Balanced Binary Tree | 🟢 Easy | Load balance checks |
| 100 | Same Tree | 🟢 Easy | Config diff checking |
| 572 | Subtree of Another Tree | 🟢 Easy | Config subset matching |
| 235 | Lowest Common Ancestor of BST | 🟡 Medium | Dependency resolution |
| 102 | Binary Tree Level Order Traversal | 🟡 Medium | BFS — network layer traversal |
| 199 | Binary Tree Right Side View | 🟡 Medium | Tree visibility |
| 1448 | Count Good Nodes in Binary Tree | 🟡 Medium | Threshold-based filtering |
| 98 | Validate Binary Search Tree | 🟡 Medium | Data structure integrity checks |
| 230 | Kth Smallest Element in BST | 🟡 Medium | Rank-based queries |
| 105 | Construct Tree from Preorder+Inorder | 🟡 Medium | Rebuilding from serialized data |
| 124 | Binary Tree Maximum Path Sum | 🔴 Hard | Longest path — network routing |
| 297 | Serialize and Deserialize Binary Tree | 🔴 Hard | State serialization (etcd, Consul) |

### Tries

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 208 | Implement Trie | 🟡 Medium | Prefix-based routing (API gateway) |
| 211 | Design Add and Search Words | 🟡 Medium | Wildcard log searching |
| 212 | Word Search II | 🔴 Hard | Multi-pattern log scanning |

### Graphs

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 200 | Number of Islands | 🟡 Medium | Network segment detection |
| 133 | Clone Graph | 🟡 Medium | Infrastructure cloning/IaC |
| 695 | Max Area of Island | 🟡 Medium | Largest subnet/cluster detection |
| 417 | Pacific Atlantic Water Flow | 🟡 Medium | Multi-direction graph traversal |
| 130 | Surrounded Regions | 🟡 Medium | Boundary-aware flood fill |
| 994 | Rotting Oranges | 🟡 Medium | BFS propagation — failure blast radius |
| 207 | Course Schedule | 🟡 Medium | Topological sort — deploy ordering |
| 210 | Course Schedule II | 🟡 Medium | Dependency-ordered deployment |
| 684 | Redundant Connection | 🟡 Medium | Cycle detection in service graph |
| 323 | Number of Connected Components | 🟡 Medium | Service cluster isolation |
| 1091 | Shortest Path in Binary Matrix | 🟡 Medium | Network shortest path |
| 127 | Word Ladder | 🔴 Hard | BFS state transitions |
| 269 | Alien Dictionary | 🔴 Hard | Topological ordering from rules |

---

## Phase 4 — Advanced Algorithms (Month 4)
*Backtracking, Heap/Priority Queue, Intervals*

### Backtracking

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 78 | Subsets | 🟡 Medium | Feature flag combinations |
| 39 | Combination Sum | 🟡 Medium | Config combination search |
| 40 | Combination Sum II | 🟡 Medium | Unique config generation |
| 46 | Permutations | 🟡 Medium | Deployment order permutations |
| 90 | Subsets II | 🟡 Medium | Deduplicated combinations |
| 79 | Word Search | 🟡 Medium | Grid-based path search |
| 131 | Palindrome Partitioning | 🟡 Medium | String segmentation |
| 51 | N-Queens | 🔴 Hard | Constraint satisfaction |

### Heap / Priority Queue

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 703 | Kth Largest Element in Stream | 🟢 Easy | Real-time top-K metrics |
| 1046 | Last Stone Weight | 🟢 Easy | Priority-based processing |
| 973 | K Closest Points to Origin | 🟡 Medium | Nearest-node queries |
| 215 | Kth Largest Element in Array | 🟡 Medium | Percentile computation |
| 621 | Task Scheduler | 🟡 Medium | Job scheduling with cooldowns |
| 355 | Design Twitter | 🟡 Medium | Feed/stream merging |
| 295 | Find Median from Data Stream | 🔴 Hard | Live latency percentiles |
| 23 | Merge K Sorted Lists | 🔴 Hard | Multi-source log aggregation |

### Intervals

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 57 | Insert Interval | 🟡 Medium | Maintenance window merging |
| 56 | Merge Intervals | 🟡 Medium | Overlapping incident windows |
| 435 | Non-overlapping Intervals | 🟡 Medium | Scheduling without conflicts |
| 252 | Meeting Rooms | 🟢 Easy | Capacity planning |
| 253 | Meeting Rooms II | 🟡 Medium | Peak concurrent load |
| 1851 | Minimum Interval to Include Query | 🔴 Hard | Time-range queries on metrics |

---

## Phase 5 — Dynamic Programming (Month 5)
*1D DP, 2D DP, Advanced DP*

> DP tests problem decomposition — a key SRE skill for cost/performance optimization.

### 1D DP

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 70 | Climbing Stairs | 🟢 Easy | Fibonacci-style state transitions |
| 746 | Min Cost Climbing Stairs | 🟢 Easy | Cost minimization |
| 198 | House Robber | 🟡 Medium | Non-adjacent selection |
| 213 | House Robber II | 🟡 Medium | Circular constraint |
| 5 | Longest Palindromic Substring | 🟡 Medium | String DP |
| 647 | Palindromic Substrings | 🟡 Medium | Counting DP |
| 91 | Decode Ways | 🟡 Medium | State machine DP |
| 322 | Coin Change | 🟡 Medium | Minimum-cost resource allocation |
| 139 | Word Break | 🟡 Medium | Segmentation problems |
| 300 | Longest Increasing Subsequence | 🟡 Medium | Trend detection in metrics |
| 416 | Partition Equal Subset Sum | 🟡 Medium | Load partitioning |

### 2D DP

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 62 | Unique Paths | 🟡 Medium | Grid-based path counting |
| 1143 | Longest Common Subsequence | 🟡 Medium | Config diff / patch generation |
| 309 | Best Time to Buy and Sell with Cooldown | 🟡 Medium | State machine with cooldown |
| 518 | Coin Change II | 🟡 Medium | Combination counting |
| 494 | Target Sum | 🟡 Medium | Subset sum variants |
| 97 | Interleaving String | 🔴 Hard | Merge validation |
| 72 | Edit Distance | 🔴 Hard | Config diff (Levenshtein) |
| 312 | Burst Balloons | 🔴 Hard | Interval DP |
| 10 | Regular Expression Matching | 🔴 Hard | Regex engine fundamentals |

---

## Phase 6 — System Design-Aligned DSA (Month 6)
*Bit Manipulation, Math, Design Problems, Mock Interviews*

> These problems mirror real SRE system design scenarios.

### Bit Manipulation

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 136 | Single Number | 🟢 Easy | XOR-based deduplication |
| 191 | Number of 1 Bits | 🟢 Easy | Bitmask operations |
| 338 | Counting Bits | 🟢 Easy | Bit population in flags |
| 190 | Reverse Bits | 🟢 Easy | Bitwise ops in low-level SRE |
| 268 | Missing Number | 🟢 Easy | Integrity checks |
| 371 | Sum of Two Integers | 🟡 Medium | Bit arithmetic |
| 7 | Reverse Integer | 🟡 Medium | Integer manipulation |

### Math & Geometry

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 202 | Happy Number | 🟢 Easy | Cycle detection |
| 66 | Plus One | 🟢 Easy | Overflow handling |
| 50 | Pow(x, n) | 🟡 Medium | Fast exponentiation |
| 43 | Multiply Strings | 🟡 Medium | Big integer arithmetic |
| 2013 | Detect Squares | 🟡 Medium | Geometry + hashing |

### Design / OOP Problems *(Very common for SRE)*

| # | Problem | Difficulty | Why It Matters for SRE |
|---|---------|------------|------------------------|
| 146 | LRU Cache | 🟡 Medium | Cache eviction (Redis, CDN) |
| 460 | LFU Cache | 🔴 Hard | Frequency-based cache eviction |
| 295 | Find Median from Data Stream | 🔴 Hard | P50/P99 latency tracking |
| 355 | Design Twitter | 🟡 Medium | Feed aggregation system |
| 981 | Time Based Key-Value Store | 🟡 Medium | Versioned config / etcd |
| 1472 | Design Browser History | 🟡 Medium | Undo/redo in deploy history |
| 380 | Insert Delete GetRandom O(1) | 🟡 Medium | Randomized load balancing |
| 706 | Design HashMap | 🟢 Easy | Hash table internals |
| 232 | Implement Queue using Stacks | 🟢 Easy | Queue internals |
| 225 | Implement Stack using Queues | 🟢 Easy | Stack internals |

---

## SRE-Specific Focus Areas

### Problems directly relevant to SRE scenarios

| Scenario | LeetCode Problem | # |
|----------|-----------------|---|
| Log stream merging | Merge K Sorted Lists | 23 |
| Incident window merging | Merge Intervals | 56 |
| Deploy ordering (dependencies) | Course Schedule II | 210 |
| Cache design (Redis) | LRU Cache | 146 |
| Latency percentiles (P99) | Find Median from Data Stream | 295 |
| Rate limiting | Task Scheduler | 621 |
| Failure blast radius | Rotting Oranges | 994 |
| Network topology cycles | Redundant Connection | 684 |
| Config versioning (etcd) | Time Based Key-Value Store | 981 |
| Routing prefixes (API Gateway) | Implement Trie | 208 |
| Consensus / replication | Serialize & Deserialize Tree | 297 |
| On-call scheduling | Meeting Rooms II | 253 |

