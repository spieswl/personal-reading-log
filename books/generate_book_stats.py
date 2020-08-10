#!/usr/bin/env python

import argparse
import os
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import yaml

from datetime import date

plt.style.use('seaborn-darkgrid')

# Genre colormap
genre_colors = { 'Nonfiction' : 'tab:cyan',
                 'Fiction'    : 'tab:orange',
                 'Technical'  : 'tab:purple' }

def main():
  """
  """
  # Get the current year from system time
  current_year = date.today().year

  # Parse arguments passed to the script
  parser = argparse.ArgumentParser(description='Generate a visualization for the target book log YAML file.')
  parser.add_argument('-y', '--year', type=int, help='What year chart should be generated? (default: current year)',
                      default=current_year)
  args = parser.parse_args()

  filepath = os.path.realpath("book_reading_log.yaml")
  if os.path.isfile(filepath):
    print(">> Parsing YAML file at [ " + filepath + " ]...")
  else:
    print(">> [ERROR] Unable to find any YAML file at [ " + filepath + " ].")
    return

  # Initializations used for data gathering
  relevant_entries = []

  # Load the file into our YAML parser
  with open(filepath, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    yaml_file.close()

  # Find the books we care about (based on dates started or finished)
  for book in data['readings']:
    try:
      book['started'] = date.fromisoformat(book['started'])
      book['finished'] = date.fromisoformat(book['finished'])
    except ValueError:
      continue

    if (book['started'].year == args.year or book['finished'].year == args.year):
      relevant_entries.append(book)

  # Set up the plot infrastructure
  fig, axes = plt.subplots()

  # Create a plot for each book in the relevant entries
  book_titles = []
  for count, entry in enumerate(relevant_entries, 1):
    # Pertinent book details
    book_titles.append(entry['title'] + "\n" + entry['author'] + "\n" + "{} pages".format(entry['pages']))
    book_color = genre_colors[entry['genre']]
    days_to_read = (entry['finished'] - entry['started']).days

    # Length of time reading the book
    axes.broken_barh([(entry['started'], days_to_read)], (count - 0.2, 0.4), color=book_color)

  # Table formatting
  axes.set_xlim(date(args.year, 1, 1), date(args.year, 12, 31))
  axes.set_xticklabels(["January", "February", "March", "April", "May", "June", "July", "August", "September",
                        "October", "November", "December"], fontname="Myriad Hebrew")
  axes.set_ylim(0, len(relevant_entries) + 1.0)
  axes.set_yticks(list(range(1, len(relevant_entries) + 1)))
  axes.set_yticklabels(book_titles, fontname="Myriad Pro", fontsize=11, fontstyle="italic", fontweight="bold")
  axes.set_title("Books Read in the Year {}".format(args.year), fontname="Myriad Pro", fontsize=18)

  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.show()
  #plt.savefig("test.png")

  return

########################################################################################################################

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("Keyboard interrupt caught. Terminating program.")
