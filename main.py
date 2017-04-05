import sys
from reader import git_tree_reader as gr

if len(sys.argv) > 1:
	gr.read_git_log(sys.argv[1])
else:
	print("Usage: main.py <file>")
