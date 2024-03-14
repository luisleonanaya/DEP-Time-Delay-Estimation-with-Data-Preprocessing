

def clear_frame(frame):
    # The next if statement checks if the frame is not None and has children widgets before clearing
    if frame is not None and frame.winfo_children():
        for widget in frame.winfo_children():
            widget.destroy()
        #print(f"Cleared all widgets from {frame}")
    elif frame is None:
        pass
        #print("Attempted to clear a frame that is None.")
    else:
        pass
        #print(f"No widgets to clear in {frame}")
