import os
import re
from pathlib import Path


def rename_subtitles(directory_path):
    target_dir = Path(directory_path)
    
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: The directory '{directory_path}' does not exist.")
        return

    # Regular expression to match SxxExx (e.g., S05E06, s05e10)
    se_pattern = re.compile(r'[Ss](\d{2})[Ee](\d{2})')

    # Dictionaries to store files by their (season, episode) tuple
    videos = {}
    subtitles = {}

    # Scan directory and categorize files
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

    # Keep track of which videos have matching subtitles
    missing_srts = []

    # Process and rename
    for season_ep, video_path in videos.items():
        if season_ep in subtitles:
            srt_path = subtitles[season_ep]
            
            # Construct the new subtitle name based on the video name
            new_srt_name = video_path.with_suffix('.srt')
            
            # Rename if the name is not already identical
            if srt_path != new_srt_name:
                try:
                    os.rename(srt_path, new_srt_name)
                    print(f"Renamed: '{srt_path.name}' -> '{new_srt_name.name}'")
                except OSError as e:
                    print(f"Failed to rename '{srt_path.name}': {e}")
            else:
                print(f"Already matches: '{srt_path.name}'")
        else:
            missing_srts.append(video_path.name)

    # Print missing subtitles
    print("\n--- Missing Subtitles ---")
    if missing_srts:
        for missing in sorted(missing_srts):
            # Extract just the SxxExx part for cleaner output
            match = se_pattern.search(missing)
            ep_str = match.group(0).upper() if match else "Unknown"
            print(f"Missing .srt for: {ep_str} ({missing})")
    else:
        print("No missing subtitles! Every video has a matching .srt file.")

if __name__ == "__main__":
    # Replace this with your actual folder path
    folder_path = r"C:\Torrents\Suits (2011) Season 1-9 S01-S09 (1080p BluRay x265 HEVC 10bit AAC 5.1 ImE)\Season 05"
    rename_subtitles(folder_path)