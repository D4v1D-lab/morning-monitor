#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent


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
                run([sys.executable, "-m", "src.jira_client"])
            case "2":
                run([sys.executable, "-m", "src.email_notifier"])
            case "3":
                print()
                print("╔══════════════════════════════════════════╗")
                print("║   \u23f0 Scheduler                           \u2551")
                print("╠══════════════════════════════════════════╣")
                print("║  This will start the scheduler in your   \u2551")
                print("║  terminal and run forever. You will NOT  \u2551")
                print("║  see the launcher menu while it runs.    \u2551")
                print("║                                          \u2551")
                print("║  To stop the scheduler and return to     \u2551")
                print("║  the launcher menu, press Ctrl+C.        \u2551")
                print("║                                          \u2551")
                print("║  Continue? (y/n):                        \u2551")
                print("╚══════════════════════════════════════════╝")
                if input().strip().lower() == "y":
                    run([sys.executable, "-m", "src.scheduler"])
            case "4":
                run([sys.executable, "-m", "pytest", "tests/", "-v"])
            case "5":
                run([sys.executable, "-m", "src.jira_client"])
                run([sys.executable, "-m", "src.email_notifier"])
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
