# personal-reading-log

This helps me keep track of books and academic papers I've read.

## Tracking Academic Papers

### Overview

(REWORK IN PROGRESS)

## Tracking Books

### Overview

Another effort to do more self-quantification (and self-reflection).

In the interest of keeping a more detailed list of the books I've been reading, I started working on some tools that I could use to create a comprehensive register of my latest reads. I opted to build up a self-contained system for maintaining such a register, which aligns more closely with my desires for portability and simplicity, instead of creating yet another account on GoodReads or some other website. Thus, this work is my ongoing effort to record and present this data.

This part of `personal-reading-log` has three components: The first is `book_reading_log.yaml`; a continuously updated log of what books I have read, when I read them, the genre a particular book falls under, and some other details that I'll figure out how to deal with later (page count, among other things). The log should be easy to parse _for humans and computers alike_ and is formatted as a YAML file. The second is a **Python** script, `generate_book_stats.py`, that parses the reading log and generates a chart showing completed readings for a given calendar year.  The third is a folder with images containing covers of each of the books listed in the log; I wanted something more visually appealing than just text on a graph, so I have small, local copies of book cover preview images that I overlay on the reading chart. This last piece is optional, the script can still generate output without the covers folder.

I discovered a couple neat things about myself when I started cataloguing my completed reads: 1) recording what I've read provides an extra push to _keep_ reading, and 2) my memories of the essential content of these books are stronger. I feel that both of these discoveries will be big contributors to my underlying goal of reading and internalizing more knowledge. If that sounds appealing to you, feel free to copy this repository and replace the contents of the `book_reading_log` with your own data.

Check the **_Script Usage_** section for more detailed operational notes on generating reading metrics. Check the **_Getting New Book Covers_** section for the workflow I use to add new book covers, if so inclined.

### Script Usage

**NOTE**: The generation script parses `book_reading_log.yaml`, which is assumed to be in the current working directory, for data. If no books are shown as _either_ **started** or **finished** in the given year, default or otherwise, an empty chart will be generated. Books that are **started** but **not finished** in the given year will show as being read up to December 31st. Books that are **not started** but **finished** in the given year will show as starting up from January 1st.

This command generates a reading log visualization for the current year (based on system time):

```bash
$ generate_book_stats.py
```

This command will generate a reading log visualization for the specified year:

```bash
$ generate_book_stats.py -y {YEAR}
```

### Getting New Book Covers

This is just how I do this. I found the cover images I can get from particular listings on Barnes & Noble's website are of the highest quality. Finding the specific listing that pairs with the book I possess (hardcover, revision counter, usually based on the ISBN-13) is the most tricky aspect of this. Some more automation here would be nice, since having to hunt down particular assets is mindnumbing.

1. Search the [Barnes & Noble website](https://www.barnesandnoble.com/) for a particular book's ISBN-13.
2. Go to that book's listing and isolate (through right-click or whatever option menu, use "View Image" or "Open Image in New Tab") the cover image.
  * If the image is hosted in `.webp` format, save as a `webp` to the local machine, reopen, and save as a new `jpg`.
3. Resize the image to have a width of 260 pixels, maintaining the aspect ratio.
4. Save the image to `./books/covers`.
5. Change the filename to the `isbn` value for the matching book entry from the reading log.
