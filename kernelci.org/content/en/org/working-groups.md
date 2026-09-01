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


## Infrastructure Committee

The Infrastructure Committee is a body of the project defined in section 3 of
the [Technical Charter](/files/KernelCI_Project_Technical_Charter_202607.pdf)
rather than an ordinary working group.  It consists of the contributors
responsible for the development, deployment and maintenance of the software
projects operated as KernelCI services, including but not limited to Maestro,
KCIDB, Storage and the Web Dashboard.  It drives the infrastructure development
of KernelCI, translating community requirements to system features.  The
[SysAdmin](#sysadmin) team functions as a sub-team within the committee, and
access to system administration secrets is granted to designated members of that
sub-team as required.

**Mailing list:** [kernelci@lists.linux.dev](mailto:<kernelci@lists.linux.dev>)

**Members**

* [Denys Fedoryshchenko](mailto:<denys.f@collabora.com>) - Lead
* [Arisu Tachibana](mailto:<arisu.tachibana@miraclelinux.com>)
* [Ben Copeland](mailto:<ben.copeland@linaro.org>)
* [Jeny Sadadia](mailto:jeny.sadadia@collabora.com)
* [Mark Brown](mailto:<broonie@kernel.org>)
* [Paweł Wieczorek](mailto:<pawiecz@collabora.com>)
* [Tales Aparecida](mailto:<tales.aparecida@redhat.com>)

The initial membership was set by the [2025-07-30 TSC
vote](/org/tsc/votes/#2025-07-30).

The committee is responsible for:

* overseeing the reliable operation, maintenance and continuous improvement of
  the KernelCI infrastructure services
* managing the SysAdmin sub-team and defining procedures for secure access and
  operational best practices
* supporting the development and deployment of new infrastructure components
  aligned with the project's technical roadmap
* defining and maintaining policies for secure and efficient service operation

The committee may vote to add or remove members at any time by a simple majority
vote.  Any member who has not actively contributed to the relevant
infrastructure projects for more than six consecutive months is automatically
removed from the committee.

The voting members of the TSC and of the Infrastructure Committee together elect
an Infrastructure Committee Lead (the "Infrastructure Lead") from among the
voting members of the committee, to serve a two-year term.  The Infrastructure
Lead is also a voting member of the [TSC](/org/tsc/).

Rules can be changed through TSC approval and documented in this git repo.

## Web dashboard

**Workboard:** https://github.com/orgs/kernelci/projects/28

**Mailing list:** [kernelci-webdashboard@groups.io](mailto:<kernelci-webdashboard@groups.io>)

**Team:**

* [Tales Aparecida](mailto:<tales.aparecida@redhat.com>) - `tales-aparecida` - Lead
* [Ben Copeland](mailto:<ben.copeland@linaro.org>) - `bhcopeland`
* [Denys Fedoryshchenko](mailto:<denys.f@collabora.com>) - `nuclearcat`
* [Gustavo Flores](mailto:<gustavobtflores@gmail.com>) - `gustavobtflores`
* [João Bertacchi](mailto:<joaobertacchi@gmail.com>) - `joaobertacchi`
* [Lucas Santos](mailto:<devlucassantoss@gmail.com>) - `LucasSantos27`
* [Marcelo Robert](mailto:<4mrSantos@gmail.com>) - `MarceloRobert`
* [Mark Brown](mailto:<broonie@kernel.org>) - `broonie`

The KernelCI [Dashboard] is a web platform (Django + React) which aims at providing an easy way for the community to look at the test results.
Its API also powers [kci-dev] - our cmdline tooling - for results visualization in the terminal.
It is still under active development, open to feedback and feature requests, all in <https://github.com/kernelci/dashboard>.

[Dashboard]: https://dashboard.kernelci.org/
[kci-dev]: https://github.com/kernelci/kci-dev/


### Dashboard WG

The KernelCI Dashboard working group meets every 2 weeks on Mondays at 14 UTC via Zoom.
There we discuss bug reports, feature requests, and prioritization.

Details to join are available in [the first invite](https://lore.kernel.org/all/CAPo4OxSPZXF+6syLrTQydnpTY-26sEHK03D7Tz=TH88F61+VHw@mail.gmail.com/).

## SysAdmin

**Workboard:** https://github.com/orgs/kernelci/projects/7

**Team:**

* [Denys Fedoryshchenko](mailto:<denys.f@collabora.com>) - `nuclearcat` - Lead
* [Ben Copeland](mailto:<ben.copeland@linaro.org>) - `bhcopeland`
* [Corentin Labbe](mailto:<clabbe@baylibre.com>) - `montjoie`
* [Kevin Hilman](mailto:<khilman@baylibre.com>) - `khilman`
* [Mark Brown](mailto:<broonie@kernel.org>) - `broonie`
* [Michał Gałka](mailto:<galka.michal@gmail.com>) - `mgalka`
* [Nikolai Kondrashov](mailto:<spbnick@gmail.com>) - `spbnick`
* [Paweł Wieczorek](mailto:<pawiecz@collabora.com>) - `pawiecz`
* [Vince Hillier](mailto:<vince@revenni.com>) - `vince`

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

## Lab WG

**Mailing list:** [kernelci@lists.linux.dev](mailto:<kernelci@lists.linux.dev>)

**Team:**

* [Ben Copeland](mailto:<ben.copeland@linaro.org>) - `bhcopeland` - Lead
* [Denys Fedoryshchenko](mailto:<denys.f@collabora.com>) - `nuclearcat`
* [Mark Brown](mailto:<broonie@kernel.org>) - `broonie`
* [Minas Hambardzumyan](mailto:<minas@ti.com>) - `minas_36361`

The Lab working group focuses on lab integration into KernelCI. Topics include Labgrid/LAVA, the pull labs approach, LAVA updates, and lowering the burden and cost of running labs within the KernelCI project.
