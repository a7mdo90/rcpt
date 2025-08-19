from receipt_maker import ReceiptMaker
import json
import random
import os
import img2pdf
from PIL import Image
import glob
from datetime import datetime, timedelta

def compress_image(image_path, quality=85):
    """Compress the image to reduce file size"""
    img = Image.open(image_path)
    img.save(image_path, 'PNG', optimize=True, quality=quality)

def create_pdf_from_images(image_folder, output_pdf):
    """Create a PDF from all PNG images in the folder"""
    # Get all PNG files in the folder
    png_files = sorted(glob.glob(os.path.join(image_folder, "receipt_*.png")))
    
    # Convert images to PDF
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(png_files))

def main():
    # Load all items from the catalog
    all_items = [
        {"name_ar": "باكيت اقلام رصاص سداسي", "price": 0.550},
        {"name_ar": "باكيت اقلام رصاص مثلث", "price": 0.550},
        {"name_ar": "باكيت اقلام حبر لون ازرق بوينتر", "price": 0.550},
        {"name_ar": "صمغ يوهو بورسلان", "price": 0.950},
        {"name_ar": "دفتر اي اند تي حلزوني حجم اي فور عدد ١٢٠ ورقه الوان بناتي متنوعة", "price": 1.550},
        {"name_ar": "اقلام فسفورية ستابيلو ٦ الوان مقاومة للجفاف", "price": 3.000},
        {"name_ar": "الوان تضليل هايلايتر كلاس راس مشطوف ٤ لون", "price": 1.000},
        {"name_ar": "الوان ضعيفة ستابيلو مجموعة ٦ لون", "price": 1.450},
        {"name_ar": "باكيت الوان باستيل فسفوري ٣ لون", "price": 1.650},
        {"name_ar": "قلم حبر زيبرا ز-١ حجم ٠.٧", "price": 0.250},
        {"name_ar": "مجموعة اقلام حبر زيبرا ساراسا ٥ الوان مقاس ٠.٧", "price": 1.950},
        {"name_ar": "دفتر اي اند تي حلزوني ٨*١٠ عدد ٦٠ ورقه الوان وبناتي متنوعة", "price": 0.850},
    ]
    
    # Load the base receipt template
    with open('atlas_all_receipts_1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        base_receipt = data['receipts'][0]
    
    # Create receipt generator
    generator = ReceiptMaker()
    
    # Generate 30 different receipts
    for i in range(1, 31):
        # Create a copy of the base receipt
        receipt_data = base_receipt.copy()
        
        # Generate random date within last 30 days
        today = datetime.now()
        random_days = random.randint(0, 29)
        random_date = today - timedelta(days=random_days)
        receipt_data['date'] = random_date.strftime("%Y-%m-%d")
        
        # Generate random time between 8 AM and 7 PM
        hour = random.randint(8, 19)
        minute = random.randint(0, 59)
        ampm = "PM" if hour >= 12 else "AM"
        display_hour = hour if hour <= 12 else hour - 12
        receipt_data['time'] = f"{display_hour:02d}:{minute:02d} {ampm}"
        
        # Generate random receipt number between 000001 and 000099
        receipt_data['receipt_no'] = f"{random.randint(1, 99):06d}"
        
        # Select random number of items (3-7 items)
        num_items = random.randint(3, 7)
        all_items = [
            {"name_ar": "باكيت اقلام رصاص مثلث", "price": 0.550},
            {"name_ar": "صمغ يوهو بورسلان", "price": 0.950},
            {"name_ar": "دفتر اي اند تي حلزوني حجم اي فور عدد ١٢٠ ورقه الوان بناتي متنوعة", "price": 1.550},
            {"name_ar": "اقلام فسفورية ستابيلو ٦ الوان مقاومة للجفاف", "price": 3.000},
            {"name_ar": "الوان تضليل هايلايتر كلاس راس مشطوف ٤ لون", "price": 1.000},
            {"name_ar": "الوان ضعيفة ستابيلو مجموعة ٦ لون", "price": 1.450},
            {"name_ar": "باكيت الوان باستيل فسفوري ٣ لون", "price": 1.650},
            {"name_ar": "قلم حبر زيبرا ز-١ حجم ٠.٧", "price": 0.250},
            {"name_ar": "مجموعة اقلام حبر زيبرا ساراسا ٥ الوان مقاس ٠.٧", "price": 1.950},
            {"name_ar": "دفتر اي اند تي حلزوني ٨*١٠ عدد ٦٠ ورقه الوان وبناتي متنوعة", "price": 0.850}
        ]
        
        # Randomly select items
        selected_items = random.sample(all_items, num_items)
        receipt_data['items'] = selected_items
        receipt_data['item_count'] = len(selected_items)
        
        # Calculate new total
        total = sum(item['price'] for item in selected_items)
        receipt_data['total'] = round(total, 3)
        
        # Create a random selection of 3-7 items
        num_items = random.randint(3, 7)
        selected_items = []
        
        # Always include one required item
        required_items = [item for item in all_items if item['price'] == 0.550]
        selected_items.append(random.choice(required_items))
        
        # Add other random items
        remaining_items = [item for item in all_items if item not in selected_items]
        selected_items.extend(random.sample(remaining_items, num_items - 1))
        
        # Update receipt data
        receipt_data['items'] = selected_items
        receipt_data['item_count'] = len(selected_items)
        receipt_data['total'] = round(sum(item['price'] for item in selected_items), 3)
        
        # Generate the receipt
        output_path = f"generated_receipts/receipt_{i:03d}.png"
        generator.save_receipt(
            receipt_data=receipt_data,
            output_path=output_path,
            logo_path="مكتبة أطلس دليلك الى النجاح.png"
        )
        
        # Compress the generated image
        compress_image(output_path)
        print(f"Generated and compressed receipt_{i:03d}.png")

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs("generated_receipts", exist_ok=True)
    
    # Generate all receipts
    main()
    
    # Create and compress PDF
    print("\nCreating PDF from all receipts...")
    create_pdf_from_images("generated_receipts", "generated_receipts/all_receipts.pdf")
    print("PDF created successfully!")
