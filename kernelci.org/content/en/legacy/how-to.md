---
title: "How-To"
date: 2024-01-18
description: "How to add a new native test suite"
---

This guide contains all the steps needed to add a native test suite to
KernelCI.  It will cover the [LAVA](../../labs/lava) use-case in particular as
it is currently the most popular framework to run tests for KernelCI.

## Background

KernelCI is still very much about running tests on hardware platforms.  More
abstract tests such as static analysis and KUnit are on the horizon but they
are not quite supported yet.  So this guide will only cover functional testing
on "real" hardware.

The only moving part is the kernel, which will get built in many flavours for
every revision covered by KernelCI.  All the tests are part of fixed root file
systems (rootfs), which get updated typically once a week.  Adding a test
therefore involves either reusing an existing rootfs or creating a new one.

A good way to start prototyping things is to use the plain [Debian Bullseye NFS
rootfs](https://storage.kernelci.org/images/rootfs/debian/bullseye/) and install
or compile anything at runtime on the target platform itself.  This is of
course slower and less reliable than using a tailored rootfs with everything
already set up, but it allows a lot more flexibility.  It is the approach
followed in this guide: first using a generic rootfs and then creating a
dedicated one.

## A simple test

For the sake of this guide, here's a very simple test to check the current OS
is Linux:

```
[ $(uname -o) = "GNU/Linux" ]
```

Let's test this locally first, just to prove it works:

```
$ [ $(uname -o) = "GNU/Linux" ]
$ echo $?
0
```

and to prove it would return an error if the test failed:

```
$ [ $(uname -o) = "OpenBSD" ]
$ echo $?
1
```

All the steps required to enable this test to run in KernelCI are detailed
below.  There is also a sample Git branch with the changes:

  https://github.com/kernelci/kernelci-core/commits/how-to-bullseye

## Step 1: Enable basic test plan

The first step is to make the minimal changes required to run the command
mentioned above.

### LAVA job template

See commit: [`config/lava: add uname test plan for the How-To
guide`](https://github.com/kernelci/kernelci-core/commit/b1464ff3986ac70513c251f3f1d87f892c556d61)

KernelCI LAVA templates use [Jinja](https://jinja.palletsprojects.com/).  To
add this `uname` test plan, create a template file
`config/lava/uname/uname.jinja2`:

```yaml
- test:
    timeout:
      minutes: 1
    definitions:
    - repository:
        metadata:
          format: Lava-Test Test Definition 1.0
          name: {{ plan }}
          description: "uname"
          os:
          - oe
          scope:
          - functional
        run:
          steps:
          - lava-test-case uname-os --shell '[ $(uname -o) = "GNU/Linux" ]'
      from: inline
      name: {{ plan }}
      path: inline/{{ plan }}.yaml
      lava-signal: kmsg
```

This is pretty much all boiler plate, except for the `lava-test-case` line
which runs the test and uses the exit code to set the result (0 is pass, 1 is
fail).  Some extra templates need to be added for each boot method, such as
GRUB, U-Boot and Depthcharge.  For example, here's the Depthcharge one to use
on Chromebooks `generic-depthcharge-tftp-nfs-uname-template.jinja2`:

```yaml
{% extends 'boot-nfs/generic-depthcharge-tftp-nfs-template.jinja2' %}
{% block actions %}
{{ super () }}

{% include 'uname/uname.jinja2' %}

{% endblock %}
```

The name of the template follows a convention to automatically generate the
variant required for a particular platform.  This one is for the `uname` test
plan on a platform using `depthcharge`, with the kernel downloaded over `tftp`
and the rootfs available over `nfs`.

### KernelCI YAML configuration

See commit: [`config/core: enable uname test plan using Bullseye
NFS`](https://github.com/kernelci/kernelci-core/commit/e7c1a1a0277fec215b778da3ada8885581464a16)

Once the LAVA templates have been created, the next step is to enable the test
plan in the [KernelCI YAML configuration](/docs/legacy/core/config/).

First add the `uname` test plan with the chosen rootfs (Debian Bullseye NFS in
this case) in `test-configs.yaml`:

```yaml
test_plans:

  uname:
    rootfs: debian_bullseye_nfs
```

Then define which platforms should run this test plan, still in
`test-configs.yaml`:

```yaml
test_configs:

  - device_type: hp-11A-G6-EE-grunt
    test_plans:
      - uname

  - device_type: minnowboard-max-E3825
    test_plans:
      - uname
```

Each test plan also needs to be enabled to run in particular test labs in
`runtime-configs.yaml`.  Some labs such as the Collabora one allow all tests to be
run, and it contains the platforms listed above so no extra changes are
required at this point.


These changes are enough to make an intial pull request in
[`kernelci-core`](https://github.com/kernelci/kernelci-core), and the test will
automatically get run on [staging](/docs/legacy/instances/staging/).  Then the
results will appear on the [web dashboard](https://staging.kernelci.org/job/).

> **Note** First-time contributors needed to be added to the [list of trusted
GitHub
users](https://github.com/kernelci/kernelci-deploy/blob/main/data/staging.ini#L4)
by a maintainer before their pull requests get merged and deployed on staging.

## Step 2: Modify the file system at runtime

Most tests will require more than what is already available in a plain Bullseye
rootfs.  Let's see how this can be done in a simple way.

### Add a C file: uname-os.c

See commit: [`config/lava: add
uname-os.c`](https://github.com/kernelci/kernelci-core/commit/d31ee9462c0edf680509431f01d7ffce0ef23074)

For example, we could have the test implemented as a C program rather than a
shell script.  See the
[`uname-os.c`](https://github.com/kernelci/kernelci-core/blob/how-to-bullseye/config/lava/uname/uname-os.c)
file.

To test it locally:

```
$ gcc -o uname-os uname-os.c
$ ./uname-os
System: 'Linux', expected: 'Linux', result: PASS
$ echo $?
0
```

and to test it would fail if the OS name was not the expected one:

```
$ ./uname-os OpenBSD
System: 'Linux', expected: 'OpenBSD', result: FAIL
$ echo $?
1
```

Now, let's see how this can be used with KernelCI.

### Build it and run the C implementation

See commit: [`config/lava: download and build uname-os.c and use
it`](https://github.com/kernelci/kernelci-core/commit/66eb1aab440157747d458e088610a1764b983441)

Any arbitrary commands can be added to the `uname.jinja2` template before
running the actual test cases.  In this example, we can install Debian packages
then download the `uname-os.c` file and compile it to be able to finally run it
as a test case:

```yaml
          steps:
          - apt update
          - apt install -y wget gcc
          - wget https://raw.githubusercontent.com/kernelci/kernelci-core/how-to-bullseye/config/lava/uname/uname-os.c
          - gcc -o uname-os uname-os.c
          - lava-test-case uname-os-shell --shell '[ $(uname -o) = "GNU/Linux" ]'
          - lava-test-case uname-os-c --shell './uname-os'
```

We now have 2 test cases, one with the shell version and one with the C
version.  After updating the pull request on GitHub, this will also get tested
automatically on staging.

> **Note** If one of the steps fails, the job will abort.  So if `apt install`
or `wget` fails, the tests won't be run and the LAVA job status will show an
error.

> **Note** Some test labs don't enable a route to the Internet from their
hardware platforms so installing things at runtime may not always work.  This
would typically be discussed as part of the pull request review, depending on
what the jobs are trying to do and which device types have been enabled to run
them.

## Step 3: Going further

With Step 2, pretty much anything can already be run within the limitations of
the CPU and network bandwidth on the target platform.  Even if this doesn't
take too long to run, there are many reasons why it's not really suitable to
enable in production.  There's no point installing the same packages and
building the same source code over and over again, it will add up as
significant wasted resources and extra causes for test job failures.  Once the
steps required to run a test suite are well defined, having a rootfs image with
everything pre-installed solves these issues.

Then for more complex tests, results may be produced in other forms than an
exit code from a command.  Some file may need to be parsed, or any extra logic
may need to be added.  For example, the
[`v4l2-parser.sh`](https://github.com/kernelci/kernelci-core/blob/main/config/rootfs/debos/overlays/v4l2/usr/bin/v4l2-parser.sh)
script will run `v4l2-compliance` and parse the output to then call
`lava-test-case` for each result found.  It also uses [LAVA test
sets](https://docs.lavasoftware.org/lava/actions-test.html#testsets), which is
a more advanced feature for grouping test results together inside a test suite.

### Adding a rootfs variant

Root file systems are built using the
[`kci_rootfs`](/docs/legacy/core/kci_rootfs) command.  All the variants are
defined in the
[`config/core/rootfs-configs.yaml`](https://github.com/kernelci/kernelci-core/blob/main/config/core/rootfs-configs.yaml)
file with some parameters.  There are also extra dedicated files in
[`config/rootfs`](https://github.com/kernelci/kernelci-core/tree/main/config/rootfs/)
such as additional build scripts.

Let's take a look at the `bullseye-v4l2` rootfs for example:

```yaml
rootfs_configs:
  bullseye-v4l2:
    rootfs_type: debos
    debian_release: bullseye
    arch_list:
      - amd64
      - arm64
      - armhf
    extra_packages:
      - libasound2
      - libelf1
      - libjpeg62-turbo
      - libudev1
    extra_packages_remove:
      - bash
      - e2fslibs
      - e2fsprogs
    extra_firmware:
        - mediatek/mt8173/vpu_d.bin
        - mediatek/mt8173/vpu_p.bin
        - mediatek/mt8183/scp.img
        - mediatek/mt8186/scp.img
        - mediatek/mt8192/scp.img
        - mediatek/mt8195/scp.img
    script: "scripts/bullseye-v4l2.sh"
    test_overlay: "overlays/v4l2"
```

* `arch_list` is to define for which architectures the rootfs should be built.
* `extra_packages` is a list passed to the package manager to install them.
* `extra_packages_remove` is a list passed to the package manager to remove
  them.
* `extra_firmware` is a list of Linux kernel firmware blobs to be installed in
  the rootfs image.
* `script` is an arbitrary script to be run after packages have been installed.
  In this case, it will build and install the `v4l2` tools to be able to run
  `v4l2-compliance`.
* `test_overlay` is the path to a directory with extra files to be copied on
  top of the file system.  In this case, it will install the `v4l2-parser.sh`
  script to parse the output of the test suite and report test case results to
  LAVA:

  ```
  $ tree config/rootfs/debos/overlays/v4l2/
  config/rootfs/debos/overlays/v4l2/
  └── usr
      └── bin
          └── v4l2-parser.sh
  ```

Here's a sample command using `kci_rootfs` to build the `bullseye-v4l2` root file
system for `amd64`:

```
$ docker run -it \
  -v $PWD:/tmp/kernelci-core \
  --privileged \
  --device /dev/kvm \
  kernelci/debos
root@759fc147da29:/# cd /tmp/kernelci-core
root@759fc147da29:~/kernelci-core# ./kci_rootfs build \
  --rootfs-config=bullseye-v4l2 \
  --arch=amd64
```

### Writing more advanced test definitions

Running fully featured test suites can involve more than just invoking a few
commands with the `lave-test-case` helper.  This very much depends on the test
itself.  Existing KernelCI native tests such as `v4l2-compliance`, `ltp`,
`kselftest`, `igt` and others provide good examples for how to do this.  The
[`test-definitions`](https://github.com/kernelci/test-definitions) repository
(forked from Linaro for KernelCI) can also be used as a reference, and new
tests may even be added there to be able to use them in LAVA outside of
KernelCI.  Finally, the LAVA documentation about [writing
tests](https://docs.lavasoftware.org/lava/writing-tests.html) describes all the
available features in detail.
