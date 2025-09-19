# Focus-Flasher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, customizable desktop application built with Python and Tkinter to help improve focus or serve as a periodic reminder by flashing the screen.

## 📖 Description

Focus Flasher is a lightweight tool designed to interrupt your workflow with a full-screen color flash at user-defined intervals. This can be used for various purposes, such as a Pomodoro-style work timer, a reminder to look away from the screen (20-20-20 rule), or as a general focus training aid. The application is self-contained in a single Python script and requires no external libraries beyond the standard Python installation.

## ✨ Features

-   **Customizable Repetitions:** Set the exact number of times you want the screen to flash.
-   **Adjustable Delay:** Control the waiting period (in seconds) between each flash.
-   **Variable Duration:** Define how long (in seconds) each flash remains on the screen.
-   **Color Picker:** Choose any color for the flash using a native color chooser dialog.
-   **Real-time Status:** A status bar keeps you updated on the current state, including a countdown timer for the next flash.
-   **Start/Stop Control:** Easily start and stop sessions at any time.
-   **Modern UI:** Uses `ttk` for a cleaner, more modern interface.
-   **Lightweight & Cross-Platform:** Built with Python's standard Tkinter library, it runs on Windows, macOS, and Linux without extra dependencies.

## 🚀 Getting Started

### Prerequisites

-   Python 3.x (Tkinter is included in most standard Python distributions)

### Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/azario0/Focus-Flasher.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd Focus-Flasher
    ```

3.  **Run the application:**
    *(Assuming you saved the code as `focus_flasher.py`)*
    ```bash
    python focus_flasher.py
    ```

## ⚙️ How to Use

The interface is straightforward:

1.  **Repetitions:** Enter the total number of times you want the screen to flash. For a continuous session, enter a very large number (e.g., `10000`).
2.  **Delay (seconds):** Set the time to wait *between* each flash. For example, a value of `45` means there will be a 45-second pause after one flash ends and before the next one begins.
3.  **Duration (seconds):** Set how long each flash will cover the screen. A value of `0.1` is a quick flash, while `1` would be a full second.
4.  **Flash Color:** Click the "Choose..." button to open a color picker and select your desired color for the flash. A preview is shown next to the button.
5.  **Start Session:** Click to begin the cycle. The input fields will be disabled.
6.  **Stop Session:** Click this button (which becomes active during a session) to interrupt the cycle and reset the application.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
