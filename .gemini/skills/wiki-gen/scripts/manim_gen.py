import os
import subprocess
import sys
from pathlib import Path

def generate_gif(scene_file, scene_name):
    """
    Runs manim to generate a GIF for the given scene.
    """
    output_dir = Path("wiki/docs/assets")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Command: manim -v WARNING --format=gif -o <name>.gif <file> <SceneName>
    # We use -v WARNING to reduce noise.
    # --format=gif ensures we get a gif.
    # Manim usually outputs to a media folder, we'll need to move it.
    
    cmd = [
        "manim",
        "-v", "WARNING",
        "--format", "gif",
        "-o", f"{scene_name}.gif",
        str(scene_file),
        scene_name
    ]
    
    print(f"Running manim: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Manim error: {result.stderr}")
            return None
        
        # Find the output file. Manim 0.18+ puts it in media/videos/...
        # But we'll try to find it.
        possible_outputs = list(Path("media").rglob(f"{scene_name}.gif"))
        if possible_outputs:
            target_path = output_dir / f"{scene_name}.gif"
            os.replace(possible_outputs[0], target_path)
            print(f"GIF saved to {target_path}")
            return target_path
        else:
            print("Could not find generated GIF in media folder.")
            return None
            
    except FileNotFoundError:
        print("Error: 'manim' command not found. Please ensure Manim and its dependencies (ffmpeg, pango, cairo) are installed.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python manim_gen.py <scene_file> <scene_name>")
        sys.exit(1)
    
    generate_gif(sys.argv[1], sys.argv[2])
