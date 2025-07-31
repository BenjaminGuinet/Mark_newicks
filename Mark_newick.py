import argparse
import os
import pandas as pd
from ete3 import EvolTree
import re

def modify_newick_format(newick_string):
    # Remove bootstrap support values from the Newick string
    modified_newick = re.sub(r'\d+\/\d+', '', newick_string)
    return modified_newick

def main():
    parser = argparse.ArgumentParser(description='Mark nodes on a phylogenetic tree by label search and save the modified tree.')
    parser.add_argument('-i', '--input_tree', required=True, help='Input tree file in Newick format')
    parser.add_argument('-l', '--label', required=True, help='Label substring to search within leaf names')
    parser.add_argument('-o', '--output_tree', required=True, help='Output file for the marked tree in Newick format')
    parser.add_argument('-m', '--midpoint_root', action='store_true', help='Midpoint root the tree before marking')

    args = parser.parse_args()

    # Read the original Newick string from the input file
    with open(args.input_tree, 'r') as f:
        newick_string = f.read().strip()

    try:
        print(f"\nLoading tree from: {args.input_tree}")
        tree = EvolTree(args.input_tree)
    except:
        print("\nBootstrap support format was not handled by EvolTree. Creating a new tree file without bootstrap support values...")
        modified_newick = modify_newick_format(newick_string)

        # Save the modified Newick string to a temporary file
        temp_tree_file = "temp_tree.nwk"
        with open(temp_tree_file, 'w') as f:
            f.write(modified_newick)

        # Load the tree from the temporary file
        tree = EvolTree(temp_tree_file)

        # Remove the temporary file
        os.remove(temp_tree_file)
        print(f"\nTemporary tree file {temp_tree_file} has been removed.")

    print("\nTree structure:")
    print(tree)
    print("\n")

    if args.midpoint_root:
        print("\nMidpoint rooting the tree...")
        R = tree.get_midpoint_outgroup()
        tree.set_outgroup(R)
        print("\nNew tree structure after midpoint rooting:")
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
        node_uid = id(node)
        new_row = pd.DataFrame({"Node_name": [node.name], "Node_id": [node_uid]})
        df_marks = pd.concat([df_marks, new_row], ignore_index=True)

    marks = list(df_marks['Node_id'])

    print("\n-------------------------------------------------------------------------")
    print(".  Adding node marks (will append '{test}' to node names)              ")
    print("-------------------------------------------------------------------------")

    for node in tree.traverse():
        if id(node) in marks:
            node.name = f"{node.name}{{test}}" if node.name else "{test}"

    print(f"Nodes marked: {marks}")
    print("\nMarked tree (Newick with marks):")
    print(tree.write(format=1))
    print("\n")

    print(f"Writing marked tree to: {args.output_tree}")
    with open(args.output_tree, 'w') as outfile:
        outfile.write(tree.write(format=1))

    print("Process complete.")

if __name__ == "__main__":
    main()
