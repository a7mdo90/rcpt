from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import os
import random

class ReceiptMaker:
    def __init__(self):
        self.width = 280  # Width of receipt in pixels
        self.margin = 15
        self.line_height = 20
        self.font_size = 14
        self.logo_max_height = 60

    def create_receipt(self, receipt_data, logo_path=None):
        # Calculate initial height
        num_lines = len(receipt_data['items']) * 2 + 12
        height = num_lines * self.line_height + 2 * self.margin

        # Create base image with white background
        image = Image.new('RGB', (self.width, height), 'white')
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", self.font_size)
            font_small = ImageFont.truetype("arial.ttf", self.font_size - 2)
            font_bold = ImageFont.truetype("arial.ttf", self.font_size + 2)
        except:
            font = ImageFont.load_default()
            font_small = font
            font_bold = font

        current_y = self.margin

        # Handle logo
        if logo_path and os.path.exists(logo_path):
            logo = Image.open(logo_path)
            aspect = logo.height / logo.width
            logo_width = min(120, self.width - 2 * self.margin)
            logo_height = min(int(logo_width * aspect), self.logo_max_height)
            logo_width = int(logo_height / aspect)
            logo = logo.resize((logo_width, logo_height))
            logo_x = (self.width - logo_width) // 2
            image.paste(logo, (logo_x, current_y))
            current_y = self.margin + logo_height + self.line_height

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

        phones = '–'.join(receipt_data['phones'])
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
        receipt_no = receipt_data['receipt_no']
        text_width = draw.textlength(receipt_no, font=font_small)
        draw.text((self.width - self.margin - text_width, current_y), receipt_no, fill='black', font=font_small)
        current_y += self.line_height * 1.5

        # Add items
        price_width = 50  # Width reserved for price
        item_margin = 10  # Space between price and name
        max_name_width = self.width - (2 * self.margin) - price_width - item_margin

        for item in receipt_data['items']:
            name = item['name_ar']
            price = item['price']
            
            # Price aligned left
            price_text = f"{price:.3f}"
            draw.text((self.margin, current_y), price_text, fill='black', font=font_small)
            
            # Calculate if name needs truncation
            name_width = draw.textlength(name, font=font_small)
            if name_width > max_name_width:
                # Truncate name and add ellipsis
                ellipsis = "..."
                while name_width > max_name_width - draw.textlength(ellipsis, font=font_small):
                    name = name[:-1]
                    name_width = draw.textlength(name, font=font_small)
                name = name + ellipsis
            
            # Name aligned right, with spacing from price
            x_position = self.width - self.margin - draw.textlength(name, font=font_small)
            draw.text((x_position, current_y), name, fill='black', font=font_small)
            current_y += self.line_height

        # Add total section
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
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        receipt.save(output_path, 'PNG')
