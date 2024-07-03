---
title: "Labs"
date: 2024-07-03
description: "Connecting labs to KernelCI"
---

Anyone can connect their test labs to KernelCI. Once a lab is connected to KernelCI, it can execute KernelCI tests.

It is up to each lab to define whether it will receive specific test configurations or a generic range of test jobs. If the lab is a LAVA lab, for example, the KernelCI [LAVA runtime](../api_pipeline/pipeline/connecting-lab) will generate test jobs for each single test that is configured to run. On the other hand, if a lab is implementing its own runtime (or bridge to Maestro APIs), they may choose to generate the individual test jobs themselves.

If you are interested it just sending the results of test runs in your infrastructure, you should look at sending the data to [KCIDB](../kcidb) - KernelCI common database for results.

There are a few ways labs can be connected to KernelCI. The documentation for connecting labs in the new architecture is evolving as we add labs.

* [Connecting a LAVA lab](../api_pipeline/pipeline/connecting-lab)
* Writing your own bride/runtime using Maestro APIs (TBD)