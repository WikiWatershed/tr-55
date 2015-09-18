## 1.0.0

- Input format was changed. Strings used to run a model now align to NLCD types. A full list is provided in the readme. Other land types that were similar to NLCD types (and used these types to do calculations) were removed.
- Output strings were changed to match NLCD types.

## 0.2.2

- Same as `0.2.1`, but with a valid `setup.py` version.

## 0.2.1

- Fixes a bug in the computation of modified censuses. (https://github.com/WikiWatershed/tr-55/pull/40)

## 0.2.0

- The output format was changed. Previously, only the overall result of the calculation was given, after this change the overall result plus the sub-results for each (nlcd,soil) pair are given. (https://github.com/WikiWatershed/tr-55/pull/30)
- Some code was added to generate and compare mini-app ables. (https://github.com/WikiWatershed/tr-55/pull/31, https://github.com/WikiWatershed/tr-55/pull/38)
- Attempt to plug in the correct NLCD codes. Previously there were some "names" in the mini-app that did not have an associated NLCD code in the TR-55. (https://github.com/WikiWatershed/tr-55/pull/32)
- Changed the the format of the input expected by the code. It allows for areas that are covered by both reclassifications and BMPs. (https://github.com/WikiWatershed/tr-55/pull/35)
- Made it easier to do Pre-Columbian calculations. (https://github.com/WikiWatershed/tr-55/pull/37)

## 0.1.0

- Added simple STEP-L based water quality routines.

## 0.1.0.dev2

- Initial development release.
