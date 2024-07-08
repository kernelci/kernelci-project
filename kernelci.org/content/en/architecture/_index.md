---
title: "KernelCI Architecture"
date: 2024-07-03
description: "Learn the inner details behind the KernelCI systems"
---

![architecture](kernelci-architecture.svg)

The first thing worth noting here is that there are two main parts of the
overall KernelCI architecture:

### [Maestro](../maestro)

The top left box of this picture shows Maestro. While Maestro is only one software system, architecturally its flow has 2 parts: (1) triggering builds and list of tests to run on each platform and (2) driving such tests.

Maestro has a [pipeline-based](../maestro/pipeline) design and an [API](../maestro/api/) that allow other systems and tools to interact with it to subscribe to events (such as new build/test triggers) or send patches to be tested by the KernelCI infrastructure.

### CI Ecosystem

Any CI/test system can be part of KernelCI by receiving triggers from Maestro and submitting their data to KCIDB. Receiving triggers is an optional for CI/test system, as many have their own trigger configuration already.

### [KCIDB](../kcidb)

CI systems producing their own kernel builds and running their own tests can submit results to [KCIDB](../kcidb), which is a
[BigQuery](https://cloud.google.com/bigquery) database to provide a unified
kernel test reporting mechanism.  Please take a look at this blog post for a
comprehensive description: [Introducing Common
Reporting](https://kernelci.org/blog/2020/08/21/introducing-common-reporting/).