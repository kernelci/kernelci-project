---
date: 2021-09-20
title: "KernelCI Hackfests"
linkTitle: "KernelCI Hackfests"
author: Guillaume Tucker
description: >
  Lessons learned from the first two hackfests
---

<img src="hackfest-2-screenshot-2021-09-08-cropped.png" alt="screenshot" width="300px" style="float: left; padding: 0 20px 20px 0" />

KernelCI hackfests span over a few days during which a number of contributors
get together to focus on upstream Linux kernel testing.  So far, mainly kernel
and automated test system developers have been taking part in the hackfests but
anyone is welcome to join.  Topics mostly include extending test coverage in
various ways: enabling new test suites as well as adding test cases to
established frameworks such as kselftest and LTP, building additional kernel
flavours, bringing up new types of hardware to be tested...

There have been two hackfests to date. The current plan is to hold one
every few months.  Future hackfests will be announced on the [KernelCI mailing
list](https://groups.io/g/kernelci/topics) as well as [LKML](https://lkml.org/)
and [Twitter](https://twitter.com/kernelci).  Stay tuned!


## Connecting the dots

There is a large ecosystem around the Linux kernel which includes testing in
many shapes and forms: kernel developers, test developers, test system
developers, OEMs testing fully integrated products...  All these teams of
people don't necessarily interact with each other very much outside of their
organisations, and kernel developers aren't necessarily in the habit of writing
tests as part of their daily work.

Events such as the KernelCI hackfests give a chance for people from these
different areas to work together on solving common issues and keep the
ecosystem healthy.  It also helps with shifting the upstream Linux kernel
development culture towards a more test-driven workflow, to bring mainline
Linux closer to the real world where it is actually being used.

Let's consider a plausible hackfest story.  A first participant writes a new
test, say in kselftest.  A second participant enables the test to run in
KernelCI, which fails in some cases and a kernel bug is found.  A third
participant makes a fix for the bug, which can then be tested directly in
KernelCI to confirm it works as expected.  This may even happen on the [staging
instance](/docs/instances/staging/) before the patches for the test and the fix
are sent to any mailing list, in which case the fix would get a `Tested-by:
"kernelci.org bot" <bot@kernelci.org>` trailer from the start.  This scenario
also relies on some hardware previously made available in test labs by other
people, putting together efforts from at least four different participants.


## Timeline

Here's a summary of the first two hackfests:

### Hackfest #1 - 27th May to 4th June 2021

* Workboard: https://github.com/orgs/kernelci/projects/3
* Participans
  * Several kernel developers from [Google Chrome
  OS](https://www.google.com/intl/en_uk/chromebook/chrome-os/)
  * Several kernel developers from [Collabora](https://collabora.com)
  * A few members of the core KernelCI team
* Achievements
  * New KernelCI instance for Chrome OS on https://chromeos.kernelci.org
  * Added support for building Chrome OS configs on top of mainline
  * Enabled clang-13 builds for Chrome OS and main KernelCI builds
  * New test suite for libcamera enabled on https://linux.kernelci.org
  * Enabled LTP crypto tests with extra kernel config fragment
  * Several patches were also sent to extend kselftest and KUnit coverage in
      the kernel tree

### Hackfest #2 - 6th to 10th September 2021

* Workboard: https://github.com/orgs/kernelci/projects/5
* Participants
  * More members of the [TSC](/docs/org/tsc/) took part than first hackfest
  * New contributor: Denis Efremov (floppy disk kernel maintainer)
  * Alice from [Civil Infrastructure Platform](https://www.cip-project.org/)
    (CIP) / [Cybertrust Japan](https://www.cybertrust.co.jp/english/)
  * Chris from [Civil Infrastructure Platform](https://www.cip-project.org/)
    (CIP) / [Renesas](https://www.renesas.com/eu/en)
  * Nikolai from [Red Hat's CKI](https://cki-project.org/)
  * Several KernelCI developers from [Collabora](https://collabora.com)
* Achievements
  * New Docker images and initial steps for running
      [`cvehound`](https://github.com/evdenis/cvehound)
  * On-going progress with Chrome OS tests using QEMU and hardware in LAVA
  * Support for CIP kernel configs
  * Initial work to enable CIP Core images (Debian based)
  * Set up redirect from [cip.kernelci.org](https://cip.kernelci.org) to the
    web dashboard page with [CIP jobs](https://linux.kernelci.org/job/cip/)
  * Support for `xilinx-zcu102` device
  * Initial work to enable IEC cybersecurity tests
  * Initial work to enable kselftest livepatch
  * Most of the content from https://foundation.kernelci.org replicated on the
    new [kernelci.org](https://kernelci.org) static site
  * Started adding support for including kernel firmware files in test jobs
  * Many various bug fixes and improvements in the KernelCI core code


## Lessons Learned

### What went well

* There were several new contributors.  The hackfest is a great way to get
  people started with KernelCI.
* Hackfest #2 showed more diversity with a wider representation from the
  ecosystem.
* There were many improvements in various areas (bug fixes, documentation)
  which is a sign of a healthy project.
* The workflow based on GitHub and the Big Blue Button platform appear to have
  been easily adopted by the participants.

### What needs to be improved

* Having more kernel maintainers involved would help with setting priorities
  and ojectives for KernelCI in accordance with kernel developers' needs.
* A hackfest every 3 months may be a bit too often, or maybe some could be
  shorter or have a more particular theme.
* Changes can take a long time to get merged.  The main limitation seems to be
  the number of people available to do code reviews and drive discussions.
* KernelCI has been focusing on running more tests for over a year (kselftest,
  LTP, IGT…).  Now the core architecture needs to be improved to scale better.


## Next hackfest

The actual dates haven't been confirmed yet, but with the current 3-month
frequency the next hackfest should be taking place early December 2021.  A
proposed theme could be "KernelCI for newbies", with a selection of tasks well
suited for first-time contributors and documentation improved in that area
prior to the hackfest.  As always, suggestions are always welcome so please do
get in touch if you have any.

See you there!
