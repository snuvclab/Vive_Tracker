import sys
import time
import argparse
from track import vive_tracker

def parse_arguments():
    parser = argparse.ArgumentParser(description="Vive Tracker Pose Data Display")
    parser.add_argument("-f", "--frequency", type=float, default=30.0,
                        help="Frequency of tracker data updates (in Hz). Default: 30 Hz")
    return parser.parse_args()

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
    # Parse command line arguments
    args = parse_arguments()

    # Calculate interval based on the specified frequency
    interval = 1 / args.frequency

    # Initialize Vive Tracker and print discovered objects
    v_tracker = vive_tracker()
    v_tracker.print_discovered_objects()

    # Print tracker data
    tracker_1 = v_tracker.devices["tracker_1"]
    print_tracker_data(tracker_1, interval)

if __name__ == "__main__":
    main()
