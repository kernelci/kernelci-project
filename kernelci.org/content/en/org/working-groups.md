---
title: "Working groups"
date: 2024-12-03
description: "KernelCI Working Groups"
weight: 4
---

Working groups are small teams of people focusing on a particular aspect of the
project.  Each group typically relies on a monthly meeting and a GitHub
workboard to keep track of things.

There should also be a lead to coordinate activities within each group, such
as:

* updating the workboard
* preparing regular meeting agendas and keeping minutes
* sharing regular reports with the TSC, board and public mailing list


## Infra WG

Formally known as the Infrastructure Committee, this group drives the infrastructure development of KernelCI, translating community requirements to system features. This group also drives Sysadmin team.

**Mailing list:** [kernelci@lists.linux.dev](mailto:<kernelci@lists.linux.dev>)

**Members**

* [Denys Fedoryshchenko](mailto:<denys.f@collabora.com>) - Lead
* [Arisu Tachibana](mailto:<arisu.tachibana@miraclelinux.com>)
* [Ben Copeland](mailto:<ben.copeland@linaro.org>)
* [Gustavo Padovan](mailto:<gustavo.padovan@collabora.com>)
* [Jeny Sadadia](mailto:jeny.sadadia@collabora.com)
* [Mark Brown](mailto:<broonie@kernel.org>)
* [Paweł Wieczorek](mailto:<pawiecz@collabora.com>)
* [Tales Aparecida](mailto:<tales.aparecida@redhat.com>)

The infrastructure WG is regulated by the KernelCI Technical Charter. Rules can be changed through
TSC approval and documented in this git repo.

## Web dashboard

**Workboard:** https://github.com/orgs/kernelci/projects/4

**Mailing list:** [kernelci-webdashboard@groups.io](mailto:<kernelci-webdashboard@groups.io>)

**Team:**

* [Gustavo Padovan](mailto:<gustavo.padovan@collabora.com>) - `padovan` - Lead
* [Mark Brown](mailto:<broonie@kernel.org>) - `broonie`
* [Tales Aparecida](mailto:<tales.aparecida@redhat.com>) - `tales-aparecida`

KernelCI designed a new [Web Dashboard](https://dashboard.kernelci.org/) from scratch. This working group has been driving the progress of that work since the beginning of the work with the UX analysis conducted with the community.

## SysAdmin

**Workboard:** https://github.com/orgs/kernelci/projects/7

**Team:**

* [Denys Fedoryshchenko](mailto:<denys.f@collabora.com>) - `nuclearcat` - Lead
* [Michał Gałka](mailto:<galka.michal@gmail.com>) - `mgalka`
* [Corentin Labbe](mailto:<clabbe@baylibre.com>) - `montjoie`
* [Kevin Hilman](mailto:<khilman@baylibre.com>) - `khilman`
* [Mark Brown](mailto:<broonie@kernel.org>) - `broonie`
* [Nikolai Kondrashov](mailto:<spbnick@gmail.com>) - `spbnick`
* [Vince Hillier](mailto:<vince@revenni.com>) - `vince`
* [Paweł Wieczorek](mailto:<pawiecz@collabora.com>) - `pawiecz`

The KernelCI common infrastructure requires some regular maintenance to keep
web servers, databases and Cloud services up and running.  This does not
include any test lab other than some Kubernetes clusters as hardware platforms
are maintained by separate companies and individuals.  Members of the SysAdmin
working group have admin rights on all KernelCI systems, wherever applicable.
As per the [2022-12-08 TSC vote](/org/tsc/votes/#2022-12-08), admin rights
cover the following items:

* Machines (SSH, sudo):
  * Azure VMs
  * Kubernetes nodes

* Web applications:
  * SysAdmin GitHub project board
  * Azure portal (admin access)
* Encrypted repositories:
  * kernelci-jenkins-data
  * builder-config-data
