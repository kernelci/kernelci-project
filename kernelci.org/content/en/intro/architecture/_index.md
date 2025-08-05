---
title: "The KernelCI architecture"
date: 2025-08-04
description: "Learn the inner details behind the KernelCI systems"
---

[![KernelCI architecture diagram](kernelci-architecture.jpg)](kernelci-architecture.jpg)

[[download svg diagram](kernelci-architecture.svg)]

## Main Components

### [Maestro](../../maestro)

The middle left box of this picture shows Maestro. While Maestro is only one software system, architecturally its flow has 2 parts: (1) triggering builds and list of tests to run on each platform and (2) driving such tests.

Maestro has a [pipeline-based](../../maestro/pipeline) design and an [API](../../maestro/api/) that allow other systems and tools to interact with it to subscribe to events (such as new build/test triggers) or send patches to be tested by the KernelCI infrastructure.

### [kci-dev](../../kci-dev)

[kci-dev](../kci-dev) is a stand-alone tool for Linux Kernel developers and maintainers to interact with KernelCI. There is full documentation available at [kci.dev](https://kci.dev) and a [PyPI package](https://pypi.org/project/kci-dev/). Source code is available on [GitHub](https://github.com/kernelci/kci-dev).

### [Web Dashboard](https://dashboard.kernelci.org/)

A new [web dashboard](https://dashboard.kernelci.org/) has been developed to allow users to easily visualise results from KernelCI testing. Development, issues and feature requests are all being tracked on [GitHub](https://github.com/kernelci/dashboard).

### [KCIDB](../../kcidb)

CI systems producing their own kernel builds and running their own tests can submit results to [KCIDB](../../kcidb).  Please take a look at this blog post for a
comprehensive description: [Introducing Common
Reporting](https://kernelci.org/blog/2020/08/21/introducing-common-reporting/).

### CI Ecosystem

Any CI/test system can be part of KernelCI by receiving triggers from Maestro and submitting their data to KCIDB. Receiving triggers is optional for CI/test system, as many have their own trigger configuration already for building and testing kernels.

## Talk to us

If you have doubts about our architecture, please [reach out](../contacts).

