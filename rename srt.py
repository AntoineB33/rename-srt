import os
import re
import tkinter as tk
from pathlib import Path


def get_clipboard_path():
    try:
        # Use tkinter to grab clipboard data natively in Windows
        root = tk.Tk()
        root.withdraw() # Hide the main window
        clipboard_text = root.clipboard_get()
        root.destroy()
        
        # Clean up any surrounding quotes or spaces from "Copy as path"
        return clipboard_text.strip(' "\'\t\n\r')
    except tk.TclError:
        raise ValueError("The clipboard is empty or does not contain text.")

def main():
    try:
        directory_path = get_clipboard_path()
    except ValueError as e:
        raise RuntimeError(f"Clipboard Error: {e}")

    target_dir = Path(directory_path)
    if not target_dir.exists() or not target_dir.is_dir():
        raise NotADirectoryError(f"The path in your clipboard is not a valid directory:\n'{directory_path}'")

    se_pattern = re.compile(r'[Ss](\d{2})[Ee](\d{2})')
    videos = {}
    subtitles = {}

    # Scan and map files
    for file_path in target_dir.iterdir():
        if not file_path.is_file():
            continue
            
        match = se_pattern.search(file_path.name)
        if match:
            season_ep = (int(match.group(1)), int(match.group(2)))
            
            if file_path.suffix.lower() in ['.mkv', '.mp4', '.avi']:
                videos[season_ep] = file_path
            elif file_path.suffix.lower() == '.srt':
                subtitles[season_ep] = file_path

    missing_srts = []
    rename_errors = []

    # Process files
    for season_ep, video_path in videos.items():
        if season_ep in subtitles:
            srt_path = subtitles[season_ep]
            new_srt_name = video_path.with_suffix('.srt')
            
            if srt_path != new_srt_name:
                try:
                    os.rename(srt_path, new_srt_name)
                    print(f"Renamed: '{srt_path.name}' -> '{new_srt_name.name}'")
                except OSError as e:
                    rename_errors.append(f"Failed to rename '{srt_path.name}': {e}")
        else:
            missing_srts.append(video_path.name)

    # Error Evaluation
    if rename_errors:
        error_msg = "\n".join(rename_errors)
        raise PermissionError(f"Encountered errors while renaming files:\n{error_msg}")

    if missing_srts:
        missing_list = "\n".join(missing_srts)
        # Throwing a real error for missing SRTs as requested
        raise FileNotFoundError(f"Missing .srt files for the following videos:\n{missing_list}")

    # If we get here, everything was successful!
    print("Success: All subtitles renamed properly. No missing files.")

if __name__ == "__main__":
    main()