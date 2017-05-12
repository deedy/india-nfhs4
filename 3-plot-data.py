import csv
from descartes import PolygonPatch
import shapefile
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry.polygon import Polygon
from IPython.core.debugger import Tracer
import matplotlib.patches as mpatches


STATE_ABBR_FILE = 'state_list.txt'
state_abbr = {}
with open(STATE_ABBR_FILE) as f:
  read = csv.reader(f)
  state_abbr = {a[0]: a[1] for a in read}

district_spell_fix = {
'Rangareddy': 'Ranga Reddy',
'Kheri': 'Lakhimpur Kheri',
'Siddharthnagar': 'Siddharth Nagar',
'Paschim Medinipur': 'Pashchim Medinipur',
'Khandwa (East Nimar)': 'East Nimar',
'Khargone (West Nimar)': 'West Nimar',
'Punch': 'Poonch',
'Nicobars': 'Nicobar Islands',
'Papumpare': 'Papum Pare',
'Janjgir Champa': 'Janjgir-Champa',
'Kabirdham': 'Kabeerdham',
'Korea': 'Koriya',
'Dohad': 'Dahod',
'Dakshin Bastar Dantewada': 'Dantewada',
'Banaskantha': 'Banas Kantha',
'Mahesena': 'Mahesana',
'Panchmahal': 'Panch Mahals',
'Sabarkantha': 'Sabar Kantha',
'Lahul and Spiti': 'Lahul & Spiti',
'Saraikela Kharsawan': 'Saraikela-kharsawan',
'Baramula': 'Baramulla',
'Leh(Ladakh)': 'Leh (Ladakh)',
'Lawngtlai': 'Lawangtlai',
'Baudh': 'Bauda',
'Rup Nagar': 'Rupnagar',
'Sahid Bhagat Singh Nagar': 'Shahid Bhagat Singh Nagar',
'Bara Banki': 'Barabanki',
'Jyotiba Phule Nagar': 'Amroha',
'Kanshiram Nagar': 'Kasganj',
'Mahamaya Nagar': 'Hathras',
'Sant Ravidas Nagar': 'Sant Ravi Das Nagar',
'Shrawasti': 'Shravasti',
'North  & Middle Andaman': 'North and Middle Andaman',
'Sri Potti Sriramulu Nellore': 'Nellore',
'Buxer': 'Buxar',
'Kaimur (Bhabua)': 'Kaimur',
'South  Goa': 'South Goa',
'Chamarajanagar': 'Chamrajnagar',
'Chikkaballapura': 'Chikballapura',
'Gadchiroli': 'Garhchiroli',
'Mumbai': 'Mumbai City',
'Ribhoi': 'Ri Bhoi',
'Coddalore': 'Cuddalore',
'Nagapattinam': 'Nagappattinam',
'Virudhunagar': 'Virudunagar',
'North Twenty Four Parganas': 'North 24 Parganas',
'South Twenty Four Parganas': 'South 24 Parganas'}

# GET NFHS-4 = 637 entries
PARSED_FILE = 'parsed/india-nfhs4.csv'
all = []
with open(PARSED_FILE) as f:
  read = csv.reader(f)
  all = [a for a in read]
all = all[3:]
nfhs4 = [(a[0], a[1]) for a in all]

# GET GEO DATA = 667 entries
sf = shapefile.Reader("IND_adm_shp/IND_adm2.shp")
map_recs = {(d[4].strip(), d[6].strip()): i for i, d in enumerate(sf.records())}
map_names = {(d[4].strip(), d[6].strip()): i for i, d in enumerate(sf.records())}
# map_names.update({(d[4].strip(), d[-1].strip()): i for i, d in enumerate(sf.records()) if d[-1].strip() and not (d[4].strip(), d[-1].strip()) in map_names})


