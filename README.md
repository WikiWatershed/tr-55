# tr-55

A Python implementation of TR-55.

## Installation
You can install the latest version from PyPI
```bash
pip install tr55
```

## Functions

`simulate_cell_year`, `simulate_water_quality`, and `simulate_modifications` are the three functions most likely to be of direct interest for users of this module.

### `simulate_cell_year`

The `simulate_cell_year` function simulates the events of an entire year for one specific type of cell.  It takes three arguments:

   1. `cell` is a string consisting of a soil type and land use pair separated by a colon, for example `"a:rock"`.

   2. `cell_count` is the number of occurrences of that type of cell in the area of interest.

   3. `precolumbian` is a boolean which determines whether to simulate the cell type as-shown or under Pre-Columbian circumstances.  When a Pre-Columbian simulation is done, all land uses other than *water* and *wetland* are treated as *mixed forest*.

The output of this function is a dictionary with three keys: `runoff-vol`, `et-vol`, and `inf-vol`.  These are the volumes of runoff, evapotranspiration, and infiltration, respectively, in units of inch-cells.  The algorithm used to calculate these quantities is close to TR-55, the algorithm found in [the USDA's Technical Release 55, revised 1986](http://www.cpesc.org/reference/tr55.pdf), but with a few differences.  The main difference is the use of *Pitt Small Storm Hydrology Model* for low levels of precipitation when the land use is a built-type.

### `simulate_water_quality`

The `simulate_water_quality` function does a water quality calculation over an entire area of interest.  The arguments are:

   1. `tree`, the tree-like dictionary which contains the distribution of cell types in the area of interest.  For example:

   ```Python
   {
       "cell_count": 8,
       "distribution": {
           "c:commercial": {"cell_count": 5},
           "a:deciduous_forest": {
               "cell_count": 3
               "distribution": {
                   "a:deciduous_forest": {"cell_count": 1},
                   "a:no_till": {"cell_count": 1},
                   "d:rock": {"cell_count", 1}
               }
           }
       }
   }
   ```

   represents an area of interest that is eight cells in size, with five of those cells of type `"c:commercial"` (*commercial* land use on top of type *C* soil), and one cell each of *deciduous forest*, *no-till farming*, and *rock*.

   The single cells of *deciduous forest*, *no-till*, and the *rock* are all underneath a node of three cells of type *deciduous forest*.  That indicates a land use modification has taken place: in this case, two of three original cells of *deciduous forest* have undergone modifications.

   2. The `cell_res` parameter gives the resolution (size) of each cell.  It is used for converting runoff, evapotranspiration, and infiltration amounts from inches to volumes.

   3. `fn` is the function that is used to perform the runoff, evapotranspiration, and infiltration calculation.  It is similar to `simulate_cell_year`, except it only takes `cell` and `cell_count` arguments.

### `simulate_modifications`

This function is used to simulate the effects of land use modifications.  The arguments are:

   1. `census` contains the distribution of cell types in the area of interest, along with an array of modifications.  For example, the following:

   ```Python
   {
       "cell_count": 8,
       "distribution": {
           "c:commercial": {"cell_count": 5},
           "a:deciduous_forest": {"cell_count": 3}
       },
       "modifications": [
           {
               "bmp": "no_till",
               "cell_count": 1,
               "distribution": {
                   "a:deciduous_forest": {"cell_count": 1},
               }
           },
           {
               "reclassification": "d:rock",
               "cell_count": 1,
               "distribution": {
                   "a:deciduous_forest": {"cell_count": 1}
               }
           }
       ]
   }
   ```

   is the census that corresponds to the `tree` given in the discusson of `simulate_wate_quality` above.  There is an area of interest eight cells in size, with five of type `"c:commercial"` and three of type `"a:deciduous_forest"`.

   modifications are given as an array of dictionaries.  Each dictionary contains a either a `bmp` key or a `reclassification` key, indicating what type of modification has taken place.

   2. The `cell_res` argument is as described previously.

   3. The `precolumbian` argument is as described previously.

   4. The `fn` argument is as described previously.  If this argument is not supplied, then `simulate_cell_year` will be used to compute the runoff, evapotranspiration, and infiltration values.  A custom function can be supplied to do different types of calculations, such as calculations over shorter or longer time spans.  If a custom function is supplied, the `precolumbian` argument will be ignored.

The output is dictionary with two keys, `modified` and `unmodified`.  These respectively contain modified and unmodified trees (as described in the discussion of `simulate_water_quality`) with runoff, evapotranspiration, infiltration, and pollutant loads included.

## Usage Example

The output of the following program:
```Python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import pprint

from tr55.model import simulate_modifications

cells = {
    "cell_count": 147,
    "distribution": {
        "d:hi_residential": {"cell_count": 33},
        "c:commercial": {"cell_count": 42},
        "a:deciduous_forest": {"cell_count": 72}
    },
    "modifications": [
        {
            "bmp": "no_till",
            "cell_count": 30,
            "distribution": {
                "d:hi_residential": {"cell_count": 10},
                "c:commercial": {"cell_count": 20}
            }
        },
        {
            "reclassification": "d:rock",
            "cell_count": 5,
            "distribution": {
                "a:deciduous_forest": {"cell_count": 5}
            }
        }
    ]
}

pprint.pprint(simulate_modifications(cells))
```
is partially reproduced here:
```Python
 'unmodified': {'bod': 1762.555509187117,
                'cell_count': 147,
                'distribution': {'a:deciduous_forest': {'bod': 0.0,
                                                        'cell_count': 72,
                                                        'et': 26.51670000000007,
                                                        'inf': 34.91810000000001,
                                                        'runoff': 0.0,
                                                        'tn': 0.0,
                                                        'tp': 0.0,
                                                        'tss': 0.0},
                                 'c:commercial': {'bod': 1061.0138827829708,
                                                  'cell_count': 42,
                                                  'et': 2.272860000000005,
                                                  'inf': 4.430079770137537,
                                                  'runoff': 36.375400229862464,
                                                  'tn': 7.786472849455671,
                                                  'tp': 1.2321451541995787,
                                                  'tss': 216.39549270630107},
                                 'd:hi_residential': {'bod': 701.5416264041463,
                                                      'cell_count': 33,
                                                      'et': 6.818579999999993,
                                                      'inf': 8.361629213022574,
                                                      'runoff': 32.167342828759615,
                                                      'tn': 4.072508593956273,
                                                      'tp': 0.6837058223430238,
                                                      'tss': 83.8282790872751}},
                'et': 15.167861632653095,
                'inf': 20.24558036990151,
                'runoff': 17.614211721110824,
                'tn': 11.858981443411944,
                'tp': 1.9158509765426026,
                'tss': 300.2237717935762}
```

The output shown is another tree-like dictionary, akin to the one in the discussion of the first parameter of the `simulate_water_quality` function, except with additional keys and values attached to each  node in the tree.  The additional keys, `runoff`, `tss`, and so on, have associated values which are the water volumes and pollutant loads that have been calculated.  The volumes and loads at the leaves of the tree are those returned by the `fn` function (the fourth parameter of the `simulate_modifications` function), while those of internal nodes are the sums of the amounts found in their child nodes.

## Testing

Run `python setup.py test` from within the project directory.


## Deployments
Deployments to PyPi are handled through [Travis-CI](https://travis-ci.org/WikiWatershed/tr-55). The following git flow commands approximate a release using Travis:

``` bash
$ git flow release start 0.1.0
$ vim CHANGELOG.md
$ git commit -m "0.1.0"
$ git flow release publish 0.1.0
$ git flow release finish 0.1.0
```

To kick off the deployment, you'll still need to push the local tags remotely
`git push --tags`

## License
This project is licensed under the terms of the Apache 2.0 license.
