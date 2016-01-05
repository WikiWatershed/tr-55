"""
Generates a table with the model output for different input values.
This table is used in the mini-app.
"""

from itertools import product

from tr55.model import simulate_day

import matplotlib.pyplot as plt
import pandas as pd

def cm_to_inches(cm):
    return cm / 2.54

def inches_to_cm(inches):
    return inches * 2.54


# values of inputs to the model
precip_cm = [1, 1.5, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5,
             5.07, 5.08, 5.09, 5.25, 5.5, 5.75, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 12, 15, 18, 21]

# The land uses in the original mini-app used non NLCD types
# (residential, high intensity residential, commercial, etc.) These were
# converted to the best matches from the NLCD types based on the NLCD
# number being used for the calculations in tables.py.
land_uses = [
    'open_water',
    'developed_open',
    'developed_low',
    'developed_med',
    'developed_high',
    'barren_land',
    'deciduous_forest',
    'evergreen_forest',
    'mixed_forest',
    'shrub',
    'grassland',
    'pasture',
    'cultivated_crops',
    'woody_wetlands',
    'herbaceous_wetlands'
]

soil_types = ['a', 'b', 'c', 'd']

soil_type_map = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3
}

look = product(precip_cm,land_uses,soil_types)


# For each input value, compute the model outputs for a
# single day and tile.

precip_list = []
lu_list = []
st_list  =[]
evapoT = []
infiltration = []
runoff = []
for precip, land_use, soil_type in product(precip_cm,
                                           land_uses,
                                           soil_types):
    cells = {
        'cell_count': 1,
        'distribution': {
            '%s:%s' % (soil_type, land_use): {'cell_count': 1}
        }
    }

    model_out = simulate_day(cells, cm_to_inches(precip))['unmodified']

    precip_list.append(precip)
    lu_list.append(land_use)
    st_list.append(soil_type)
    evapoT.append(inches_to_cm(model_out['et']))
    infiltration.append(inches_to_cm(model_out['inf']))
    runoff.append(inches_to_cm(model_out['runoff']))

d = {'precip' : pd.Series(precip_list),
     'land_use' : pd.Series(lu_list),
     'soil_type' : pd.Series(st_list),
     'evapotrans' : pd.Series(evapoT),
     'infiltration' : pd.Series(infiltration),
     'runoff' : pd.Series(runoff),

}
df = pd.DataFrame(d)

df.to_csv(path_or_buf='Results_20151118_WetTo30.csv',
          columns=('precip','land_use','soil_type','evapotrans','infiltration','runoff'),
          index=False)

grouped = df.groupby(['soil_type','land_use'])

# Plot
plt.close('all')
figure, axes = plt.subplots()
for name, group in grouped:
    axes.plot(group.precip, group.runoff, label=name[1])
axes.legend()

plt.show()