## Developer Notes

### Handling Terminal Freeze from Background Thread Errors

If the terminal becomes stuck due to a background thread crash (e.g., `AttributeError` in `WhisperRecognizer`), and `Ctrl+C` doesn't fully stop the program, use one of the following methods:

#### Method 1: Force kill the running Python process
```bash
# Press Ctrl + Z to suspend the program
# Then type:
kill %1
```
This will terminate the background process and return control to your terminal.

#### Method 2: Restart the terminal
- Close the current terminal tab or window
- Open a new terminal session
- Navigate to the project directory and re-run your script
