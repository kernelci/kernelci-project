---
title: "Native tests"
date: 2021-02-10T11:48:13Z
draft: true
description: "KernelCI native tests"
---

# KernelCI Native Tests

## Kselftest

Initial Github Issue: [#331](https://github.com/kernelci/kernelci-core/issues/331)

The table below shows a summary of the devices and kselftest collections that have been tested, with their current status.

|             | asus-C523NA-A20057-coral | hip07-d05 | hp-11A-G6-EE-grunt | hp-x360-12b-n4000-octopus | meson-g12b-odroid-n2 | rk3288-veyron-jaq |
|-------------|------|-------|-------|-------|-------|-------|
| filesystems | pass | ---  | pass  | pass  | ---  | ---  |
| futex       | pass | pass  | pass  | pass  | ---  | ---  |
| lib         | pass | ---  | pass  | pass  | pass  | pass  |
