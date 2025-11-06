#!/usr/bin/env python3
# mp3_to_pdf.py
# mp3ToTxt project - terminal "hacker style" MP3 -> PDF binary dump
# Requires: reportlab, tqdm, colorama

import sys
import os
import time
from reportlab.pdfgen import canvas
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)


def mp3_to_pdf(mp3_path, byte_limit=2500000):
    base_name = os.path.splitext(mp3_path)[0]
    pdf_path = f"{base_name}_dump.pdf"

    if not os.path.exists(mp3_path):
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} File not found: {mp3_path}")
        sys.exit(1)

    total_size = os.path.getsize(mp3_path)
    byte_limit = min(byte_limit, total_size)

    print(f"\n{Fore.CYAN}>>> INPUT FILE:{Style.RESET_ALL} {mp3_path}")
    print(f"{Fore.CYAN}>>> BYTE LIMIT:{Style.RESET_ALL} {byte_limit:,}")
    print(f"{Fore.CYAN}>>> OUTPUT FILE:{Style.RESET_ALL} {pdf_path}\n")

    # read in chunks with progress bar
    chunk_size = 50000
    data = bytearray()
    with open(mp3_path, "rb") as f:
        with tqdm(total=byte_limit, unit="B", unit_scale=True,
                  bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            while len(data) < byte_limit:
                read_size = min(chunk_size, byte_limit - len(data))
                chunk = f.read(read_size)
                if not chunk:
                    break
                data.extend(chunk)
                pbar.update(len(chunk))
                time.sleep(0.005)

    print(f"\n{Fore.YELLOW}[INFO]{Style.RESET_ALL} Processing binary stream...")
    time.sleep(0.6)

    text_data = data.decode('latin-1', errors='replace')

    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Generating PDF dump...")
    c = canvas.Canvas(pdf_path)
    c.setFont("Courier", 8)
    c.drawString(80, 800, f"MP3 BINARY DUMP (first {byte_limit:,} bytes)")

    y = 780
    line_height = 10
    page_count = 1

    # split to lines
    lines = [text_data[i:i+90] for i in range(0, len(text_data), 90)]
    for _line in tqdm(lines, desc="[WRITE]"):
        c.drawString(50, y, _line)
        y -= line_height
        if y < 50:
            c.showPage()
            c.setFont("Courier", 8)
            y = 800
            page_count += 1

    c.save()
    print(f"\n{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} PDF generated successfully.")
    print(f"{Fore.CYAN}>>> FILE:{Style.RESET_ALL} {pdf_path}")
    print(f"{Fore.CYAN}>>> PAGES:{Style.RESET_ALL} {page_count}")
    print(f"{Fore.CYAN}>>> STATUS:{Style.RESET_ALL} COMPLETE\n")


def print_usage_and_exit():
    print(f"Usage: python mp3_to_pdf_hacker.py <mp3_file> [byte_limit]")
    print("If byte_limit omitted, default is 2,500,000 bytes (~2.5 MB).")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage_and_exit()

    mp3_file = sys.argv[1]
    try:
        byte_limit = int(sys.argv[2]) if len(sys.argv) > 2 else 2500000
    except ValueError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} byte_limit must be a number.")
        sys.exit(1)

    mp3_to_pdf(mp3_file, byte_limit)
