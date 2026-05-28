#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent


def print_menu():
    print()
    print("╔══════════════════════════════════╗")
    print("║   🌅 Morning Monitor - Launcher  ║")
    print("╠══════════════════════════════════╣")
    print("║  1) View Jira tickets            ║")
    print("║  2) Send email report            ║")
    print("║  3) Start scheduler              ║")
    print("║  4) Run tests                    ║")
    print("║  5) Run all in order             ║")
    print("║                                  ║")
    print("║  q) Quit                         ║")
    print("╚══════════════════════════════════╝")


def run(cmd):
    print()
    proc = subprocess.Popen(cmd, cwd=PROJECT_DIR)
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    print()


def main():
    while True:
        print_menu()
        choice = input("Select an option: ").strip().lower()

        match choice:
            case "1":
                run([sys.executable, "jira_client.py"])
            case "2":
                run([sys.executable, "email_notifier.py"])
            case "3":
                print()
                print("╔══════════════════════════════════════════╗")
                print("║   ⏰ Scheduler                           ║")
                print("╠══════════════════════════════════════════╣")
                print("║  This will start the scheduler in your   ║")
                print("║  terminal and run forever. You will NOT  ║")
                print("║  see the launcher menu while it runs.    ║")
                print("║                                          ║")
                print("║  To stop the scheduler and return to     ║")
                print("║  the launcher menu, press Ctrl+C.        ║")
                print("║                                          ║")
                print("║  Continue? (y/n):                        ║")
                print("╚══════════════════════════════════════════╝")
                if input().strip().lower() == "y":
                    run([sys.executable, "scheduler.py"])
            case "4":
                run([sys.executable, "-m", "pytest", "tests/", "-v"])
            case "5":
                run([sys.executable, "jira_client.py"])
                run([sys.executable, "email_notifier.py"])
                run([sys.executable, "-m", "pytest", "tests/", "-v"])
            case "q":
                print("\nGoodbye!")
                break
            case _:
                print(f"\nUnknown option: {choice}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
