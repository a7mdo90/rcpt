from PIL import Image, ImageDraw, ImageFont
from datetime import datetime            current_y = self.margin

        try:
            # Load fonts with specific sizes for different parts of the receipt
            font = ImageFont.truetype("arial.ttf", self.font_size)
            font_small = ImageFont.truetype("arial.ttf", self.font_size - 2)
            font_bold = ImageFont.truetype("arial.ttf", self.font_size + 2)
        except:
            # Fallback to default font if arial is not available
            font = ImageFont.load_default()
            font_small = font
            font_bold = font
            
        # Create a clean white background with subtle border
        border = 1
        border_color = (240, 240, 240)
        draw.rectangle([(0, 0), (self.width-1, height-1)], outline=border_color, width=border)a
import os
import random

class ReceiptGenerator:
    def __init__(self):
        self.width = 280  # Width of receipt in pixels (matching React version)
        self.margin = 15
        self.line_height = 20
        self.font_size = 14
        self.logo_max_height = 60  # Maximum height for the logo

        # Required items (at least one must be in each receipt)
        self.required_items = [
            {"name_ar": "باكيت اقلام رصاص سداسي", "price": 0.550},
            {"name_ar": "باكيت اقلام رصاص مثلث", "price": 0.550},
            {"name_ar": "باكيت اقلام حبر لون ازرق بوينتر", "price": 0.550}
        ]

    def generate_random_receipt_number(self):
        return f"{random.randint(1, 99):06d}"

    def generate_random_date_in_last_30_days(self):
        today = datetime.now()
        days_ago = random.randint(0, 29)
        random_date = today - timedelta(days=days_ago)
        return random_date.strftime("%Y-%m-%d")

    def generate_random_time(self):
        hours = random.randint(8, 19)  # 8 AM to 7 PM
        minutes = random.randint(0, 59)
        ampm = "PM" if hours >= 12 else "AM"
        display_hours = hours if hours <= 12 else hours - 12
        return f"{display_hours:02d}:{minutes:02d} {ampm}"

    def create_receipt(self, receipt_data, logo_path=None):
        # Calculate initial height (we'll adjust based on content)
        num_lines = len(receipt_data['items']) * 2 + 12  # Items (2 lines each) + header + footer + spacing
        height = num_lines * self.line_height + 2 * self.margin

        # Create the image with white background
        # Create the base image with white background
        image = Image.new('RGB', (self.width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Add subtle border
        border_color = (240, 240, 240)
        draw.rectangle([(0, 0), (self.width-1, height-1)], outline=border_color, width=1)
        
        if logo_path and os.path.exists(logo_path):
            logo = Image.open(logo_path)
            # Resize logo to fit receipt width while maintaining aspect ratio
            aspect = logo.height / logo.width
            logo_width = min(120, self.width - 2 * self.margin)  # Smaller logo width
            logo_height = min(int(logo_width * aspect), self.logo_max_height)
            logo_width = int(logo_height / aspect)
            logo = logo.resize((logo_width, logo_height))
            # Center the logo
            logo_x = (self.width - logo_width) // 2
            image.paste(logo, (logo_x, self.margin))
            current_y = self.margin + logo_height + self.line_height
        else:
            current_y = self.margin

        # Create a white image (like thermal paper)
        image = Image.new('RGB', (self.width, height), 'white')
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", self.font_size)
        except:
            font = ImageFont.load_default()

        current_y = self.margin

        # Add logo if provided
        if logo_path and os.path.exists(logo_path):
            image.paste(logo, (self.margin, current_y))
            current_y += logo_height + self.line_height

        try:
            font = ImageFont.truetype("arial.ttf", self.font_size)
            font_small = ImageFont.truetype("arial.ttf", self.font_size - 2)
            font_bold = ImageFont.truetype("arialbd.ttf", self.font_size + 2)
        except:
            font = ImageFont.load_default()
            font_small = font
            font_bold = font

        # Add store name
        store_name = "Atlas LIBRARY مكتبة أطلس"
        text_width = draw.textlength(store_name, font=font_bold)
        x = (self.width - text_width) / 2
        draw.text((x, current_y), store_name, fill='black', font=font_bold)
        current_y += self.line_height * 1.5

        # Add contact info
        email = receipt_data['email']
        text_width = draw.textlength(email, font=font_small)
        x = (self.width - text_width) / 2
        draw.text((x, current_y), email, fill='black', font=font_small)
        current_y += self.line_height

        phones = ' – '.join(receipt_data['phones'])
        text_width = draw.textlength(phones, font=font_small)
        x = (self.width - text_width) / 2
        draw.text((x, current_y), phones, fill='black', font=font_small)
        current_y += self.line_height * 1.5

        # Add receipt details
        draw.text((self.margin, current_y), "REG", fill='black', font=font_small)
        date_time = f"{receipt_data['date']} {receipt_data['time']}"
        text_width = draw.textlength(date_time, font=font_small)
        draw.text((self.width - self.margin - text_width, current_y), date_time, fill='black', font=font_small)
        current_y += self.line_height

        # Receipt number
        receipt_no = f"#{receipt_data['receipt_no']}"
        text_width = draw.textlength(receipt_no, font=font_small)
        draw.text((self.width - self.margin - text_width, current_y), receipt_no, fill='black', font=font_small)
        current_y += self.line_height * 1.5

        date_str = f"{receipt_data['date']} {receipt_data['time']}"
        draw.text((self.margin, current_y), date_str, fill='black', font=font)
        current_y += self.line_height * 1.5

        # Add items
        draw.line([(self.margin, current_y), (self.width - self.margin, current_y)], fill='black')
        current_y += self.line_height

        for item in receipt_data['items']:
            name = item['name_ar']
            price = item['price']
            qty = item.get('qty', 1)
            total = price * qty

            # Item name
            draw.text((self.margin + 50, current_y), name, fill='black', font=font_small)
            
            # Price
            price_text = f"{price:.3f}"
            text_width = draw.textlength(price_text, font=font_small)
            draw.text((self.margin, current_y), price_text, fill='black', font=font_small)
            
            current_y += self.line_height

        # Add total
        current_y += self.line_height / 2
        draw.line([(self.margin, current_y), (self.width - self.margin, current_y)], fill='black')
        current_y += self.line_height

        # Item count
        count_text = f"{receipt_data['item_count']} No"
        text_width = draw.textlength(count_text, font=font)
        x = (self.width - text_width) / 2
        draw.text((x, current_y), count_text, fill='black', font=font)
        current_y += self.line_height * 1.5

        # Total amount
        total_label = "TOTAL"
        total_amount = f"{receipt_data['total']:.3f}"
        
        draw.text((self.width - self.margin - draw.textlength(total_label, font=font_bold), current_y), 
                 total_label, fill='black', font=font_bold)
        draw.text((self.margin, current_y), 
                 total_amount, fill='black', font=font_bold)
        current_y += self.line_height

        # Payment method
        payment_text = receipt_data['payment_method']
        payment_amount = f"{receipt_data['total']:.3f}"
        
        draw.text((self.width - self.margin - draw.textlength(payment_text, font=font), current_y), 
                 payment_text, fill='black', font=font)
        draw.text((self.margin, current_y), 
                 payment_amount, fill='black', font=font)

        current_y += self.line_height * 1.5
        
        # Add footer
        footer_text = receipt_data['footer_ar']
        text_width = draw.textlength(footer_text, font=font)
        x = (self.width - text_width) / 2
        draw.text((x, current_y), footer_text, fill='black', font=font)
        
        # Resize image to actual height used
        current_y += self.line_height * 2
        image = image.crop((0, 0, self.width, current_y))

        return image

    def save_receipt(self, receipt_data, output_path, logo_path=None):
        receipt = self.create_receipt(receipt_data, logo_path)
        receipt.save(output_path, 'PNG')
