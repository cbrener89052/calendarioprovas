"""Job worker scaffold — polls jobs table (T5 implements pipeline)."""

import os
import time


def run() -> None:
    poll_interval = int(os.getenv("WORKER_POLL_INTERVAL", "5"))
    print(f"calendarioprovas worker started (poll={poll_interval}s)", flush=True)
    while True:
        time.sleep(poll_interval)


if __name__ == "__main__":
    run()
