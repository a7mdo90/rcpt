# Atlas Library Receipt Generator

A Python-based receipt generator for Atlas Library that creates thermal receipt-style images with Arabic text support.

## Features

- Generates receipt images with thermal receipt styling
- Supports Arabic text and right-to-left alignment
- Includes store logo
- Proper price formatting with 3 decimal places
- Multiple receipt generation with varying items
- PDF compilation of all receipts
- Image compression for optimal file sizes

## Requirements

- Python 3.x
- Pillow (PIL)
- img2pdf

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/atlas-receipt-generator.git
cd atlas-receipt-generator
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install pillow img2pdf
```

## Usage

1. Generate a single receipt:
```bash
python test_receipt.py
```

2. Generate multiple receipts and combine into PDF:
```bash
python test_receipt.py
```

The generated receipts will be saved in the `generated_receipts` folder:
- Individual receipt images: `receipt_001.png`, `receipt_002.png`, etc.
- Combined PDF: `all_receipts.pdf`

## Receipt Format

Each receipt includes:
- Store logo
- Store name in Arabic and English
- Contact information
- Receipt number
- Date and time
- Item list with prices
- Total amount
- Payment method
- Footer in Arabic

## File Structure

- `receipt_maker.py`: Main receipt generation class
- `test_receipt.py`: Script to generate sample receipts
- `atlas_all_receipts_1.json`: Sample receipt data
- `مكتبة أطلس دليلك الى النجاح.png`: Store logo

## License

MIT License
