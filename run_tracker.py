import sys
import time
from track import vive_tracker

def get_interval():
    # Check the number of command line arguments
    args_count = len(sys.argv)
    if args_count == 1:
        # If there's no input argument, use the default interval (30 Hz) 
        return 1/30
    elif args_count == 2:
        # If there's one input argument, use it as the frequency (in Hz)
        return 1 / float(sys.argv[1])
    else:
        print("Invalid number of arguments")
        return None

def print_tracker_data(tracker, interval):
    # Continuously print tracker pose data at the specified interval
    while True:
        start_time = time.time()

        # Get pose data for the tracker device and format as a string
        pose_data = " ".join(["%.4f" % val for val in tracker.get_pose_euler()])

        # Print pose data in the same line
        print("\r" + pose_data, end="")

        # Calculate sleep time to maintain the desired interval
        sleep_time = interval - (time.time() - start_time)

        # Sleep if necessary
        if sleep_time > 0:
            time.sleep(sleep_time)

def main():
    # Initialize Vive Tracker and print discovered objects
    v_tracker = vive_tracker()
    v_tracker.print_discovered_objects()

    # Get interval based on command line arguments
    interval = get_interval()

    # If the interval is valid, print tracker data
    if interval:
        tracker_1 = v_tracker.devices["tracker_1"]
        print_tracker_data(tracker_1, interval)

if __name__ == "__main__":
    main()
