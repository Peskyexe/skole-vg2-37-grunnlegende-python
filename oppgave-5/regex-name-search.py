import re
from pathlib import Path

file_to_search = Path(__file__).resolve().parent / "EleverVG2IT.txt"
name_to_find = "Jørgen"

# Åpner filen å sjekker linje for linje. Om navnet er i linjen så blir det printet ut
with open(file_to_search, "r", encoding="utf-8") as file:
    for line in file:
        # Sjekker om linjen inneholder navnet
        match = re.search(rf"{re.escape(name_to_find)}", line)
        
        if match:
            # Gjør om tab indents til vanlig mellomrom
            name_formatted = re.sub(r"\t", " ", line)
            print("Found match:", name_formatted)