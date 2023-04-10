import re
import csv
from collections import defaultdict

user_stats = defaultdict(lambda: {"INFO": 0, "ERROR": 0})
error_stats = defaultdict(int)

with open("syslog.log") as f:
    for line in f:
        line = line.strip()
        match = re.search(r"\((.*?)\).* (INFO|ERROR) (.*)", line)
        if match:
            username, level, message = match.groups()
            user_stats[username][level] += 1
            if level == "ERROR":
                error_stats[message] += 1

with open("user_statistics.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Username", "INFO", "ERROR"])
    for username, stats in sorted(user_stats.items()):
        writer.writerow([username, stats["INFO"], stats["ERROR"]])

with open("error_message.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Error", "Count"])
    for error, count in sorted(error_stats.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([error, count])
