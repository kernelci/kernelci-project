---
title: "Technical Steering Committee"
date: 2021-02-10T11:41:14Z
draft: true
description: "Core developers and maintainers"
---

The Technical Steering Committee (TSC) is a team of people who are responsible
for keeping the KernelCI project in a good shape and driving its development.

The rules for adding or removing members from the TSC are defined in the LF
project charter.  Typically, major contributors eventually become members and
those who have stopped contributing for an extended period of time may be
removed.  This is done in agreement with the TSC and the AB.

As of today, the committee is composed of the members listed below with their
respective email address and IRC nicknames:

* [Kevin Hilman](mailto:<khilman@baylibre.com>) - `khilman`
* [Mark Brown](mailto:<broonie@kernel.org>) - `broonie`
* [Guillaume Tucker](mailto:<guillaume.tucker@collabora.com>) - `gtucker`
* [Corentin Labbe](mailto:<clabbe@baylibre.com>) - `montjoie`
* [Nikolai Kondrashov](mailto:<spbnick@gmail.com>) - `spbnick`
* [Michał Gałka](mailto:<michal.galka@collabora.com>) - `mgalka`
* [Alexandra Pereira](mailto:<alexandra.pereira@collabora.com>) - `apereira`
* [Lakshmipathi Ganapathi](mailto:<lakshmipathi.ganapathi@collabora.com>)
* [Alice Ferrazzi](mailto:<alice.ferrazzi@miraclelinux.com>) - `alicef`

For general discussions, the regular
[`kernelci@groups.io`](mailto:<kernelci@groups.io>) mailing list can be used.
To contact only the TSC members directly, the
[`kernelci-tsc@groups.io`](mailto:<kernelci-tsc@groups.io>) private list may be
used instead.

There are essentially three kinds of maintainer roles:

