import subprocess
from pathlib import Path


def extract_m4a_audio_track_from_mp4_one_file(
    input_mp4_file: Path,
    output_m4a_file: Path,
    ffmpeg: str,
) -> None:
    """
    从 MP4 文件中无损提取音频轨道（copy），输出为 M4A
    等价 CLI:
    ffmpeg -i input.mp4 -vn -c:a copy output.m4a
    """
    if not input_mp4_file.is_file():
        raise FileNotFoundError(f"MP4 not found: {input_mp4_file}")

    if input_mp4_file.suffix.lower() != ".mp4":
        raise ValueError(f"Input file is not mp4: {input_mp4_file}")
    output_m4a_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg,
        "-y",                      # 覆盖输出文件
        "-i", str(input_mp4_file),
        "-vn",                     # 不要视频流
        "-c:a", "copy",            # 音频流直接 copy（无损）
        str(output_m4a_file),
    ]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"ffmpeg failed:\n{stderr}") from None
    if not output_m4a_file.is_file():
        raise RuntimeError("ffmpeg finished but output m4a not found")

def extract_m4a_audio_track_from_mp4_dir(
    src_dir: Path,
    dst_dir: Path,
    ffmpeg: str,
) -> None:
    """
    对指定目录下的所有 MP4 文件提取音频轨道，输出为 M4A
    - 不递归子目录
    - 输出文件名与源文件同名，仅后缀改为.m4a
    """
    if not src_dir.is_dir():
        raise NotADirectoryError(f"Source dir not found: {src_dir}")

    dst_dir.mkdir(parents=True, exist_ok=True)

    mp4_files = sorted(src_dir.glob("*.mp4"))

    if not mp4_files:
        print(f"mp4 files not found")
        return
    print(f"find {len(mp4_files)} mp4 files，start converting...")
    for mp4_file in mp4_files:
        output_m4a = dst_dir / (mp4_file.stem + ".m4a")
        extract_m4a_audio_track_from_mp4_one_file(
            input_mp4_file=mp4_file,
            output_m4a_file=output_m4a,
            ffmpeg=ffmpeg,
        )
        print(f"[extract] {mp4_file} to {output_m4a} audio track")

if __name__ == "__main__":
    """
    extract_m4a_audio_track_from_mp4_one_file(
        input_mp4_file=Path(r"D:\PyCharmProjects\ffmpeg_utils\merged_files\前后缀分解【力扣周赛 482】.mp4"),
        output_m4a_file=Path(r"D:\PyCharmProjects\ffmpeg_utils\merged_files\前后缀分解【力扣周赛 482】.m4a"),
        ffmpeg="ffmpeg",
    )
    """
    extract_m4a_audio_track_from_mp4_dir(
        src_dir=Path(r"D:\PyCharmProjects\ffmpeg_utils\merged_files"),
        dst_dir=Path(r"D:\PyCharmProjects\ffmpeg_utils\m4a_files"),
        ffmpeg="ffmpeg",
    )
