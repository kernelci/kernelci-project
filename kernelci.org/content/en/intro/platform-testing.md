---
title: "Test your platform"
date: 2025-08-04
description: "Learn how to enable KernelCI testing for your platform"
---

Many developers or companies need to execute kernel tests on specific platforms be it embedded boards, servers or virtual machines in the cloud. Let's explore the options to integrate with KernelCI for testing.

If we look at the KernelCI [architecture](../architecture), there are two main ways to connect with KernelCI.
Either you implement a lab* that is connected to directly to [Maestro](../../maestro). Or bring your system to be part of our ecosystem and contribute your results.

\* In KernelCI terminology, a **lab** is a system that allows direct access for KernelCI's Maestro to submit the test requests (with kernel artifacts and rootfs built by KernelCI).

## Option 1: Connecting your lab to Maestro

If you want you allow KernelCI direct access to your test farm, you have to setup [LAVA](https://www.lavasoftware.org/) based lab and give submission tokens to the KernelCI sysadmin team. For this to work your lab should be accessible on the internet. If yours is hidden behind a firewall, this option won't work for you.

Today, Maestro only supports LAVA as a lab runtime, but nothing prevents us from accepting contributions for other lab runtimes if there is community interest.

For detailed information, check our [Connecting a LAVA lab](../../maestro/pipeline/connecting-lab) documentation.

The LAVA lab option comes only with the cost of maintaining the LAVA lab and the hardware in it. You don't need maintain any CI system to drive the execution in this case.

This is an option for you if you want to use LAVA as your hardware automation test system and is not limited by firewalls or IT policies in your organization. Some companies won't allow receiving the test requests from an external party.

## Option 2: Joining the CI ecosystem

The other option is to bring your system to the KernelCI ecosystem. That means you already have a CI/test ecosystem and want to integrate with KernelCI. Or you want to setup test for your platform but don't want to follow the lab option described in the previous section.

Joining the KernelCI ecosystem means:

1. Contributing your tests results to our common results [database](../../kcidb). You will only contribute the tests results you want to make public. There is no requirement from KernelCI to share private tests you don't want to(eg. on pre-release hardware).
2. Optionally listening to [test events](https://github.com/kernelci/kernelci-pipeline/blob/main/tools/example_api_events.py) from Maestro to frequently pick up kernel artifacts to test. Maestro will pull and build a number of git trees every hour. You can listen and chose the kernels you want to test.

This option gives you flexibility and control in what and how to test. It requires maintenance of your own CI/test system, so will be more costly than just maintaining a KernelCI lab. However, it might be only option for some companies with strict IT policies.

## Option 3: Contract hardware lab services

Some companies in the KernelCI community provide hosting services for maintaining your hardware in their labs for testing by KernelCI and other community CI systems. If you are interested ask in the community channels.
