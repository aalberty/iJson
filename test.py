import os
import curses

def file_explorer(stdscr):
    # Hide cursor and clear screen
    curses.curs_set(0)
    stdscr.clear()

    # Starting path
    current_path = os.getcwd()
    selected_index = 0

    while True:
        # Get list of files/folders in the current directory
        files = os.listdir(current_path)
        files.insert(0, "..")  # Option to go up to parent directory

        # Ensure selected index is within range
        selected_index = max(0, min(selected_index, len(files) - 1))

        # Clear screen
        stdscr.clear()

        # Display the current path at the top
        stdscr.addstr(0, 0, f"Current Directory: {current_path}", curses.color_pair(1))

        # Display files and highlight the selected file
        for i, file in enumerate(files):
            # Highlight the current selection
            if i == selected_index:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(i + 2, 0, file)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, file)

        # Refresh the screen to show the changes
        stdscr.refresh()

        # Wait for user input
        key = stdscr.getch()

        # Handle navigation
        if key == curses.KEY_UP:
            selected_index = (selected_index - 1) % len(files)
        elif key == curses.KEY_DOWN:
            selected_index = (selected_index + 1) % len(files)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # Enter directory or open file
            selected_file = files[selected_index]
            selected_path = os.path.join(current_path, selected_file)

            if os.path.isdir(selected_path):
                # Navigate into the selected directory
                current_path = selected_path
                selected_index = 0  # Reset index for new directory
            elif selected_file == "..":
                # Go up one directory if not at the root
                current_path = os.path.dirname(current_path)
                selected_index = 0
            else:
                stdscr.addstr(len(files) + 3, 0, f"Selected file: {selected_file}")
                stdscr.refresh()
                stdscr.getch()
        elif key == ord('q'):
            # Press 'q' to quit the program
            break

# Run the curses application
curses.wrapper(file_explorer)

