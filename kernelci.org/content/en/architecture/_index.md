---
title: "KernelCI Architecture"
date: 2024-07-03
description: "Learn the inner details behind the KernelCI systems"
---

![architecture](/image/kernelci-architecture.png)

The first thing worth noting here is that there are two main parts of the
overall KernelCI architecture:

### [API & Pipeline](../api_pipeline)

The top half of this picture shows native services interacting directly with
the API: LAVA test labs, Kubernetes clusters, custom test environments and the
job scheduler.  These are referred to as the KernelCI Pipeline in a loose
sense.  Such services can be run pretty much anywhere, they are just API
clients with a particular purpose.

### [KCIDB](../kcidb)

Other fully autonomous systems producing their own kernel builds and running
their own tests can submit results to
[KCIDB](../kcidb), which is a
[BigQuery](https://cloud.google.com/bigquery) database to provide a unified
kernel test reporting mechanism.  Please take a look at this blog post for a
comprehensive description: [Introducing Common
Reporting](https://kernelci.org/blog/2020/08/21/introducing-common-reporting/).