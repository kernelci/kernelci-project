---
title: "Bisection"
date: 2021-02-10T11:41:21Z
description: "KernelCI Automated Bisection support"
---

## Why run automated bisections?

KernelCI periodically monitors a number of kernel branches (mainline, stable,
next...), and builds them when it detects new revisions.  It then runs some
tests with the resulting kernel binaries on a variety of platforms.  When a
test fails, it compares the results with previous kernel revisions from that
same branch and on the same platform.  If it was working previously, then
KernelCI has detected a new failure and stores it as a regression.

As there may have been an incoming branch merge with many commits between the
last working revision and the now failing one, a bisection is needed in order
to isolate the individual commit that introduced the failure.  At least this is
the idea, it can get more complicated if several different failures were
introduced in the meantime or if the branch got rebased.  In many cases, it
works.

## How does it work?

The KernelCI automated bisection is implemented as a [Jenkins Pipeline
job](https://github.com/kernelci/kernelci-jenkins/blob/main/jobs/bisect.jpl),
with some functionality in Python.

The current status of automated bisection is as follows:

- Triggered for each regression found, with some logic to avoid duplicates
- Run on mainline, stable, next and several maintainer trees
- Several checks are in place to avoid false positives:
  - Check the initial good and bad revisions coming from the regression
  - When the bisection finds a commit, check that it does fail 3 times
  - Revert the found commit in-place and check that it does pass 3 times
  - When started manually, it's also possible to test each kernel
    iteration several times
- Send an email report to a set of recipients determined from the
  breaking commit found

## Where are the results?

The bisection results are only shared by email.  The
[kernelci-results](https://groups.io/g/kernelci-results/topics) list is always
on Cc so all the reports can be found in the archive.

## What's left to do?

Potential improvements to the automated bisection include:

- Dealing with persistent regressions that keep producing the same bisection
  results: reply to previous email report rather than sending a new one.
- Possibility to manually start semi-automatic bisections for special cases,
  with parameters entered by hand.
- Better support for identifying which tree a bisection failure occurs in (eg,
  identifying if a bisection failure was merged in from mainline and reporting
  it as a mainline issue).
- Include list of other platforms or configurations that show have the same
  regression as the one used for the bisection.
- Web interface for viewing bisection results.
