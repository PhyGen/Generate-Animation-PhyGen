import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load biến môi trường từ file .env nếu có

# Gán API Key Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Chọn model Gemini (gemini-pro hoặc gemini-1.5-pro nếu được cấp quyền)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_manim_code(prompt_text: str) -> str:
    system_prompt = """
Bạn là một trợ lý AI chuyên tạo hoạt hình giáo dục bằng Manim Community v0.19.0.

Yêu cầu:
- Sinh mã Python hợp lệ, không có lỗi cú pháp (SyntaxError), không có ký tự lạ, ký tự không hợp lệ, hoặc ký tự đặc biệt nào sau dấu \\ (backslash).
- Tuyệt đối không sinh ra bất kỳ ký tự đặc biệt, ký tự Unicode, ký tự dấu cách không chuẩn, hoặc ký tự không phải ASCII sau dấu \\ (backslash) trong mã Python.
- Khi viết chuỗi LaTeX hoặc Python, hãy kiểm tra kỹ các ký tự escape (\\, \\n, \\t, v.v.) để đảm bảo không gây lỗi cú pháp.
- Đảm bảo mọi chuỗi ký tự trong mã Python đều hợp lệ và không gây lỗi 'unexpected character after line continuation character'.
- Sử dụng MathTex() hoặc Tex() để hiển thị công thức toán học.
- Nếu dùng Tex(), không được dùng \\text{} ở ngoài môi trường $...$.
- Đảm bảo biểu thức toán học luôn nằm trong $...$ hoặc MathTex().
- Nếu hiển thị đơn vị vật lý như nm hoặc Hz, hãy dùng: \\ \\text{nm} bên trong môi trường toán học.
- Tránh các lỗi LaTeX như “Missing $ inserted”, “Option clash with babel”, hoặc lỗi babel khác.
- Không xuất ra giải thích, chỉ xuất ra mã Python sử dụng thư viện Manim.
- Nếu muốn lấy độ dài vector numpy, hãy dùng np.linalg.norm(vector).
- Khi muốn cộng hai vector numpy (ví dụ: RIGHT, UP), chỉ cần cộng trực tiếp. Nếu cộng hai đối tượng Vector của Manim, hãy dùng .get_vector().
- **Không dùng \\degree trong MathTex/Tex. Nếu muốn ký hiệu độ, hãy dùng ^\\circ trong môi trường toán học.**
- **Khi tạo Arrow, Vector, Line... trong Manim, luôn truyền vector 3 chiều (dạng [x, y, 0]). Nếu kết quả phép toán ra vector 2 chiều, hãy chuyển thành [x, y, 0] trước khi truyền vào.**
- **Chỉ dùng các animation như Create, Write, FadeIn, FadeOut... cho các đối tượng Mobject (Arrow, Vector, Line, Dot, MathTex, Tex, ...). Không dùng cho biến số, numpy array, list, tuple. Nếu muốn vẽ vector, phải tạo Arrow hoặc Vector từ ORIGIN đến vector đó trước.**
- Nếu sử dụng f-string trong Python để sinh LaTeX có chứa dấu ngoặc nhọn `{}` (ví dụ: \\text{N}), hãy dùng dấu ngoặc kép đôi `{{` và `}}` để tránh lỗi NameError. Ví dụ: MathTex(f"T_x = {tension_x:.2f} \\\\text{{ N}}")
- Đảm bảo mã Python sinh ra có thể chạy trực tiếp với Manim mà không bị lỗi cú pháp hoặc lỗi ký tự escape.
"""

    full_prompt = f"{system_prompt}\n\nĐề bài: {prompt_text}"

    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"# Lỗi khi gọi Gemini AI: {str(e)}"