def get_proper_state_name(i):
  if i[0] == 'DL':
    return [(state_abbr[i[0]], 'West')]
  if i == ('SK', 'North'):
    return [(state_abbr[i[0]], 'North Sikkim')]
  if i == ('SK', 'South'):
    return [(state_abbr[i[0]], 'South Sikkim')]
  if i == ('SK', 'West'):
    return [(state_abbr[i[0]], 'West Sikkim')]
  if i == ('SK', 'East'):
    return [(state_abbr[i[0]], 'East Sikkim')]
  if i == ('CT', 'Surguja'):
    return [(state_abbr[i[0]], 'Surguja'), (state_abbr[i[0]], 'Surajpur'), (state_abbr[i[0]], 'Balrampur')]
  if i == ('CT', 'Bilaspur'):
    return [(state_abbr[i[0]], 'Bilaspur'), (state_abbr[i[0]], 'Mungeli')]
  if i == ('CT', 'Raipur'):
    return [(state_abbr[i[0]], 'Raipur'), (state_abbr[i[0]], 'Baloda Bazar'), (state_abbr[i[0]], 'Gariaband')]
  if i == ('CT', 'Durg'):
    return [(state_abbr[i[0]], 'Durg'), (state_abbr[i[0]], 'Bemetara'), (state_abbr[i[0]], 'Balod')]
  if i == ('CT', 'Dakshin Bastar Dantewada'):
    return [(state_abbr[i[0]], 'Sukma'), (state_abbr[i[0]], 'Dantewada')]
  if i == ('CT', 'Bastar'):
    return [(state_abbr[i[0]], 'Bastar'), (state_abbr[i[0]], 'Kondagaon')]
  if i == ('GJ', 'Junagadh'):
    return [(state_abbr[i[0]], 'Junagadh'), (state_abbr[i[0]], 'Gir Somnath')]
  if i == ('GJ', 'Jamnagar'):
    return [(state_abbr[i[0]], 'Jamnagar'), (state_abbr[i[0]], 'Devbhumi Dwarka')]
  if i == ('GJ', 'Panchmahal'):
    return [(state_abbr[i[0]], 'Mahisagar'), (state_abbr[i[0]], 'Panch Mahals')]
  if i == ('GJ', 'Rajkot'):
    return [(state_abbr[i[0]], 'Rajkot'), (state_abbr[i[0]], 'Morbi')]
  if i == ('GJ', 'Sabarkantha'):
    return [(state_abbr[i[0]], 'Sabar Kantha'), (state_abbr[i[0]], 'Aravalli')]
  if i == ('GJ', 'Bhavnagar'):
    return [(state_abbr[i[0]], 'Bhavnagar'), (state_abbr[i[0]], 'Botad')]
  if i == ('GJ', 'Bhavnagar'):
    return [(state_abbr[i[0]], 'Bhavnagar'), (state_abbr[i[0]], 'Botad')]
  if i == ('GJ', 'Vadodara'):
    return [(state_abbr[i[0]], 'Vadodara'), (state_abbr[i[0]], 'Chhota Udaipur')]
  if i == ('PB', 'Gurdaspur'):
    return [(state_abbr[i[0]], 'Gurdaspur'), (state_abbr[i[0]], 'Pathankot')]
  if i == ('PB', 'Firozpur'):
    return [(state_abbr[i[0]], 'Firozpur'), (state_abbr[i[0]], 'Fazilka')]
  if i == ('AR', 'Lohit'):
    return [(state_abbr[i[0]], 'Lohit'), (state_abbr[i[0]], 'Namsai')]
  if i == ('AR', 'Tirap'):
    return [(state_abbr[i[0]], 'Tirap'), (state_abbr[i[0]], 'Longding')]
  if i == ('ML', 'West Khasi Hills'):
    return [(state_abbr[i[0]], 'West Khasi Hills'), (state_abbr[i[0]], 'South West Khasi Hills')]
  if i == ('ML', 'East Garo Hills'):
    return [(state_abbr[i[0]], 'East Garo Hills'), (state_abbr[i[0]], 'North Garo Hills')]
  if i == ('ML', 'West Garo Hills'):
    return [(state_abbr[i[0]], 'West Garo Hills'), (state_abbr[i[0]], 'South West Garo Hills')]
  if i == ('WB', 'Jalpaiguri'):
    return [(state_abbr[i[0]], 'Jalpaiguri'), (state_abbr[i[0]], 'Alipurduar')]
  if i == ('TR', 'North Tripura'):
    return [(state_abbr[i[0]], 'North Tripura'), (state_abbr[i[0]], 'Unokoti')]
  if i == ('TR', 'South Tripura'):
    return [(state_abbr[i[0]], 'South Tripura'), (state_abbr[i[0]], 'Gomati')]
  if i == ('TR', 'West Tripura'):
    return [(state_abbr[i[0]], 'West Tripura'), (state_abbr[i[0]], 'Sipahijala'), (state_abbr[i[0]], 'Khowai')]
  if i == ('UP', 'Sultanpur'):
    return [(state_abbr[i[0]], 'Sultanpur'), (state_abbr[i[0]], 'Amethi')]
  if i == ('UP', 'Budaun'):
    return [(state_abbr[i[0]], 'Budaun'), (state_abbr[i[0]], 'Sambhal')]
  if i == ('UP', 'Muzaffarnagar'):
    return [(state_abbr[i[0]], 'Muzaffarnagar'), (state_abbr[i[0]], 'Shamli')]
  if i == ('UP', 'Ghaziabad'):
    return [(state_abbr[i[0]], 'Ghaziabad'), (state_abbr[i[0]], 'Hapur')]
  if i == ('MP', 'Shajapur'):
    return [(state_abbr[i[0]], 'Shajapur'), (state_abbr[i[0]], 'Agar Malwa')]
  if i == ('MH', 'Thane'):
    return [(state_abbr[i[0]], 'Thane'), (state_abbr[i[0]], 'Palghar')]
  if i[1] in district_spell_fix:
    return [(state_abbr[i[0]], district_spell_fix[i[1]])]
  return [(state_abbr[i[0]], i[1])]

