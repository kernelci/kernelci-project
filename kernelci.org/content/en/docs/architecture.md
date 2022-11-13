---
title: "Architecture"
date: 2021-08-06
description: "KernelCI architecture"
weight: 1
---

The "bigger picture" image below, taken from the [LPC 2020
talk](https://www.youtube.com/watch?v=y9Glc90WUN0&list=PLVsQ_xZBEyN1HgWTOCn2Q96Q-RyfBSdKs&t=10973s),
shows the overall KernelCI architecture from a user point of view:

![bigger picture](/image/kernelci-bigger-picture.png)

The first thing worth noting is that there are two main categories of
[tests](../tests): the "native" ones are orchestrated by KernelCI itself and
stored in the KernelCI backend while others are imported into
[KCIDB](https://github.com/kernelci/kcidb) from other autonomous systems.

## KernelCI native architecture

KernelCI native tests are orchestrated using the following components:

* [Core tools](../core) contain all the primitive functions implemented in
  Python as well as the system [configuration](../core/config).  This is how
  kernels are built, test definitions are generated etc.
* [kernelci-backend](https://github.com/kernelci/kernelci-backend) which
  provides an API on top of Mongo DB to store all the data.  It also performs
  some post-processing such as generating email reports, detecting regressions
  and triggering automated bisections.
* [kernelci-frontend](https://github.com/kernelci/kernelci-frontend) which
  provides a web dashboard such as the one hosted on
  [linux.kernelci.org](https://linux.kernelci.org).  This makes use of the backend API
  to retrieve results.
* [kernelci-jenkins](https://github.com/kernelci/kernelci-jenkins) to run a
  [Jenkins](https://www.jenkins.io/) instance and orchestrate all the builds
  and tests being scheduled.  It also relies on
  [Kubernetes](https://kubernetes.io/) provided by [Microsoft
  Azure](https://azure.microsoft.com/) and [Google Compute
  Engine](https://cloud.google.com/) to run all the kernel builds.
* [Test labs](../labs), typically using LAVA but not only, are hosted by people
  and organisations outside of the KernelCI project.  They are however
  connected to KernelCI services to run tests and send results directly to the
  backend.

There are several [instances](../instances) hosted by the KernelCI project, for
different needs as explained in the documentation.  Each instance is made up of
all the components listed above.  It's possible for anyone to set up their own
private instance too.  However, developers typically don't need to set up a
full instance but only the components they need to make changes to.  Here's how
they all relate to each other:

```mermaid
graph TD
  frontend(Web frontend) --> backend(Backend API)
  backend --> mongo[(Mongo DB)]
  core(Core tools) -.-> backend
  core -.-> lava[LAVA labs]
  lava -.-> backend
  jenkins(Jenkins) --> core
  jenkins --> k8s[Kubernetes]
```

Dotted lines are optional dependencies, and solid lines are required ones.  To
put this in words:

The Core tools can be used on their own on the command line without anything
else installed.  They may be used to build kernels locally, submit data to a
Backend API, or schedule jobs in test labs such as LAVA.  Jobs may be run
without any Backend API, but if there is one then results can be sent to it.
Then Jenkins uses Core tools to do all that, via Kubernetes for kernel builds.
Finally, the Web frontend uses a Backend API but nothing depends on it (apart
from end users) so it's entirely optional.

## External systems and KCIDB

Other fully autonomous systems producing their own kernel builds and running
their own tests can submit results to KCIDB, which is a
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

The monthly KCIDB [engagement
reports](https://groups.io/g/kernelci/search?q=%23KCIDB&ct=1) provide more
details about the latest status.
