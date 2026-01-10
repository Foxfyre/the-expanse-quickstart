#!/usr/bin/env python3
"""Remove all images from PDF files in pdfs/ and save to pdfs_clean/."""

import fitz  # PyMuPDF
from pathlib import Path


def remove_images_from_pdf(input_path, output_path):
    """Remove all images from a PDF file and save to output_path."""
    doc = fitz.open(input_path)
    for page in doc:
        images = page.get_images()
        for img in images:
            xref = img[0]
            page.delete_image(xref)
        page.clean_contents()
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    return input_path.stat().st_size, output_path.stat().st_size


def main():
    """Process all PDFs in pdfs/ folder, save cleaned versions to pdfs_clean/."""
    pdfs_dir = Path('pdfs')
    output_dir = Path('pdfs_clean')
    output_dir.mkdir(exist_ok=True)

    pdf_files = list(pdfs_dir.glob('*.pdf'))
    print(f"Found {len(pdf_files)} PDF files to process")

    for pdf_path in sorted(pdf_files):
        output_path = output_dir / pdf_path.name
        print(f"Processing: {pdf_path.name}...")
        original_size, new_size = remove_images_from_pdf(pdf_path, output_path)
        reduction = (1 - new_size / original_size) * 100
        print(f"  Saved to: {output_path} ({reduction:.1f}% size reduction)")

    print(f"\nDone! Processed {len(pdf_files)} files.")


if __name__ == '__main__':
    main()
