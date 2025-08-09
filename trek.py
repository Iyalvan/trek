#!/usr/bin/env python3
import sys
import argparse
from collections import defaultdict

FILES_KEY = "__files__"  # special bucket for files at each node

def node():
    """Create a new directory node."""
    return defaultdict(node)

def add_path(root, parts):
    parts = [p for p in parts if p]  # remove empty parts from //
    if not parts:
        return
    if len(parts) == 1:
        # Ensure FILES_KEY exists and is a set
        if FILES_KEY not in root:
            root[FILES_KEY] = set()
        root[FILES_KEY].add(parts[0])
    else:
        add_path(root[parts[0]], parts[1:])

def build_tree(lines):
    root = node()
    for line in lines:
        path = line.strip().replace("//", "/").strip("/")
        if not path:
            continue
        add_path(root, path.split("/"))
    return root

def get_subtree(root, start_path):
    if not start_path:
        return root, ""
    parts = [p for p in start_path.replace("//", "/").strip("/").split("/") if p]
    cur = root
    traversed = []
    for p in parts:
        if p in cur:
            cur = cur[p]
            traversed.append(p)
        else:
            return None, start_path
    return cur, "/".join(traversed)

def print_tree(n, prefix="", max_depth=None, depth=0, show_files=False):
    dirs = sorted([k for k in n.keys() if k != FILES_KEY])
    entries = dirs[:]
    if show_files and FILES_KEY in n:
        entries += sorted(n[FILES_KEY])
    for i, key in enumerate(entries):
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "
        print(prefix + connector + key)
        if key in n:
            if max_depth is None or depth + 1 < max_depth:
                new_prefix = prefix + ("    " if is_last else "│   ")
                print_tree(n[key], new_prefix, max_depth, depth + 1, show_files)

def collect_dirs_at_level(n, target_level, level=0, path_prefix=""):
    out = []
    if level == target_level:
        subdirs = [k for k in n.keys() if k != FILES_KEY]
        out.append((path_prefix.rstrip("/"), len(subdirs)))
        return out
    for k in sorted([k for k in n.keys() if k != FILES_KEY]):
        out.extend(collect_dirs_at_level(n[k], target_level, level + 1, f"{path_prefix}{k}/"))
    return out

def read_lines_from_file_or_stdin(filename):
    if filename:
        with open(filename, "r", encoding="utf-8") as f:
            return f.readlines()
    return sys.stdin.readlines()

def main():
    ap = argparse.ArgumentParser(description="Render a directory tree and query levels.")
    ap.add_argument("input", nargs="?", help="Input file (or use stdin).")
    ap.add_argument("--start", "-s", default="", help="Start at this subpath.")
    ap.add_argument("--max-depth", "-d", type=int, default=None, help="Limit printed tree depth.")
    ap.add_argument("--show-files", action="store_true", help="Also display leaf files.")
    ap.add_argument("--list-level", "-L", type=int, help="List directories at this exact level.")
    ap.add_argument("--counts", action="store_true", help="Show count of immediate subdirectories.")
    args = ap.parse_args()

    lines = read_lines_from_file_or_stdin(args.input)
    root = build_tree(lines)

    subtree, resolved = get_subtree(root, args.start)
    if subtree is None:
        print(f"Path not found: {args.start}", file=sys.stderr)
        sys.exit(1)

    if args.list_level is not None:
        results = collect_dirs_at_level(subtree, args.list_level, level=0, path_prefix=(resolved + "/" if resolved else ""))
        if not results:
            print("No directories at that level.")
            return
        for path, count in results:
            if args.counts:
                print(f"{path or '/'}  (subdirs: {count})")
            else:
                print(path or "/")
        return

    if resolved:
        print(resolved)
        print_tree(subtree, prefix="", max_depth=args.max_depth, depth=0, show_files=args.show_files)
    else:
        print_tree(subtree, prefix="", max_depth=args.max_depth, depth=0, show_files=args.show_files)

if __name__ == "__main__":
    main()
