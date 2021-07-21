---
title: "Tests"
date: 2021-02-10T20:29:45Z
draft: true
description: KernelCI Tests
---

KernelCI native tests are orchestrated by KernelCI.  They are initiated in test
labs directly connected to KernelCI and results are visible on the [web
frontend](https://linux.kernelci.org/job/).  Non-native tests are run in fully
autonomous systems, such as syzbot or CKI, and results are shared alongside
KernelCI native test results via [KCIDB](https://kcidb.kernelci.org).
