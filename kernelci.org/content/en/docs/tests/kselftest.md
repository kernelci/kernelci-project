---
title: "kselftest"
date: 2021-07-21T18:00:00Z
draft: true
description: "Native tests: kselftest"
---

## About

[kselftest](https://www.kernel.org/doc/html/latest/dev-tools/kselftest.html) is
one of the main test suites that comes with the Linux kernel source tree
itself.  As such, it is an obvious one to cover by KernelCI.  For each kernel
revision built by KernelCI, an extra build is produced for each CPU
architecture with a kselftest config fragment merged on top of the main
defconfig.  The resulting kernel and kselftest binaries are then stored
together and used together, to guarantee compatibility between the tests and
the kernel.

## KernelCI coverage

Initial Github Issue: [#331](https://github.com/kernelci/kernelci-core/issues/331)

The aim is to run all of kselftest, whenever applicable.  Only a subset of all
the available test collections are currently being run while infrastructure is
getting prepared for gradually expanding coverage to the full set.

The table below shows a summary of the current KernelCI kselftest coverage per
CPU architecture and platform for each collection.  Until a more dynamic
orchestration becomes available, this is all defined in
[`test-configs.yaml`](https://github.com/kernelci/kernelci-core/blob/master/test-configs.yaml).
The goal is to have each kselftest collection run on at least 2 platforms of
each CPU architecture.  All these tests are typically run on every kernel
revision built by KernelCI, except for those that aren't present in older
kernel revisions.

| Platform                           | arch    | filesystems | futex | lib | lkdtm | seccomp |
|------------------------------------|---------|-------------|-------|-----|-------|---------|
| asus-C433TA-AJ0005-rammus          | x86\_64 |             |       |     | ✔     | ✔       |
| asus-C523NA-A20057-coral           | x86\_64 | ✔           | ✔     | ✔   | ✔     | ✔       |
| asus-C436FA-Flip-hatch             | x86\_64 | ✔           | ✔     |     |       |         |
| hp-11A-G6-EE-grunt                 | x86\_64 | ✔           | ✔     | ✔   | ✔     | ✔       |
| hp-x360-12b-n4000-octopus          | x86\_64 | ✔           | ✔     | ✔   |       |         |
| mt8173-elm-hana                    | arm64   | ✔           | ✔     | ✔   | ✔     | ✔       |
| mt8183-kukui-jacuzzi-juniper-sku16 | arm64   | ✔           | ✔     | ✔   | ✔     | ✔       |
| rk3288-veyron-jaq                  | arm     |             |       | ✔   |       |         |
