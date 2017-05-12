import csv
from descartes import PolygonPatch
import shapefile
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry.polygon import Polygon
import numpy as np

GRAY = '#cccccc'

# IND_adm_shp/IND_adm3.shp - Taluk Map - 2339 taluks
def print_taluk_map():
  sf = shapefile.Reader("IND_adm_shp/IND_adm3.shp")
  fig = plt.figure()
  ax = fig.gca()
  for i, district in enumerate(sf.shapes()):
    mp = district.__geo_interface__
    print(i)
    if mp['type'] == 'Polygon':
      ax.add_patch(PolygonPatch(Polygon(mp['coordinates'][0]), fc=GRAY, ec='#000000', alpha=1.0, zorder=2 ))
    elif mp['type'] == 'MultiPolygon':
      for poly in mp['coordinates']:
        ax.add_patch(PolygonPatch(Polygon(poly[0]), fc=GRAY, ec='#000000', alpha=1.0, zorder=2 ))
  ax.axis('equal')
  plt.savefig('india_taluk_map.png', dpi=300)

# IND_adm_shp/IND_adm2.shp - District Map - 666 taluks
def print_district_map():
  sf = shapefile.Reader("IND_adm_shp/IND_adm2.shp")
  fig = plt.figure()
  ax = fig.gca()
  for i, district in enumerate(sf.shapes()):
    mp = district.__geo_interface__
    print(i)
    if mp['type'] == 'Polygon':
      ax.add_patch(PolygonPatch(Polygon(mp['coordinates'][0]), fc=GRAY, ec='#000000', alpha=1.0, zorder=2 ))
    elif mp['type'] == 'MultiPolygon':
      for poly in mp['coordinates']:
        ax.add_patch(PolygonPatch(Polygon(poly[0]), fc=GRAY, ec='#000000', alpha=1.0, zorder=2 ))
  ax.axis('equal')
  plt.savefig('india_district_map.png', dpi=300)

# IND_adm_shp/IND_adm1.shp - State Map - 36 states and territories
def print_state_map():
  sf = shapefile.Reader("IND_adm_shp/IND_adm1.shp")
  fig = plt.figure()
  ax = fig.gca()
  for i, district in enumerate(sf.shapes()):
    mp = district.__geo_interface__
    print(i)
    if mp['type'] == 'Polygon':
      ax.add_patch(PolygonPatch(Polygon(mp['coordinates'][0]), fc='none', ec='#000000', alpha=0.5, zorder=2 ))
    elif mp['type'] == 'MultiPolygon':
      for poly in mp['coordinates']:
        ax.add_patch(PolygonPatch(Polygon(poly[0]), fc='none', ec='#000000', alpha=0.5, zorder=2, linewidth=0.5, joinstyle='round', capstyle='round'))
  ax.axis('equal')
  plt.savefig('india_state_map.png', dpi=300)

# IND_adm_shp/IND_adm0.shp - India Map - 1 nation
def print_nation_map():
  sf = shapefile.Reader("IND_adm_shp/IND_adm0.shp")
  fig = plt.figure()
  ax = fig.gca()
  for i, district in enumerate(sf.shapes()):
    mp = district.__geo_interface__
    print(i)
    if mp['type'] == 'Polygon':
      ax.add_patch(PolygonPatch(Polygon(mp['coordinates'][0]), fc=GRAY, ec='#000000', alpha=1.0, zorder=2, linewidth=1))
    elif mp['type'] == 'MultiPolygon':
      for poly in mp['coordinates']:
        ax.add_patch(PolygonPatch(Polygon(poly[0]), fc=GRAY, ec='#000000', alpha=1.0, zorder=2, linewidth=1, joinstyle='round', capstyle='round'))
  ax.axis('equal')
  plt.savefig('india_map.png', dpi=300)




def print_state_district_map():
  fig = plt.figure()
  ax = fig.gca()
  sf = shapefile.Reader("IND_adm_shp/IND_adm1.shp")
  records = sf.records()
  states = set({d[4] for d in records})
  colors = sns.color_palette("Set2", len(states)).as_hex()
  np.random.shuffle(colors)
  color_map = {s: colors[i] for i, s in enumerate(list(states))}
  for i, district in enumerate(sf.shapes()):
    mp = district.__geo_interface__
    print(i)
    if mp['type'] == 'Polygon':
      ax.add_patch(PolygonPatch(Polygon(mp['coordinates'][0]), fc=color_map[records[i][4]], ec='#000000', alpha=1.0, zorder=2, linewidth=0.75, joinstyle='round', capstyle='round'))
    elif mp['type'] == 'MultiPolygon':
      for poly in mp['coordinates']:
        ax.add_patch(PolygonPatch(Polygon(poly[0]), fc=color_map[records[i][4]], ec='#000000', alpha=1.0, zorder=2, linewidth=0.75, joinstyle='round', capstyle='round'))
  sf = shapefile.Reader("IND_adm_shp/IND_adm2.shp")
  records = sf.records()
  for i, district in enumerate(sf.shapes()):
    mp = district.__geo_interface__
    print(i)
    if mp['type'] == 'Polygon':
      ax.add_patch(PolygonPatch(Polygon(mp['coordinates'][0]), fc='none', ec='#000000', alpha=0.5, zorder=2, linewidth=0.25, joinstyle='round', capstyle='round'))
    elif mp['type'] == 'MultiPolygon':
      for poly in mp['coordinates']:
        ax.add_patch(PolygonPatch(Polygon(poly[0]), fc='none', ec='#000000', alpha=0.5, zorder=2, linewidth=0.25, joinstyle='round', capstyle='round'))
  ax.axis('equal')
  plt.savefig('india_district_map.png', dpi=300)





