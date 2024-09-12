---
title: "CIP"
date: 2022-09-20T15:16:00Z
description: "About the cip.kernelci.org instance"
weight: 4
---

The [Civil Infrastructure Platform](https://www.cip-project.org/) project (CIP)
manages a separate instance of KernelCI. In reality this "instance" is part of
the main [linux.kernelci.org](https://linux.kernelci.org) instance but the
configuration of what is built and tested is managed in separate configuration
files by [maintainers](https://kernelci.org/org/tsc/#cip-instance) from the
CIP project.

The development and production workflows are identical to the main KernelCI
instance. Visit the
[production documentation](https://docs.kernelci.org/instances/production/) to
learn more about the process.

The CIP "instance" can be accessed at the
[cip.kernelci.org](https://cip.kernelci.org/) URI, which is essentially a
shortcut to [linux.kernelci.org/job/cip/](https://linux.kernelci.org/job/cip/).

## Trees
KernelCI currently monitors two CIP Linux kernel trees.
* *cip*: The "upstream" CIP Linux kernel tree is located at on
[kernel.org](https://git.kernel.org/pub/scm/linux/kernel/git/cip/linux-cip.git/).
* *cip-gitlab*: This is a mirror of the upstream CIP tree hosted on GitLab. In
addition this tree has extra, unique branches that are used to trigger specific
CI build and test jobs

## Configuration
The build configurations (trees, branches, configurations etc.) are defined in
[build-configs-cip.yaml](https://github.com/kernelci/kernelci-core/blob/main/config/core/build-configs-cip.yaml)
from the [kernelci-core](https://github.com/kernelci/kernelci-core) project.

The test configurations (devices, test cases, rootfs etc.) are defined in
[test-configs-cip.yaml](https://github.com/kernelci/kernelci-core/blob/main/config/core/test-configs-cip.yaml).

## Project Board
There is a separate [issues board](https://github.com/orgs/kernelci/projects/11)
on GitHub for the CIP instance. Recent, current and future activities can be
viewed.

## Contributing
If you have any new features/requests/bugs to request/report, please raise a
GitHub issue against the relevant [KernelCI](https://github.com/kernelci)
repository and add `CIP` to the subject. One of the CIP maintainers will then
assign the issue to the *CIP* GitHub project as appropriate.

We also welcome any GitHub Pull Requests. Again, please prepend these with `CIP`
so that they can be identified easily.
