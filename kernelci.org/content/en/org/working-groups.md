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

## Web dashboard

**Workboard:** https://github.com/orgs/kernelci/projects/4

**Mailing list:** [kernelci-webdashboard@groups.io](mailto:<kernelci-webdashboard@groups.io>)

**Team:**

* [Gustavo Padovan](mailto:<gustavo.padovan@collabora.com>) - `padovan` - Lead
* [Greg Kroah-Hartman](mailto:<gregkh@linuxfoundation.org>) - `gregkh`
* [Ricardo Cañuelo](mailto:<ricardo.canuelo@collabora.com>) - `hardboprobot`
* [Nikolai Kondrashov](mailto:<spbnick@gmail.com>) - `spbnick`

As KernelCI keeps growing, and based on the results of the [2020 Community
Survey](http://localhost:1313/blog/posts/2020/07/09/), a new web dashboard is
necessary in order to achieve the goals set by the project.  Several attempts
have been made in the past to replace the current one on
[linux.kernelci.org](https://linux.kernelci.org) but none of them actually
provided a viable alternative.  We've since started gathering ideas from a
range of users in order to produce user stories and get a clear understanding
of what is required.  Based on this, we'll then be looking for technical
solutions including existing frameworks, dashboards used by other projects and
potentially a new design from scratch using modern web technology.

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
