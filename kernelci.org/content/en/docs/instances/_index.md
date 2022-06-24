---
title: "Instances"
date: 2021-07-21T21:00:00Z
description: "KernelCI public instances"
weight: 2
---

There are a number of KernelCI instances for various purposes.  The main
"production" one on [linux.kernelci.org](https://linux.kernelci.org) is
dedicated to the upstream Linux kernel.  It gets updated typically once a week
and continuously builds and tests all the trees listed in
[`build-configs.yaml`](https://github.com/kernelci/kernelci-core/blob/main/config/core/build-configs.yaml).
The "staging" instance on [staging.kernelci.org](https://staging.kernelci.org)
is used to test changes made to KernelCI itself before they get deployed in
production.  Then there are specific instances such as the Chrome OS one on
[chromeos.kernelci.org](https://chromeos.kernelci.org) and
for CIP on [cip.kernelci.org](https://cip.kernelci.org).
