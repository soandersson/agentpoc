#!/usr/bin/env python3
"""
Command-line interface for running agent examples.

Usage:
    python run_example.py simple         # Run simple reactive agent
    python run_example.py learning       # Run Q-learning agent
    python run_example.py --help         # Show help
"""

import sys
import os

# Add src to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def show_help():
    """Display help information."""
    print(__doc__)
    print("\nAvailable examples:")
    print("  simple    - Simple reactive agent (thermostat)")
    print("  learning  - Q-learning agent (grid world)")
    print("\nOptions:")
    print("  --help    - Show this help message")
    print("  -h        - Show this help message")

def run_simple():
    """Run the simple reactive agent example."""
    from examples import simple_agent
    simple_agent.main()

def run_learning():
    """Run the Q-learning agent example."""
    from examples import learning_agent_example
    learning_agent_example.main()

def main():
    """Main entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        show_help()
        return
    
    example = sys.argv[1].lower()
    
    if example == 'simple':
        run_simple()
    elif example == 'learning':
        run_learning()
    else:
        print(f"Error: Unknown example '{example}'")
        print("\nRun 'python run_example.py --help' for available examples")
        sys.exit(1)

if __name__ == "__main__":
    main()