def translate_nfhs_to_geo(state, district):
  res = get_proper_state_name((state, district))
  all = []
  for r in res:
    if r in map_names:
      all.append(map_names[r])
  if len(all) == 0:
    Tracer()()
  return all


# NFHS4 that has not been mapped (multiple to one possible)
unmapped_nfhs4 = [name for i in nfhs4 for name in  get_proper_state_name(i) if not name in map_names]
assert(len(unmapped_nfhs4) == 0)

# NFHS-4 UNION GEO_DATA == 629 entries (less than 637 because multiple to one, all for Delhi)
# Delhi surveyed in 9 areas, but on map is one area.
# union = set({map_names[get_proper_state_name(i)] for i in all if get_proper_state_name(i) in map_names})
union = set({j for i in all for j in translate_nfhs_to_geo(*i[:2])})


# GEO DATA - NFHS4 == geo areas not mapped, because GEO is newer than NFHS4
unmapped_geo = [(s, d) for s, d in map_recs.keys() if not map_names[(s,d)]  in union] # 37
# No data available for Dadra Nagar Haveli, Lakshwadweep and Chandigarh
assert(len(unmapped_geo) == 3)

# N = Data available in the NFHS4
# M = Data available to map
# Multiple Ns map to single M (Delhi -> )
# All Ns mapped to M. (translations)
# All M must be mapped back (except 3 exceptions)
# Single N can map to multiple M. (district divisions)

def plot_shape(ax, shape, color, alphaval = 1, linewidth = 0.25):
  mp = shape.__geo_interface__
  if mp['type'] == 'Polygon':
    ax.add_patch(PolygonPatch(Polygon(mp['coordinates'][0]), fc=color, ec=BLACK, alpha=alphaval, zorder=2, linewidth=linewidth))
  elif mp['type'] == 'MultiPolygon':
    for poly in mp['coordinates']:
      ax.add_patch(PolygonPatch(Polygon(poly[0]), fc=color, ec=BLACK, alpha=alphaval, zorder=2, linewidth=linewidth))

def plot_state_outlines():
  states = shapefile.Reader("IND_adm_shp/IND_adm1.shp")
  for i, state in enumerate(states.shapes()):
    plot_shape(ax, state, 'none', alphaval = 1, linewidth = 0.75)

def get_color_and_alpha_for_sex_ratio_3():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 3])
    if data >= 1000:
      color = RED # female
    else:
      color = BLUE # male
    return color, 1
  def titlefunc(ax):
    ax.set_title('Sex Ratio')
    red_patch = mpatches.Patch(color=RED, label='More Women')
    blue_patch = mpatches.Patch(color=BLUE, label='More Men')
    plt.legend(handles=[red_patch, blue_patch])
  return colorfunc, titlefunc

