---
title: "FAQ"
date: 2021-03-30T22:02:52Z
description: Frequently asked questions
weight: 90
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
on anything in particular.

When prototyping some new tests to run in LAVA, the easiest approach is to use
nfsroot with the plain Debian image provided by KernelCI and install extra
packages at runtime, before starting the tests. Then when this is working
well, dependencies and any data files can be baked into a fixed rootfs image
for performance and reproducibility.

**Q: I have developed a new test suite. Should I add it to Maestro or submit
results directly to KCIDB?**

As a rule of thumb: if your tests look like the suites Maestro already runs,
add them to Maestro; if they amount to a CI system of their own, keep running
them yourself and send the results to KCIDB.

A test suite is a good fit for Maestro when it follows the same pattern as
kselftest, LTP or v4l-utils: the kernel is booted on a device under test
(hardware or a VM) and the tests run from user space, so the binaries and
their dependencies can be baked into one of the KernelCI rootfs images.
Maestro then builds the kernels, schedules the jobs in the labs and submits
the results to KCIDB for you.  Be aware that this integration is not free:
it requires writing — and then maintaining — job definitions, job templates,
platform and device names, and rootfs recipes in `kernelci-pipeline`.  See
[adding new test suites](/components/maestro/pipeline/developer-documentation/)
for the details.

Some suites that don't need a device under test can also run in Maestro, the
way KUnit and cvehound do: they execute on the kernel build infrastructure
in Kubernetes.  Builder capacity is a scarce resource, paid for by the
project or provided by sponsors and members, so enabling a new job of this
kind incurs additional expenses and needs to be discussed with the community
first.

To see how existing tests are wired up, look at these places:

* **Job definitions**:
  [`config/jobs.yaml`](https://github.com/kernelci/kernelci-pipeline/blob/main/config/jobs.yaml)
  in `kernelci-pipeline`.  Each test suite is an entry under `jobs` naming
  its template, rootfs and KCIDB test suite mapping.  The `kselftest-*` and
  `ltp-*` entries are good examples of DUT-style suites; `kunit` and
  `cvehound` are builder-side ones.
* **Job templates**:
  [`config/runtime/`](https://github.com/kernelci/kernelci-pipeline/tree/main/config/runtime)
  in `kernelci-pipeline` holds the `jinja2` templates that generate the
  actual job definitions.  Most DUT-style suites reuse `generic.jinja2`,
  while `kunit.jinja2` and `cvehound.jinja2` show jobs running on the build
  infrastructure.
* **Scheduling and platforms**:
  [`config/scheduler.yaml`](https://github.com/kernelci/kernelci-pipeline/blob/main/config/scheduler.yaml)
  defines which events trigger each job and in which runtime it runs, and
  [`config/platforms.yaml`](https://github.com/kernelci/kernelci-pipeline/blob/main/config/platforms.yaml)
  describes the device types jobs can target.
* **Rootfs recipes**:
  [`config/core/rootfs-configs.yaml`](https://github.com/kernelci/kernelci-core/blob/main/config/core/rootfs-configs.yaml)
  in `kernelci-core`.  For example, the `trixie-kselftest` entry lists the
  extra Debian packages and the build script baked into the kselftest
  image.  The images are built with the debos recipes under
  [`config/rootfs/debos/`](https://github.com/kernelci/kernelci-core/tree/main/config/rootfs/debos)
  and published at
  [storage.kernelci.org](https://storage.kernelci.org/images/rootfs/).

If what you built is essentially its own CI system — a fuzzer, unit tests,
static analysis, or a custom harness with special scheduling or
infrastructure needs — it is usually better to keep running it on your own
infrastructure and [submit the results directly to
KCIDB](/components/kcidb/submitting).  You stay in full control of how and
when the tests run, your results still appear in the common database and the
[Web Dashboard](https://dashboard.kernelci.org/), and you can optionally
listen to Maestro events to test the kernels KernelCI already builds.

Finally, if your tests are standard but they require hardware that only you
have, consider [connecting a lab](/intro/platform-testing) to Maestro
instead.
