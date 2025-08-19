from receipt_generator import ReceiptGenerator
import json
from datetime import datetime

def main():
    # Create a sample receipt with a required item
    receipt_data = {
        "store": "Atlas Library",
        "store_ar": "مكتبة أطلس",
        "email": "sales@atlaslibrary.net",
        "phones": ["22661259", "22619259"],
        "date": "2025-08-19",  # Today's date
        "time": "10:30 AM",
        "receipt_no": "000001",
        "items": [
            {
                "name_ar": "باكيت اقلام رصاص مثلث",
                "price": 0.550,
                "qty": 1
            },
            {
                "name_ar": "صمغ يوهو بورسلان",
                "price": 0.95,
                "qty": 1
            },
            {
                "name_ar": "دفتر اي اند تي حلزوني",
                "price": 1.55,
                "qty": 1
            }
        ],
        "item_count": 3,
        "total": 3.050,
        "payment_method": "CASH",
        "footer_ar": "شكرا لزيارتكم"
    }
    
    # Create receipt
    generator = ReceiptGenerator()
    
    # Generate receipt with logo
    generator.save_receipt(
        receipt_data=receipt_data,
        output_path="generated_receipts/receipt.png",
        logo_path="مكتبة أطلس دليلك الى النجاح.png"  # Arabic library logo
    )

if __name__ == "__main__":
    main()
