---
title: "Tests"
date: 2023-08-11
description: "Tests"
---

## Native tests

KernelCI native tests are orchestrated by KernelCI.  They are initiated in test
labs directly connected to KernelCI and results are visible on the [web
frontend](https://linux.kernelci.org/job/).

Tests run natively by KernelCI such as [kselftest](kselftest) and [LTP](ltp)
but also some KernelCI specific ones are all described with dedicated pages
under this current section.

It's possible for anyone to add new native tests.  See the [How-To
guide](howto) to get started.

## External tests and KCIDB

Non-native tests are run in fully autonomous systems, such as syzbot or CKI.
Their results are shared alongside KernelCI native test results via
[KCIDB](https://kcidb.kernelci.org).
