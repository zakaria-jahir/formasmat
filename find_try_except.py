import os
import re

def find_try_except_blocks(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Find try blocks without except or with incomplete except
                    try_matches = list(re.finditer(r'try:\n(.*?)\n', content, re.DOTALL))
                    for match in try_matches:
                        try_block = match.group(0)
                        start_line = content[:match.start()].count('\n') + 1
                        # Check if there's a corresponding except block
                        except_pattern = r'except:|\nexcept\s*\w*\s*:'
                        if not re.search(except_pattern, content[match.end():], re.MULTILINE):
                            print(f"Incomplete try block in {filepath} at line {start_line}:")
                            print(try_block)
                            print("---")

# Specify the directory to search
search_dir = r'c:/Users/bpics/CascadeProjects/formation_assmat/CascadeProjects/windsurf-project'
find_try_except_blocks(search_dir)
