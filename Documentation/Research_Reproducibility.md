# Research Reproducibility Blueprint & Protocol

**AIORI Hackathon 3 — Problem Statement PS-001 | Team: Cipher Aegis**

---

## 1. Benchmark Protocol & Seeds

    To ensure absolute scientific reproducibility across independent compute environments, the benchmark specifies:

    - **Master Random State:** <code>random_state = 42</code> (fixed across NumPy, Scikit-Learn, and Python random).

    - **Window Configuration:** Window duration = 30.0 seconds, sliding step = 10.0 seconds.

    - **Dataset Composition:** 240 scenarios (120 Benign: 40 normal, 45 document_editing, 35 photo_backup; 120 Suspicious: 31 modification_burst, 46 rename_burst, 43 gradual_activity).

    - **Scenario-Level Partitioning:**

      - Train Set: 167 scenarios, 2,672 rolling windows.

      - Validation Set: 37 scenarios, 592 rolling windows.

      - Unseen Test Set: 36 scenarios, 576 rolling windows (18 benign, 18 suspicious).

    - **Zero Data Leakage Guarantee:** Partitions are segregated strictly at the scenario level. Overlapping rolling windows from the same scenario are never divided across train and test sets.
    

## 2. Hyperparameters

    **RandomForestClassifier Hyperparameter Configuration:**

    - <code>n_estimators</code>: 200 trees

    - <code>criterion</code>: 'gini' impurity

    - <code>max_depth</code>: 12

    - <code>min_samples_split</code>: 2

    - <code>min_samples_leaf</code>: 2

    - <code>max_features</code>: 'sqrt'

    - <code>bootstrap</code>: True

    - <code>class_weight</code>: 'balanced'

    - <code>random_state</code>: 42

    - <code>n_jobs</code>: -1
    

## 3. Gini Feature Importance Rankings

| Rank | Feature Name | Relative Importance | Physical Security Significance |
|---|---|---|---|
| 1 | rename_ratio | 0.3779 (37.79%) | Strongest discriminator for extension appending (.locked, .crypto) |
| 2 | rename_count | 0.2660 (26.60%) | Absolute volume of file rename events in 30s window |
| 3 | total_ops | 0.0843 (8.43%) | Gross operation velocity indicator |
| 4 | ops_per_second | 0.0772 (7.72%) | Normalized operational throughput rate |
| 5 | write_count | 0.0576 (5.76%) | New file creation rate (differentiates photo backup) |
| 6 | modify_count | 0.0458 (4.58%) | In-place overwrite frequency |
| 7 | unique_files | 0.0368 (3.68%) | Filesystem breadth and target spread |
| 8 | modify_ratio | 0.0300 (3.00%) | Proportion of window dedicated to overwriting |
| 9 | delete_count | 0.0149 (1.49%) | Batch file deletion / wiper actions |
| 10 | delete_ratio | 0.0094 (0.94%) | Proportion of operations dedicated to deletion |
