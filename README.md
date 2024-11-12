# Special Character Typing Trainer 🎯⌨️

A command-line application designed to improve your typing speed and accuracy with special characters. Features two modes - regular (peek) and pro (no-peek) - to help you master those tricky characters like `!@#$%^&*()_+}{][":';?></.,=-~``.

## Features

- 🔄 Two practice modes:
  - **Regular Mode**: Practice with keyboard visibility
  - **Pro Mode**: Touch typing practice with fun challenges
- 📊 Comprehensive statistics tracking:
  - Per-character error rates
  - Typing speed measurements
  - Progress tracking over time
- 🎯 Adaptive practice:
  - Focuses on your challenging characters
  - Adjusts to your skill level
- 📈 Detailed performance visualization:
  - Error rate analysis
  - Speed comparisons
  - Practice distribution

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/special-char-typing-trainer.git
cd special-char-typing-trainer
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

## Usage

### Training Mode

Run the typing trainer:
```bash
python typing_trainer.py
```

1. Choose your mode:
   - `1` for Regular Mode (peeking allowed)
   - `2` for Pro Mode (no peeking!)
2. Enter desired practice string length (5-30 characters)
3. Type the displayed characters
4. View your results
5. Press any key to continue or ESC to exit

### Statistics Visualization

Visualize your performance:
```bash
python visualize_stats.py
```

This will generate comprehensive visualizations showing:
- Most practiced characters
- Error rates
- Average typing speeds
- Performance comparisons between modes

## Files

- `typing_trainer.py`: Main training application
- `visualize_stats.py`: Statistical analysis and visualization tool
- `typing_stats.json`: Your progress data (automatically generated)

## Data Storage

Your typing statistics are stored in `typing_stats.json` and include:
- Attempt counts
- Error rates
- Typing speeds
- Mode-specific performance data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the need to master special characters in programming
- Built with Python's curses library for terminal interaction
- Visualization powered by matplotlib and seaborn
