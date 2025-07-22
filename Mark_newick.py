import argparse
import os
import pandas as pd
from ete3 import EvolTree

def main():
    parser = argparse.ArgumentParser(description='Mark nodes on a phylogenetic tree by label search and save the modified tree.')
    parser.add_argument('-i', '--input_tree', required=True, help='Input tree file in Newick format')
    parser.add_argument('-l', '--label', required=True, help='Label substring to search within leaf names')
    parser.add_argument('-o', '--output_tree', required=True, help='Output file for the marked tree in Newick format')
    # Example usage:
    # python3 Mark_newick.py -i input_tree.nwk -l artic -o output_tree_marked.nwk
    
    args = parser.parse_args()

    print(f"\nLoading tree from: {args.input_tree}")
    tree = EvolTree(args.input_tree)

    print("\nTree structure:")
    print(tree)
    print("\n")

    print(f"Searching for leaves containing label: '{args.label}'")
    target_leaves = [leaf for leaf in tree if args.label in leaf.name]
    
    if not target_leaves:
        print(f"No leaves found with label '{args.label}'. Exiting.")
        return
    
    print(f"\nFound {len(target_leaves)} leaves containing '{args.label}'. Finding MRCA...")
    mrca_node = tree.get_common_ancestor(target_leaves)

    print("\nCollecting all node IDs under the MRCA (including the MRCA itself)...")
    df_marks = pd.DataFrame(columns=['Node_name', 'Node_id'])

    for node in mrca_node.traverse("levelorder"):
        new_row = pd.DataFrame({"Node_name": [node.name], "Node_id": [node.node_id]})
        df_marks = pd.concat([df_marks, new_row], ignore_index=True)

    # No slicing here — include the MRCA node itself
    marks = list(df_marks['Node_id'].astype(int))

    print("\n-------------------------------------------------------------------------")
    print(".  Adding node marks (will append '#1' to node names)                   ")
    print("-------------------------------------------------------------------------")
    
    # Apply marks visually to node names
    for node in tree.traverse():
        if node.node_id in marks:
            node.name = f"{node.name} #1" if node.name else "#1"

    print(f"Nodes marked: {marks}")
    print("\nMarked tree (Newick with marks):")
    print(tree.write(format=1))  # Includes branch lengths if available
    print("\n")

    print(f"Writing marked tree to: {args.output_tree}")
    with open(args.output_tree, 'w') as outfile:
        outfile.write(tree.write(format=1))

    print("Process complete.")

if __name__ == "__main__":
    main()
