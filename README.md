# Telegram Sports Card Maker (Persian)

Create a captioned card for Telegram posts (RTL Persian) without Photoshop. Adds a bottom banner similar to the sample style.

## Quick start

```bash
pip install -r requirements.txt
python make_telegram_card.py /path/to/input.jpg /path/to/output.jpg --text "فوتبالیست قهوه خور"
```

If Persian glyphs do not render correctly on your system, pass a font that supports Arabic/Persian:

```bash
python make_telegram_card.py input.jpg output.jpg --text "بازیکن جدید" --font /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
```

## Web UI

```bash
python app.py
```
Open the printed URL and upload the player image, type the Persian text, and download the result.

Fonts that work well: DejaVuSans, NotoSansArabic, NotoNaskhArabic, Vazirmatn.