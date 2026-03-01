# run_both_multiprocessing.py
import multiprocessing
import subprocess
import time

def run_script(script_name):
    # Use subprocess to call another Python script
    subprocess.run(["python3", script_name])

if __name__ == "__main__":
    # Create a process for each script
    p1 = multiprocessing.Process(target=run_script, args=("tommy_b_openai_realtime.py",))
    p2 = multiprocessing.Process(target=run_script, args=("tommy_b_eyes.py",))

    # Start both processes
    p1.start()
    time.sleep(2)
    p2.start()

    # Wait for both to finish
    p1.join()
    p2.join()

    #print("Both scripts have finished.")