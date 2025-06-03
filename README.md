# Afrah

# ESP32 Dual LED Matrix Display System

A dual-display system using ESP32 to show synchronized animated GIFs on a 16x16 matrix alongside scrolling text on a 40x8 matrix. 

## 🎯 Features

- **Dual Matrix Control**: Simultaneous operation of GIF and text displays
- **Variable Frame Rates**: Each GIF can have its own timing
- **SD Card Storage**: Store unlimited GIF/text pairs
- **Serial Commands**: Real-time control and debugging
- **Auto-Cycling**: Automatically advance through content pairs
- **Color Format Support**: Handles RGB/GRB NeoPixel variants
- **Robust Error Handling**: SD card failures, file corruption protection

## 📋 Table of Contents

- [Hardware Requirements](#-hardware-requirements)
- [Wiring Diagram](#-wiring-diagram)
- [Software Setup](#-software-setup)
- [Content Creation](#-content-creation)
- [Installation Guide](#-installation-guide)
- [Usage & Commands](#-usage--commands)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)

## 🛠 Hardware Requirements

### Core Components
| Component | Specification | Quantity | Notes |
|-----------|---------------|----------|--------|
| **ESP32 Dev Board** | Any ESP32 variant | 1 | Tested with ESP32-WROOM-32 |
| **16x16 LED Matrix** | WS2812B/NeoPixel | 1 | For GIF display |
| **40x8 LED Matrix** | WS2812B/NeoPixel | 1 | For text scrolling |
| **MicroSD Card Module** | SPI interface | 1 | Class 10 recommended |
| **MicroSD Card** | 1GB+ capacity | 1 | FAT32 formatted |
| **Power Supply** | 5V, 10A+ | 1 | Calculate based on LED count |
| **Capacitor** | 1000µF, 6.3V+ | 1 | Power smoothing |
| **Resistors** | 470Ω | 3 | Data line protection |

### Optional Components
- **Level Shifter** (3.3V→5V) - Recommended for reliable data transmission
- **Breadboard/PCB** - For prototyping
- **Enclosure** - Weather protection for permanent installations

### LED Matrix Specifications
```
GIF Matrix: 16x16 pixels = 256 LEDs
Text Matrix: 40x8 pixels = 320 LEDs
Total Power: ~576 LEDs × 60mA = 34.6A (theoretical max)
Typical Usage: ~30% brightness = 10A actual consumption
```

## 🔌 Wiring Diagram

### Pin Connections
```
ESP32 Pin  →  Component
─────────────────────────
GPIO 21    →  GIF Matrix Data In
GPIO 2    →  Text Matrix Data In
GPIO 4    →  SD Card CS (Chip Select)
GPIO 11    →  SD Card MOSI
GPIO 13    →  SD Card MISO  
GPIO 12    →  SD Card CLK
5V         →  LED Matrix Power (+)
GND        →  LED Matrix Power (-) & SD Card GND
3.3V       →  SD Card VCC
```

### Wiring Schematic
```
                    ESP32
                 ┌─────────┐
                 │    5V   ├─── Power Rail (+5V)
                 │   GND   ├─── Ground Rail
                 │  GPIO21 ├─── 470Ω ─── GIF Matrix Data
                 │  GPIO2 ├─── 470Ω ─── Text Matrix Data
                 │  GPIO4 ├─── SD Card CS
                 │  GPIO11 ├─── SD Card MOSI
                 │  GPIO13 ├─── SD Card MISO
                 │  GPIO12 ├─── SD Card CLK
                 │   3.3V  ├─── SD Card VCC
                 └─────────┘

Power Supply (5V/10A+)
     │
     ├─── 1000µF Capacitor ─── GND
     ├─── LED Matrix VCC
     └─── ESP32 5V Pin
```

### Matrix Connection Notes
- **Data Flow**: ESP32 → Matrix 1 → Matrix 2 → Matrix 3 → etc.
- **Power Injection**: Connect power every 100-150 LEDs for large installations
- **Ground**: Common ground for ESP32, LEDs, and power supply

## 💻 Software Setup

### Arduino IDE Setup

1. **Install ESP32 Board Support**
   ```
   File → Preferences → Additional Board Manager URLs:
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   
   Tools → Board → Boards Manager → Search "ESP32" → Install
   ```

2. **Install Required Libraries**
   ```
   Tools → Manage Libraries → Install:
   - Adafruit NeoPixel (latest)
   - Adafruit NeoMatrix (latest)
   - Adafruit GFX Library (latest)
   ```

3. **Board Configuration**
   ```
   Tools → Board → ESP32 Arduino → ESP32 Dev Module
   Tools → Upload Speed → 921600
   Tools → CPU Frequency → 240MHz
   Tools → Flash Size → 4MB
   Tools → Partition Scheme → Default 4MB
   ```

### Python Environment Setup

```bash
# Install Python dependencies
pip install Pillow

# Clone/download the project files
# Copy the gif_converter.py script to your working directory
```

## 🎨 Content Creation

### GIF Preparation

**Optimal GIF Specifications:**
- **Resolution**: Any size (auto-resized to 16x16)
- **Colors**: 256 colors max recommended
- **Frame Rate**: 10-20 FPS ideal
- **Duration**: 2-10 seconds per loop
- **File Size**: <2MB per GIF

**Creating GIFs:**
1. **From Video**: Use FFmpeg or online converters
2. **From Images**: Use GIMP, Photoshop, or online tools
3. **Pixel Art**: Use Aseprite, Piskel, or similar tools

### Text File Format

Create `.txt` files with this structure:
```
# Comments start with hash (optional)
First scrolling message
Second message here
Another line of text
# More comments allowed
Final message
```

**Text Guidelines:**
- **Length**: No hard limit, but 20-50 characters work best
- **Characters**: Standard ASCII recommended
- **Encoding**: UTF-8
- **Line Breaks**: Each line = separate scrolling message

### File Naming Convention

```
Your Project Folder/
├── gif1.bin          (Generated by converter)
├── text1.txt         (Your text file)
├── gif2.bin          (Generated by converter)
├── text2.txt         (Your text file)
├── ...
└── gif999.bin/text999.txt (Max supported)
```

**Important**: Pair numbers must match! `gif1.bin` works with `text1.txt`, etc.

## 📦 Installation Guide

### Step 1: Prepare Content

1. **Collect Your GIFs**
   ```bash
   # Place all .gif files in a folder
   mkdir my_display_content
   cd my_display_content
   cp ~/Downloads/*.gif .
   ```

2. **Convert GIFs to Binary Format**
   ```bash
   # Copy the converter script to your content folder
   cp gif_converter.py ./
   
   # Run the converter
   python gif_converter.py
   ```

3. **Create Text Files**
   ```bash
   # Create matching text files
   echo "Welcome to my display!" > text1.txt
   echo "Second animation text" > text2.txt
   echo "Add more messages here" > text3.txt
   ```

### Step 2: Prepare SD Card

1. **Format SD Card**
   - Format as FAT32
   - Use 32GB or smaller cards for best compatibility

2. **Copy Files to SD Card**
   ```
   SD Card Root/
   ├── gif1.bin
   ├── text1.txt
   ├── gif2.bin
   ├── text2.txt
   └── ... (all your pairs)
   ```

### Step 3: Hardware Assembly

1. **Wire According to Diagram** (see above)
2. **Double-check Connections**
   - Power: 5V to LED matrices
   - Data: GPIO pins through 470Ω resistors
   - SD Card: SPI connections
3. **Insert SD Card** into module
4. **Connect Power** (start with low brightness for testing)

### Step 4: Upload & Test

1. **Upload ESP32 Code**
   ```
   Arduino IDE → Open sketch → Select COM port → Upload
   ```

2. **Open Serial Monitor**
   ```
   Tools → Serial Monitor → 115200 baud
   ```

3. **Watch Startup Sequence**
   ```
   *** Starting matrix display system... ***
   Initializing LED matrices...
   Initializing SD card... SUCCESS!
   Scanning for GIF/text pairs...
   Found pair #1
   Found pair #2
   *** System ready! ***
   ```

### Step 5: Color Calibration

If colors appear wrong (white shows as green, etc.):

1. **Option 1: Modify Converter**
   ```python
   # In gif_converter.py, try different color orders:
   def rgb_to_grb(r, g, b):
       return r, g, b  # RGB (no conversion)
       # return g, r, b  # GRB (default)
       # return b, g, r  # BGR
   ```

2. **Option 2: Modify ESP32 Code**
   ```cpp
   // In ESP32 code, try different formats:
   NEO_RGB + NEO_KHZ800  // Instead of NEO_GRB
   ```

3. **Test & Iterate** until colors are correct

## 🎮 Usage & Commands

### Serial Commands

Connect to serial monitor (115200 baud) and use these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `status` | Show system information | `status` |
| `list` | List all SD card files | `list` |
| `pairs` | Show available content pairs | `pairs` |
| `pair=X` | Load specific pair number | `pair=3` |
| `next` | Skip to next pair | `next` |
| `clear` | Clear all displays | `clear` |
| `debug` | Toggle debug mode | `debug` |
| `rescan` | Refresh SD card content | `rescan` |

### Example Session
```
> status
*** Status Report ***
System ready: Yes
Current pair: 1 (1 of 5)
Current frame delay: 100 ms
Current message: 1 of 3
Text scroll complete: No
GIF loop count: 2

> pair=3
*** Loading pair #3 ***
Number of frames: 24
Frame delay: 150 ms
First message: Hello World!

> debug
Debug mode ON
```

### Auto-Cycling Behavior

1. **System loads pair #1**
2. **GIF plays continuously**
3. **Text scrolls through all messages**
4. **When text finishes, advances to next pair**
5. **Cycles through all pairs infinitely**

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 🚨 Green LED Stuck On
**Symptoms**: Single green LED stays on at power-up
**Solutions**:
```
1. Send 'clear' command via serial
2. Check power supply capacity
3. Verify ground connections
4. Wait for full startup sequence (2+ seconds)
```

#### 🚨 SD Card Not Found
**Symptoms**: "SD Card initialization failed!"
**Solutions**:
```
1. Check all SPI wiring connections
2. Try different SD card (Class 10, <32GB)
3. Reformat card as FAT32
4. Verify 3.3V power to SD module
5. Add pull-up resistors (10kΩ) to SPI lines if needed
```

#### 🚨 Wrong Colors Displayed
**Symptoms**: White appears green, red appears white, etc.
**Solutions**:
```
1. Modify gif_converter.py color function
2. Change NEO_GRB to NEO_RGB in ESP32 code
3. Test with simple solid color images first
4. Verify NeoPixel type (WS2812B vs SK6812)
```

#### 🚨 No Animation/Static Display
**Symptoms**: GIFs don't animate, show single frame
**Solutions**:
```
1. Check GIF file has multiple frames
2. Verify frame delay values in serial output
3. Test with known-good animated GIF
4. Increase frame delay if animation too fast
```

#### 🚨 Text Not Scrolling
**Symptoms**: Text appears but doesn't move
**Solutions**:
```
1. Check text file format (simple ASCII)
2. Verify messages loaded in serial output
3. Test with shorter text strings
4. Check TEXT_SCROLL_DELAY setting
```

### Debug Process

1. **Serial Monitor First**
   ```
   Always check serial output for error messages
   Use 'status' command to verify system state
   ```

2. **Test Individual Components**
   ```
   Use 'clear' command to test LED control
   Use 'list' command to verify SD card access
   Use 'pairs' to check content detection
   ```

3. **Isolate Problems**
   ```
   Test with single GIF/text pair first
   Use simple solid-color GIFs for color testing
   Create short text messages for scroll testing
   ```

### Performance Optimization

```cpp
// Adjust these values in ESP32 code for better performance:
#define BRIGHTNESS 20           // Lower = less power, dimmer
#define TEXT_SCROLL_DELAY 100   // Higher = slower scrolling
#define DEFAULT_GIF_FRAME_DELAY 50  // Higher = slower animation
```

## 📁 Project Structure

```
ESP32-LED-Matrix-Display/
├── README.md                    # This file
├── esp32_code/
│   └── dual_matrix_controller.ino  # Main ESP32 Arduino sketch
├── python_tools/
│   └── gif_converter.py         # GIF to binary converter
├── examples/
│   ├── sample_gifs/             # Example GIF files
│   ├── sample_texts/            # Example text files
│   └── wiring_photos/           # Assembly reference photos
├── docs/
│   ├── HARDWARE.md              # Detailed hardware guide
│   ├── TROUBLESHOOTING.md       # Extended troubleshooting
│   └── API.md                   # Serial command reference
└── tools/
    ├── color_test.ino           # Color calibration sketch
    └── sd_card_test.ino         # SD card diagnostics
```

## 🎯 Advanced Features

### Custom Matrix Layouts

Modify `getGifIndex()` function for different matrix arrangements:
```cpp
// For different 16x16 matrix wiring patterns
int getGifIndex(int row, int col) {
    // Customize based on your matrix layout
    // Examples: serpentine, tile-based, custom shapes
}
```

### Multiple Display Support

```cpp
// Add more matrices by defining additional pins
#define MATRIX3_PIN 19
#define MATRIX4_PIN 20
// Initialize additional NeoMatrix objects
```


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Adafruit** - For excellent NeoPixel libraries
- **ESP32 Community** - For Arduino core support

## 📚 Additional Resources

### Learning Resources
- [ESP32 Getting Started Guide](https://docs.espressif.com/projects/esp32/)
- [NeoPixel Überguide](https://learn.adafruit.com/adafruit-neopixel-uberguide)
- [Arduino ESP32 Reference](https://github.com/espressif/arduino-esp32)

### Related Projects
- [LED Matrix Games](https://github.com/topics/led-matrix)
- [ESP32 Art Projects](https://github.com/topics/esp32-art)
- [Digital Signage Solutions](https://github.com/topics/digital-signage)

### Community Support
- [ESP32 Reddit Community](https://reddit.com/r/esp32)
- [Arduino Forums](https://forum.arduino.cc/)
- [Adafruit Discord](https://discord.gg/adafruit)

---

**Made with ❤️ for the Maker Community**

*If this project helped you, please ⭐ star the repository and share your builds!*
