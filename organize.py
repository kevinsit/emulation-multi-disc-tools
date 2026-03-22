import os
import re
import shutil
from pathlib import Path

# Configuration
SOURCE_DIR = Path('.')
DEST_DIR = Path('./organized')

# Regex to identify disc numbers
# Matches: " (Disc 1)", " (Disc A)", " (CD 1)", " (Disk 1 of 2)"
DISC_REGEX = re.compile(r'\s*\((?:Disc|Disk|CD)\s*([0-9A-Z]+)(?:.*)?\)', re.IGNORECASE)

def get_base_name(filename):
    """
    Extracts the base name of a game by removing the disc identifier.
    If no disc identifier is found, returns the filename without extension.
    """
    stem = filename.stem
    match = DISC_REGEX.search(stem)
    if match:
        # Return the part of the filename before the match
        return stem[:match.start()].strip()
    return stem

def organize_files():
    # 1. Create destination directory
    DEST_DIR.mkdir(exist_ok=True)

    # 2. Find all .chd files
    chd_files = list(SOURCE_DIR.rglob('*.chd'))
    
    if not chd_files:
        print("No .chd files found in the current directory.")
        return

    print(f"Found {len(chd_files)} .chd files.")

    # 3. Group files by base name
    games = {}
    for file_path in chd_files:
        # Skip files already in the destination folder to prevent re-processing issues
        if DEST_DIR in file_path.parents:
            continue
            
        base_name = get_base_name(file_path)
        if base_name not in games:
            games[base_name] = []
        games[base_name].append(file_path)

    # 4. Process groups
    for base_name, files in games.items():
        # Sort files to ensure disc order is correct (e.g., Disc 1, Disc 2)
        files.sort(key=lambda p: p.name)

        if len(files) == 1:
            # Single disc game
            file_path = files[0]
            print(f"Processing single-disc game: {file_path.name}")
            
            # Move directly to DEST_DIR
            dest_path = DEST_DIR / file_path.name
            if dest_path.exists():
                print(f"  Skipping {file_path.name}: Destination already exists.")
            else:
                shutil.move(str(file_path), str(dest_path))
                print(f"  Moved to {dest_path}")
        else:
            # Multi-disc game
            print(f"Processing multi-disc game: {base_name} ({len(files)} discs)")
            
            # Create a folder ending in .m3u
            game_dir = DEST_DIR / f"{base_name}.m3u"
            game_dir.mkdir(exist_ok=True)
            
            m3u_content = []
            
            for file_path in files:
                # Move to the game specific folder
                dest_path = game_dir / file_path.name
                
                if dest_path.exists():
                    print(f"  Skipping move for {file_path.name}: Destination already exists.")
                else:
                    shutil.move(str(file_path), str(dest_path))
                    print(f"  Moved {file_path.name} to {game_dir.name}/")
                
                # Add filename to m3u content (files are in the same dir)
                m3u_content.append(file_path.name)
            
            # Create M3U file inside the folder
            m3u_path = game_dir / f"{base_name}.m3u"
            with open(m3u_path, 'w') as f:
                f.write('\n'.join(m3u_content))
            print(f"  Created playlist: {m3u_path}")

    print("\nOrganization complete. Files are in the 'organized' folder.")

if __name__ == "__main__":
    organize_files()
