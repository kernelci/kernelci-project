---
date: 2023-12-12
title: "Adding Patchwork integration to KernelCI"
linkTitle: "Adding Patchwork integration to KernelCI"
author: Gustavo Padovan
description: >
  Upcoming Patchwork integration in KernelCI aims helping maintainers reduce their workload, by deferring first line level of checks to KernelCI.
---

At KernelCI, one of our main goals is to support upstream developers and maintainers on their jobs, speeding up the code integration and reducing the number of regressions in the Linux Kernel. KernelCI wants to contribute to saving precious time in an already busy schedule that community members have.

Last month, at [Linux Plumbers](https://lpc.events/), most of the KernelCI Board Members were present and engaging with the community on several kernel testing related topics. One topic in particular has been grabbing the attention of some kernel maintainers: the ability to test patches out of Patchwork automatically. That way, maintainers can have a round of automated testing done before they put their hands on the patches.

Testing the patches at the moment they arrive at the mailing list may be one of the best approaches because we can identify issues even before a person puts their eyes on the code. Developing a robust system to test new patches landing in Patchwork is not a trivial task. It will take some time to stabilize the support and deal with different corner cases. There is also the resource availability side, as doing that kind of testing at scale for several subsystems requires a lot of compute power. Last but not least, security is key, as blindly testing any patch that lands on the mailing list is not a great idea security-wise.

Fortunately, we are not starting from scratch, as we already have a few examples of the Patchwork integration with CI in the BPF and netdev subsystems. (see the results for this [patch](https://patchwork.kernel.org/project/netdevbpf/patch/20231206095044.17844-1-duanqiangwen@net-swift.com/) for example).

The big advantage of adding such support in KernelCI is that we can solve the problem for virtually all subsystems at the same time without reinventing and maintaining different CI infra across the board. 

So recently, Nikolay Yurin, a Production Engineer from Meta, started developing the support [patchwork in the KernelCI](https://github.com/getpatchwork/patchwork/issues/557). It is still under heavy development and should reach a point that we can experiment with in early 2024.

It is very important to put experimental support in place as we still don't know all the challenges we will face with the Patchwork integration, so engaging with the community to gather early feedback will be quite helpful. There are definitely corner cases and considerations that we will find out only when we start experimenting with it. 

Luckily, some kernel maintainers kindly raised their hands to participate in the early phase of the Patchwork integration in KernelCI. Thank you, maintainers!!!

