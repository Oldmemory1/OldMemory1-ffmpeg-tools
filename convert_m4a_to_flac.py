from pathlib import Path
import subprocess




def convert_m4a_to_flac_one_file(src_file: Path, dst_file: Path, ffmpeg: str) -> None:

    dst_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg,
        "-y",
        "-i", str(src_file),
        "-c:a", "flac",
        str(dst_file)
    ]
    subprocess.run(
        cmd,
        check=True,
        stdout=subprocess.DEVNULL,  # suppress output
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )


def convert_m4a_to_flac_dir(src_dir: Path, dst_dir: Path, ffmpeg: str) -> None:

    m4a_files = list(src_dir.rglob("*.m4a"))
    if not m4a_files:
        print("m4a files not found.")
        return
    print(f"find {len(m4a_files)} m4a files，start converting...")
    for src in m4a_files:
        relative = src.relative_to(src_dir)
        dst = (dst_dir / relative).with_suffix(".flac")
        if dst.exists():
            print(f"[jump] {dst}")
            continue
        try:
            print(f"[convert] {src} -> {dst}")
            convert_m4a_to_flac_one_file(src_file=src, dst_file=dst, ffmpeg=ffmpeg)
        except subprocess.CalledProcessError as e:
            print(f"[fail] {src}: {e}")
    print("done.")


if __name__ == "__main__":
    src_dir1 = Path(r"D:\音乐\audios")
    dst_dir1 = Path(r"D:\音乐\audios_flac")
    ffmpeg1 = "ffmpeg"
    convert_m4a_to_flac_dir(src_dir=src_dir1, dst_dir=dst_dir1, ffmpeg=ffmpeg1)
