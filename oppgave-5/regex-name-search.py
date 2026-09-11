import re
from pathlib import Path

file_to_search = Path(__file__).resolve().parent / "EleverVG2IT.txt"
name_to_find = "Jørgen"

# Opens the file and checks line for line. If the name is found in a line, it will be formatted and printed out.
with open(file_to_search, "r", encoding="utf-8") as file:
    for line in file:
        # Checks if the line contains the name to find
        match = re.search(rf"{re.escape(name_to_find)}", line)
        
        if match:
            # Converts tab indentation over to regular spaces
            name_formatted = re.sub(r"\t", " ", line)
            print("Found match:", name_formatted)