[software maintainers](#software-maintainers)
: in charge of the KernelCI software components

[service maintainers](#service-maintainers)
: in charge of the KernelCI hosted services

[feature maintainers](#feature-maintainers)
: in charge of features that span across the whole KernelCI stack

[channel maintainers](#channel-maintainers)
: in charge of the communication channels used by KernelCI


## Software Maintainers

At least one maintainer is assigned to each software component.  The work
involves reviewing pull requests, triaging and reviving old ones, updating
GitHub settings and facilitating the development workflow.  Having “deputy”
maintainers whenever possible also helps with the continuity of the project.

### Core tools

The [core tools](/docs/core) provide the command line utilities and the
`kernelci` Python package used to implement a KerneLCI pipeline.

* Repository: [`kernelci-core`](https://github.com/kernelci/kernelci-core)
* Maintainer: `gtucker`
* Deputy: `mgalka`

### Backend

The KernelCI backend provides a [web API](https://api.kernelci.org/) to send
build and test results and let the frontend dashboard retrieve.  It also
generates email reports, tracks regressions and triggers automated bisections.

* Main repository: [`kernelci-backend`](https://github.com/kernelci/kernelci-backend)
* Ansible config repository: [`kernelci-backend-config`](https://github.com/kernelci/kernelci-backend-config)
* Maintainer: `mgalka`
* Deputy: `gtucker`

### Frontend

The KernelCI frontend provides a dynamic [web
dashboard](https://linux.kernelci.org/job/) showing the data available from the
backend.

* Main repository: [`kernelci-frontend`](https://github.com/kernelci/kernelci-frontend)
* Ansible config repository: [`kernelci-frontend-config`](https://github.com/kernelci/kernelci-frontend-config)
* Maintainer: Alexandra
* Deputy: `gtucker`

### KCIDB

KCIDB provices a set of tools to submit kernel test data to a common database.

* Main repositories: [`kcidb`](https://github.com/kernelci/kcidb), [`kcidb-io`](https://github.com/kernelci/kcidb-io)
* Grafana dashboard: [`kcidb-grafana`](https://github.com/kernelci/kcidb-grafana)
* Maintainer: `spbnick`


## Service maintainers

Services hosted by KerneLCI all need someone to look after them and ensure they
stay online and available.

### Pipeline / Jenkins

The current KernelCI pipeline is using Jenkins.  While this may change with
Jenkins X, Tekton or some other framework, the service is essentially the same:
orchestrating the builds and tests on kernelci.org.

* Maintainers: `broonie`, `gtucker`
* Components: [`kernelci-jenkins`](https://github.com/kernelci/kernelci-jenkins)
* Resources: Azure, GCE

### Kubernetes

Several Kubernetes clusters are used by KernelCI, to build kernels and run
platform-independent tasks or kernel tests in VMs (static analysis, QEMU...).

* Maintainers: `khilman`, `montjoie`
* Resources: Azure, GCE

### VM Servers

A number of virtual machine servers are being used, to host the kernelci.org
and staging.kernelci.org services.  They are currently all managed in MS Azure,
but this can change over time.  The services remain the same.  They require SSL
certificates, monitoring tools, backups...

* Maintainers: `montjoie`, `gtucker`, `mgalka`
* Resources: Azure (VMs, Mongo DB)

### BigQuery

KCIDB uses BigQuery as a database engine.  This requires setting up tokens and
managing the associated Cloud resources.

* Maintainers: `spbnick`, `khilman`
* Resources: BigQuery, GCE

### Grafana

KCIDB uses a Grafana instance as a prototype dashboard.  Additional instances
may be set up for other use-cases, such as showing statistics about the
KernelCI project in general.

* Maintainers: `spbnick`
* Resources: VM Servers

### Docker Hub

All the Docker images used by KernelCI are pushed to the [Docker
Hub](https://hub.docker.com/).  This requires some maintenance in particular to
keep an eye on resource usage and adjust permissions.

* Maintainers: `gtucker`, `mgalka`, Alexandra

## Feature maintainers

Some advanced KernelCI features involve coordination between multiple software
components and services, but still require dedicated maintainders to ensure
they behave as intended.

### Native tests

Tests orchestrated on kernelci.org are called the *native* KernelCI tests,
unlike tests running in external CI systems.  This covers integration with test
labs, rootfs images, pipeline configuration... anything related to running
those tests and getting their results into the database.

* Maintainers: Alexandra, Lakshmipathi
* Components: [`test-definitions`](https://github.com/kernelci/test-definitions), [`kernelci-core/config`](https://github.com/kernelci/kernelci-core/tree/main/config)
* Services: Jenkins

### Native builds

Just like tests, kernel builds orchestrated on kerlci.org are called the
*native* KernelCI builds.

* Maintainer: `broonie`
* Components: [`kernelci-core/config`](https://github.com/kernelci/kernelci-core/tree/main/config), [`kernelci-jenkins`](https://github.com/kernelci/kernelci-jenkins)
* Services: Pipeline / Jenkins

### Bisections

For every test regression detected, an automated bisection is typically run
(with supported test lab types).  This involves building kernels, running tests
and checking their results in a coordinated way.

* Maintainer: `gtucker`
* Components: [`kernelci-core`](https://github.com/kernelci/kernelci-core),
  [`bisect.jpl`](https://github.com/kernelci/kernelci-jenkins/blob/main/jobs/bisect.jpl)
* Services: Pipeline / Jenkins

### Staging workflow

All the incoming pull requests are merged into temporary integration branches
and deployed on [staging.kernelci.org](https://staging.kernelci.org] for
testing.  This is explained in greater detail in the
[Staging](/docs/workflow/staging) section.

* Maintainers: `gtucker`, `broonie`
* Components: [`kernelci-deploy`](https://github.com/kernelci/kernelci-deploy)

### Production Deployment

The KernelCI components and services need to be regularly updated, with code
and configuration changes.  This includes typically building new kenel branches
or running new tests, as well as updating rootfs and Docker images with the
latest versions of all the packages being used.

It is currently done one a week on average, although it may become more
continuous as more services start to get hosted in the Cloud and run in Docker
containers.

* Maintainers: `gtucker`, `mgalka`
* Components: [`kernelci-deploy`](https://github.com/kernelci/kernelci-deploy)


## Channel Maintainers

### IRC

This is about keeping the `#kernelci` IRC channel updated and managing
automated notifications sent to it (monitoring services, GitHub and Jenkins
integration...)

* Maintainers: `montjoie`

### groups.io

All the KernelCI mailing lists are managed via [groups.io](https://groups.io).
This includes moderating incoming messages and new subscriptions, keeping
settings up to date and dealing with changes to the schemes for each price
plan.

* Maintainers: `broonie`, `khilman`

### Slack

The [KernelCI Slack channel](https://kernelci.slack.com) may be used as an
alternative to IRC.  However, more people are using IRC so Slack is only there
to facilitate communication when IRC is not practical.

* Maintainers: `khilman`

### kernelci.org update emails

Emails are sent regularly with a summary of the changes going into production
and minutes from the various [TSC](/docs/team/tsc) and
[board](/docs/team/board) meetings.

* Maintainers: `gtucker`

### Twitter

The [KernelCI Twitter](https://twitter.com/kernelci) account is used to engage
with public events, kernel developers and other test systems in particular.  It
is also a way for the project to quickly share updates about new features or
events.

* Maintainers: `gtucker`

### Blog

The [KernelCI blog](https://foundation.kernelci.org/blog/) is currently hosted
on the Linux Foundation project website using Wordpress.  Managing it involves
communicating with the LF when needed to make certain changes, and either
giving access to people who have a blog post to publish or publishing it
directly on their behalf.

* Maintainers: `khilman`
