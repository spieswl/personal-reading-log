#!/usr/bin/env python

import argparse
import os
import glob
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.transforms as mtrans
from matplotlib.offsetbox import AnnotationBbox
from matplotlib.offsetbox import OffsetImage
import yaml

from datetime import date
from matplotlib import font_manager as fm, rcParams

plt.style.use('seaborn-darkgrid')

# Global font inclusions
font_dir = "C:\\Users\\spies\\AppData\\Local\\Microsoft\\Windows\\Fonts"
font_files = fm.findSystemFonts(fontpaths=font_dir)
font_list = fm.createFontList(font_files)
fm.fontManager.ttflist.extend(font_list)

# Genre colormap
genre_colors = { 'Nonfiction' : 'tab:cyan',
                 'Fiction'    : 'tab:orange',
                 'Technical'  : 'tab:purple' }


def month_day_splits(year):
  """This function will return a list containing the number of the first
  day for each month in the target year.
  """
  month_days = []
  for i in range(1, 13):
    month_days.append(date(year, i, 1).timetuple().tm_yday)
  return month_days


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

  yaml_path = os.path.realpath("book_reading_log.yaml")
  if os.path.isfile(yaml_path):
    print(">> Parsing YAML file at [ " + yaml_path + " ]...")
  else:
    print(">> [ERROR] Unable to find any YAML file at [ " + yaml_path + " ].")
    return

  cover_dir = os.path.join(os.path.realpath("."), "covers")

  # Date-time handling
  months_in_year = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                    "November", "December"]
  days_in_year = (date((args.year + 1), 1, 1) - date(args.year, 1, 1)).days
  first_days_of_month = month_day_splits(args.year)

  # Initializations used for data presentation
  relevant_entries = []

  # Load the file into our YAML parser
  with open(yaml_path, 'r') as yaml_file:
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

  # Set up the plot infrastructure (plot figure is set to 25.6 W x 19.2 H or a 1.333:1 aspect ratio)
  fig, axes = plt.subplots()
  fig.set_figheight(19.2)
  fig.set_figwidth(25.6)
  plt.subplots_adjust(left=0.15, bottom=0.1, right=0.95, top=0.9, wspace=1, hspace=1)

  # Create a plot for each book in the relevant entries
  book_titles = []
  for count, entry in enumerate(relevant_entries, 1):
    # Pertinent book details
    book_titles.append(entry['title'] + "\n" + entry['author'] + " - " + entry['genre'] + "\n" + "({} pages)".format(entry['pages']))
    book_color = genre_colors[entry['genre']]
    start_day = entry['started'].timetuple().tm_yday
    end_day = entry['finished'].timetuple().tm_yday
    days_to_read = end_day - start_day

    # Length of time reading the book
    axes.broken_barh([(start_day, days_to_read)], (count - 0.2, 0.4), color=book_color)

    # Annotations showing the book covers
    entry_isbn = entry['isbn'] + '.jpg'
    cover_img = plt.imread(os.path.join(cover_dir, entry_isbn), format='jpg')
    cover_img_box = OffsetImage(cover_img, zoom=0.25)

    cover_anno_pos = (start_day - 9, count)
    cover_anno = AnnotationBbox(cover_img_box, cover_anno_pos, xycoords='data')
    axes.add_artist(cover_anno)

  # Table formatting
  ## X-Axis
  axes.set_xlim(1, days_in_year)
  axes.set_xticks(first_days_of_month)
  axes.set_xticklabels(months_in_year, fontname="Open Sans SemiBold", fontsize=18)
  plt.xticks(rotation=45)

  ## Shift the X-axis tick labels
  x_offset = mtrans.ScaledTranslation(50/72, -10/72, fig.dpi_scale_trans)
  for label in axes.xaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + x_offset)

  ## Y-Axis
  axes.set_ylim(0, len(relevant_entries) + 1.0)
  axes.set_yticks(list(range(1, len(relevant_entries) + 1)))
  axes.set_yticklabels(book_titles, fontname="Open Sans SemiBold", fontsize=18, fontstyle="italic")

  ## Shift the Y-axis tick labels
  y_offset = mtrans.ScaledTranslation(-10/72, 0/72, fig.dpi_scale_trans)
  for label in axes.yaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + y_offset)

  ## Title Bar
  axes.set_title("Books Read in the Year {}".format(args.year), fontname="Montserrat ExtraBold", fontsize=36, pad=30)

  # Save the figure in a local image file
  plt.savefig('reading_log_{}.png'.format(args.year), format='png')

  return

########################################################################################################################

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("Keyboard interrupt caught. Terminating program.")
