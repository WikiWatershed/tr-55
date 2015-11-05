##### Instructions for contributing code to be included in the [MMW](https://github.com/WikiWatershed/model-my-watershed) implementation of this module.

#### Branches

* `develop` - commits made to `develop` will be deployed during the following release.
* `master` - commits are merged from `develop` when we create a release.  `master` typically reflects the contents of the current release on [PyPi](https://pypi.python.org/pypi/tr55)
* feature branches - new work is branched from an up-to-date `develop` branch
```bash
git pull origin develop
git checkout -b feature/[my initials]/[short-desc-of-feature]
```


#### Adding commits to `develop`
All feature branches should be merged into `develop` through a [Pull Request](https://help.github.com/articles/using-pull-requests/) on GitHub.  This ensures that other developers have a chance to review the changes and make comments about the suitability/implications, etc.  Typically when you receive several `+1` comments, it’s ok to merge in via the GitHub web interface.

Typically, one would push their local feature branch containing the new commits to the origin:
```bash
git push origin [feature/branch-name]
```

Commit messages should follow standard formatting: 1 short line acting as a title of the commit followed by a linebreak and then a summary of the goal of the commit and why it was necessary, plus any additional information that would be helpful for reviewing.

All created Pull Requests will kick off a job that runs the current suite of tests against the new code on [TravisCI](https://travis-ci.org/WikiWatershed/tr-55) - a service to enforce that test pass before allowing GitHub merges. The status of the tests can be seen at the bottom of the PR comment thread. You will not be able to merge until the tests have passed.

#### Testing
Running `python setup.py test` from the root of the project will run the test suite.  Please make sure to run the tests before submitting a PR.  If you are adding or altering functionality, it is advised to add a test to the [suite](https://github.com/WikiWatershed/tr-55/tree/develop/test) to verify that it works, or modify a test of the changed functionality.


#### Requesting version update in MMW
The release process, as described in the [README](https://github.com/WikiWatershed/tr-55/blob/develop/README.md) will result in a new version of this package being released to PyPi.  When that is done, the changes won't automatically appear in new releases of MMW, which are pinned to a specific version.  Discuss with Azavea to arrange an initiation of a release and update to MMW.
