import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_typing_stats(file_path="typing_stats.json"):
    """Load and process typing statistics from JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def process_stats(stats_data):
    """Process raw stats into analyzable format."""
    peek_stats = []
    
    for char, stats in stats_data['peek'].items():
        if stats['attempts'] > 0:
            avg_time = sum(stats['times']) / len(stats['times']) if stats['times'] else 0
            error_rate = stats['errors'] / stats['attempts'] if stats['attempts'] > 0 else 0
            peek_stats.append({
                'character': char,
                'attempts': stats['attempts'],
                'avg_time': avg_time,
                'error_rate': error_rate * 100  # Convert to percentage
            })
    
    return peek_stats

def create_visualizations(stats):
    """Create and display visualizations."""
    # Sort stats for different views
    most_attempted = sorted(stats, key=lambda x: x['attempts'], reverse=True)[:10]
    slowest = sorted(
        [s for s in stats if s['attempts'] >= 2], 
        key=lambda x: x['avg_time'], 
        reverse=True
    )[:10]
    highest_error_rate = sorted(
        [s for s in stats if s['attempts'] >= 2],
        key=lambda x: x['error_rate'],
        reverse=True
    )[:10]

    # Set up the figure with three subplots
    plt.style.use('seaborn')
    fig = plt.figure(figsize=(15, 12))
    fig.suptitle('Typing Statistics Analysis', fontsize=16, y=0.95)

    # 1. Most Attempted Characters
    ax1 = plt.subplot(311)
    chars = [s['character'] for s in most_attempted]
    attempts = [s['attempts'] for s in most_attempted]
    error_rates = [s['error_rate'] for s in most_attempted]
    
    x = np.arange(len(chars))
    width = 0.35
    
    ax1.bar(x - width/2, attempts, width, label='Attempts', color='skyblue')
    ax1.bar(x + width/2, error_rates, width, label='Error Rate (%)', color='lightcoral')
    ax1.set_title('Most Practiced Characters')
    ax1.set_xticks(x)
    ax1.set_xticklabels(chars)
    ax1.legend()
    ax1.set_ylabel('Count / Percentage')
    
    # Add value labels on the bars
    for i, v in enumerate(attempts):
        ax1.text(i - width/2, v, str(v), ha='center', va='bottom')
    for i, v in enumerate(error_rates):
        ax1.text(i + width/2, v, f'{v:.1f}%', ha='center', va='bottom')

    # 2. Slowest Characters
    ax2 = plt.subplot(312)
    chars = [s['character'] for s in slowest]
    times = [s['avg_time'] for s in slowest]
    
    bars = ax2.bar(chars, times, color='lightseagreen')
    ax2.set_title('Slowest Characters (Average Time)')
    ax2.set_ylabel('Seconds')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}s', ha='center', va='bottom')

    # 3. Highest Error Rates
    ax3 = plt.subplot(313)
    chars = [s['character'] for s in highest_error_rate]
    errors = [s['error_rate'] for s in highest_error_rate]
    
    bars = ax3.bar(chars, errors, color='salmon')
    ax3.set_title('Highest Error Rates (≥2 attempts)')
    ax3.set_ylabel('Error Rate (%)')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom')

    # Adjust layout and display
    plt.tight_layout()
    plt.show()

    # Print summary statistics
    print("\nKey Insights:")
    print("\nMost Challenging Characters (≥2 attempts):")
    for stat in highest_error_rate[:3]:
        print(f"'{stat['character']}': {stat['error_rate']:.1f}% error rate")
        
    print("\nSlowest Characters (≥2 attempts):")
    for stat in slowest[:3]:
        print(f"'{stat['character']}': {stat['avg_time']:.2f}s average")
        
    print("\nMost Practiced Characters:")
    for stat in most_attempted[:3]:
        print(f"'{stat['character']}': {stat['attempts']} attempts, "
              f"{stat['error_rate']:.1f}% error rate")

def main():
    # Check if stats file exists
    if not Path("typing_stats.json").exists():
        print("Error: typing_stats.json not found in current directory")
        return
        
    # Load and process data
    data = load_typing_stats()
    stats = process_stats(data)
    
    # Create visualizations
    create_visualizations(stats)

if __name__ == "__main__":
    main()
