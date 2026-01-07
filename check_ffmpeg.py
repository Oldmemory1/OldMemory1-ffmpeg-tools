import shutil

def detect_ffmpeg_environment()-> None:
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        raise RuntimeError("ffmpeg 未安装或未加入 PATH")
    else:
        # print("检测到ffmpeg，ffmpeg 路径为："+ffmpeg_path)
        return
if __name__ == "__main__":
    detect_ffmpeg_environment()
