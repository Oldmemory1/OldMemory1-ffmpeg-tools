import subprocess
from pathlib import Path

def convert_wav_to_flac_one_file(src_file: Path, dst_file: Path, ffmpeg: str) -> None:
    dst_file.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        ffmpeg,
        "-y",
        "-i", str(src_file),
        "-vn",
        "-c:a", "flac",
        "-compression_level", "8",
        str(dst_file),
    ]

    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"ffmpeg failed when converting {src_file}:\n{e.stderr.decode(errors='replace')}"
        ) from e

def convert_wav_to_flac_dir(src_dir: Path, dst_dir: Path, ffmpeg: str) -> None:

    wav_files = list(src_dir.rglob("*.wav"))
    if not wav_files:
        print("wav files not found.")
        return
    print(f"find {len(wav_files)} wav files，start converting...")
    for src in wav_files:
        relative = src.relative_to(src_dir)
        dst = (dst_dir / relative).with_suffix(".flac")
        if dst.exists():
            print(f"[jump] {dst}")
            continue
        try:
            print(f"[convert] {src} -> {dst}")
            convert_wav_to_flac_one_file(src_file=src, dst_file=dst, ffmpeg=ffmpeg)
        except subprocess.CalledProcessError as e:
            print(f"[fail] {src}: {e}")
    print("done.")

if __name__ == "__main__":
    """
    convert_wav_to_flac_one_file(src_file=Path(r"D:\PyCharmProjects\ffmpeg_utils\file_example_WAV_1MG.wav"),
                                 dst_file=Path(r"D:\PyCharmProjects\ffmpeg_utils\file_example_FLAC_1MG.flac"),
                                 ffmpeg="ffmpeg")
    """
    convert_wav_to_flac_dir(src_dir=Path(r"D:\PyCharmProjects\ffmpeg_utils\input"),
                            dst_dir=Path(r"D:\PyCharmProjects\ffmpeg_utils\output"),
                            ffmpeg="ffmpeg")