#!/usr/bin/env python3

import re
import operator
import csv


error_store = {}
user_store = {}


def convert_to_csv(file_name, data):
  with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(data)
    file.close()


def analyze_log(log):
  """Verifies the log argument and then adds it to the corresponding dictionary"""
  regex_user = r"\(([a-z\.]*)\)"
  regex_error = r"ERROR ([\w ']*) "
  user = re.search(regex_user, log)
  error = re.search(regex_error, log)

  if user.group(1) not in user_store:
      user_store[user.group(1)] = [0, 0]

  if "INFO" in log:
    user_store[user.group(1)][0] += 1

  if "ERROR" in log:
    user_store[user.group(1)][1] += 1
    if error.group(1) not in error_store:
      error_store[error.group(1)] = 0
    error_store[error.group(1)] += 1


def main(file):
  """Process the argument file with analyze_log function and turn the contents
     of "error_store" and "user_store" dictionaries into a CSV files"""
  user_statistics = [["Username", "INFO", "ERROR"]]
  error_message = [["Error", "Count"]]

  # Process the data and turn it into a dict
  with open(file) as f:
    for line in f.readlines():
      log = line.strip()
      analyze_log(log)
    f.close()

  sorted_user_store = sorted(user_store.items())
  sorted_error_store = sorted(error_store.items(), key=operator.itemgetter(1), reverse=True)

  # Convert the sorted data from dictionary into a list of lists
  for username, value in sorted_user_store:
    info, error = value[0], value[1]
    user_statistics.append([username, info, error])

  for error, count in sorted_error_store:
    error_message.append([error, count])

  # Create CSV file for report
  convert_to_csv("user_statistics.csv", user_statistics)
  convert_to_csv("error_message.csv", error_message)



if __name__ == "__main__":
  main("syslog.log")
