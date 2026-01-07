import subprocess
from pathlib import Path




def convert_mp3_to_flac_one_file(
    src_file: Path,
    dst_file: Path,
    ffmpeg: str,
) -> None:
    if not src_file.is_file():
        raise FileNotFoundError(f"MP3 not found: {src_file}")
    if src_file.suffix.lower() != ".mp3":
        raise ValueError(f"Input file is not mp3: {src_file}")
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg,
        "-y",
        "-i", str(src_file),

        "-map_metadata", "0",  # 保留标签
        "-vn",                 # 禁止封面视频流

        "-c:a", "flac",
        str(dst_file),
    ]

    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"ffmpeg failed when converting {src_file}:\n{e.stderr.decode(errors='replace')}"
        ) from e

def convert_mp3_to_flac_dir(src_dir: Path, dst_dir: Path, ffmpeg: str) -> None:

    mp3_files = list(src_dir.rglob("*.mp3"))
    if not mp3_files:
        print("mp3 files not found.")
        return
    print(f"find {len(mp3_files)} mp3 files，start converting...")
    for src in mp3_files:
        relative = src.relative_to(src_dir)
        dst = (dst_dir / relative).with_suffix(".flac")
        if dst.exists():
            print(f"[jump] {dst}")
            continue
        try:
            print(f"[convert] {src} -> {dst}")
            convert_mp3_to_flac_one_file(src_file=src, dst_file=dst, ffmpeg=ffmpeg)
        except subprocess.CalledProcessError as e:
            print(f"[fail] {src}: {e}")
    print("done.")
if __name__ == "__main__":
    """
    convert_mp3_to_flac_one_file(src_file=Path(r"D:\PyCharmProjects\ffmpeg_utils\吉俣良 - 砂打芽.mp3"),
                            dst_file=Path(r"D:\PyCharmProjects\ffmpeg_utils\吉俣良 - 砂打芽.flac"),
                            ffmpeg="ffmpeg")
    """
    convert_mp3_to_flac_dir(src_dir=Path(r"D:\PyCharmProjects\ffmpeg_utils\test"),
                            dst_dir=Path(r"D:\PyCharmProjects\ffmpeg_utils\test1"),
                            ffmpeg="ffmpeg")
