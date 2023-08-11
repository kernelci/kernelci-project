---
title: "ChromeOS"
date: 2022-09-23
description: "The chromeos.kernelci.org instance"
weight: 3
---

The [chromeos.kernelci.org](https://chromeos.kernelci.org) instance is
dedicated to testing upstream kernels with
[ChromeOS](https://www.google.com/chromebook/chrome-os/) user-space.  It
focuses primarily on LTS kernel branches (5.15, 5.10) with some ChromeOS
configuration fragments to run open-source builds of [Chromium
OS](https://www.chromium.org/chromium-os/) on
[Chromebook](https://www.google.com/intl/en_uk/chromebook/) devices.

While the main [linux.kernelci.org](https://linux.kernelci.org) instance uses
generic distros such as buildroot and Debian, ChromeOS is specific to a range
of products.  This may lead to different results compared to Debian for a same
test when user-space components have a role to play (for example, the C library
or the toolchain).  Also, some ChromeOS kernels may be built by KernelCI in the
future using production branches which are not upstream.  For these reasons, a
separate instance appeared to be necessary in order to keep the main production
instance entirely dedicated to upstream.

The [Tast](https://chromium.googlesource.com/chromiumos/platform/tast/)
framework provides a comprehensive series of tests to run on ChromeOS.  This is
typically what the ChromeOS KernelCI instance is running, in addition to some
generic tests such as kselftest, LTP etc.

## Development workflow

While the ChromeOS KernelCI instance is hosted on the production server, it has
a development workflow closer to [staging](../staging).  An integration branch
`chromeos.kernelci.org` is created for each GitHub code repository used on the
ChromeOS instance with all the pending pull requests on top of a `chromeos`
branch.  This is analogous to the `staging.kernelci.org` branch which is based
on `main` instead.

Pull requests for the chromeos.kernelci.org instance should be made with the
`chromeos` branch as a base and commits should include `CHROMEOS` in their
subject.  For example:

```
CHROMEOS section: Describe your patch
```

Once the changes have run successfully, and once reviewed and approved, they
get merged on the `chromeos` branch.  This branch then gets rebased
periodically on top of `main`, typically once a week after each production
update.

Changes on the `chromeos` branch may be merged into the `main` branch to reduce
the number of "downstream" commits it contains.  This can involve refactoring
the changes to make it suitable for the general use-cases, renaming things to
follow some conventions, squashing commits etc.

> **Note** A potential new feature could be to add a `chromeos` label to pull
> requests made against the `main` branch so that they also get deployed via
> the `chromeos.kernelci.org` branch but are merged directly into `main`.

## How ChromeOS tests are run by KernelCI

It is assumed that the reader has some experience with
[`LAVA`](https://www.lavasoftware.org/index.html).

With the Chromebook boot process used on products, the bootloader
([Coreboot](https://www.coreboot.org/) /
[Depthcharge](https://chromium.googlesource.com/chromiumos/platform/depthcharge))
looks for a special kernel partition, and then loads the latest working kernel.
See the [ChromeOS boot
documentation](https://chromium.googlesource.com/chromiumos/docs/+/HEAD/disk_format.md#Google-ChromeOS-devices)
for more details.  In KernelCI, each boot needs to be done with a different
kernel image.  For this reason, a modified version of Depthcharge is used to
load the kernel image over TFTP via an interactive command line interface on
the serial console.  This is managed by the [LAVA
depthcharge](https://docs.lavasoftware.org/lava/actions-boot.html#depthcharge)
boot method.

An additional complication is that ChromeOS can't be easily run over NFS.  It
requires a specific partition layout, and running on the eMMC provides similar
performance to a regular product.  Many tests are about performance so this is
a major aspect to take into account.  It was also not designed to boot with an
initrd, and as a result the kernel modules have to be installed on the eMMC
root partition before the Chromebook starts.  This is done via 2-stage LAVA
job, as can be seen in the
[`cros-boot.jinja2`](https://github.com/kernelci/kernelci-core/blob/chromeos/config/lava/chromeos/cros-boot.jinja2)
LAVA job template.  The Chromebook first boots with Debian NFS to install the
kernel modules on the eMMC (`modules` namespace), then reboots with ChromeOS
(`chromeos` namespace).

> **Note** It is worth noting that testing in **QEMU** is a bit different from
> testing on Chromebooks as the image can be manipulated more easily.
> Installing the modules is done in the rootfs file using deploy postprocess
> before booting the QEMU image.  See the
> [`cros-boot-qemu.jinja2`](https://github.com/kernelci/kernelci-core/blob/chromeos.kernelci.org/config/lava/chromeos/cros-boot-qemu.jinja2)
> LAVA job template for more details.

In the next step, we expect a login prompt on the serial console and
successfull login over it.  The serial console is not used to run tests,
instead they are run over SSH from a Docker container running on a LAVA server.
This proves to be more reliable as serial console hardware can more easily have
issues and kernel console messages can interfere with test results.  The only
downside is that we can't detect networking errors this way.

## Types of tests performed

At the moment, we are running baseline tests that check for critical errors
when loading the kernel (dmesg) and special internal ChromeOS tests "tast".

Tests that have -fixed suffix use downstream kernel (from Google or
compiled inside ChromeOS rootfs) and are "reference" to compare against
the tested, upstream kernel.

## Building and structure of ChromeOS rootfs

Building a ChromeOS rootfs image involves building by [`Google recipe`](https://chromium.googlesource.com/chromiumos/docs/+/main/developer_guide.md#Building-ChromiumOS)
with our own tweaks, as following:
* Enable USB serial support for console
* Build not only by a specific manifest tag, but fix (manifest snapshot)
to certain commits level, this will allow us to get identical builds
and consistent test results on all devices
* Add generated ".bin" image to special "flasher" debos image to save
time
* Extract the kernel and modules for -fixed tests from the generated image
and publish them separately as bzImage and modules.tar.xz
* Extract required tast files to run tast tests in LAVA Docker (tast.tgz)

You can build it manually using following commands, for qemu (amd64-generic):
```yaml
git clone -b chromeos https://github.com/kernelci/kernelci-core/
cd kernelci-core
mkdir temp
chmod 0777 temp
docker run \
    --name kernelci-build-cros \
    -itd \
    -v $(pwd):/kernelci-core \
    --device /dev/kvm \
    -v /dev:/dev \
    --privileged \
    kernelci/cros-sdk
docker exec \
    -it kernelci-build-cros \
    ./kci_rootfs \
    build \
    --rootfs-config chromiumos-amd64-generic \
    --data-path config/rootfs/chromiumos \
    --arch amd64 \
    --output temp
```
Or specify the appropriate parameters in jenkins chromeos/rootfs-builder,
and after that the rootfs will be automatically published on [`storage server`](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/)

## How to add new Chromebook type to KernelCI

To build rootfs (used for flashing chromebook, kernel and modules for -fixed tests)
you need to add similar fragment to the config
file **config/core/rootfs-configs-chromeos.yaml**:
```yaml
  chromiumos-octopus:
    rootfs_type: chromiumos
    board: octopus
    branch: release-R100-14526.B
    serial: ttyS1
    arch_list:
      - amd64
```
* **board**: codename of Chromebook board, check for your at this [`list`](https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices/)

* **branch**: it is recommended to use the same one as other Chromebooks,
unless an exception needs to be made
(for example, a new model is only supported in the latest release)

* **serial**: is hardware dependent, you need to check Chromebook
manual for correct value.

In order to add a Chromebook to the testing, you need to add a similar
entry to the config file **config/core/test-configs-chromeos.yaml**:
```
  asus-C436FA-Flip-hatch_chromeos:
    base_name: asus-C436FA-Flip-hatch
    mach: x86
    arch: x86_64
    boot_method: depthcharge
    filters: &pineview-filter
      - passlist: {defconfig: ['chromeos-intel-pineview']}
    params:
      block_device: nvme0n1
      cros_flash_nfs:
        base_url: 'https://storage.kernelci.org/images/rootfs/debian/bullseye-cros-flash/20220623.0/amd64/'
        initrd: 'initrd.cpio.gz'
        initrd_compression: 'gz'
        rootfs: 'full.rootfs.tar.xz'
        rootfs_compression: 'xz'
      cros_flash_kernel:
        base_url: 'http://storage.chromeos.kernelci.org/images/kernel/v5.10.112-x86-chromebook/'
        image: 'kernel/bzImage'
        modules: 'modules.tar.xz'
        modules_compression: 'xz'
      cros_image:
        base_url: 'https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-hatch/20220621.0/amd64/'
        flash_tarball: 'cros-flash.tar.gz'
        flash_tarball_compression: 'gz'
        tast_tarball: 'tast.tgz'
      reference_kernel:
        image: 'https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-hatch/20220621.0/amd64/bzImage'
        modules: 'https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-hatch/20220621.0/amd64/modules.tar.xz'
```
* **filters**, indicates which kernel builds are suitable for this Chromebook,
fragment names can be found by the name of board in the ChromeOS sources.

For example:
chromiumos-sdk/src/overlays/baseboard-octopus in
chromiumos-sdk/src/overlays/baseboard-octopus/profiles/base/parent is set:
chipset-glk:base

Then:
chromiumos-sdk/src/overlays/chipset-glk/profiles/base/make.defaults
CHROMEOS_KERNEL_SPLITCONFIG="chromeos-intel-pineview"

* **block_device** device name of the persistent storage of Chromebook.
In some devices, this may be eMMC (mmcblkN) or NVMe, as in this case,
in some exceptional cases it can be set to detect (like on "grunt",
where block device name is not persistent)
* **cros_flash_nfs** points to the debos filesystem that flashes the Chromebook.
* **cros_flash_kernel** points to the upstream kernel that will be used for
the above system (it must support the peripherals of the flashed Chromebook,
especially persistent storage, such as eMMC, NVMe, etc)
* **cros_image points** to **cros_flash_nfs.rootfs** repacked together with rootfs
.bin image we built
* **reference_kernel** is ChromeOS downstream kernel that is used for -fixed tests,
in some cases this is the kernel provided by Google, and in some cases
it is extracted from the rootfs we built.

And also a snippet with the tests you want to, run in test configs section:
```
  - device_type: asus-C436FA-Flip-hatch_chromeos
    test_plans:
      - cros-boot
      - cros-boot-fixed
      - cros-tast
      - cros-tast-fixed
```

# How to Prepare a known type of Chromebook for KernelCI testing

If you got a new Chromebook, connected it to LAVA, and want to set it up,
so it can be used in KernelCI, you need to flash the Chromebook with
the firmware(rootfs) compiled and set in kernelci configuration files.

The easiest way is to generate a LAVA template for the flashing job.
If you look in test-configs-chromeos.yaml you will see test definition
"cros-flash".
To generate a flashing template for "octopus", you need to add **cros-flash**
to our local configuration **test-configs-chromeos.yaml**. For example like this:
```
  - device_type: hp-x360-12b-ca0010nr-n4020-octopus_chromeos
    test_plans:
      - cros-flash
```
Then you need to generate, using any suitable kernel, LAVA job template:

```
./kci_test generate --lab-config=lab-collabora --install-path=_install_\
 --output=jobs --db-config=staging.kernelci.org\
 --storage=https://storage.chromeos.kernelci.org/\
  --plan=cros-flash
```
Installing OS image can take quite a long time, 10-15 minutes, and successful
firmware log ends with sync, partprobe, exit commands.

To check if the new firmware was successfully loaded, it is recommended
to generate the **cros-baseline-fixed** job definition for LAVA in a similar way.

## "cros://" kernel configuration fragments

Perhaps by looking at the source code at ChromeOS branch in kernelci-core
you have already noticed unusual kernel fragments with prefix **"cros://"**.

As this instance kernel builds is different from the "main" ones
in many cases it borrows the configuration fragments from the ChromeOS source code.

For example **"cros://chromeos-5.10/armel/chromiumos-arm.flavour.config"** using configuration fragment archive file:
https://chromium.googlesource.com/chromiumos/third_party/kernel/+archive/refs/heads/chromeos-5.10/chromeos/config.tar.gz
then fragments from it:
* **base.config**
* architecture dependent (in our case armel) **armel/common.config**
* **chromeos/armel/chromiumos-arm.flavour.config** from this archive.

## Prebuilt ChromiumOS images published by KernelCI

KernelCI builds and publishes ChromiumOS images for supported boards at the
following location:

https://storage.chromeos.kernelci.org/images/rootfs/chromeos/

Please consult the official [ChromiumOS flashing instructions](https://chromium.googlesource.com/chromiumos/docs/+/HEAD/cros_flash.md)
for examples how to install the images within the published `chromiumos_test_image.bin.gz`.

KernelCI maintains a [Changelog](../chromeos/chromeos_changelog/) which tracks the evolution
between published ChromiumOS releases as well as divergences between the KernelCI
images and ChromiumOS upstream.
