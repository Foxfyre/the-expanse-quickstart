#!/usr/bin/env python3
"""Extract text content from PDF files for processing.

This script extracts text from PDFs page by page, avoiding the API size limits
that occur when sending PDFs as images. The extracted text can be saved to
individual text files or processed in chunks.
"""

import fitz  # PyMuPDF
from pathlib import Path
import argparse
import sys


def extract_text_from_pdf(pdf_path: Path, output_dir: Path = None,
                          pages: list = None, chunk_size: int = None) -> str:
    """Extract text from a PDF file.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Optional directory to save per-page text files
        pages: Optional list of page numbers to extract (0-indexed)
        chunk_size: Optional max characters per chunk for API-friendly output

    Returns:
        Full extracted text as a string
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    if pages is None:
        pages = range(total_pages)

    all_text = []

    for page_num in pages:
        if page_num >= total_pages:
            print(f"Warning: Page {page_num} does not exist (max: {total_pages - 1})")
            continue

        page = doc[page_num]
        text = page.get_text("text")

        # Add page marker
        page_text = f"\n{'='*60}\n"
        page_text += f"PAGE {page_num + 1} of {total_pages}\n"
        page_text += f"{'='*60}\n\n"
        page_text += text

        all_text.append(page_text)

        # Optionally save individual page files
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            page_file = output_dir / f"{pdf_path.stem}_page_{page_num + 1:03d}.txt"
            page_file.write_text(page_text)
            print(f"Saved: {page_file}")

    doc.close()

    full_text = "\n".join(all_text)

    # If chunk_size specified, also create chunked output
    if chunk_size and output_dir:
        create_chunks(full_text, output_dir, pdf_path.stem, chunk_size)

    return full_text


def create_chunks(text: str, output_dir: Path, base_name: str, chunk_size: int):
    """Split text into API-friendly chunks.

    Args:
        text: Full text to chunk
        output_dir: Directory to save chunk files
        base_name: Base filename for chunks
        chunk_size: Maximum characters per chunk
    """
    chunks = []
    current_chunk = []
    current_size = 0

    # Split by page markers to keep pages together when possible
    pages = text.split("=" * 60)

    for segment in pages:
        segment = segment.strip()
        if not segment:
            continue

        segment_with_marker = f"{'='*60}\n{segment}\n"
        segment_size = len(segment_with_marker)

        if current_size + segment_size > chunk_size and current_chunk:
            # Save current chunk
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_size = 0

        current_chunk.append(segment_with_marker)
        current_size += segment_size

    # Don't forget the last chunk
    if current_chunk:
        chunks.append("\n".join(current_chunk))

    # Save chunks to files
    for i, chunk in enumerate(chunks, 1):
        chunk_file = output_dir / f"{base_name}_chunk_{i:02d}.txt"
        chunk_file.write_text(chunk)
        print(f"Saved chunk {i}/{len(chunks)}: {chunk_file} ({len(chunk):,} chars)")

    return chunks


def extract_pdf_tables(pdf_path: Path) -> list:
    """Extract tables from a PDF (if any).

    Note: Basic table extraction. For complex tables, consider using
    additional libraries like camelot or tabula-py.
    """
    doc = fitz.open(pdf_path)
    tables = []

    for page_num, page in enumerate(doc):
        # PyMuPDF can find tables in newer versions
        try:
            page_tables = page.find_tables()
            for table in page_tables:
                tables.append({
                    'page': page_num + 1,
                    'data': table.extract()
                })
        except AttributeError:
            # Older PyMuPDF version without table support
            pass

    doc.close()
    return tables


def get_pdf_info(pdf_path: Path) -> dict:
    """Get metadata about a PDF file."""
    doc = fitz.open(pdf_path)
    info = {
        'filename': pdf_path.name,
        'pages': len(doc),
        'metadata': doc.metadata,
        'file_size_mb': pdf_path.stat().st_size / (1024 * 1024),
    }

    # Estimate text size
    total_chars = 0
    for page in doc:
        total_chars += len(page.get_text("text"))
    info['estimated_chars'] = total_chars
    info['estimated_tokens'] = total_chars // 4  # Rough estimate

    doc.close()
    return info


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files for API processing"
    )
    parser.add_argument("pdf", help="Path to PDF file or 'all' for all PDFs in pdfs/")
    parser.add_argument("-o", "--output", help="Output directory for text files",
                        default="pdfs_text")
    parser.add_argument("-p", "--pages", help="Specific pages to extract (comma-separated, 1-indexed)",
                        default=None)
    parser.add_argument("-c", "--chunk-size", type=int, default=50000,
                        help="Max characters per chunk (default: 50000)")
    parser.add_argument("--info", action="store_true",
                        help="Just show PDF info without extracting")
    parser.add_argument("--stdout", action="store_true",
                        help="Print text to stdout instead of saving files")

    args = parser.parse_args()

    # Determine which PDFs to process
    if args.pdf.lower() == 'all':
        pdf_files = list(Path('pdfs').glob('*.pdf'))
    else:
        pdf_files = [Path(args.pdf)]

    output_dir = Path(args.output) if not args.stdout else None

    # Parse page numbers if specified
    pages = None
    if args.pages:
        pages = [int(p.strip()) - 1 for p in args.pages.split(',')]  # Convert to 0-indexed

    for pdf_path in sorted(pdf_files):
        if not pdf_path.exists():
            print(f"Error: {pdf_path} not found", file=sys.stderr)
            continue

        print(f"\n{'='*60}")
        print(f"Processing: {pdf_path.name}")
        print(f"{'='*60}")

        # Show info
        info = get_pdf_info(pdf_path)
        print(f"  Pages: {info['pages']}")
        print(f"  File size: {info['file_size_mb']:.2f} MB")
        print(f"  Estimated text: {info['estimated_chars']:,} chars (~{info['estimated_tokens']:,} tokens)")

        if args.info:
            continue

        # Extract text
        pdf_output_dir = output_dir / pdf_path.stem if output_dir else None
        text = extract_text_from_pdf(
            pdf_path,
            output_dir=pdf_output_dir,
            pages=pages,
            chunk_size=args.chunk_size if output_dir else None
        )

        if args.stdout:
            print(text)
        elif output_dir:
            # Also save complete text file
            complete_file = pdf_output_dir / f"{pdf_path.stem}_complete.txt"
            complete_file.write_text(text)
            print(f"Complete text saved to: {complete_file}")


if __name__ == '__main__':
    main()
