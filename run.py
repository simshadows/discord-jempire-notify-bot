import multiprocessing as mp
import time

import clepbot

def run():
    while True:
        proc = mp.Process(target=clepbot.run, daemon=True)
        proc.start()
        proc.join()
        ret = proc.exitcode
        print("Bot terminated. Return value: " + str(ret))
        print("Reconnecting in 10 seconds.")
        time.sleep(10)
        print("Attempting to reconnect...")

if __name__ == '__main__':
    run()
