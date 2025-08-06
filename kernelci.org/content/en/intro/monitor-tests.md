---
title: "Monitor tests"
date: 2024-07-03
description: "Adding trees, tests and interacting with tests results"
weight: 2
---

The Kernel Community is the main audience of KernelCI. Upstream maintainers and developers, product makers, hardware vendors, etc. are all interested in getting the kernel tested on a variety of scenarios.

> We know that the documentation above may not answer all your questions. We are working to improve it. We ask you to reach out to our mailing list at [kernelci@lists.linux.dev](mailto:kernelci@lists.linux.dev)  with questions and feedback. We are eager to hear from you!

When using KernelCI, the first step is to configure trees, kernel configs and tests. Then, with the tests running, users want to evaluate results through the [dashboard](https://dashboard.kernelci.org/), [kci-dev](https://kci.dev/) and setup notifications.

## Enabling trees and tests

### Check if KernelCI already runs what you need

Before we learn how to add a tree and/or tests to KernelCI, we should check if that tree is already being tested by the KernelCI ecosystem and which tests are running on it. To do that navigate through the [dashboard](https://dashboard.kernelci.org/) and look for the tree you are interested in. Multiple CI systems (origins) send test results to KernelCI, so remember to check all different origins in the Dashboard. There you can search for specific tests being run.

### Add new trees and tests

If you look at the [KernelCI Architecture](../architecture/), you see **Maestro** and the systems in the **CI ecosystem** contributing results to KCIDB. This guide will explain how to add trees and tests to [Maestro](/components/maestro/) as it is part of the Core KernelCI infrastructure we make available for the community. If you need to add your tests to another CI system, contact them directly.

This section of the documentation shares instructions to:
* [enable kernel testing for your tree/branch](/components/maestro/pipeline/developer-documentation/#enabling-a-new-kernel-tree)
* [enable specific tests](/components/maestro/pipeline/developer-documentation/#enabling-a-new-test)

For suggestions of tests to enable see [tests](../../tests).

## Interacting with the results

The Kernel Community has a few options to interact with the test results available in KernelCI. Remember this data includes results from several CI systems.

### Web Dashboard

Our [Web Dashboard](https://dashboard.kernelci.org/): The new Dashboard aims at providing an easy way for the community to look at the test results. It is still under development and we are open to your [feedback and feature requests](https://github.com/kernelci/dashboard/issues).

### kci-dev cli

We created [kci-dev](https://kci.dev/) - a command-line tool for interacting with KernelCI. You can use the [kci-dev results](https://kci.dev/results/) command to pull results from the dashboard in your shell.

### Grafana

Our [Grafana](https://grafana.kernelci.org/) instance allow users to create specific dashboard with tailored queries and boards. Those who want to dive deeper into their data can engage with our Grafana instance.

## Setting up notifications

Although still under development, the dashboard is already capable of sending notifications of two types:

* new build regressions ([example](https://groups.io/g/kernelci-results/message/58781))
* status summary for a given revision of tree/branch([example](https://groups.io/g/kernelci-results/message/58778))

If you want to have notifications enabled for you needs, create an [new issue](https://github.com/kernelci/dashboard/issues/new) on the dashboard project detailing your usecase and we will work together with you to enable what you need.
