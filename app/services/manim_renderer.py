import os
import subprocess
import uuid
import re
import glob

MANIM_OUTPUT_DIR = "outputs"  # Đặt video vào folder outputs cùng cấp với app

def render_manim_code(manim_code: str) -> str:
    """
    Lưu mã Manim vào file tạm thời, biên dịch thành video, trả về đường dẫn file video.
    """
    os.makedirs(MANIM_OUTPUT_DIR, exist_ok=True)

    # Loại bỏ markdown code block nếu có
    if manim_code.strip().startswith("```"):
        manim_code = "\n".join(
            line for line in manim_code.splitlines()
            if not line.strip().startswith("```")
        )

    # Thay thế .get_length() thành np.linalg.norm()
    manim_code = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\.get_length\(\)', r'np.linalg.norm(\1)', manim_code)

    # Thay phép cộng Vector của Manim thành cộng các vector số (chỉ khi cả hai vế là Vector)
    def replace_vector_addition(match):
        var, left, right = match.group(1), match.group(2), match.group(3)
        # Chỉ thay nếu tên biến có 'Vector' (giả định AI luôn đặt tên như vậy)
        if 'Vector' in left or 'Vector' in right:
            return f"{var} = Vector([a + b for a, b in zip({left}.get_vector(), {right}.get_vector())], color=WHITE)"
        else:
            return match.group(0)

    manim_code = re.sub(
        r'(\w+)\s*=\s*(\w+)\s*\+\s*(\w+)',
        replace_vector_addition,
        manim_code
    )

    # Đảm bảo import zip nếu dùng
    if "zip(" in manim_code and "from itertools import zip_longest" not in manim_code:
        manim_code = "from itertools import zip_longest as zip\n" + manim_code

    # Đảm bảo import numpy nếu dùng np.linalg.norm
    if "np.linalg.norm" in manim_code and "import numpy as np" not in manim_code:
        manim_code = "import numpy as np\n" + manim_code

    file_id = str(uuid.uuid4())
    temp_file = os.path.join(MANIM_OUTPUT_DIR, f"{file_id}.py")
    # output_file = os.path.join(MANIM_OUTPUT_DIR, f"{file_id}.mp4")  # Không dùng nữa

    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(manim_code)

    try:
        subprocess.run(
            [
                "manim",
                temp_file,
                "Scene",
                "-qk",
                "-o", f"{file_id}.mp4",
                "--fps", "30",
                "--media_dir", MANIM_OUTPUT_DIR
            ],
            check=True
        )
        # Tìm file mp4 thực tế trong outputs/videos/<file_id>/*/<file_id>.mp4
        video_search_pattern = os.path.join(
            MANIM_OUTPUT_DIR, "videos", file_id, "*", f"{file_id}.mp4"
        )
        video_files = glob.glob(video_search_pattern)
        if not video_files:
            raise RuntimeError(f"Không tìm thấy file video render: {video_search_pattern}")
        return video_files[0]

    except subprocess.CalledProcessError as e:
        print("❌ Lỗi manim:", e)
        raise RuntimeError(f"Render thất bại: {e}")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
