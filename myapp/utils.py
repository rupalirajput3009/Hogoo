from io import BytesIO
import qrcode

import barcode
from barcode.writer import ImageWriter
from django.conf import settings
from django.core.files.base import ContentFile
from django.urls import reverse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.core.files.base import ContentFile
from django.urls import reverse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Image as RLImage



def generate_inventory_barcode(serial_instance, request=None):
    """
    Generate QR code image:
    - Encoded value = full product URL
    - Visible text below QR = only serial_number
    """

    serial_number = str(serial_instance.serial_number).strip()
    if not serial_number:
        raise ValueError("serial_instance.serial_number is required.")

    relative_url = reverse("product-scan-detail")

    if request is not None:
        full_url = request.build_absolute_uri(f"{relative_url}?barcode={serial_number}")
    else:
        base_url = getattr(settings, "SCAN_BASE_URL", "https://hogofilm.pythonanywhere.com/").rstrip("/")
        full_url = f"{base_url}{relative_url}?barcode={serial_number}"

    # --- Generate QR Code ---
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(full_url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # --- Add Serial Number Text Below ---
    extra_height = 50
    final_img = Image.new(
        "RGB",
        (qr_img.width, qr_img.height + extra_height),
        "white"
    )
    final_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(final_img)

    try:
        # Try to use a nice font, fallback to default
        font = ImageFont.truetype("arial.ttf", 24)
    except Exception:
        font = ImageFont.load_default()

    text = f"Serial: {serial_number}"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text
    x = (final_img.width - text_width) // 2
    y = qr_img.height + ((extra_height - text_height) // 2) - 5

    draw.text((x, y), text, fill="black", font=font)

    # --- Save to Instance ---
    final_buffer = BytesIO()
    final_img.save(final_buffer, format="PNG")
    final_buffer.seek(0)

    filename = f"barcode_{serial_number}.png"

    if serial_instance.barcode_image:
        serial_instance.barcode_image.delete(save=False)

    serial_instance.barcode_image.save(
        filename,
        ContentFile(final_buffer.getvalue()),
        save=False
    )
    serial_instance.save(update_fields=["barcode_image"])

    return serial_instance.barcode_image.url



# utils.py
from pathlib import Path

def create_folder():
    folder_path = Path("myapp/templates")
    folder_path.mkdir(parents=True, exist_ok=True)




def generate_warranty_card_pdf(serial_instance, buffer=None):
    """
    Generate a single professional Warranty Card PDF (Credit Card Size).
    """
    if buffer is None:
        buffer = BytesIO()

    # CR80 Card Size: 85.6mm x 53.98mm
    card_width = 85.6 * mm
    card_height = 54 * mm

    p = canvas.Canvas(buffer, pagesize=(card_width, card_height))

    # 1. Background (Dark Premium Theme)
    p.setFillColor(colors.HexColor("#0f172a")) # Dark Navy
    p.rect(0, 0, card_width, card_height, fill=1, stroke=0)

    # 2. Add subtle accent (Corner gradient-like triangle)
    p.setFillColor(colors.HexColor("#1e293b"))
    p.pathBegin()
    p.moveTo(card_width * 0.6, 0)
    p.lineTo(card_width, 0)
    p.lineTo(card_width, card_height * 0.4)
    p.pathClose()
    p.fillPath()

    # 3. Logo / Branding
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(5 * mm, card_height - 10 * mm, "HOGO AUTOFILM")

    p.setFont("Helvetica", 6)
    p.setFillColor(colors.HexColor("#94a3b8"))
    p.drawString(5 * mm, card_height - 13 * mm, "PREMIUM PROTECTION")

    # 4. Product Details
    p.setFont("Helvetica-Bold", 8)
    p.setFillColor(colors.white)
    product_name = serial_instance.product_id.product_name[:30]
    p.drawString(5 * mm, 30 * mm, product_name)

    p.setFont("Helvetica", 7)
    p.setFillColor(colors.HexColor("#cbd5e1"))
    p.drawString(5 * mm, 25 * mm, f"S/N: {serial_instance.serial_number}")

    warranty_text = f"Warranty: {serial_instance.product_id.warranty or 'N/A'}"
    p.drawString(5 * mm, 21 * mm, warranty_text)

    # 5. QR Code
    if not serial_instance.barcode_image:
        # Generate it if missing
        generate_inventory_barcode(serial_instance)
        serial_instance.refresh_from_db()

    if serial_instance.barcode_image:
        qr_path = serial_instance.barcode_image.path
        # We need to be careful with paths in different environments,
        # but reportlab accepts file paths.
        p.drawImage(qr_path, card_width - 25 * mm, 5 * mm, width=20 * mm, height=20 * mm)

    # 6. Footer Decoration
    p.setStrokeColor(colors.HexColor("#2563eb")) # Primary Blue
    p.setLineWidth(1)
    p.line(5 * mm, 18 * mm, 15 * mm, 18 * mm)

    p.setFont("Helvetica-Oblique", 5)
    p.setFillColor(colors.HexColor("#94a3b8"))
    p.drawRightString(card_width - 5 * mm, 2 * mm, "Scan for authenticity & details")

    p.showPage()
    p.save()

    if isinstance(buffer, BytesIO):
        buffer.seek(0)
    return buffer


def generate_bulk_warranty_cards_pdf(serial_instances):
    """
    Generate multiple warranty cards on A4 pages.
    Layout: 2 columns, 4 rows = 8 cards per page.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    card_w = 85.6 * mm
    card_h = 54 * mm

    margin_x = (width - (2 * card_w)) / 3
    margin_y = 20 * mm

    x_positions = [margin_x, margin_x * 2 + card_w]
    y_positions = [height - margin_y - card_h - (i * (card_h + 10 * mm)) for i in range(4)]

    card_idx = 0
    for serial in serial_instances:
        if card_idx > 0 and card_idx % 8 == 0:
            p.showPage()

        pos_idx = card_idx % 8
        col = pos_idx % 2
        row = pos_idx // 2

        x = x_positions[col]
        y = y_positions[row]

        # --- Draw Card Content at (x, y) ---
        # (Re-implementing the draw logic relative to x, y)
        p.saveState()
        p.translate(x, y)

        # Background
        p.setFillColor(colors.HexColor("#0f172a"))
        p.rect(0, 0, card_w, card_h, fill=1, stroke=0)

        # Accent
        p.setFillColor(colors.HexColor("#1e293b"))
        p.pathBegin()
        p.moveTo(card_w * 0.6, 0)
        p.lineTo(card_w, 0)
        p.lineTo(card_w, card_h * 0.4)
        p.pathClose()
        p.fillPath()

        # Logo
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(5 * mm, card_h - 10 * mm, "HOGO AUTOFILM")

        # Details
        p.setFont("Helvetica-Bold", 8)
        p.drawString(5 * mm, 25 * mm, serial.product_id.product_name[:30])
        p.setFont("Helvetica", 7)
        p.setFillColor(colors.HexColor("#cbd5e1"))
        p.drawString(5 * mm, 20 * mm, f"Serial: {serial.serial_number}")
        p.drawString(5 * mm, 16 * mm, f"Warranty: {serial.product_id.warranty or 'N/A'}")

        # QR Code
        if not serial.barcode_image:
            generate_inventory_barcode(serial)
            serial.refresh_from_db()

        if serial.barcode_image:
            p.drawImage(serial.barcode_image.path, card_w - 25 * mm, 5 * mm, width=20 * mm, height=20 * mm)

        # Border for cutting
        p.setStrokeColor(colors.lightgrey)
        p.setDash(1, 2)
        p.rect(0, 0, card_w, card_h, fill=0, stroke=1)

        p.restoreState()
        card_idx += 1

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
