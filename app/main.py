from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

from app.services.ocr import extract_text_from_image
from app.services.ai_generator import generate_manim_code
from app.services.manim_renderer import render_manim_code

app = FastAPI()

# Cho phép CORS nếu bạn có frontend riêng
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Có thể thay "*" bằng domain frontend bạn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/solve-physics-problem/")
async def solve_physics_problem(file: UploadFile = File(...)):
    try:
        # 1. Lưu ảnh tạm
        image_id = str(uuid.uuid4())
        image_path = f"temp/{image_id}_{file.filename}"
        os.makedirs("temp", exist_ok=True)
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())
        print("✅ Đã đọc ảnh upload")

        # 2. OCR → đề bài + latex
        extracted = extract_text_from_image(image_path)
        print("📝 Kết quả OCR:", extracted)
        question_text = extracted["text"]
        latex = extracted["latex"]

        # ✅ 3. Ghép prompt và latex lại
        full_prompt = f"{question_text}\n\nCông thức LaTeX:\n{latex}"

        # 4. AI sinh mã Manim
        manim_code = generate_manim_code(full_prompt)
        print("🧠 Mã Manim AI sinh ra:", manim_code)

        # 5. Render video
        video_path = render_manim_code(manim_code)
        print("🎬 Video đã render:", video_path)

        # 6. Trả về file video luôn
        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename=os.path.basename(video_path)
        )

    except Exception as e:
        print("❌ Lỗi xảy ra:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
