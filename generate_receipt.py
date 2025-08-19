from receipt_generator import ReceiptGenerator
import json
from datetime import datetime

def main():
    # Load the existing receipt data from JSON
    with open('atlas_all_receipts_1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        receipt_data = data['receipts'][0]

    # Create receipt generator and generate the receipt
    generator = ReceiptGenerator()
    generator.save_receipt(
        receipt_data=receipt_data,
        output_path="generated_receipts/receipt_001.png",
        logo_path="مكتبة أطلس دليلك الى النجاح.png"
    )

if __name__ == "__main__":
    main()
