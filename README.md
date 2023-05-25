# Screen Writer

This Python project uses the PyQt5 library to create a simple, topmost overlay window with specified text. This overlay window is frameless and has a translucent background. It can be used to display brief notifications or messages on the desktop.

## Features
- **Overlay Window**: Creates a simple, translucent overlay window with the specified text.
- **Timer**: The window will auto-close after the specified amount of seconds.
- **Hotkey Support**: The window can be manually closed by pressing the 'Q' key.
- **Multi-processing**: The window can be displayed in a separate process.
- **Update Text**: Use queue to update text.

## How to Use

### Function Definitions
1. `OverlayWindow(text: str, timer: Optional[int]) -> None`: Initializes and configures the overlay window.
2. `write_to_screen(text: str, timer: Optional[int]) -> None`: Initializes a QApplication, creates an OverlayWindow, and starts the app's event loop.
3. `write_to_screen_process(text: str, timer: Optional[int]) -> None`: Starts the `write_to_screen` function in a separate process.

### Example Usage
```python
# Display "Hello, world!" for 5 seconds
write_to_screen_process("Hello, world!", 5)
```

```python
# Use returned queue to update text
queue = write_to_screen_process("Hello, world!", 60, True)
queue.put("Goodbye, world!")
```

### Dependencies
This project requires PyQt5. Install it with pip:
```python
pip install PyQt5
```
Remember, this is a simple GUI application. There are endless possibilities for what you can do by extending the provided classes or adding new features. Happy coding!
