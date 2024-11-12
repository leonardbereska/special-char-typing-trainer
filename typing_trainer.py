import random
import time
import json
import os
import curses
from collections import defaultdict
from datetime import datetime
import statistics

class TypingStats:
    def __init__(self, stats_file="typing_stats.json"):
        self.stats_file = stats_file
        # Separate statistics for peeking and no-peeking modes
        self.char_stats = {
            'peek': defaultdict(lambda: {"attempts": 0, "errors": 0, "times": []}),
            'no_peek': defaultdict(lambda: {"attempts": 0, "errors": 0, "times": []})
        }
        self.load_stats()
    
    def load_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                stats = json.load(f)
                for mode in ['peek', 'no_peek']:
                    if mode in stats:
                        for char, data in stats[mode].items():
                            self.char_stats[mode][char].update(data)

    def save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(dict(self.char_stats), f, indent=2)

    def update_char_stat(self, char, time_taken, is_error, mode):
        self.char_stats[mode][char]["attempts"] += 1
        if is_error:
            self.char_stats[mode][char]["errors"] += 1
        self.char_stats[mode][char]["times"].append(time_taken)
        self.save_stats()

    def get_difficult_chars(self, all_chars, mode):
        """Return characters sorted by difficulty (error rate) for given mode"""
        difficulties = {}
        for char in all_chars:
            stats = self.char_stats[mode][char]
            if stats["attempts"] > 0:
                error_rate = stats["errors"] / stats["attempts"]
                avg_time = statistics.mean(stats["times"]) if stats["times"] else float('inf')
                difficulties[char] = error_rate * avg_time
            else:
                difficulties[char] = float('inf')  # Prioritize untested chars
        return sorted(difficulties.items(), key=lambda x: x[1], reverse=True)

class TypingTrainer:
    def __init__(self):
        self.special_chars = "!@#$%^&*()_+}{][\"\\:';?></.,=-~`0123456789"
        self.stats = TypingStats()
        
    def generate_practice_string(self, length=10, mode='peek'):
        """Generate practice string with emphasis on difficult characters for given mode"""
        difficult_chars = self.stats.get_difficult_chars(self.special_chars, mode)
        weights = [1/(i+1) for i in range(len(difficult_chars))]
        chars = [char for char, _ in difficult_chars]
        return ''.join(random.choices(chars, weights=weights, k=length))

    def run(self, stdscr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        NO_PEEK_MESSAGES = [
            "Pinky promise no peeking! 🙈",
            "Eyes up here! Keyboard is lava! 🌋",
            "Touch typing mode: Your keyboard just turned invisible! 😎",
            "Warning: Looking at keyboard causes bad luck! 🍀",
            "Jedi mode activated: Trust in the Force! ⭐"
            "No peeking! I'm watching you! 👀"
            "Special characters are special! No peeking! 🎭"
            "No peeking! You got this! 💪"
            "<Insert motivational message here> 🚀"
            "Look at the screen only! 📺"
        ]

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Special Character Typing Trainer")
            stdscr.addstr(1, 0, "Choose your mode:")
            stdscr.addstr(2, 0, "1) Regular Mode (Peeking allowed)")
            stdscr.addstr(3, 0, "2) Pro Mode (No peeking!)")
            stdscr.addstr(4, 0, "ESC to exit")
            stdscr.refresh()

            # Get mode selection
            while True:
                key = stdscr.getch()
                if key == 27:  # ESC
                    return
                # elif key in [49, 50]:  # 1 or 2
                else:
                    mode = 'no_peek' if key == 50 else 'peek'
                    break

            if mode == 'no_peek':
                stdscr.clear()
                message = random.choice(NO_PEEK_MESSAGES)
                stdscr.addstr(0, 0, message, curses.color_pair(4))
                stdscr.addstr(2, 0, "Press any key when ready...")
                stdscr.refresh()
                stdscr.getch()

            stdscr.clear()
            stdscr.addstr(0, 0, "Special Character Typing Trainer")
            stdscr.addstr(1, 0, "Press ESC to exit, or select length (5-100): ")
            stdscr.refresh()

            # Get practice string length
            try:
                length = ''
                while True:
                    key = stdscr.getch()
                    if key == 27:  # ESC
                        return
                    elif key == curses.KEY_ENTER or key == 10:
                        length = max(5, min(100, int(length)))
                        break
                    elif 48 <= key <= 57:  # Numbers
                        length += chr(key)
                        stdscr.addch(key)
                    # if enter is pressed, break
                    elif key == 10: 
                        if length:
                            length = max(5, min(100, int(length)))
                        else:
                            length = 10
            except ValueError:
                length = 10

            # Generate and display practice string
            target = self.generate_practice_string(length, mode)
            typed = ''
            errors = 0
            start_time = time.time()
            char_times = {}

            while len(typed) < len(target):
                stdscr.clear()
                stdscr.addstr(0, 0, "Type the following characters:")
                stdscr.addstr(1, 0, target, curses.color_pair(1)) 
                stdscr.addstr(2, 0, target)
                # Display number of errors
                max_errors = 3
                stdscr.addstr(3, 0, f"Errors: {errors}/{max_errors}")
                
                # Display typed characters with color coding
                for i, char in enumerate(typed):
                    color = curses.color_pair(1) if char == target[i] else curses.color_pair(2)
                    stdscr.addstr(2, i, char, color)
                
                # Show cursor position
                if len(typed) < len(target):
                    stdscr.addstr(2, len(typed), "_", curses.color_pair(3))
                
                stdscr.refresh()

                # Get input and measure time
                char_start = time.time()
                key = stdscr.getch()
                if key == 27:  # ESC
                    return
                
                char = chr(key)
                char_time = time.time() - char_start
                char_times[len(typed)] = char_time
                
                typed += char
                if char != target[len(typed)-1]:
                    errors += 1
                    # break after 3 errors
                    # display errors in red
                    # display number of errors
                    if errors == max_errors:
                        break

            # Session complete - update statistics
            total_time = time.time() - start_time
            
            for i, (char, time_taken) in enumerate(zip(target, char_times.values())):
                is_error = typed[i] != char
                self.stats.update_char_stat(char, time_taken, is_error, mode)

            # Display results
            wpm = (len(target) / 5) / (total_time / 60)
            accuracy = (len(target) - errors) / len(target) * 100
            
            stdscr.clear()
            stdscr.addstr(0, 0, f"Results:")
            stdscr.addstr(2, 0, f"Speed: {wpm:.1f} WPM")
            stdscr.addstr(3, 0, f"Accuracy: {accuracy:.1f}%")
            stdscr.addstr(4, 0, f"Time: {total_time:.1f} seconds")
            stdscr.addstr(6, 0, "Press any key to continue, ESC to exit")
            stdscr.refresh()

            if stdscr.getch() == 27:  # ESC
                return

def main():
    trainer = TypingTrainer()
    curses.wrapper(trainer.run)

if __name__ == "__main__":
    main()
