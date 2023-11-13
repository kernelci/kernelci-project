---
title: "ChromeOS image changelog"
date: 2023-04-25
weight: 4
---

This file tracks divergences between the KernelCI built ChromiumOS images and upstream ChromiumOS as well as any changes between image relases.

Divergences can be considered tech-debt and in the long run need to be kept under control and minimized, therefore this chanelog should reflect its evolution from version to version.

### Fetching latest images

It is recommended to use the latest published image versions for each board from [this list](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/).

The latest version can be found either from the directory date name (e.g. `chromiumos-asurada/20230208.0`) or by the `distro_version` field in the `manifest.json` file, where for e.g. R106 is greater than R100.

### ChromiumOS release documentation

[This page](https://chromium.googlesource.com/chromiumos/docs/+/HEAD/releases.md) contains information on how ChromiumOS manages its releases, schedules, support windows and other such useful information.

For an up-to-date overview of current and planned releases, please visit the [schedule dashboard](https://chromiumdash.appspot.com/schedule).

## R118

### Repo manifest

The following images have been built using [this manifest](https://raw.githubusercontent.com/kernelci/kernelci-core/chromeos/config/rootfs/chromiumos/cros-snapshot-release-R118-15604.B.xml). The [repo tool](https://code.google.com/archive/p/git-repo/) can fetch the sources specified in the manifest file.

Specific instructions on how to fetch and build ChromiumOS from a manifest file can be found in the [developer guide](https://chromium.googlesource.com/chromiumos/docs/+/main/developer_guide.md).

### Supported boards

Direct links for each supported board in this release are provided below for convenience.
| Board       | Kernels shipped in image | Kernels tested by KernelCI (replacing image kernels during boot) |
|-------------|:------------:|:-------:|
| [asurada](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-asurada/20231106.0/arm64) | v6.4.x<br> + display patches<br> + panfrost | stable:linux-6.1.y |
| [brya](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-brya/20231106.0/amd64) | default | stable:linux-6.1.y |
| [cherry](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-cherry/20231106.0/arm64) | linux-next 20230203<br> + mtk HW enablement patches<br> + panfrost | |
| [coral](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-coral/20231106.0/amd64) | default | stable:linux-6.1.y |
| [dedede](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-dedede/20231106.0/amd64/) | default | stable:linux-6.1.y |
| [grunt](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-grunt/20231106.0/amd64/) | default | stable:linux-6.1.y |
| [guybrush](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-guybrush/20231106.0/amd64/) | default | stable:linux-6.1.y |
| [hatch](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-hatch/20231106.0/amd64/) | default | stable:linux-6.1.y |
| [jacuzzi](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-jacuzzi/20231106.0/arm64/) | v6.4.x <br> + panfrost | stable:linux-6.1.y <br> next-integration-branch (for-kernelci) |
| [nami](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-nami/20231106.0/amd64/) | default | stable:linux-6.1.y |
| [octopus](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-octopus/20231106.0/amd64/) | chromeos-5.15 | stable:linux-6.1.y |
| [puff](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-puff/20231106.0/amd64/) | default | stable:linux-6.1.y |
| [rammus](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-rammus/20231106.0/amd64/) | default | stable:linux-6.1.y |
| [sarien](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-sarien/20231106.0/amd64/) | default | stable:linux-6.1.y |
| [trogdor](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-trogdor/20231106.0/arm64/) | default | stable:linux-6.1.y |
| [volteer](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-volteer/20231106.0/amd64/) | default | stable:linux-6.1.y |
| [zork](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-zork/20231106.0/amd64/) | default | stable:linux-6.1.y |


### New workarounds/patches since previous version (R116)

#### minigbm:
- Dropped mediatek backend in favor of drv_dumb backend, no more divergence for the platform/minigbm component.

#### chromiumos-overlay:
- Reworked the minigbm patch into a single two liner patch to activate drv_dumb
- Droppped the bump to make chromeos-kernel-5_10 use our own forked 5.10 branch, in favor of the 5.10 branch shipped in R118 by CrOS upstream.
- Fixed broken portage manifest for media-libs/cros-camera-libfs
- Masked newer chromeos-chrome ebuild version which doesn't have a binpkg, to avoid unnecessarily long build times.
- Bumped chromeos-installer ebuild as a result of forking the platform2 overlay.

#### platform2:
- Forked to disable failing installer tpm check, until a fix is  landed for b:291036452.

#### graphics:
- Backported patch from R119 to avoid a conflict, still need to keep this patch in R118

#### board-overlays:
- Forward ported the last remaining commit without conflicts. Will keep it for now but gradually will reduce its footprint as MTK SoCs start using the newer Google kernels with 6.6
- Bumped octopus to 5.15 because tast fails with 4.14.

#### third_party/kernel/v5.10:
- Removed fork in favor of chromeos-kernel-5_10

## R116

### Repo manifest

The following images have been built using [this manifest](https://raw.githubusercontent.com/kernelci/kernelci-core/chromeos/config/rootfs/chromiumos/cros-snapshot-release-R116-15509.B.xml). The [repo tool](https://code.google.com/archive/p/git-repo/) can fetch the sources specified in the manifest file.

Specific instructions on how to fetch and build ChromiumOS from a manifest file can be found in the [developer guide](https://chromium.googlesource.com/chromiumos/docs/+/main/developer_guide.md).

### Supported boards
Direct links for each supported board in this release are provided below for convenience.
| Board       | Kernels shipped in image | Kernels tested by KernelCI (replacing image kernels during boot) |
|-------------|:------------:|:-------:|
| [asurada](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-asurada/20230825.0/arm64) | v6.2.7<br> + display patches<br> + panfrost | stable:linux-6.1.y |
| [brya](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-brya/20230825.0/amd64) | default | stable:linux-6.1.y |
| [cherry](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-cherry/20230825.0/arm64) | linux-next 20230203<br> + mtk HW enablement patches<br> + panfrost | |
| [coral](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-coral/20230825.0/amd64) | default | stable:linux-6.1.y |
| [dedede](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-dedede/20230825.0/amd64/) | default | stable:linux-6.1.y |
| [grunt](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-grunt/20230825.0/amd64/) | chromeos-5_10 | stable:linux-6.1.y |
| [guybrush](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-guybrush/20230825.0/amd64/) | default | stable:linux-6.1.y |
| [hatch](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-hatch/20230825.0/amd64/) | default | stable:linux-6.1.y |
| [jacuzzi](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-jacuzzi/20230825.0/arm64/) | v6.2.7 <br> + panfrost | stable:linux-6.1.y <br> next-integration-branch (for-kernelci) |
| [nami](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-nami/20230825.0/amd64/) | default | stable:linux-6.1.y |
| [octopus](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-octopus/20230825.0/amd64/) | default | stable:linux-6.1.y |
| [puff](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-puff/20230825.0/amd64/) | default | stable:linux-6.1.y |
| [rammus](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-rammus/20230825.0/amd64/) | default | stable:linux-6.1.y |
| [sarien](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-sarien/20230825.0/amd64/) | default | stable:linux-6.1.y |
| [trogdor](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-trogdor/20230825.0/arm64/) | default | stable:linux-6.1.y |
| [volteer](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-volteer/20230825.0/amd64/) | default | stable:linux-6.1.y |
| [zork](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-zork/20230825.0/amd64/) | default | stable:linux-6.1.y |


### New workarounds/patches since previous version (R114)

* Updated minigbm backend for Mediatek
* Updated separate patches for tpm2 flag where it is necessary
* Added workaround for b/295364868 (orphan_files feature not supported by old kernels) by updating mke2fs.conf
* Added workaround for PS1/command prompt
* Backported fix for b/300303585. The fix was upstreamed starting with R119, after which KernelCI should drop it.

### Removed workarounds since previous version (R114)

* Removed trogdor patch revert for arm64 userspace
* Removed manual kernel version override for grunt
* Removed build fixes for coral, sarien

## R114

### Repo manifest

The following images have been built using [this manifest](https://github.com/kernelci/kernelci-core/blob/chromeos/config/rootfs/chromiumos/cros-snapshot-release-R114-15437.B.xml). The [repo tool](https://code.google.com/archive/p/git-repo/) can fetch the sources specified in the manifest file.

Specific instructions on how to fetch and build ChromiumOS from a manifest file can be found in the [developer guide](https://chromium.googlesource.com/chromiumos/docs/+/main/developer_guide.md).

### Supported boards

Direct links for each supported board in this release are provided below for convenience.
| Board       | Kernels shipped in image | Kernels tested by KernelCI (replacing image kernels during boot) |
|-------------|:------------:|:-------:|
| [asurada](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-asurada/20230620.0/arm64) | v6.2.7<br> + display patches<br> + panfrost | stable:linux-6.1.y |
| [cherry](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-cherry/20230620.0/arm64) | linux-next 20230203<br> + mtk HW enablement patches<br> + panfrost | |
| [coral](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-coral/20230620.0/amd64) | default | stable:linux-6.1.y |
| [dedede](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-dedede/20230620.0/amd64/) | default | stable:linux-6.1.y |
| [grunt](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-grunt/20230620.0/amd64/) | chromeos-5_10 | stable:linux-6.1.y |
| [hatch](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-hatch/20230620.0/amd64/) | default | stable:linux-6.1.y |
| [jacuzzi](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-jacuzzi/20230620.0/arm64/) | v6.2.7 <br> + panfrost | stable:linux-6.1.y <br> next-integration-branch (for-kernelci) |
| [nami](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-nami/20230620.0/amd64/) | default | stable:linux-6.1.y |
| [octopus](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-octopus/20230620.0/amd64/) | default | stable:linux-6.1.y |
| [rammus](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-rammus/20230620.0/amd64/) | default | stable:linux-6.1.y |
| [sarien](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-sarien/20230620.0/amd64/) | default | stable:linux-6.1.y |
| [trogdor](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-trogdor/20230620.0/arm64/) | default | stable:linux-6.1.y |
| [volteer](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-volteer/20230620.0/amd64/) | default | stable:linux-6.1.y |
| [zork](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-zork/20230620.0/amd64/) | default | stable:linux-6.1.y |

### Changes since previous version (R111)

* Dropped separate initramfs patches, as it is upstream now, [this CL](https://chromium-review.googlesource.com/c/chromiumos/platform/initramfs/+/4262007)

## R111

### Repo manifest

The following images have been built using [this manifest](https://github.com/kernelci/kernelci-core/blob/chromeos/config/rootfs/chromiumos/cros-snapshot-release-R111-15329.B.xml). The [repo tool](https://code.google.com/archive/p/git-repo/) can fetch the sources specified in the manifest file.

Specific instructions on how to fetch and build ChromiumOS from a manifest file can be found in the [developer guide](https://chromium.googlesource.com/chromiumos/docs/+/main/developer_guide.md).

### Supported boards

Direct links for each supported board in this release are provided below for convenience.
| Board       | Kernels shipped in image | Kernels tested by KernelCI (replacing image kernels during boot) |
|-------------|:------------:|:-------:|
| [amd64-generic](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-amd64-generic/20230511.0/amd64) | chromeos-5_15 | stable:linux-6.1.y |
| [asurada](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-asurada/20230511.0/arm64) | v6.2.7<br> + display patches<br> + panfrost | stable:linux-6.1.y |
| [cherry](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-cherry/20230511.0/arm64) | linux-next 20230203<br> + mtk HW enablement patches<br> + panfrost | |
| [coral](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-coral/20230511.0/amd64) | chromeos-5_10 | stable:linux-6.1.y |
| [dedede](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-dedede/20230511.0/amd64/) | chromeos-5_4 | stable:linux-6.1.y |
| [grunt](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-grunt/20230606.0/amd64/) | chromeos-5_10 | stable:linux-6.1.y |
| [hatch](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-hatch/20230511.0/amd64/) | chromeos-4_19 | stable:linux-6.1.y |
| [jacuzzi](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-jacuzzi/20230511.0/arm64/) | v6.2.7 <br> + panfrost | stable:linux-6.1.y <br> next-integration-branch (for-kernelci) |
| [nami](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-nami/20230511.0/amd64/) | chromeos-4_4 | stable:linux-6.1.y |
| [octopus](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-octopus/20230511.0/amd64/) | chromeos-4_14 | stable:linux-6.1.y |
| [rammus](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-rammus/20230511.0/amd64/) | chromeos-4_4 | stable:linux-6.1.y |
| [sarien](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-sarien/20230511.0/amd64/) | chromeos-4_19 | stable:linux-6.1.y |
| [trogdor](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-trogdor/20230606.0/arm64/) | chromeos-5_4 | stable:linux-6.1.y |
| [volteer](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-volteer/20230511.0/amd64/) | chromeos-5_4 | stable:linux-6.1.y |
| [zork](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-zork/20230511.0/amd64/) | chromeos-5_4 | stable:linux-6.1.y |

### Changes since previous version (R106)
* Grunt kernel manually forced from 4.14 to 5.10 in overlay [patch](https://github.com/kernelci/kernelci-core/pull/1948/commits/71ee9f81a4c6ed9b4d50813eef37dbbd20c25f35)
* Trogdor patch to enable arm64 userspace reverted [patch](https://github.com/kernelci/kernelci-core/pull/1948/commits/71ee9f81a4c6ed9b4d50813eef37dbbd20c25f35)
* CR50 firmware extracted from image to prevent automatic upgrade, available in same directory for standalone upgrade [patch1](https://github.com/kernelci/kernelci-core/pull/1816/commits/194a3173be29bab9ae035c2d1b7247fb205ca923) [patch2](https://github.com/kernelci/kernelci-core/pull/1872/commits/3ce3959fd1b26876f975a6e6132c9510d05166d2)

## R106

### Repo manifest

The following images have been built using [this manifest](https://github.com/kernelci/kernelci-core/blob/chromeos/config/rootfs/chromiumos/cros-snapshot-release-R106-15054.B.xml). The [repo tool](https://code.google.com/archive/p/git-repo/) can fetch the sources specified in the manifest file.

Specific instructions on how to fetch and build ChromiumOS from a manifest file can be found in the [developer guide](https://chromium.googlesource.com/chromiumos/docs/+/main/developer_guide.md).

### Supported boards

Direct links for each supported board in this release are provided here for convenience:
- [amd64-generic](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-amd64-generic/20221102.0/arm64)
- [asurada](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-asurada/20230208.0/arm64)
- [cherry](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-cherry/20230330.0/arm64)
- [coral](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-coral/20221026.0/amd64)
- [dedede](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-dedede/20221113.0/amd64/)
- [grunt](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-grunt/20221028.0/amd64/)
- [hatch](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-hatch/20221027.0/amd64/)
- [jacuzzi](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-jacuzzi/20230206.0/arm64/)
- [nami](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-nami/20221120.0/amd64/)
- [octopus](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-octopus/20221025.0/amd64/)
- [rammus](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-rammus/20221116.0/amd64/)
- [sarien](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-sarien/20221111.0/amd64/)
- [trogdor](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-trogdor/20230214.0/arm64/)
- [volteer](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-volteer/20221115.0/amd64/)
- [zork](https://storage.chromeos.kernelci.org/images/rootfs/chromeos/chromiumos-zork/20221115.0/amd64/)

### Changes since previous version (R100)
- A custom repo manifest is used to build images which points to forked repositories.
- SElinux is now disabled in userspace, see issue https://github.com/kernelci/kernelci-core/issues/1372 .
- chromeos-kernel-upstream is used for Mediatek image builds.

### Known divergences

#### src/third-party/kernel/next
- Points to the [Mediatek Integration branch](https://gitlab.collabora.com/google/chromeos-kernel/-/tree/for-kernelci).
- Currently only used for cherry board builds because upstream support is still WIP.

#### src/third-party/kernel/upstream
- Based on v6.2.7 stable kernel release.
- `arch/arm64/configs/defconfig` was extended with Mediatek specific config fragments. In the future we might find a better way to fetch these for the upstream kernel builds.
- Backported and cherry-picked ~ 19 patches to enable Panfrost on mediatek. These will be dropped in future kernel versions.

#### src/third-party/chromiumos-overlay
- Disable selinux in the global profile for all boards.
- Upgrade mesa-panfrost to latest 22.3.3 for Mali valhall GPU support.
- Add USE flag to skip cr50 FW upgrades.
- Bump ebuilds for divergence in other components (kernel, minigbm).

#### src/platform/minigbm
- Add patch to allow minigbm to work with panfrost BO ioctls. This works but needs significant changes before being sent upstream.

#### src/platform/initramfs
- Contains a backport of a commit which got upstreamed in [this CL](https://chromium-review.googlesource.com/c/chromiumos/platform/initramfs/+/4262007).
- This fork can be removed when upgrading to a newer ChromiumOS version containing the above commit.

#### src/overlays
- Added fix for broken upstream chipset-mt8183 virtual/opengles panfrost dependencies.
- Panfrost added as a graphics alternative for all Mediatek chipsets.
- Removed Mali G-57 empty job workaround firmware which is not required for upstream graphics.
- Instructed mt8183/8192 builds to use upstream kernel.
- Instructed mt8195 builds to use linux-next kernel / Mediatek Integration branch (see above).
