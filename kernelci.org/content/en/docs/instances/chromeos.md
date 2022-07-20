---
title: "ChromeOS"
date: 2022-07-20T08:30:00Z
description: "How chromeos.kernelci.org works"
---

In many aspects ChromeOS.kernelci.org it works similar to 
[Staging instance](https://kernelci.org/docs/instances/staging/),
such as merging pull requests and running them on staging.
The main purpose of this instance is to test the functionality of new kernel versions 
with ChromeOS userspace, compiled on KernelCI servers from publicly available sources (ChromiumOS).

Since ChromeOS requires different way of kernel features configuration than regular distributions,
and rootfs builds also significantly different too, this instance uses a separate 
kernelci-core and kernelci-jenkins project branches chromeos/chromeos.kernel.org.

The chromeos branch has the changes that have been merged, whereas 
chromeos.kernelci.org had all pending PRs for the chromeos branch 
dynamically merged on top of it.

## Contributing

In case you want to submit a patch for KernelCI ChromeOS tests, please send a github PR, with
commit title in the format:

```
CHROMEOS patched_filename: Describe your patch
```

## How [`Chromebooks`](https://www.google.com/intl/en_uk/chromebook/) testing works, in general

It is assumed that the reader has some experience with [`LAVA`](https://www.lavasoftware.org/index.html).

In the traditional Chromebook boot process - bootloader looks for a 
special kernel partition, and then loads the latest working kernel 
[`(ChromeOS boot documentation)`](https://chromium.googlesource.com/chromiumos/docs/+/HEAD/disk_format.md#Google-ChromeOS-devices) . 
In our testing, we take control of the device before this stage, we load 
the tested kernel over the network, via 
[`LAVA depthcharge`](https://docs.lavasoftware.org/lava/actions-boot.html#depthcharge).

An additional complication is that we cannot place kernel modules on the nfs image 
or initrd like "usual" LAVA DUT, due to the ChromeOS architecture, so in the case of ChromeOS, 
we need to _preload_ tested kernel modules to device persistent storage 
partition 3 on the DUT(Chromebook), before booting ChromeOS kernel.
This is done via 2-stage LAVA job, pay attention to this section test, 
namespace modules: [`cros-boot.jinja2`](https://github.com/kernelci/kernelci-core/blob/chromeos/config/lava/chromeos/cros-boot.jinja2).

It is worth noting that testing in QEMU is a bit different from testing 
on Chromebooks, so installing modules is done in the rootfs file using 
deploy postprocess before booting qemu image:
[`cros-boot-qemu.jinja2`](https://github.com/kernelci/kernelci-core/blob/chromeos.kernelci.org/config/lava/chromeos/cros-boot-qemu.jinja2).

In the next step, we expect a login prompt on the serial console and
successfull login over it, but due to reliability problems for LAVA, 
we use serial console minimally. Success indicates kernel and operating system loaded
properly.

And the last step is to run the docker image in LAVA and connect to the DUT 
via ssh using the developer key and perform the necessary tests.

## Types of tests performed

At the moment, we are running baseline tests that check for critical errors 
when loading the kernel (baseline) and special internal ChromeOS tests 
"tast".

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

