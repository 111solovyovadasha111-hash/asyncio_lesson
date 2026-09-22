
import sys
import asyncio
import time
import subprocess


def run_script(script_name, arg):
    start_time = time.time()

    result = subprocess.run(
        [sys.executable, script_name, arg],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )

    return time.time() - start_time

def main():
    word = sys.argv[1] if len(sys.argv) > 1 else "музыка"
    time_sync= run_script("phil.py", word)
    print(f"обычная реализация отработала за {time_sync:.2f}")

    async_time = run_script("async_phil.py", word)
    print(f"асинхронная реализация отработала за {async_time:.2f}")

if __name__ == '__main__':
    main()


