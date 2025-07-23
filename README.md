# Mark_newick.py

**Mark_newick.py** is a Python script to mark nodes in a **Newick-format phylogenetic tree** based on a given label. It identifies the **Most Recent Common Ancestor (MRCA)** of matching leaves, marks it and all descendants, and outputs a new Newick file with those marks.

---

## 📦 Features

- Load and parse a Newick tree.
- Search for leaves containing a specific label.
- Identify the MRCA of matching leaves.
- Mark MRCA and descendants by appending `#1` to labels.
- Export the marked tree.

---

## ✅ Requirements

- Python 3.x
- Dependencies:
  - [`ete3`](http://etetoolkit.org/)
  - `numpy`
  - `scipy` (✅ Version **>=1.23.5** and **<2.3.0**)

> ⚠️ If you see:
> ```
> UserWarning: A NumPy version >=1.23.5 and <2.3.0 is required for this version of SciPy
> ```
> Ensure you're using the correct SciPy version.

---

## 🔧 Installation

```pip install ete3 numpy scipy==1.11.4```

## 🚀 Usage

```python3 Mark_newick.py -i <input_tree> -l <label> -o <output_tree>```

## 📌 Arguments

| Argument | Description                         |
|----------|-------------------------------------|
| -i     | Path to the input Newick tree file. |
| -l     | Label (substring) to search for.    |
| -o     | Path to the output Newick file.     |
| -m     | If midpoint rooting needed.         |

## ✅ Example Command

```python3 Mark_newick.py \
    -i Tree.nwk \
    -l red \
    -o Tree_marked.nwk \
    -m
```

---

## 📥 Example Output

```

Loading tree from: /path/to/Tree.nwk

Tree structure:
... (prints full tree structure)

Searching for leaves containing label: 'red'
Found 3 leaves containing 'red'. Finding MRCA...
Collecting all node IDs under the MRCA (including the MRCA itself)...

-------------------------------------------------------------------------
.  Adding node marks (will append '#1' to node names)
-------------------------------------------------------------------------
Nodes marked: [36, 29, 30, 31]

Writing marked tree to: /path/to/Tree_marked.nwk
Process complete.
```

---

## 📤 Output

- The script saves a **Newick file** where:
  - The MRCA and all descendant nodes of the label provided are marked by appending \`#1\`.
  - The structure of the tree remains unchanged aside from these markings and removing of boostraps.


## Use output for HyPhy dN/dS analysis : 
```
Eg usage :
- hyphy relax --alignment your_file.ali --tree Tree_marked.nwk --test test
- hyphy busted --alignment your_file.al --tree Tree_marked.nw --branches test 
```
---
