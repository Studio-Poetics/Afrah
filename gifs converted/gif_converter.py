#!/usr/bin/env python3
"""
Fixed GIF Converter for ESP32 LED Matrix

This script processes ALL GIF files in the current directory and converts them 
to the correct binary format expected by the ESP32 code.

Key fixes:
- Matches ESP32 file format exactly
- Handles RGB to GRB conversion
- Scales images to 16x16 matrix size
- Uses average frame delay for animated GIFs

Output files are named sequentially (gif1.bin, gif2.bin, etc.)

Usage:
    python fixed_gif_converter.py
"""

import os
import sys
from PIL import Image
import struct

def resize_image_to_matrix(img, target_width=16, target_height=16):
    """Resize image to match LED matrix dimensions"""
    return img.resize((target_width, target_height), Image.Resampling.LANCZOS)

def rgb_to_grb(r, g, b):
    """Convert RGB to GRB format for NeoPixels"""
    # Try different color orders if colors are wrong:
    # Option 1: RGB (no conversion) - uncomment this line:
    return r, g, b
    # Option 2: GRB (current) - this is active:
    #return g, r, b
    # Option 3: BGR - uncomment this line:
    # return b, g, r

def get_gif_properties(gif_path):
    """Extracts frame delays and other properties from a GIF"""
    try:
        with Image.open(gif_path) as img:
            width, height = img.size
            is_animated = getattr(img, 'is_animated', False)
            frame_count = img.n_frames if is_animated else 1
            
            # Get frame delays
            delays = []
            if is_animated:
                for frame in range(frame_count):
                    img.seek(frame)
                    delay = img.info.get('duration', 100)
                    # Some GIFs have very short delays, enforce minimum
                    delays.append(max(delay, 50))
            else:
                delays = [100]  # Default for static GIFs
            
            # Calculate average delay for the entire GIF
            avg_delay = sum(delays) // len(delays) if delays else 100
            
            return {
                'width': width,
                'height': height,
                'frame_count': frame_count,
                'delays': delays,
                'average_delay': avg_delay,
                'is_animated': is_animated
            }
    except Exception as e:
        print(f"Error reading GIF properties: {e}")
        return None

def convert_gif_to_binary(gif_path, output_path, matrix_width=16, matrix_height=16):
    """Converts GIF to ESP32-compatible binary format"""
    try:
        props = get_gif_properties(gif_path)
        if not props:
            return False
        
        print(f"  Processing {'animated' if props['is_animated'] else 'static'} GIF")
        print(f"  Original size: {props['width']}x{props['height']}")
        print(f"  Frames: {props['frame_count']}")
        print(f"  Average frame delay: {props['average_delay']}ms")
        
        with open(output_path, 'wb') as bin_file:
            # Write header in ESP32 expected format:
            # 4 bytes: number of frames (int32)
            # 4 bytes: frame delay in milliseconds (int32)
            bin_file.write(struct.pack('<I', props['frame_count']))  # Little-endian unsigned int
            bin_file.write(struct.pack('<I', props['average_delay'])) # Little-endian unsigned int
            
            # Process each frame
            with Image.open(gif_path) as img:
                for frame in range(props['frame_count']):
                    if props['is_animated']:
                        img.seek(frame)
                    
                    # Resize to matrix dimensions
                    frame_img = resize_image_to_matrix(img.convert('RGB'), matrix_width, matrix_height)
                    
                    # Convert to pixel data with GRB format
                    for y in range(matrix_height):
                        for x in range(matrix_width):
                            r, g, b = frame_img.getpixel((x, y))
                            # Convert RGB to GRB and write
                            grb_r, grb_g, grb_b = rgb_to_grb(r, g, b)
                            bin_file.write(bytes([grb_r, grb_g, grb_b]))
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {gif_path}: {str(e)}")
        return False

def main():
    print("Fixed GIF Converter for ESP32 LED Matrix")
    print("=" * 50)
    
    # Find all GIF files in current directory
    gif_files = sorted([f for f in os.listdir() 
                       if f.lower().endswith('.gif')])
    
    if not gif_files:
        print("No GIF files found in current directory")
        return 1
    
    print(f"Found {len(gif_files)} GIF files:")
    for i, gif in enumerate(gif_files, 1):
        print(f"  {i}. {gif}")
    
    print(f"\nProcessing all GIFs to 16x16 matrix format...")
    print("=" * 50)
    
    successful = 0
    failed = 0
    
    for i, gif_file in enumerate(gif_files, 1):
        output_file = f"gif{i}.bin"
        print(f"\nProcessing {gif_file} → {output_file}")
        
        success = convert_gif_to_binary(gif_file, output_file)
        
        if success:
            file_size = os.path.getsize(output_file)
            print(f"  ✅ Successfully created {output_file} ({file_size} bytes)")
            successful += 1
        else:
            print(f"  ❌ Failed to convert {gif_file}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Conversion complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print("\n📁 Binary files created:")
        total_size = 0
        for i in range(1, successful + 1):
            output_file = f"gif{i}.bin"
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                total_size += size
                print(f"  {output_file} ({size} bytes)")
        
        print(f"\nTotal size: {total_size} bytes")
        print("\n📋 Next steps:")
        print("1. Copy the .bin files to your ESP32 SD card")
        print("2. Create corresponding text files (text1.txt, text2.txt, etc.)")
        print("3. Upload your ESP32 code")
        print("4. Test with the 'status' command to verify frame delays")
        
        print("\n💡 Tips:")
        print("- All images are resized to 16x16 pixels")
        print("- Colors are converted to GRB format for NeoPixels")
        print("- Animated GIFs use average frame timing")
        print("- Static GIFs will display as single frames")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())