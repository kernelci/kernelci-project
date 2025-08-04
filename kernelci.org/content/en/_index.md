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

*Welcome to the KernelCI documentation website!*

The KernelCI project mission is to ensure the quality, stability and long-term maintenance of the Linux kernel.

To achieve that, we are building an ecosystem to foster collaboration around Linux kernel testing and validation, facilitating the process of executing tests for a given subsystem or the whole kernel and following up on the results, **helping you catch issues early and maintain kernel quality**!

There are many ways to interact with the KernelCI ecosystem. For example, some users like upstream maintainers want to enable testing for their trees. Others like hardware vendors may be interested in contributing the results of tests they run on their own infra, companies or community members may be interested in contributing new features to the project code base, etc.

Below, you will find starting point for the main areas of interaction with the project:

<div class="container border border-primary rounded p-2">
  <h2 class="text-center">
    <a href="kernel-community">Monitor testing</a>
  </h2>
  <p class="text-center">Are you an upstream kernel developer? Start here if you want to use KernelCI to execute tests, follow results on our <a href="https://dashboard.kernelci.org">Web Dashboard</a> and setup notifications.</p>
</div>

<div class="container border border-primary rounded p-2 mt-3">
  <h2 class="text-center">
    <a href="intro/platform-testing">Test your platform</a>
  </h2>
  <p class="text-center">Start here if you want to bring your platform to KernelCI.
   Our technical architecture allows different options depending or your setup. You can connect a test lab that will be drive by us. Or run the tests yourself and then publish the only the results you can share publicly to our database.</p>
</div>

<div class="container border border-primary rounded p-2 mt-3">
  <h2 class="text-center">
    <a href="kcidb">Contribute test results</a>
  </h2>
  <p class="text-center">Do you have a established CI system and want to contribute your results to the KernelCI ecosystem? You can send you data to our common results [database](kcidb) and use our dashboard and notification system to monitor results.</p>
</div>


<div class="container border border-primary rounded p-2 mt-3">
  <h2 class="text-center">
    <a href="architecture">Contribute to the KernelCI codebase</a>
  </h2>
  <p class="text-center">Start here if you want to contribute to KernelCI and/or learn
  more about our <a href="architecture">technical architecture</a>.</p>
</div>

## Talk to us

If you are unsure about where to fit your need, reach out to us through our [Discord server](https://discord.gg/KWbrbWEyqb) or the mailing list at [kernelci@lists.linux.dev](mailto:kernelci@lists.linux.dev). More [contact options](https://kernelci.org/community-contact/).
