#!/usr/bin/env python3

import csv
import sys

def print_n(n):
  if n != '' and n.isdigit():
    if len(n) < 10:
      print('+5524{}'.format(n))
    else:
      print('+55{}'.format(n))

phone_numbers_file = sys.argv[1]
print('number')
with open(phone_numbers_file, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      number_formatted = row['Phone 1 - Value'].replace('-', '').replace(' ', '')
      if number_formatted != '':
        if ':::' in number_formatted:
          for n in number_formatted.split(':::'):
            print_n(n)
        else:
          print_n(number_formatted)
