---
title: "Native tests"
date: 2021-02-10T11:48:13Z
draft: true
description: "KernelCI native tests"
---

# KernelCI Native Tests

## LTP

Initial GitHub issue: [#506](https://github.com/kernelci/kernelci-core/issues/506)

The table below shows a summary of the devices and LTP subsets that have been
tested, with their current status.

|                  | hp-x360-12b-ca0004na-octopus | jetson-tk1 | bcm2836-rpi-2-b | odroid-xu3 | beaglebone-black | imx6q-sabrelite | hp-11A-G6-EE-grunt | sun50i-h6-pine-h64 | rk3288-rock2-square | hip07-d05 | rk3288-veyron-jaq | rk3399-gru-kevin |
| ---------------- | ---------------------------- | ---------- | --------------- | ---------- | ---------------- | --------------- | ------------------ | ------------------ | ------------------- | --------- | ----------------- | ---------------- |
| admin_tools      | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| connectors       | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| containers       | pass                         | pass       | pass            | pass       | pass             | **fail**            | pass               | pass               | pass                | pass      | pass              | pass             |
| controllers      | pass                         | pass       | pass            | pass       | pass             | **fail**            | **fail**         | pass               | pass                | **fail**      | pass              | pass             |
| crypto           | pass                         | [#538](https://github.com/kernelci/kernelci-core/pull/538)       | [#538](https://github.com/kernelci/kernelci-core/pull/538)            |  **fail**      | [#538](https://github.com/kernelci/kernelci-core/pull/538)             | [#538](https://github.com/kernelci/kernelci-core/pull/538)            | pass               | pass               | [#538](https://github.com/kernelci/kernelci-core/pull/538)                 | pass     | [#538](https://github.com/kernelci/kernelci-core/pull/538)              | [#538](https://github.com/kernelci/kernelci-core/pull/538)             |
| device-drivers   | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| fcntl-locktests  | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| filecaps         | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| firmware         | stuck                        | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| fs               | pass                         | pass       | pass            | pass       | pass             | **fail**            | pass               | pass               | pass                | pass      | pass              | pass             |
| fsx              | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| fs_bind          | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| hotplug          | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| hugetlb          | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| include          | pass                         | pass       | pass            | pass       | **fail**             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| input            | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| io               | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| ipc              | pass                         | ~~[#521](https://github.com/kernelci/kernelci-core/pull/521)~~       | ~~[#521](https://github.com/kernelci/kernelci-core/pull/521)~~            | ~~[#521](https://github.com/kernelci/kernelci-core/pull/521)~~       | ~~[#521](https://github.com/kernelci/kernelci-core/pull/521)~~             | ~~[#521](https://github.com/kernelci/kernelci-core/pull/521)~~            | pass               | pass               | pass                | pass      | ~~[#520](https://github.com/kernelci/kernelci-core/pull/520)~~              | ~~[#503](https://github.com/kernelci/kernelci-core/pull/503)~~ |
| lib              | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| logging          | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| mce-test         | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| mem              | pass                         | pass       | pass            | pass       | pass            | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| math             | pass                         | pass       | pass           | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| mm               | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| nptl             | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | **fail**      | pass              | pass             |
| numa             | pass                         | pass       | pass            | pass       | **fail**             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| power_management | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| pty              | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| sched            | pass                         | pass       | pass            | pass       | pass             | **fail**            | pass               | pass               | pass                | pass      | pass              | pass             |
| security         | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| sound            | pass                         | pass       | pass            | pass       | pass             | **fail**            | pass               | pass               | pass                | pass      | pass              | pass             |
| syscalls         | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| timers           | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
| tracing          | pass                         | pass       | pass            | pass       | **fail**             | **fail**            | pass               | pass               | pass                | pass      | pass              | pass             |
| uevents          | pass                         | pass       | pass            | pass       | pass             | pass            | pass               | pass               | pass                | pass      | pass              | pass             |
