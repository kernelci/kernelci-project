---
name: API Early Access
about: Request to get an early-access account for the new API
title: Request API account for USER
labels: ''
assignees:
  - nuclearcat
  - JenySadadia
---

As per the [API Transition Timeline](https://kernelci.org/blog/posts/2023/api-timeline/), the Early Access phase is from 4th September to 4th December 2023.  It allows users to request an account on the new KernelCI API for beta-testing purposes.

There are still lots of incomplete or missing features with the new API & Pipeline.  It now has a [production-like deployment](https://github.com/kernelci/kernelci-api/tree/main/kube/aks) and can already run a minimalist pipeline with KUnit, a kernel build and a boot test on QEMU.  The aim of the Early Access phase is to make all the adjustments to the design that are necessary before reaching full production status.  So please give it a go and create issues on GitHub and ask questions on the [mailing list](mailto:kernelci@lists.linux.dev), IRC `#kernelci` on libera.chat or [Slack](https://kernelci.slack.com) with whatever you may find.

The number of users and amount of resources available is limited, so while we'll try and provide an account for every request we can't give any guarantee.

Once accepted, a user account will be created by an admin and a random password will be sent to your email address.  You can then use `kci user password update` to set your own password, `kci user verify` to verify your email address, and `kci user token` to get an API token.  We'll also provide you with an AzureFiles share to use alongside the API, even though you may use any other storage as long as artifacts can be reached with a public HTTP URL.

Please provide the required information below and also replace `USER` with your name or username in the issue title:

* User name:
* Email address:
