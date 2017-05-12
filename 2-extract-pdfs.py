# Special Cases
# 137: GJ-Junagadh
# 404: OR-Debagarh.pdf

import PyPDF2, csv
import os, re
from IPython.core.debugger import Tracer

# Take PDF file reader, read page 1 and return
# households, women, men, urban_rural_total
# from the first page and return
def read_meta(read_pdf):
  intro_page = read_pdf.getPage(1)
  intro_txt = intro_page.extractText().replace('\n', '')
  hwm = re.search('gathered from ([^ ]{1,}) households, ([^ ]{1,}) women, and ([^ ]{1,}) men.', intro_txt)
  if not hwm:
    print('error')
  urban_rural_total=[]
  if '30-70%' in intro_txt:
    urban_rural_total = 'Both'
  elif '70% rural population' in intro_txt:
    urban_rural_total = 'Rural'
  elif '70% urban population' in intro_txt:
    urban_rural_total = 'Urban'
  return hwm.group(1), hwm.group(2), hwm.group(3), urban_rural_total

# Take the chunk of raw text which contains the data and use different parsing
# grammars/patterns to split it into chunks
# This splitting is based on index, not text because of many of redundant spaces
# between text. This has been tested to work on 635 of the 637 district files.
def segment_txt(txt):
  i = 1
  txt = txt[txt.index('{0}. '.format(i)):]
  final = []
  # 100 is arbitrary, greater than 93 which is all we need.
  while i < 100:
    next_numstr = str(i+1)
    next_str = [' {0}. '.format(next_numstr),
                ' {0} . '.format(next_numstr)]
    if len(next_numstr) > 1:
      next_str += [' {0} {1}. '.format(next_numstr[0], next_numstr[1]),
                   ' {0} {1} . '.format(next_numstr[0], next_numstr[1]),
                   ' {0} {1} 2 ) '.format(next_numstr[0], next_numstr[1]),
                   ' {0}2)'.format(next_numstr),
                   ' {0} {1} '.format(next_numstr[0], next_numstr[1]),
                   ' {0} '.format(next_numstr)]
    indices = []
    for trial in next_str:
      try:
        indices.append(txt.index(trial))
      except Exception as e:
        continue
    if len(indices) == 0:
      break
    ind = min(indices)
    final.append(txt[:ind])
    txt = txt[ind:]
    i = i + 1
  final.append(txt)
  return final

# Each cell contains some number or data. Parses out the data we need and
# validates it.
# There are a few formats:
# (46.9)
# 10,231
# 1,298
# 5.7
# 40.1
# *
def parse_cell(cell):
  if cell.startswith('(') and cell.endswith(')'):
    cell = cell[1:-1]
  cell = cell.replace(',','')
  if cell == '*':
    return cell
  try:
    float(cell)
  except Exception as e:
    print("Couldn't parse cell")
    Tracer()()
  return cell

# A row is either 2 or 3 (for urban, total or rural, total and urban, rural,
# total). The cell text is like " <cell> <cell> <cell>" or " <cell> <cell> "
# The format of a cell is above.
def split_and_parse_row(cell_txt, how_many):
  parts = cell_txt.split()
  if not len(parts) == how_many:
    print("Cell splitting unexpected")
    Tracer()()
  return [parse_cell(p) for p in parts]

# Does the following.
# Takes in the raw text and how_many (the number of columns for urban/rural/total)
# 1. Segments the text into the rows (and validates that there are 93 rows)
# 2. Splits the rows
# 3. Validates and parses the cells
# 4. Return parsed rows - arrays of arrays of 2-3 elements.
def parse_txt(txt, how_many):
  how_many = str(how_many)
  segments = segment_txt(txt)
  if not len(segments) == 93:
    print("Couldn't Segment")
    Tracer()()
  parses = []
  for i, seg in enumerate(segments):
    regex = ''
    # parse 3-4 digit nums which are rows 2 3 and 36
    # 3. Sex ratio of the total population (females per 1,000 males)
    # 4. Sex ratio at birth for children born in the last five years (females per 1,000 males)
    # 37. Average out of pocket expenditure per delivery in public health facility (Rs.)
    if i == 2 or i == 3 or i == 36:
      regex = ' (((\(?[0-9]{1,2}?,?[0-9]{1,3}\)?)|\*) ){'  + how_many + '}'
    else:
      regex = ' (((\(?[0-9]{1,3}\.[0-9]\)?)|\*) ){'  + how_many + '}'
    parse =  re.search(regex, ' {0} '.format(seg))
    if not parse:
      print("Couldn't parse {0} {1}".format(i, seg))
    parses.append(split_and_parse_row(parse.group(0),int(how_many)))
  return parses

# Takes a file for a district with filename format <StateCode>-<DistrictName>.pdf
# like WB-Kolkata.pdf:
# 1. Reads it
# 2. Gets metadata
# 3. Parses the data
# 4. Flattens the data into a 285 length array:
# (state, district, households, women, men, urban/rural/or total) (6)
# all total data rows (93), all urban data rows (93), all rural data rows (93) = 285
# 5. Validates the length and returns data
def extract_from_file(fname):
  print(fname)
  pdf_file = open('data/' + fname, 'rb')
  state = fname[:2]
  district = fname[3:-4]
  read_pdf = PyPDF2.PdfFileReader(pdf_file)
  number_of_pages = read_pdf.getNumPages()
  households, women, men, urban_rural_total = read_meta(read_pdf)
  pages = [read_pdf.getPage(2), read_pdf.getPage(3), read_pdf.getPage(4)]
  # Need to remove redundant newlines to make parsing patterns easy/possible
  txt = ' '.join(' '.join([page.extractText().replace('\n','') for page in pages]).split())
  urban, rural, total = [], [], []
  if urban_rural_total == 'Both':
    parses = parse_txt(txt, 3)
    for u, r, t in parses:
      urban.append(u)
      rural.append(r)
      total.append(t)
  else:
    parses = parse_txt(txt, 2)
    for ur, t in parses:
      if urban_rural_total == 'Urban':
        urban.append(ur)
      elif urban_rural_total == 'Rural':
        rural.append(ur)
      total.append(t)
  if len(urban) == 0:
    urban = [''] * 93
  if len(rural) == 0:
    rural = [''] * 93
  final = [state, district, households, women, men, urban_rural_total] + total + urban + rural
  if not len(final) == 285:
    print("Final length doesn't add")
    Tracer()()
  return final

# Reads all the data files, iterates through, parses them
data2 = []
files = os.listdir('data')[1:]
for f in files:
  # 137: GJ-Junagadh and 404: OR-Debagarh
  # do not parse properly in the PDF, and need special casing.
  if f in {'GJ-Junagadh.pdf', 'OR-Debagarh.pdf'}:
    continue
  data2.append(extract_from_file(f))

Tracer()()
# Writes them to a file
with open('india-nhfs4-final.csv', 'w') as f:
  w = csv.writer(f)
  w.writerows(data2)
