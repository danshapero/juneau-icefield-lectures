import csv
from datetime import datetime
import pathlib
import numpy as np
import matplotlib.pyplot as plt

def extract_data(input_file, start_time, end_time):
    lines = input_file.readlines()
    index = lines.index("Date/Time,Unit,Value\n") + 1
    reader = list(csv.reader(lines[index:]))

    fmt = "%m/%d/%y %I:%M:%S %p"
    times = np.array([datetime.strptime(line[0], fmt) for line in reader])
    temps = np.array([float(line[-1]) for line in reader])

    indices = (start_time <= times) & (times <= end_time)
    return times[indices], temps[indices]

if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.set_xlabel("Time/date")
    ax.set_ylabel("Temperature (${}^\circ$C)")

    start_time = datetime(year=2023, month=7, day=21, hour=16, minute=5)
    end_time = datetime(year=2023, month=7, day=22, hour=16, minute=5)
    csv_files = pathlib.Path("./").glob("*.csv")
    for filename in csv_files:
        with open(filename, "r") as input_file:
            times, temps = extract_data(input_file, start_time, end_time)
        ax.plot(times, temps, label=f"{str(filename)[5:7]}")
    ax.legend()
    plt.show()
