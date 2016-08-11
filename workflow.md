1. Use github extensively.
2. Make an issue for every feature/change/bug you can think of. 
 * If you are doing something, there should always be a corresponding issue for it.
 * Possibly also use issue labels to indicate importance, bugs, etc.
 * Be as granular with issues as possible. If there are issues that are sub-issues, that may mean that the issue is actually a milestone.
3. If you start working on an issue, assign yourself to it.
4. Make a new branch for whatever you're working on.
 * Never do any work on the master branch.
5. When finished, create a pull request to the master branch. 
 * If you reference the issue/s with "fixes" or "resolves" the issue/s will automatically close. For example `resolves #4` or `fixes #2` (Actually [here](https://github.com/gitbucket/gitbucket/wiki/How-to-Close-Reference-issues-&-pull-request) is a full doc of this feature)
6. Another person (or possibly multiple people) takes a look at it. If they deem the PR acceptable, they will pull the branch into master branch and then delete the branch (and close the corresponding issue if it's not done automatically).
7. Rinse and repeat.
