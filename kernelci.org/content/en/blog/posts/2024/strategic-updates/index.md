---
date: 2024-04-08
title: "Strategic updates from the KernelCI project"
linkTitle: "Strategic updates from the KernelCI project"
author: Gustavo Padovan
description: >
    Check out our strategic overview of the steps we have taken towards KernelCI mission over the past few months.
---

The KernelCI project continues on its mission to ensure the quality, stability and long-term maintenance of the Linux kernel. That means supporting the community (especially maintainers) to not just run their code in a Continuous Integration (CI) system, but also deliver relevant, high confidence results and reports. In this post, we will give you a strategic overview of the steps we have taken towards our mission over the past few months.

## Enabling new infrastructure to run tests

Our legacy system has shown its age and it has been failing to meet the growing testing needs of the community. It is a quite limited, unstable python2 project that focuses on embedded hardware. We continue on the journey to put in place our new infrastructure, so we can finally move away from the legacy KernelCI system.

We bring good news! The new core service for running tests is already in place, but still going through a stabilization phase. So, the team is ramping up the number of tests slowly to deal with issues that arise especially when it comes to the quality of the testing KernelCI provides. We do not want to repeat past mistakes with results that can't really be trusted, so our focus right now is on quality rather than quantity. The team is iterating quickly on that process to enable open, wide adoption in the coming months.

In our new KernelCI infrastructure, we already have support to run tests in labs (through [LAVA](https://www.lavasoftware.org/) only at the moment), Docker containers, Kubernetes and natively. Adding new labs or test environments should be relatively straightforward. Then, as we add more test environments, we are also laying down the foundation for integration with other CI systems across the community so we can share kernel builds and offer test environments.

As we shared [before](https://kernelci.org/blog/posts/2023/api-early-access/), the new infrastructure exposes an API for users to create accounts, query results and even drive tests themselves. At the moment, we are focusing on enabling our own pipeline there, so we can shut down the legacy system. But anyone is welcome to request a user account and try it out.

Another initiative from the KernelCI community is the [GitLab CI support in the mainline](https://lore.kernel.org/lkml/20240228225527.1052240-1-helen.koike@collabora.com/) kernel. Here, the goal is to offer maintainers a CI environment that they can manage themselves. With time, KernelCI API can be leveraged to provide a backend for builds and test runs for repositories using GitLab CI.

## Trusting tests results and reports

On one end, we are stabilizing our new infrastructure to run the tests. On the other end, we are looking into improving the quality of the reports KernelCI sends out, so maintainers and developers can actually trust them. Given the huge amount of data coming out of test systems and bots today, we must invest in improving the delivery of the results, or else, KernelCI will be contributing to increasing the maintainer burnout rather than helping solve it. That means improving the quality and confidence of the data, so maintainers and developers only receive reports packed with relevant information and no noise or false-positives.

At the time of this writing, we have a handful of trees enabled, boot testing and a few tests enabled (including kselftest support) in our new test infrastructure. That setup is enabling the team to triage **ALL** the results to identify infrastructure failures and test patterns in general (flakiness, config issue, intermittent issues, etc). There is a significant investment to develop better tests together with the community (like the [device tree probe kselftest](https://www.collabora.com/news-and-blog/blog/2023/12/11/a-new-kselftest-for-verifying-driver-probe-of-devicetree-based-platforms/)) that is improving the quality of the results compared to what exists in our legacy system.

As part of the effort, we are developing a layer for **post-processing the test results** in [KCIDB](https://github.com/kernelci/kcidb) - the KernelCI database to collect test results from the entire Linux kernel test ecosystem. The work in this area is at proof-of-concept level, but it is already enabling the team to evaluate the results coming from our new infrastructure. The post-processing layer should be a key part of the feedback loop with the community. The goal is to increase [automation in triaging the results](https://www.collabora.com/news-and-blog/blog/2024/03/14/automatic-regression-handling-and-reporting-for-the-linux-kernel/), saving precious time from kernel maintainers. Also, because KCIDB collects data from various CI systems, the post-processing of test results can be enabled for more systems than just KernelCI.

On top of that, the KernelCI team is redesigning the Web Dashboard UX to enable rich visualization of all that data for the entire community. A public request for feedback on UX should go out in the coming weeks.

## It's all about engaging the community in testing

Solving CI needs for the Linux kernel community is not just a technical challenge. It is in big part a community engagement challenge too. The KernelCI project has a strong focus on engaging the community in testing processes. With our new infrastructure coming into place, we are ready to give a new spin to our Community Engagement initiative.

For that, we are forming a Community Engagement Working Group (WG). The WG will focus on connecting with maintainers to discuss and implement improvements in test quality for their subsystems and also act as a feedback recipient for improvements in our post-processing of the test results. The Community Engagement WG will be led by Shuah Khan, kernel maintainer & Linux
Fellow at The Linux Foundation.

A dedicated [announcement](https://lore.kernel.org/kernelci/bf81be70-61ec-4169-b66a-5c3136869107@gmail.com/T/#u) of the Community Engagement WG was sent to the KernelCI mailing list. If you are interested in participating, raise your hand!

## Where are we going from here?

As you can see, a lot is going on in KernelCI at the moment. The team is iterating quickly on the development of the new infrastructure, so we will be engaging with new maintainers and developers every month from now on, bringing them to the new infra and pushing the system limit further. If you are a maintainer and want to bring your tests to KernelCI please send us an email at [kernelci@lists.linux.dev](mailto:kernelci@lists.linux.dev).

That's all for now! Stay tuned for updates on topics discussed in this article. Likewise, as the new infrastructure stabilizes, expect a significant amount of documentation updates too.

We thank all KernelCI [member organizations](https://docs.kernelci.org/org/members/) and developer community who have been investing in the project over the years. It is only because of the continued support from our community that we are making the legacy system a past story!