#!/usr/bin/env python3

import sys
from urllib.request import urlopen
import hashlib

def main(argc, argv):
  if argc != 4:
    print(
        f"Usage:\n\t{argv[0]} https://url/to/file.txt /path/to/destination/file.txt <expected_sha256_hash>"
    )
    return 1

  url = argv[1]
  destination_file = argv[2]
  expected_hash = argv[3]

  try:
    print("Downloading...") 
    response = urlopen(url)

    with open(destination_file, "wb") as f:
      f.write(response.read())

  except Exception as e:
    print("Failed to retrieve the file from the given url")
    print(e)
    return 1

  print("Verifying the file hash...")
  file_hash = get_file_hash(destination_file)
  if file_hash is None:
    print("Failed to compute the file hash")
    return 1

  if file_hash != expected_hash:
    print("The downloaded file seems to be corrupted")
    return 1

  print("The file has been successfully downloaded!")
  return 0

def get_file_hash(path):
  try:
    hasher = hashlib.sha256()
    input_file = open(path, "rb")

    while True:
      if buffer := input_file.read(1048576):
        hasher.update(buffer)

      else:
        break

    return hasher.hexdigest()

  except:
    return None
if __name__ == "__main__":
  exit_code = main(len(sys.argv), sys.argv)
  exit(exit_code)

