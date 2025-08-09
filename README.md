# trek it

A Python CLI tool to display directory structures from a list of file paths.  
Supports pretty `tree`-style output, filtering by start path, depth limiting,  
and listing directories at specific levels with optional counts.

## Features
- Reads input from a **file** or from **stdin** (`<` or `|`).
- Pretty **tree-like output** using `├──` and `└──`.
- **Limit depth** with `--max-depth` to see only top levels.
- **Start from a subpath** with `--start` to view part of the tree.
- **List directories at a specific level** with `--list-level`.
- Optionally **count immediate subdirectories** at a level with `--counts`.
- Show **leaf files** with `--show-files`.

---

## Installation
Clone or copy the script:
```bash
git clone <repo_url>
cd <repo_folder>
chmod +x trek.py
```

Requires **Python 3.6+**.

---

## Usage

### Basic Tree View
```bash
python3 trek.py paths.txt
```
Reads file paths from `paths.txt` and prints the full tree.

### Read from stdin
```bash
cat paths.txt | python3 trek.py
# or
python3 trek.py < paths.txt
```

### Limit Depth
```bash
python3 trek.py paths.txt --max-depth 1
```
Shows only the first level of directories from the root.

```bash
python3 trek.py paths.txt --max-depth 2
```
Shows only two levels.

### Start from a Subpath
```bash
python3 trek.py paths.txt --start kv2/mc/multipass/dev
```
Displays only the tree starting at `kv2/mc/multipass/dev`.

---

## Listing Directories at a Specific Level

**Example:** Show directories directly under the root:
```bash
python3 trek.py paths.txt --list-level 0
```

**Example:** Show directories 2 levels below the root:
```bash
python3 trek.py paths.txt --list-level 2
```

**With Counts:**
```bash
python3 trek.py paths.txt --list-level 0 --counts
```
Displays directory name and how many **immediate subdirectories** it has.

---

## Showing Files
By default, only directories are shown.  
To include leaf file names:
```bash
python3 trek.py paths.txt --show-files
```

---

## Example Output

### Input:
```
galaxy/milkyway/solarsystem//earth//asia//india.txt
galaxy/milkyway/solarsystem//mars//olympus_mons.jpg
```

### Command:
```bash
python3 trek.py paths.txt
```

### Output:
```
galaxy
└── milkyway
    └── solarsystem
        ├── earth
        │   └── asia
        │       └── india.txt
        └── mars
            └── olympus_mons.jpg
```

---

## Arguments Summary
| Option | Description |
|--------|-------------|
| `input` | Optional path to file containing list of paths. If not provided, reads from stdin. |
| `--start` / `-s` | Start printing from a specific subpath. |
| `--max-depth` / `-d` | Limit tree output to this depth. |
| `--show-files` | Include leaf files in the output. |
| `--list-level` / `-L` | List directories at a specific level. |
| `--counts` | Show count of immediate subdirectories (only with `--list-level`). |

---

## License
MIT License
