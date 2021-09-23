# tr-55

A Python implementation of a modified TR-55 stormwater runoff model with STEP-L like water quality routines.


## Installation

You can install the latest version from PyPI
```bash
pip install tr55
```

The `simulate_day` is the function most likely to be of direct interest for users of this module.

The `simulate_water_quality` and `simulate_modifications` functions are two other functions which can be used to create simulations with additional behaviors beyond those supplied by `simulate_day`.


## `simulate_day`

This function takes four arguments: a census of the area of interest (see the description given below in the discussion of `simulate_modifications`), an amount of precipitation in inches, an optional cell resolution (the size of a cell in square meters), and an optional Boolean  to control whether or not a Pre-Columbian simulation is done.

For each cell type present in the area of interest, it calculates runoff, infiltration, evapotranspiration, and pollutant loads caused by that cell type.  The algorithm used to calculate the water volumes is close to TR-55, the algorithm found in [the USDA's Technical Release 55, revised 1986](http://www.cpesc.org/reference/tr55.pdf), but with a few differences.  The main difference is the use of *Pitt Small Storm Hydrology Model* for low levels of precipitation when the land use is a built-type.  STEP-L like routines are used for the water quality calculations.

## Functions for Custom Scenarios

### `simulate_water_quality`

The `simulate_water_quality` function does a water quality calculation over an entire area of interest.  The arguments are:

   1. `tree`, the tree-like dictionary which contains the distribution of cell types in the area of interest.  For example:

   ```Python
   {
       "cell_count": 8,
       "distribution": {
           "c:developed_high": {"cell_count": 5},
           "a:deciduous_forest": {
               "cell_count": 3
               "distribution": {
                   "a:deciduous_forest": {"cell_count": 1},
                   "a:no_till": {"cell_count": 1},
                   "d:barren_land": {"cell_count", 1}
               }
           }
       }
   }
   ```

   represents an area of interest that is eight cells in size, with five of those cells of type `"c:developed_high"` (*Developed High Intensity* land use on top of type *C* soil), and one cell each of *deciduous forest*, *no-till farming*, and *barren land*.

   The single cells of *deciduous forest*, *no-till*, and the *barren land* are all underneath a node of three cells of type *deciduous forest*.  That indicates a land use modification has taken place: in this case, two of three original cells of *deciduous forest* have undergone modifications.

   2. The `cell_res` parameter gives the resolution (size) of each cell.  It is used for converting runoff, evapotranspiration, and infiltration amounts from inches to volumes.

   3. `fn` is the function that is used to perform the runoff, evapotranspiration, and infiltration calculation.  It takes `cell` and `cell_count` as arguments.

   4. The optional parameter `current_cell` contains the string description of the cell currently being worked on (e.g. "a:deciduous_forest").

   5. The optional Boolean `precolumbian` determines whether to simulate the cell type as-shown or under Pre-Columbian circumstances.  When a Pre-Columbian simulation is done, all developed land (NLCD 21-24) uses are treated as *mixed forest*.

In all probability, the fourth parameter will not need to be supplied if you are calling this function from external code.

### `simulate_modifications`

This function is used to simulate the effects of land use modifications.  The arguments are:

   1. `census` contains the distribution of cell types in the area of interest, along with an array of modifications.  For example, the following:

   ```Python
   {
       "cell_count": 8,
       "distribution": {
           "c:developed_high": {"cell_count": 5},
           "a:deciduous_forest": {"cell_count": 3}
       },
       "modifications": [
           {
               "change": "::no_till",
               "cell_count": 1,
               "distribution": {
                   "a:deciduous_forest": {"cell_count": 1},
               }
           },
           {
               "change": "d:barren_land:",
               "cell_count": 1,
               "distribution": {
                   "a:deciduous_forest": {"cell_count": 1}
               }
           }
       ]
   }
   ```

   is the census that corresponds to the `tree` given in the discussion of `simulate_water_quality` above.  There is an area of interest eight cells in size, with five of type `"c:developed_high"` and three of type `"a:deciduous_forest"`.

   Modifications are given as an array of dictionaries.  Each dictionary contains a `change` key whose value encodes the modification that has taken place.  In the example above, `"::no_till"` indicates that the no-till farming BMP has been applied, while `"a:barren_land:"` means that that particular area has been reclassified as being most barren_land sitting on top of A-type soil.

   2. The `fn` argument is as described previously in the discussion of `simulate_water_quality`.  It is responsible for performing the simulation at each cell.

   3. The `cell_res` argument is as described previously.

   4. The optional Boolean parameter `precolumbian` determines whether to simulate the cell type as-shown or under Pre-Columbian circumstances.  When a Pre-Columbian simulation is done, all land uses other than *water* and *wetland* are treated as *mixed forest*.

The output is dictionary with two keys, `modified` and `unmodified`.  These respectively contain modified and unmodified trees (the trees are as described in the discussion of `simulate_water_quality`) with runoff, evapotranspiration, infiltration, and pollutant loads included.


## Allowed Types

The following land use values are implemented and correspond to the keys listed:

 - 'open_water' - NLCD Type 11, Open Water
 - 'developed_open' - NLCD Type 21, Developed, Open Space
 - 'developed_low'- NLCD Type 22, Developed, Low Intensity
 - 'developed_med' - NLCD Type 23, Developed, Medium Intensity
 - 'developed_high' - NLCD Type 24, Developed, High Intensity
 - 'barren_land' - NLCD Type 31, Barren Land (Rock/Sand/Clay)
 - 'deciduous_forest' - NLCD Type 41, Deciduous Forest
 - 'evergreen_forest' - NLCD Type 42, Evergreen Forest
 - 'mixed_forest' - NLCD Type 43, Mixed Forest
 - 'shrub' - NLCD Type 52, Shrub/Scrub
 - 'grassland' - NLCD Type 71, Grassland/Herbaceous
 - 'pasture' - NLCD Type 81, Pasture/Hay
 - 'cultivated_crops' - NLCD Type 82, Cultivated Crops
 - 'woody_wetlands' - NLCD Type 90, Woody Wetlands
 - 'herbaceous_wetlands' - NLCD Type 95, Emergent Herbaceous Wetlands


## Usage Example

The output of the following program:
```Python
# -*- coding: utf-8 -*-

import pprint

from tr55.model import simulate_day

census = {
    "cell_count": 147,
    "distribution": {
        "d:developed_med": {"cell_count": 33},
        "c:developed_high": {"cell_count": 42},
        "a:deciduous_forest": {"cell_count": 72}
    },
    "modifications": [
        {
            "change": "::no_till",
            "cell_count": 30,
            "distribution": {
                "d:developed_med": {"cell_count": 10},
                "c:developed_high": {"cell_count": 20}
            }
        },
        {
            "change": "d:barren_land:",
            "cell_count": 5,
            "distribution": {
                "a:deciduous_forest": {"cell_count": 5}
            }
        }
    ]
}

pprint.pprint(simulate_day(census, 0.984))
```
is partially reproduced here:
```Python
u'unmodified': {u'bod': 43.11309178874012,
                 u'cell_count': 147,
                 u'distribution': {u'a:deciduous_forest': {u'bod': 0.0,
                                                           u'cell_count': 72,
                                                           u'et': 0.14489999999999997,
                                                           u'inf': 0.8391,
                                                           u'runoff': 0.0,
                                                           u'tn': 0.0,
                                                           u'tp': 0.0,
                                                           u'tss': 0.0},
                                   u'c:developed_high': {u'bod': 28.342317499361275,
                                                         u'cell_count': 42,
                                                         u'et': 0.012322664565942195,
                                                         u'inf': 0.0,
                                                         u'runoff': 0.9716773354340579,
                                                         u'tn': 0.2079960397130545,
                                                         u'tp': 0.03291365903151632,
                                                         u'tss': 5.780461367410053},
                                   u'd:developed_med': {u'bod': 14.770774289378844,
                                                        u'cell_count': 33,
                                                        u'et': 0.037259999999999995,
                                                        u'inf': 0.26946506358880085,
                                                        u'runoff': 0.6772749364111992,
                                                        u'tn': 0.08574559651037718,
                                                        u'tp': 0.014395246129479379,
                                                        u'tss': 1.764982351527472}},
                 u'et': 0.08285667967190184,
                 u'inf': 0.47147991223422064,
                 u'runoff': 0.4296634080938776,
                 u'tn': 0.2937416362234317,
                 u'tp': 0.0473089051609957,
                 u'tss': 7.545443718937525}
```

The output shown is a tree-like dictionary, akin to the one in the discussion of the first parameter of the `simulate_water_quality` function, except with additional keys and values attached to each  node in the tree.  The additional keys, `runoff`, `tss`, and so on, have associated values which are the water volumes and pollutant loads that have been calculated.  The volumes and loads at the leaves of the tree are those returned by the `fn` function (the second parameter of the `simulate_modifications` function), while those of internal nodes are the sums of the amounts found in their child nodes.


## Development

Development uses [pipenv](https://pipenv.pypa.io/en/latest/). After cloning this repository, setup your local development environment with:

```console
$ pipenv install --dev
```

## Testing

```console
$ pipenv run nosetests --verbosity=2
```

## Deployments

Create a new release using git flow:

```console
$ git flow release start 2.0.0
$ vim CHANGELOG.md
$ vim setup.py
$ git add CHANGELOG.md setup.py
$ git commit -m "2.0.0"
$ git flow release publish 2.0.0
```

Then create a wheel to publish to PyPI using [build](https://github.com/pypa/build):

```console
$ pipenv run python -m build
```

This should create two files under `dist/`:

```console
$ ls -1 dist/
tr55-2.0.0.tar.gz
tr55-2.0.0-py2.py3-none-any.whl
```

Then publish the wheel to PyPI using [twine](https://github.com/pypa/twine/) and credentials from LastPass:

```console
$ python -m twine check dist/*
Checking dist/tr55-2.0.0-py2.py3-none-any.whl: PASSED
Checking dist/tr55-2.0.0.tar.gz: PASSED
```
```console
$ python -m twine upload dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: azavea
Enter your password:
Uploading tr55-2.0.0-py2.py3-none-any.whl
100%|
Uploading tr55-2.0.0.tar.gz
100%|

View at:
https://pypi.org/project/tr-55/2.0.0/
```

Finally, finish the release:

```console
$ git flow release finish -p 2.0.0
```

## License

This project is licensed under the terms of the Apache 2.0 license.
