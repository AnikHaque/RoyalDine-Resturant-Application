import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_order_pdf(order):
    """সম্পূর্ণ পাইথন লজিক ব্যবহার করে ইনভয়েস তৈরি"""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"RoyalDine - Invoice #{order.id}")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Customer: {order.full_name}")
    p.drawString(100, 715, f"Phone: {order.phone}")
    p.drawString(100, 700, f"Address: {order.address}")
    p.drawString(100, 685, f"Total Amount: BDT {order.total_price}")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer