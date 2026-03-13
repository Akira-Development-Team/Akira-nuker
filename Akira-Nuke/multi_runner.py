import os
import sys
import subprocess


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(base_dir, "main.py")

    raw_tokens = input("Enter bot tokens (comma-separated): ").strip()
    if not raw_tokens:
        print("No tokens provided.")
        return

    server_ids = input("server id(s) or all: ").strip()
    if not server_ids:
        print("No server IDs provided.")
        return

    action = input("menu action code (e.g. 01 for Nuke, 33 for Spam): ").strip()
    if not action:
        print("No action code provided.")
        return

    tokens = [t.strip() for t in raw_tokens.split(",") if t.strip()]
    if not tokens:
        print("No valid tokens parsed.")
        return

    procs = []
    for idx, token in enumerate(tokens, start=1):
        env = os.environ.copy()
        env["VOIDNUKE_TOKEN"] = token
        env["VOIDNUKE_SERVERS"] = server_ids
        env["VOIDNUKE_ACTION"] = action
        print(f"Starting bot #{idx}...")
        procs.append(
            subprocess.Popen(
                [sys.executable, main_path],
                env=env,
            )
        )

    print(f"Started {len(procs)} bot instance(s). They will run concurrently.")

    # wait for all child processes to finish
    for p in procs:
        try:
            p.wait()
        except KeyboardInterrupt:
            print("Stopping all child bots...")
            p.terminate()


if __name__ == "__main__":
    main()

