---
title: "Bisection"
date: 2021-02-10T11:41:21Z
draft: true
description: "KernelCI Bisection support"
---


Why run automated bisections?

KernelCI periodically monitors a series of kernel trees (mainline,
stable, next...), and builds them when it detects some changes in them.
It then runs some tests with the resulting kernel binaries on a variety
of platforms. When a test fails, it compares the results with previous
kernel revisions from that same branch on the same platform. If it was
working previously, then KernelCI has detected a new failure and stores
it as a regression.

As there may have been a topic branch merge with many commits between
the last working revision and the now failing one, a bisection is needed
in order to isolate the individual commit that introduced the failure.
At least this is the idea, it can get more complicated if several
different failures were introduced in the meantime or if the branch got
rebased.

### How does it work?

The KernelCI automated bisection is implemented as a Jenkins Pipeline
job, with some functionality in Python.

The current status of automated bisection is as follows:

- Triggered for each regression found
- Run on mainline, stable, next and several maintainer trees
- Several checks are in place to avoid false positives due to board issues:
  - Check the initial good and bad revisions coming from the found regression
  - When the bisection finds a commit, check that it does fail 3 times
  - Revert the found commit in-place and check that it does pass 3 times
  - When started manually, it's also possible to test each kernel
    iteration several times send an email report to a set of recipients
- Semd an email report to a set of recipients determined from the
  breaking commit found

### Where are the results?

The bisection results are only shared by email. They could also be added
to the kernelci.org web front-end next to test results.  

### What's left to do?

Potential improvements to the automated bisection include:

- Possibility to manually start semi-automatic bisections for special
  cases.
- Better support for identifying which tree a bisection failure occurs
  in (eg, identifying if a bisection failure was merged in from
  mainline and reporting it as a mainline issue).
- Robustness improvements in recipient identification.
- Web interface for viewing bisection results.
