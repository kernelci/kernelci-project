---
title: "Maintainers"
date: 2023-08-11
description: "KernelCI maintainers (legacy system)"
---

## Software Maintainers

### Frontend (deprecated)

The KernelCI frontend provides a dynamic [web
dashboard](https://linux.kernelci.org/job/) showing the data available from the
backend.  A new workboard is currently being developed to replace it and
include data from KCIDB.

* Main repository:
  [`kernelci-frontend`](https://github.com/kernelci/kernelci-frontend)
* Ansible config repository:
  [`kernelci-frontend-config`](https://github.com/kernelci/kernelci-frontend-config)
* Maintainer: `mgalka`
* Deputy: `apereira`

### Backend (deprecated)

The KernelCI backend provides a [web API](https://api.kernelci.org/) to send
build and test results and let the frontend dashboard retrieve.  It also
generates email reports, tracks regressions and triggers automated bisections.
The new API will eventually replace it.

* Main repository:
  [`kernelci-backend`](https://github.com/kernelci/kernelci-backend)
* Ansible config repository:
  [`kernelci-backend-config`](https://github.com/kernelci/kernelci-backend-config)
* Maintainer: `mgalka`
* Deputy: `gtucker`

### Jenkins (deprecated)

The current KernelCI pipeline is using Jenkins.  While this is about to be
replaced with the new pipeline and API, the purpose remains essentially the
same: orchestrating the builds and tests on kernelci.org.

* Maintainers: `broonie`, `mgalka`, `nuclearcat`
* Components:
  [`kernelci-jenkins`](https://github.com/kernelci/kernelci-jenkins)
* Resources: Azure, GCE

## Instance maintainers

As there are several KernelCI instances, it's necessary to have people
dedicated to each of them.

### Production instance (legacy)

The KernelCI components and services need to be regularly updated on the
production instance with the latest code and configuration changes.  This
includes typically enabling coverage for new kernel branches or running new
tests, as well as updating rootfs and Docker images with the latest versions of
all the packages being used.

It is currently done once a week on average, although deployment may become
gradually more continuous as services start to get hosted in the Cloud and run
in Docker containers.

* Dashboard: [linux.kernelci.org](https://linux.kernelci.org)
* Description: [Production](/docs/instances/production)
* Maintainers: `mgalka`, `nuclearcat`
* Components: [`kernelci-deploy`](https://github.com/kernelci/kernelci-deploy)

### Staging instance (legacy)

All the incoming pull requests are merged into temporary integration branches
and deployed on [staging.kernelci.org](https://staging.kernelci.org] for
testing.  This is explained in greater detail in the
[Staging](/docs/instances/staging) section.

* Dashboard: [staging.kernelci.org](https://staging.kernelci.org)
* Description: [Staging](/docs/instances/staging)
* Maintainers: `gtucker`, `broonie`, `nuclearcat`
* Components: [`kernelci-deploy`](https://github.com/kernelci/kernelci-deploy)

### ChromeOS instance (legacy)

The Chrome OS KernelCI instance is dedicated to building specific kernels and
running Chrome OS tests on Chromebooks.  This is very close to the code used in
production but has continuous deployment like the staging one, including open
pull requests for the `chromeos` branches.  These branches need to be regularly
rebased with any extra patches that are not merged upstream, typically after
each production update.

* Dashboard: [chromeos.kernelci.org](https://chromeos.kernelci.org)
* Description: [ChromeOS](/docs/instances/chromeos)
* Maintainers: `mgalka`, `nuclearcat`
* Components: [`kernelci-deploy`](https://github.com/kernelci/kernelci-deploy)

### CIP instance (legacy)

The CIP instance is dedicated to building CIP specific kernels with CIP
configurations. Currently the CIP KernelCI code is in production.

* Dashboard: [cip.kernelci.org](https://cip.kernelci.org)
* Description: [CIP](/docs/instances/cip)
* Maintainers: `arisut`
* Components: [`kernelci-deploy`](https://github.com/kernelci/kernelci-deploy)
