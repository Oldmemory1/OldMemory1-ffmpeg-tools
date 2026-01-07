import os
from pathlib import Path
import subprocess


def merge_equal_long_m4a_and_mp4_one_file(
    input_mp4_file: Path,
    input_m4a_file: Path,
    output_mp4_file: Path,
    ffmpeg: str,
) -> None:
    if not input_mp4_file.is_file():
        raise FileNotFoundError(f"MP4 not found: {input_mp4_file}")
    if not input_m4a_file.is_file():
        raise FileNotFoundError(f"M4A not found: {input_m4a_file}")
    if input_m4a_file.suffix.lower() != ".m4a":
        raise ValueError(f"Input m4a file is not m4a: {input_m4a_file}")
    if input_mp4_file.suffix.lower() != ".mp4":
        raise ValueError(f"Input mp4 file is not mp4: {input_mp4_file}")

    cmd = [
        ffmpeg,
        "-y",
        "-i", str(input_mp4_file),
        "-i", str(input_m4a_file),
        "-c", "copy",
        str(output_mp4_file),
    ]

    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"ffmpeg failed when converting {input_mp4_file,input_m4a_file}:\n{e.stderr.decode(errors='replace')}"
        ) from e


def merge_equal_long_m4a_and_mp4_dir(
    src_dir: Path,
    dst_dir: Path,
    ffmpeg: str,
    delete_original_files: bool,
) -> None:
    if not src_dir.is_dir():
        raise NotADirectoryError(f"Source dir not found: {src_dir}")

    dst_dir.mkdir(parents=True, exist_ok=True)

    mp4_files = list(src_dir.glob("*.mp4"))

    if not mp4_files:
        print(f"mp4 files not found")
        return  # 没有MP4文件，退出
    print(f"find {len(mp4_files)} mp4 files，start converting...")

    for mp4_path in mp4_files:
        stem = mp4_path.stem
        m4a_path = src_dir / f"{stem}.m4a"

        # 没有对应音轨，跳过（或记录日志）
        if not m4a_path.is_file():
            print(f"warning! {m4a_path} not found")
            continue

        output_mp4 = dst_dir / mp4_path.name
        try:
            merge_equal_long_m4a_and_mp4_one_file(
                input_mp4_file=mp4_path,
                input_m4a_file=m4a_path,
                output_mp4_file=output_mp4,
                ffmpeg=ffmpeg,
            )
            print(f"[convert] {mp4_path} and {m4a_path} to {output_mp4}")
            if delete_original_files:
                if os.path.exists(mp4_path):
                    os.remove(mp4_path)
                    print(f"合并成功，原文件 {mp4_path} 已删除")
                else:
                    print(f"文件 {mp4_path} 不存在")
                if os.path.exists(m4a_path):
                    os.remove(m4a_path)
                    print(f"合并成功，原文件 {m4a_path} 已删除")
                else:
                    print(f"文件 {m4a_path} 不存在")
        except subprocess.CalledProcessError as e:
            print(f"[fail] {mp4_path,m4a_path}: {e}")
    print("done.")

if __name__ == "__main__":
    merge_equal_long_m4a_and_mp4_dir(src_dir=Path(r"D:\PyCharmProjects\ffmpeg_utils\origin_files"),
                                     dst_dir=Path(r"D:\PyCharmProjects\ffmpeg_utils\merged_files"),
                                     ffmpeg="ffmpeg",
                                     delete_original_files=True)
