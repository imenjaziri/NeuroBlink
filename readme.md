# NeuroBlink
NeuroBlink is a real-time eye-blink recognition system designed to assist individuals with neurodegenerative diseases in expressing themselves through simple, intuitive interactions.

# 💡 Inspiration
This project was inspired by remarkable individuals such as Stephen Hawking and Jean-Dominique Bauby, who, despite severe physical limitations, retained full intellectual capacity. NeuroBlink aims to empower those facing similar challenges by offering an accessible communication method based on eye-blinking detection.

# 🧠 Project Overview
NeuroBlink enables users to input and display messages through intentional eye blinks. It detects predefined Morse-like blink patterns in real time and sends the decoded text to an STM32F746 Discovery board, where it is displayed on an integrated LCD-TFT screen using TouchGFX.

# 🔧 Tools & Technologies
Software:
STM32CubeIDE – Firmware development for STM32.

TouchGFX Designer – UI design and display integration.

PyCharm – Python development environment for PC-side processing.

Hardware:
STM32F746G-DISCO – Development board with LCD-TFT display.

Libraries & Frameworks:
OpenCV – For video capture and image processing.

dlib – For facial landmark detection.

Facemark API – Used to track and analyze eye landmarks for blink detection.

# 📷 Features
Real-time video stream processing.

Accurate eye-blink detection using facial landmarks.

Morse-like pattern recognition via blinking.

Serial communication with STM32 board.

Display of decoded messages on LCD screen.

🚀 Future Work
This project is always under development for future enhancements and features.
I'm open to any suggestion !