def get_color_and_alpha_for_sex_ratio_last_5_4():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 4])
    if data >= 1000:
      color = RED # female
    else:
      color = BLUE # male
    return color, 1
  def titlefunc(ax):
    ax.set_title('Sex Ratio in the last 5 years')
    red_patch = mpatches.Patch(color=RED, label='More Women')
    blue_patch = mpatches.Patch(color=BLUE, label='More Men')
    plt.legend(handles=[red_patch, blue_patch])
  return colorfunc, titlefunc

def get_color_and_alpha_for_obese_men_75():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 75])
    colors = sns.color_palette("Paired")
    if data <= 10:
      color = colors[0]
    elif data <= 15:
      color = colors[1]
    elif data <= 20:
      color = colors[2]
    elif data <= 30:
      color = colors[3]
    elif data <= 40:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Men who are Obese')
    colors = sns.color_palette("Paired")
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 10%'))
    patches.append(mpatches.Patch(color=colors[1], label='10-15%'))
    patches.append(mpatches.Patch(color=colors[2], label='15-20%'))
    patches.append(mpatches.Patch(color=colors[3], label='20-30%'))
    patches.append(mpatches.Patch(color=colors[4], label='30-40%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 40%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_obese_women_74():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 74])
    colors = sns.color_palette("Paired")
    if data <= 10:
      color = colors[0]
    elif data <= 15:
      color = colors[1]
    elif data <= 20:
      color = colors[2]
    elif data <= 30:
      color = colors[3]
    elif data <= 40:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Women who are Obese')
    colors = sns.color_palette("Paired")
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 10%'))
    patches.append(mpatches.Patch(color=colors[1], label='10-15%'))
    patches.append(mpatches.Patch(color=colors[2], label='15-20%'))
    patches.append(mpatches.Patch(color=colors[3], label='20-30%'))
    patches.append(mpatches.Patch(color=colors[4], label='30-40%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 40%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_high_blood_sugar_84():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 84])
    if data >= 5:
      color = RED
    else:
      color = BLUE
    return color, 1
  def titlefunc(ax):
    ax.set_title('Men with very high blood sugar (> 160mg/dl) ')
    red_patch = mpatches.Patch(color=RED, label='Above 5%')
    blue_patch = mpatches.Patch(color=BLUE, label='Below 5%')
    plt.legend(handles=[red_patch, blue_patch])
  return colorfunc, titlefunc

def get_color_and_alpha_for_women_high_blood_sugar_82():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 82])
    if data >= 5:
      color = RED
    else:
      color = BLUE
    return color, 1
  def titlefunc(ax):
    ax.set_title('Women with very high blood sugar (> 160mg/dl) ')
    red_patch = mpatches.Patch(color=RED, label='Above 5%')
    blue_patch = mpatches.Patch(color=BLUE, label='Below 5%')
    plt.legend(handles=[red_patch, blue_patch])
  return colorfunc, titlefunc

def get_color_and_alpha_for_rural_urban_both():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = entry[BUFFER_IND]
    colors = sns.color_palette("hls", 3)
    color = '#cccccc'
    if data == 'Rural':
      color = colors[0]
    elif data == 'Both':
      color = colors[1]
    elif data == 'Urban':
      color = colors[2]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Rural / Urban / Both Distribution')
    colors = sns.color_palette("hls", 3)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='Rural'))
    patches.append(mpatches.Patch(color=colors[1], label='Both'))
    patches.append(mpatches.Patch(color=colors[2], label='Urban'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_literacy_women_12():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 12])
    colors = sns.cubehelix_palette(6)
    if data <= 50:
      color = colors[0]
    elif data <= 60:
      color = colors[1]
    elif data <= 70:
      color = colors[2]
    elif data <= 80:
      color = colors[3]
    elif data <= 90:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Literacy Rate (Women)')
    colors = sns.cubehelix_palette(6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 50%'))
    patches.append(mpatches.Patch(color=colors[1], label='50-60%'))
    patches.append(mpatches.Patch(color=colors[2], label='60-70%'))
    patches.append(mpatches.Patch(color=colors[3], label='70-80%'))
    patches.append(mpatches.Patch(color=colors[4], label='80-90%'))
    patches.append(mpatches.Patch(color=colors[5], label='90%+'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_literacy_men_13():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 13])
    colors = sns.cubehelix_palette(6)
    if data <= 50:
      color = colors[0]
    elif data <= 60:
      color = colors[1]
    elif data <= 70:
      color = colors[2]
    elif data <= 80:
      color = colors[3]
    elif data <= 90:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Literacy Rate (Men)')
    colors = sns.cubehelix_palette(6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 50%'))
    patches.append(mpatches.Patch(color=colors[1], label='50-60%'))
    patches.append(mpatches.Patch(color=colors[2], label='60-70%'))
    patches.append(mpatches.Patch(color=colors[3], label='70-80%'))
    patches.append(mpatches.Patch(color=colors[4], label='80-90%'))
    patches.append(mpatches.Patch(color=colors[5], label='90%+'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_women_10_years_14():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 14])
    colors = sns.cubehelix_palette(6, start = 0.5, rot=-.75)
    if data <= 10:
      color = colors[0]
    elif data <= 20:
      color = colors[1]
    elif data <= 30:
      color = colors[2]
    elif data <= 40:
      color = colors[3]
    elif data <= 50:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Women with more than 10 years schooling')
    colors = sns.cubehelix_palette(6, start = 0.5, rot=-.75)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 10%'))
    patches.append(mpatches.Patch(color=colors[1], label='10-20%'))
    patches.append(mpatches.Patch(color=colors[2], label='20-30%'))
    patches.append(mpatches.Patch(color=colors[3], label='30-40%'))
    patches.append(mpatches.Patch(color=colors[4], label='40-50%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 50%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_women_marraige_18_years_15():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 15])
    colors = sns.cubehelix_palette(6, start = 0.5, rot=-.75)
    if data <= 10:
      color = colors[0]
    elif data <= 20:
      color = colors[1]
    elif data <= 30:
      color = colors[2]
    elif data <= 40:
      color = colors[3]
    elif data <= 50:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Women between 20-24 married before 18')
    colors = sns.cubehelix_palette(6, start = 0.5, rot=-.75)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 10%'))
    patches.append(mpatches.Patch(color=colors[1], label='10-20%'))
    patches.append(mpatches.Patch(color=colors[2], label='20-30%'))
    patches.append(mpatches.Patch(color=colors[3], label='30-40%'))
    patches.append(mpatches.Patch(color=colors[4], label='40-50%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 50%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_condom_use_24():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 24])
    colors = sns.light_palette("green", 3)
    if data <= 5:
      color = colors[0]
    elif data <= 10:
      color = colors[1]
    else:
      color = colors[2]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Use of Condom for Contraception')
    colors = sns.light_palette("green", 3)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 5%'))
    patches.append(mpatches.Patch(color=colors[1], label='5-10%'))
    patches.append(mpatches.Patch(color=colors[2], label='> 10%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_pill_use_23():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 23])
    colors = sns.light_palette("green", 3)
    if data <= 5:
      color = colors[0]
    elif data <= 10:
      color = colors[1]
    else:
      color = colors[2]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Use of Pill for Contraception')
    colors = sns.light_palette("green", 3)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 5%'))
    patches.append(mpatches.Patch(color=colors[1], label='5-10%'))
    patches.append(mpatches.Patch(color=colors[2], label='> 10%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_iud_use_22():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 22])
    colors = sns.light_palette("green", 3)
    if data <= 5:
      color = colors[0]
    elif data <= 10:
      color = colors[1]
    else:
      color = colors[2]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Use of IUD/PPIUD for Contraception')
    colors = sns.light_palette("green", 3)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 5%'))
    patches.append(mpatches.Patch(color=colors[1], label='5-10%'))
    patches.append(mpatches.Patch(color=colors[2], label='> 10%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_female_sterilization_use_20():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 20])
    colors = sns.light_palette("green", 3)
    if data <= 5:
      color = colors[0]
    elif data <= 10:
      color = colors[1]
    else:
      color = colors[2]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Use of Female Sterilization for Contraception')
    colors = sns.light_palette("green", 3)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 5%'))
    patches.append(mpatches.Patch(color=colors[1], label='5-10%'))
    patches.append(mpatches.Patch(color=colors[2], label='> 10%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_male_sterilization_use_21():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 21])
    colors = sns.light_palette("green", 3)
    if data <= 5:
      color = colors[0]
    elif data <= 10:
      color = colors[1]
    else:
      color = colors[2]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Use of Male Sterilization for Contraception')
    colors = sns.light_palette("green", 3)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 5%'))
    patches.append(mpatches.Patch(color=colors[1], label='5-10%'))
    patches.append(mpatches.Patch(color=colors[2], label='> 10%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_antenatal_4_30():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 30])
    colors = sns.light_palette("red", 5)
    if data <= 20:
      color = colors[0]
    elif data <= 40:
      color = colors[1]
    elif data <= 60:
      color = colors[2]
    elif data <= 80:
      color = colors[3]
    else:
      color = colors[4]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Mothers with 4 or more pre-birth doctor visits')
    colors = sns.light_palette("red", 5)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 20%'))
    patches.append(mpatches.Patch(color=colors[1], label='20-40%'))
    patches.append(mpatches.Patch(color=colors[2], label='40-60%'))
    patches.append(mpatches.Patch(color=colors[3], label='60-80%'))
    patches.append(mpatches.Patch(color=colors[4], label='> 80%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_antenatal_full_33():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 33])
    colors = sns.color_palette("PuBu", 5)
    if data <= 20:
      color = colors[0]
    elif data <= 40:
      color = colors[1]
    elif data <= 60:
      color = colors[2]
    elif data <= 80:
      color = colors[3]
    else:
      color = colors[4]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Mothers with full pre-birth care')
    colors = sns.color_palette("PuBu", 5)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 20%'))
    patches.append(mpatches.Patch(color=colors[1], label='20-40%'))
    patches.append(mpatches.Patch(color=colors[2], label='40-60%'))
    patches.append(mpatches.Patch(color=colors[3], label='60-80%'))
    patches.append(mpatches.Patch(color=colors[4], label='> 80%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_caesarian_44():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 44])
    colors = sns.color_palette("PuBu", 8)
    if data <= 5:
      color = colors[0]
    elif data <= 10:
      color = colors[1]
    elif data <= 15:
      color = colors[2]
    elif data <= 20:
      color = colors[3]
    elif data <= 25:
      color = colors[4]
    elif data <= 30:
      color = colors[5]
    elif data <= 35:
      color = colors[6]
    else:
      color = colors[7]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Caesarean Births')
    colors = sns.color_palette("PuBu", 8)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 5%'))
    patches.append(mpatches.Patch(color=colors[1], label='5-10%'))
    patches.append(mpatches.Patch(color=colors[2], label='10-15%'))
    patches.append(mpatches.Patch(color=colors[3], label='15-20%'))
    patches.append(mpatches.Patch(color=colors[4], label='20-25%'))
    patches.append(mpatches.Patch(color=colors[5], label='25-30%'))
    patches.append(mpatches.Patch(color=colors[6], label='30-35%'))
    patches.append(mpatches.Patch(color=colors[7], label='> 35%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_population_below_15_2():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 2])
    colors = sns.light_palette("green", 6)
    if data <= 20:
      color = colors[0]
    elif data <= 25:
      color = colors[1]
    elif data <= 30:
      color = colors[2]
    elif data <= 35:
      color = colors[3]
    elif data <= 40:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Percent of the Population below 15')
    colors = sns.light_palette("green", 6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 20%'))
    patches.append(mpatches.Patch(color=colors[1], label='20-25%'))
    patches.append(mpatches.Patch(color=colors[2], label='25-30%'))
    patches.append(mpatches.Patch(color=colors[3], label='30-35%'))
    patches.append(mpatches.Patch(color=colors[4], label='35-40%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 40%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_female_under_six_school_1():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 1])
    colors = sns.light_palette("green", 6)
    if data <= 50:
      color = colors[0]
    elif data <= 60:
      color = colors[1]
    elif data <= 70:
      color = colors[2]
    elif data <= 80:
      color = colors[3]
    elif data <= 90:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Percent of the Females under 6 who went to School')
    colors = sns.light_palette("green", 6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 50%'))
    patches.append(mpatches.Patch(color=colors[1], label='50-60%'))
    patches.append(mpatches.Patch(color=colors[2], label='60-70%'))
    patches.append(mpatches.Patch(color=colors[3], label='70-80%'))
    patches.append(mpatches.Patch(color=colors[4], label='80-90%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 90%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_households_electricity_6():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 6])
    colors = sns.cubehelix_palette(3)
    if data <= 80:
      color = colors[0]
    elif data <= 90:
      color = colors[1]
    else:
      color = colors[2]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Percentage of Households with Electricity')
    colors = sns.cubehelix_palette(3)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 80%'))
    patches.append(mpatches.Patch(color=colors[1], label='80-90%'))
    patches.append(mpatches.Patch(color=colors[2], label='> 90%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_households_health_insurance_11():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 11])
    colors = sns.cubehelix_palette(4)
    if data <= 20:
      color = colors[0]
    elif data <= 40:
      color = colors[1]
    elif data <= 60:
      color = colors[2]
    else:
      color = colors[3]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Percentage of Households with Health Insurance')
    colors = sns.cubehelix_palette(4)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 20%'))
    patches.append(mpatches.Patch(color=colors[1], label='20-40%'))
    patches.append(mpatches.Patch(color=colors[2], label='40-60%'))
    patches.append(mpatches.Patch(color=colors[3], label='> 60%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_households_children_polio_49():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    colors = sns.color_palette("PuBu", 6)
    if entry[BUFFER_IND + 49] == '*':
      return colors[0], 1
    data = float(entry[BUFFER_IND + 49])
    if data <= 50:
      color = colors[0]
    elif data <= 60:
      color = colors[1]
    elif data <= 70:
      color = colors[2]
    elif data <= 80:
      color = colors[3]
    elif data <= 90:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Children 1-2 years old who received Polio')
    colors = sns.color_palette("PuBu", 6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 50%'))
    patches.append(mpatches.Patch(color=colors[1], label='50-60%'))
    patches.append(mpatches.Patch(color=colors[2], label='60-70%'))
    patches.append(mpatches.Patch(color=colors[3], label='70-80%'))
    patches.append(mpatches.Patch(color=colors[4], label='80-90%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 90%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_fully_immunized_47():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    colors = sns.color_palette("PuBu", 6)
    if entry[BUFFER_IND + 47] == '*':
      return colors[0], 1
    data = float(entry[BUFFER_IND + 47])
    if data <= 50:
      color = colors[0]
    elif data <= 60:
      color = colors[1]
    elif data <= 70:
      color = colors[2]
    elif data <= 80:
      color = colors[3]
    elif data <= 90:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Children 1-2 years old who are fully Immunized')
    colors = sns.color_palette("PuBu", 6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 50%'))
    patches.append(mpatches.Patch(color=colors[1], label='50-60%'))
    patches.append(mpatches.Patch(color=colors[2], label='60-70%'))
    patches.append(mpatches.Patch(color=colors[3], label='70-80%'))
    patches.append(mpatches.Patch(color=colors[4], label='80-90%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 90%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_obese_men_75_2():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 75])
    colors = sns.light_palette("green", 6)
    if data <= 10:
      color = colors[0]
    elif data <= 15:
      color = colors[1]
    elif data <= 20:
      color = colors[2]
    elif data <= 30:
      color = colors[3]
    elif data <= 40:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Men who are Obese')
    colors = sns.light_palette("green", 6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 10%'))
    patches.append(mpatches.Patch(color=colors[1], label='10-15%'))
    patches.append(mpatches.Patch(color=colors[2], label='15-20%'))
    patches.append(mpatches.Patch(color=colors[3], label='20-30%'))
    patches.append(mpatches.Patch(color=colors[4], label='30-40%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 40%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_obese_women_74_2():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 74])
    colors = sns.light_palette("green", 6)
    if data <= 10:
      color = colors[0]
    elif data <= 15:
      color = colors[1]
    elif data <= 20:
      color = colors[2]
    elif data <= 30:
      color = colors[3]
    elif data <= 40:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Women who are Obese')
    colors = sns.light_palette("green", 6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 10%'))
    patches.append(mpatches.Patch(color=colors[1], label='10-15%'))
    patches.append(mpatches.Patch(color=colors[2], label='15-20%'))
    patches.append(mpatches.Patch(color=colors[3], label='20-30%'))
    patches.append(mpatches.Patch(color=colors[4], label='30-40%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 40%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_underweight_men_73():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 73])
    colors = sns.light_palette("green", 6)
    if data <= 10:
      color = colors[0]
    elif data <= 15:
      color = colors[1]
    elif data <= 20:
      color = colors[2]
    elif data <= 30:
      color = colors[3]
    elif data <= 40:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Men who are Underweight')
    colors = sns.light_palette("green", 6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 10%'))
    patches.append(mpatches.Patch(color=colors[1], label='10-15%'))
    patches.append(mpatches.Patch(color=colors[2], label='15-20%'))
    patches.append(mpatches.Patch(color=colors[3], label='20-30%'))
    patches.append(mpatches.Patch(color=colors[4], label='30-40%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 40%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_underweight_women_72():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = float(entry[BUFFER_IND + 72])
    colors = sns.light_palette("green", 6)
    if data <= 10:
      color = colors[0]
    elif data <= 15:
      color = colors[1]
    elif data <= 20:
      color = colors[2]
    elif data <= 30:
      color = colors[3]
    elif data <= 40:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Women who are Underweight')
    colors = sns.light_palette("green", 6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 10%'))
    patches.append(mpatches.Patch(color=colors[1], label='10-15%'))
    patches.append(mpatches.Patch(color=colors[2], label='15-20%'))
    patches.append(mpatches.Patch(color=colors[3], label='20-30%'))
    patches.append(mpatches.Patch(color=colors[4], label='30-40%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 40%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_normal_men_73_75():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = 100 - float(entry[BUFFER_IND + 73]) - float(entry[BUFFER_IND + 75])
    colors = sns.light_palette("green", 6)
    if data <= 50:
      color = colors[0]
    elif data <= 60:
      color = colors[1]
    elif data <= 70:
      color = colors[2]
    elif data <= 80:
      color = colors[3]
    elif data <= 90:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Men who are Normal weight')
    colors = sns.light_palette("green", 6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 50%'))
    patches.append(mpatches.Patch(color=colors[1], label='50-60%'))
    patches.append(mpatches.Patch(color=colors[2], label='60-70%'))
    patches.append(mpatches.Patch(color=colors[3], label='70-80%'))
    patches.append(mpatches.Patch(color=colors[4], label='80-90%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 90%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

def get_color_and_alpha_for_normal_women_72_74():
  def colorfunc(entry):
    # + x corresponds to the number of the metric from the document pdf
    data = 100 - float(entry[BUFFER_IND + 72]) - float(entry[BUFFER_IND + 74])
    colors = sns.light_palette("green", 6)
    if data <= 50:
      color = colors[0]
    elif data <= 60:
      color = colors[1]
    elif data <= 70:
      color = colors[2]
    elif data <= 80:
      color = colors[3]
    elif data <= 90:
      color = colors[4]
    else:
      color = colors[5]
    return color, 1
  def titlefunc(ax):
    ax.set_title('Women who are Normal weight')
    colors = sns.light_palette("green", 6)
    patches = []
    patches.append(mpatches.Patch(color=colors[0], label='< 50%'))
    patches.append(mpatches.Patch(color=colors[1], label='50-60%'))
    patches.append(mpatches.Patch(color=colors[2], label='60-70%'))
    patches.append(mpatches.Patch(color=colors[3], label='70-80%'))
    patches.append(mpatches.Patch(color=colors[4], label='80-90%'))
    patches.append(mpatches.Patch(color=colors[5], label='> 90%'))
    plt.legend(handles=patches)
  return colorfunc, titlefunc

BLUE = '#6699cc'
RED = '#ff3333'
BLACK = '#000000'
GRAY = '#cccccc'
WHITE = '#ffffff'

colfunc, titlefunc = get_color_and_alpha_for_women_high_blood_sugar_82()
fig = plt.figure()
ax = fig.gca()
shapes = sf.shapes()
BUFFER_IND = 5
for i, entry in enumerate(all):
  print(i)
  color, alphaval = colfunc(entry)
  map_indices = translate_nfhs_to_geo(*all[i][:2])
  for j in map_indices:
    shape = shapes[j]
    plot_shape(ax, shape, color, alphaval)
titlefunc(ax)
plot_state_outlines()
ax.autoscale(tight=True)
ax.set_aspect('equal')
plt.savefig('india.png', dpi=300, bbox_inches='tight', pad_inches=0)










