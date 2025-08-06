---
title: "FAQ"
date: 2021-03-30T22:02:52Z
description: Frequently asked questions
---

**Q: How can I add a kernel branch to kernelci.org?**

You can create a [GitHub
issue](https://github.com/kernelci/kernelci-core/issues/new?assignees=&labels=&template=new-kernel-branch.md&title=Add+branch+BRANCH+from+TREE)
and fill the form to describe what you need.  Typically, branches from
individuals can get a small number of builds while large subsystems or mainline
will get full build and test coverage to be able to use available resources in
a sustainable way.

**Q: What is KCIDB?**

The KCIDB project, or Kernel CI Database, is a place where all kernel test
results can be sent together and combined.  One of the main goals is to be able
to send a single email report on behalf of the multitude of test systems that
produced the data.  This should make maintainers' lives easier and be more
effective.  All the data sent to KCIDB can be visualized in our [Web Dashboard](https://dashboard.kernelci.org/).

**Q: How to enable my platform (hardware, Cloud VM, etc) to be tested in KernelCI?**

We would love to see your platform in KernelCI. Check our [platform testing](/intro/platform-testing) guide to learn about the different possibilities.

**Q: What is the relationship between KernelCI and LAVA? Does KernelCI have
non-upstream changes to LAVA? Do LAVA people participate in KernelCI?**

LAVA is used in many test labs that provide results to KernelCI, but KernelCI
doesn’t run any labs itself. Some people do contribute to both, as KernelCI is
one of the biggest public use-cases of LAVA, but they really are independent
projects. The core KernelCI tools are designed to facilitate working with LAVA
labs, but this is not a requirement and other test lab frameworks are also
used.

**Q: Is there any documentation on how to write “custom” tests and to integrate
them with KernelCI?**

A section of the documentation is dedicated to [adding new test
suites](/components/maestro/pipeline/developer-documentation/).

Each test is a bit different as they all have their own dependencies and are
written in various languages. Typically, they will require a user-space image
with all the required packages installed to be able to run as well as the
latest versions of some test suites built from source. This is the case with
`v4l-utils`, `igt-gpu-tools` or `LTP`. Some are plain scripts and don’t depend
on anything in particular`.

When prototyping some new tests to run in LAVA, the easiest approach is to use
nfsroot with the plain Debian Buster image provided by KernelCI and install
extra packages at runtime, before starting the tests. Then when this is working
well, dependencies and any data files can be baked into a fixed rootfs image
for performance and reproducibility.
