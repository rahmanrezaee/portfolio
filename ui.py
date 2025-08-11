import gradio as gr
from PIL import Image
from make_telegram_card import draw_banner

DEFAULT_TEXT = "فوتبالیست قهوه خور"


def generate(img: Image.Image, text: str, font_path: str | None):
    if img is None:
        return None
    if not text or not text.strip():
        text = DEFAULT_TEXT
    result = draw_banner(img, text=text, font_path=font_path or None)
    return result

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("**ساخت کارت تلگرامی بدون فتوشاپ** — متن فارسی خود را روی عکس اضافه کنید")
    with gr.Row():
        with gr.Column():
            inp_img = gr.Image(type="pil", label="عکس بازیکن")
            inp_text = gr.Textbox(value=DEFAULT_TEXT, label="متن (فارسی)")
            inp_font = gr.Textbox(value="", label="مسیر فونت (اختیاری)؛ مثلا DejaVuSans.ttf")
            btn = gr.Button("ساخت تصویر")
        with gr.Column():
            out_img = gr.Image(type="pil", label="خروجی")

    btn.click(generate, inputs=[inp_img, inp_text, inp_font], outputs=[out_img])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, show_api=False)