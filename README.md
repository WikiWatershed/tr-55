# tr-55

A Python implementation of TR-55.

## Functions

`simulate_all_tiles` and `simulate_year` are the two functions intended for consumers of this module.

### `simulate_all_tiles`

The `simulate_all_tiles` function simulates the events of a single day.  It takes three arguments:

   1. `parameters` which is either a `date` object (which is mapped to *precipitation* and *evapotranspiration* using sample year data) or that argument is a single day's *precipitation* and *evapotranspiration* as a tuple of two floats (in units of inches).

      If the sample year data are to be considered typical, *precipitation* should generally be between 0 and 3 inches daily, and *evapotranspiration* should be between 0 and 0.2 inches daily.

   2. `tile_census` is a dictionary containing the number of appearances of each type of tile in the query area, e.g.
   ```Python
       {
           "result": {
               "cell_count": 147,
               "distribution": {
                   "d:hi_residential": 33,
                   "c:commercial": 42,
                   "a:deciduous_forest": 72
               }
           }
       }
   ```
   Here, `"d:hi_residential"` indicates *High-Intensity Residential* land use on top of *Type D* soil.

   3. `pre_columbian` is a boolean argument which controls whether or not to simulate the given area under pre-Columbian conditions.  When this is set to true, all land-uses other than *water* and *wetland* are treated as *mixed forest*.

The algorithm used is close to TR-55 (the algorithm found in [the USDA's Technical Release 55, revised 1986](http://www.cpesc.org/reference/tr55.pdf)), but with a few differences.  The main differences are:

   * it applies the TR-55 algorithm on a tile-by-tile basis and aggregates the results rather than running the TR-55 algorithm once over the entire area
   * it uses the *Pitt Small Storm Hydrology Model* on tiles which are of a "built-type" when precipitation is two inches or less

and there are numerous other small differences, as well.

`simulate_all_tiles` returns a triple of *runoff*, *evapotranspiration*, and *infiltration* (all in units of inches).

### `simulate_year`

The `simulate_year` function takes two parameters, `tile_census` and `pre_columbian` as described above, and simulates an entire year using a year's worth of sample precipitation and evapotranspiration data.  It returns a triple of *runoff*, *evapotranspiration*, and *infiltration* for the given area over the entire sample year.

## Usage Example

The following program:
```Python
from tr55.model import simulate_year

tiles = {
    "result": {
        "cell_count": 147,
        "distribution": {
            "d:hi_residential": 33,
            "c:commercial": 42,
            "a:deciduous_forest": 72
        }
    }
}

(q,et,inf) = simulate_year(tiles)
print "%f inches of runoff, %f inches of et, %f inches of infiltration." % (q, et, inf)
```
should produce the following output:
```
17.614212 inches of runoff, 15.167862 inches of et, 20.245580 inches of infiltration.
```

## Testing

Run `nosetests` from within the project directory.
