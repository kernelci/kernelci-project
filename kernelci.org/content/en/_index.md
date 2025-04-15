---
title: "Documentation"

cascade:
- type: "blog"
  toc_root: true
  _target:
    path: "/blog/**"
- type: "docs"
  _target:
    path: "/**"
---

Welcome to the KernelCI documentation website.

The KernelCI mission is to ensure the quality, stability and long-term maintenance of the Linux kernel. To achieve that we are building an architecture to foster collaboration among different parties around Linux kernel testing and validation.

The KernelCI architecture is complex and there are many ways to interact with it. For example, some users like upstream maintainers want to enable testing for their trees, hardware vendors may be interesting in contributing the results of tests they run on their own infra, companies or community members may be interested in contributing new features to the project code base, etc.

Below, you will find starting point for the 3 main areas of interaction with the project:

<div class="container border border-primary rounded p-2">
  <h2 class="text-center">
    <a href="kernel-community">Using KernelCI services</a>
  </h2>
  <p class="text-center">Start here if you want to use KernelCI to execute tests, follow results and setup notifications. For upstream developers and/or those who care about upstream state of specific platforms.</p>
</div>

<div class="container border border-primary rounded p-2 mt-3">
  <h2 class="text-center">
    <a href="labs">Connecting your Lab</a>
  </h2>
  <p class="text-center">Start here if you want to add a lab to run KernelCI tests.</p>
</div>

<div class="container border border-primary rounded p-2 mt-3">
  <h2 class="text-center">
    <a href="kcidb">Contributing test results</a>
  </h2>
  <p class="text-center">Start here if you want
  to contribute your results to the KernelCI common database. KCIDB can receive tests results from any CI system.</p>
</div>

<div class="container border border-primary rounded p-2 mt-3">
  <h2 class="text-center">
    <a href="kci-dev">kci-dev cli</a>
  </h2>
  <p class="text-center">Start here if you want to interact with KernelCI instances programmatically.</p>
</div>

<div class="container border border-primary rounded p-2 mt-3">
  <h2 class="text-center">
    <a href="architecture">Contributing to KernelCI</a>
  </h2>
  <p class="text-center">Start here if you want to contribute to KernelCI and learn
  more about our <a href="architecture">technical architecture</a>.</p>
</div>

---
If you are unsure about where to fit your need, reach out to us through our [Discord server](https://discord.gg/KWbrbWEyqb) or the mailing list at [kernelci@lists.linux.dev](mailto:kernelci@lists.linux.dev). More [contact options](https://kernelci.org/community-contact/).
