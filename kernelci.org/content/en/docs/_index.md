---
title: "Documentation"
date: 2023-08-21
menu: main
---

Welcome to the KernelCI documentation website.  You'll find below a summary of
the overall architecture and pointers to the main sections.

## Overall Architecture

![architecture](/image/kernelci-architecture.png)

The first thing worth noting here is that there are two main parts of the
overall KernelCI architecture:

### [API & Pipeline](/docs/api)

The top half of this picture shows native services interacting directly with
the API: LAVA test labs, Kubernetes clusters, custom test environments and the
job scheduler.  These are referred to as the KernelCI Pipeline in a loose
sense.  Such services can be run pretty much anywhere, they are just API
clients with a particular purpose.

### [KCIDB](/docs/kcidb)

Other fully autonomous systems producing their own kernel builds and running
their own tests can submit results to
[KCIDB](/docs/kcidb), which is a
[BigQuery](https://cloud.google.com/bigquery) database to provide a unified
kernel test reporting mechanism.  Please take a look at this blog post for a
comprehensive description: [Introducing Common
Reporting](https://foundation.kernelci.org/blog/2020/08/21/introducing-common-reporting/).
