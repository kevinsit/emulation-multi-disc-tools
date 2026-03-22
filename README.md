# CHD Converter

This tool uses Docker to convert `.cue` and `.bin` files to `.chd` format using `chdman`.

## Prerequisites

- Docker
- Docker Compose
- Python 3 (for organization script)

## Usage

1.  **Place your `.cue` and `.bin` files in the root of this project directory.**
2.  Run the conversion:

    ```bash
    docker-compose up --build
    ```

3.  The script will recursively find all `.cue` files in the current directory and convert them to `.chd`.
4.  Original `.cue` and `.bin` files are preserved. `.chd` files are created alongside them.

## Organizing for ES-DE

If you have multi-disc games, you can use the `organize.py` script to structure your files for EmulationStation Desktop Edition (ES-DE).

1.  Run the script:

    ```bash
    python3 organize.py
    ```

2.  This will create an `organized` directory in the project root with the following structure:
    -   **Single-disc games:** Moved directly to `organized/`.
    -   **Multi-disc games:**
        -   A folder named `{GameName}.m3u/` is created.
        -   `.chd` files are moved into this folder.
        -   An `{GameName}.m3u` playlist is created inside this folder.

3.  Copy the contents of the `organized` folder to your ROMs directory. ES-DE will see the `.m3u` files as single entries and allow disc swapping.

## Project Structure

-   `convert.sh`: The script used inside the Docker container to perform the conversion.
-   `Dockerfile`: Defines the environment for `chdman`.
-   `docker-compose.yaml`: Orchestrates the Docker container.
-   `organize.py`: Python script to organize `.chd` files and generate `.m3u` playlists.
-   `to_process/`: A directory ignored by git where you can store your source files (zips, isos, etc.) or processed output to keep the root directory clean.

## Notes

- The conversion process preserves the directory structure.
- If a `.chd` file already exists for a `.cue` file, it is skipped.
- Ensure your `.cue` files reference the `.bin` files using relative paths (filenames only), not absolute paths.
