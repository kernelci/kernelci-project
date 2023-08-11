---
title: "Architecture"
date: 2023-08-11
description: "KernelCI Overall Architecture"
weight: 1
---

![architecture](/image/kernelci-architecture.png)

The first thing worth noting here is that there are two main parts of the
overall KernelCI architecture:

API & Pipeline
: which orchestrates the native tests initiated by KernelCI via services that
  communicate directly with the API,

KCIDB
: which groups results sent from other CI systems into a common reporting
  database.

## API & Pipeline

The top half of this picture shows native services interacting directly with
the API: LAVA test labs, Kubernetes clusters, custom test environments and the
job scheduler.  These are referred to as the KernelCI Pipeline in a loose
sense.  Such services can be run pretty much anywhere, they are just API
clients with a particular purpose.

## KCIDB

Other fully autonomous systems producing their own kernel builds and running
their own tests can submit results to
[KCIDB](/docs/kcidb), which is a
[BigQuery](https://cloud.google.com/bigquery) database to provide a unified
kernel test reporting mechanism.  Please take a look at this blog post for a
comprehensive description: [Introducing Common
Reporting](https://foundation.kernelci.org/blog/2020/08/21/introducing-common-reporting/).

Here's the list of systems currently submitting data:

* [KernelCI native tests](https://linux.kernelci.org/job/)
* [Red Hat CKI](https://cki-project.org/)
* [Google syzbot](https://syzkaller.appspot.com/)
* [Linaro Tuxsuite](https://tuxsuite.com/)
* [ARM](https://arm.com)
* [Gentoo GKernelCI](https://github.com/GKernelCI/GBuildbot)

The KCIDB [engagement
reports](https://groups.io/g/kernelci/search?q=%23KCIDB&ct=1) provide more
details about the latest status.
