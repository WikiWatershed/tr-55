# tr-55

A Python implementation of TR-55.

## Installation
You can install the latest version from PyPI
```bash
pip install tr55
```

## Functions

`simulate_day`, `simulate_year`, `simulate_modifications` are the three functions most likely to be of direct interest for users of this module.

### `simulate_day`

The `simulate_day` function simulates the events of a single day.  It takes four arguments:

   1. `day` has one of two types.  If it is an integer, it representing the day of the year (where `day == 0` represents October 15th) and is used to retrieve the precipitation and evapotranspiration for that day from the sample year table.  Alternatively, `day` can be a tuple of precipitation and evapotranspiration.

      If the sample year data are to be considered typical, *precipitation* should generally be between 0 and 3 inches daily, and *evapotranspiration* should be between 0 and 0.2 inches daily.

   2. `tile_census` is a dictionary containing the number of appearances of each type of tile in the query area, as well as modifications, e.g.
   ```Python
    {
        "cell_count": 147,
        "distribution": {
            "d:hi_residential": {"cell_count": 33},
            "c:commercial": {"cell_count": 42},
            "a:deciduous_forest": {"cell_count": 72}
        },
        "modifications": {
            ":no_till": {
                "cell_count": 30,
                "distribution": {
                    "d:hi_residential": {"cell_count": 10},
                    "c:commercial": {"cell_count": 20}
                }
            },
            "d:rock": {
                "cell_count": 5,
                "distribution": {
                    "a:deciduous_forest": {"cell_count": 5}
                }
            }
        }
    }
   ```
   Here, `"d:hi_residential"` indicates *High-Intensity Residential* land use on top of *Type D* soil, `"c:commerical"` indicates *Commercial* land use on top of *Type C* soil, and so on.

   The `":no_till"` key and its value say that 10 units of `"d:hi_residential"` should be turned into `"d:no_till"` and 20 units of `"c:commercial"` should be turned into `"c:no_till"`.  The `"d:rock"` key and its value say that 5 units of `"a:deciduous_forest"` should be reclassified as `"d:rock"`.

   3. `subst` is a substitution that should be performed on the census.  It is used to implement the BMPs/reclassifications mentioned above.  When `subst` is a colon followed by a BMP, then the BMP is superimposed on all of the tiles in the census.  When `subst` is a soil type and a land use, then all tiles in the census are treated as if they have that soil type and land use.

   4. `pre_columbian` is a boolean argument which controls whether or not to simulate the given area under pre-Columbian conditions.  When it set to true, all land-uses other than *water* and *wetland* are treated as *mixed forest*.

The algorithm implemented by this code is close to TR-55, the algorithm found in [the USDA's Technical Release 55, revised 1986](http://www.cpesc.org/reference/tr55.pdf), but with a few differences.  The main differences are:

   * it applies the TR-55 algorithm on a tile-by-tile basis and aggregates the results rather than running the TR-55 algorithm once over the entire area
   * it uses the *Pitt Small Storm Hydrology Model* on tiles which are of a "built-type" when precipitation is two inches or less

and there are numerous other small differences.

`simulate_day` returns a dictionary with `runoff`, `et`, and `inf` keys.  All three of these numbers are in units of inches.

### `simulate_year`

The `simulate_year` and simulates an entire year using one year of sample precipitation and evapotranspiration data.  It returns a dictionary of with `runoff`, `et`, and `inf` keys, and also keys which map associated with various pollutant loads.

The function takes four parameters.  `tile_census`, `subst`, and `pre_columbian` as described above.  The `cell_res` argument gives the resolution in meters of the data.

### `simulate_modifications`

This function takes three parameters, `tile_census`, `cell_res`, and `pre_columbian`, all as described above.  The output of this function is similar to that of `simulate_year`, except it shows the results both with and without modifications.

## Usage Example

The following program:
```Python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import pprint

from tr55.model import simulate_modifications

tiles = {
    "cell_count": 147,
    "distribution": {
        "d:hi_residential": {"cell_count": 33},
        "c:commercial": {"cell_count": 42},
        "a:deciduous_forest": {"cell_count": 72}
    },
    "modifications": {
        ":no_till": {
            "cell_count": 30,
            "distribution": {
                "d:hi_residential": {"cell_count": 10},
                "c:commercial": {"cell_count": 20}
            }
        },
        "d:rock": {
            "cell_count": 5,
            "distribution": {
                "a:deciduous_forest": {"cell_count": 5}
            }
        }
    }
}

pprint.pprint(simulate_modifications(tiles))
```
should produce the following output:
```Python
{u'modified': {u'bod': 1155.5832690023512,
               u'cell_count': 147,
               u'distribution': {u'a:deciduous_forest': {u'bod': 1.9676947491691286,
                                                         u'cell_count': 72,
                                                         u'et': 24.675262500000017,
                                                         u'inf': 34.53218880673186,
                                                         u'runoff': 0.7999320266014792,
                                                         u'tn': 0.006128885284297285,
                                                         u'tp': 0.00019354374581991428,
                                                         u'tss': 1.258034347829443},
                                 u'c:commercial': {u'bod': 619.3321622220828,
                                                   u'cell_count': 42,
                                                   u'et': 17.42526,
                                                   u'inf': 16.198443763932524,
                                                   u'runoff': 21.23295052178176,
                                                   u'tn': 4.545098932436254,
                                                   u'tp': 0.7192244464514511,
                                                   u'tss': 126.3137934080361},
                                 u'd:hi_residential': {u'bod': 534.2834120310993,
                                                       u'cell_count': 33,
                                                       u'et': 15.08352545454543,
                                                       u'inf': 13.967458770273502,
                                                       u'runoff': 24.498158107332266,
                                                       u'tn': 3.101560485095788,
                                                       u'tp': 0.5206999354540374,
                                                       u'tss': 63.842339912190674}},
               u'et': 20.450586122448982,
               u'inf': 24.67740388835977,
               u'runoff': 11.957947247429287,
               u'tn': 7.652788302816338,
               u'tp': 1.2401179256513084,
               u'tss': 191.41416766805622},
 u'unmodified': {u'bod': 1762.555509187117,
                 u'cell_count': 147,
                 u'distribution': {u'a:deciduous_forest': {u'bod': 0.0,
                                                           u'cell_count': 72,
                                                           u'et': 26.51670000000007,
                                                           u'inf': 34.91810000000001,
                                                           u'runoff': 0.0,
                                                           u'tn': 0.0,
                                                           u'tp': 0.0,
                                                           u'tss': 0.0},
                                   u'c:commercial': {u'bod': 1061.0138827829708,
                                                     u'cell_count': 42,
                                                     u'et': 2.272860000000005,
                                                     u'inf': 4.430079770137537,
                                                     u'runoff': 36.375400229862464,
                                                     u'tn': 7.786472849455671,
                                                     u'tp': 1.2321451541995787,
                                                     u'tss': 216.39549270630107},
                                   u'd:hi_residential': {u'bod': 701.5416264041463,
                                                         u'cell_count': 33,
                                                         u'et': 6.818579999999993,
                                                         u'inf': 8.361629213022574,
                                                         u'runoff': 32.167342828759615,
                                                         u'tn': 4.072508593956273,
                                                         u'tp': 0.6837058223430238,
                                                         u'tss': 83.8282790872751}},
                 u'et': 15.167861632653095,
                 u'inf': 20.24558036990151,
                 u'runoff': 17.614211721110824,
                 u'tn': 11.858981443411944,
                 u'tp': 1.9158509765426026,
                 u'tss': 300.2237717935762}}
```

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
