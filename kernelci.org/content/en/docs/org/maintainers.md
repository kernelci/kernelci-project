---
title: "Maintainers"
date: 2021-09-23
description: "KernelCI maintainers"
weight: 5
---

There are several types of maintainer roles with different responsibilities:

[software maintainers](#software-maintainers)
: in charge of the KernelCI software components

[service maintainers](#service-maintainers)
: in charge of the KernelCI hosted services

[feature maintainers](#feature-maintainers)
: in charge of features that span across the whole KernelCI stack

[instance maintainers](#instance-maintainers)
: in charge of a particular KernelCI instance (production, staging...)

[channel maintainers](#channel-maintainers)
: in charge of the communication channels used by KernelCI

Most maintainers are members of the [TSC](/docs/org/tsc) but additional people
can be involved too.

## Software Maintainers

At least one maintainer is assigned to each software component.  The work
involves reviewing pull requests on GitHUb, triaging issue, updating GitHub
settings and facilitating the development workflow.  Having “deputy”
maintainers whenever possible also helps with the continuity of the project
when regular maintainers are not available.

In addition to maintainers for each project, some GitHub administrators are
available to make configuration changes at the organisation level.  This
includes managing teams, permissions for each project, adding / moving /
removing projects, configurating workboards and updating any other general
settings.

* Organisation: https://github.com/kernelci
* Owners: `broonie`, `khilman`, `gtucker`, `nuclearcat`

### Project

The project repository contains the source code for the
[kernelci.org](https://kernelci.org) static website as well as some encrypted
files and other administrative documents.  Therefore it's not strictly software
but has the same requirements from a maintainer point of view.

Please note that other people not listed here might also have access to the
encrypted files for practical resons (shared account passwords, sysadmin
information etc.).

* Repository: [`kernelci-project`](https://github.com/kernelci/kernelci-project)
* Maintainers: `gtucker`, `nuclearcat`
* Deputy: `patersonc`

### Core tools

The [core tools](/docs/core) provide the command line utilities and the
`kernelci` Python package used to implement a KerneLCI pipeline and run
individual steps by hand (building kernels, scheduling tests...).

* Repository: [`kernelci-core`](https://github.com/kernelci/kernelci-core)
* Maintainers: `nuclearcat`, `jeny`
* Deputy: `alicef`

### API

The new [KernelCI API](/docs/api) is a work-in-progress replacement for the
backend currently used in production.  It also features a Pub/Sub interface to
coordinate the pipeline services in a modular fashion.

* Repository: [`kernelci-api`](https://github.com/kernelci/kernelci-api)
* Maintainers: `jeny`

### Pipeline

The [KernelCI pipeline](/docs/api/overview/#pipeline-design) is also a
work-in-progress based on the new API and its Pub/Sub interface.  This is
essentially to replace the Jenkins pipeline currently used in production.

* Repository:
  [`kernelci-pipeline`](https://github.com/kernelci/kernelci-pipeline)
* Maintainers: `jeny`

### KCIDB

[KCIDB](/docs/kcidb) provides a set of tools to submit kernel test data to a
common database.

* Main repositories: [`kcidb`](https://github.com/kernelci/kcidb),
  [`kcidb-io`](https://github.com/kernelci/kcidb-io)
* Grafana dashboard:
  [`kcidb-grafana`](https://github.com/kernelci/kcidb-grafana)
* Maintainer: `spbnick`

### lava-docker (interim)

> **Note**: The `lava-docker` repository is about to join the LAVA GitLab
> organisation.  See the [email
> discussion](https://groups.io/g/kernelci/topic/moving_lava_docker_out_of_the/93248754)
> for more details.

This project is to Simplify the installation and maintenance of a LAVA lab
using Docker containers.

* Repository: [`lava-docker`](https://github.com/kernelci/lava-docker)
* Maintainers: `alicef`, `montjoie`

## Service maintainers

Services hosted by KernelCI all need someone to look after them and ensure they
stay online and available.  This is essentially sysadmin work with some code
maintannce too depending on the cases.

### Kubernetes

Several Kubernetes clusters are used by KernelCI, to build kernels and run
platform-independent tasks or kernel tests in containers (static analysis,
KUnit, QEMU...).

* Maintainers: `khilman`, `broonie`
* Resources: Azure, GCE

### VM Servers

A number of virtual machine servers are being used to host various services
such as Jenkins and the web frontend.  They are currently all managed in Azure,
but this may evolve over time.  They require sysadmin maintenance, monitoring
tools, backups...

* Maintainers: `nuclearcat`
* Resources: Azure (VMs, Mongo DB)

### BigQuery

KCIDB uses BigQuery as a database engine.  This requires setting up tokens and
managing the associated Cloud resources.

* Maintainers: `spbnick`, `khilman`
* Resources: BigQuery, GCE

### Grafana

KCIDB uses a [Grafana](https://kcidb.kernelci.org) instance as a prototype web
dashboard.  Additional instances may be set up for other use-cases, such as
showing statistics about the KernelCI project in general.

* Maintainers: `spbnick`
* Resources: VM Servers

### Docker Hub

All the Docker images used by KernelCI are pushed to the [Docker
Hub](https://hub.docker.com/).  This requires some maintenance in particular to
keep an eye on resource usage and to adjust permissions.

* Maintainers: `gtucker`, `nuclearcat`

## Feature maintainers

Some advanced KernelCI features involve coordination between multiple software
components and services.  They also require dedicated maintainers to ensure
they keep running as intended.

### Native tests

Tests orchestrated on kernelci.org are called the *native* KernelCI tests,
unlike tests running in independent CI systems which provide results directly
to KCIDB.  This covers integration with test labs, rootfs images, pipeline
configuration... anything related to running those tests and getting their
results into the database.

* Maintainers: `nuclearcat`
* Components:
  [`test-definitions`](https://github.com/kernelci/test-definitions),
  [`bootrr`](https://github.com/kernelci/bootrr),
  [`buildroot`](https://github.com/kernelci/buildroot),
  [`kernelci-core/config`](https://github.com/kernelci/kernelci-core/tree/main/config)
* Services: Jenkins

### Native builds

Just like tests, kernel builds orchestrated on kernelci.org are called the
*native* KernelCI builds.

* Maintainers: `broonie`, `nuclearcat`
* Components:
  [`kernelci-core/config`](https://github.com/kernelci/kernelci-core/tree/main/config),
  [`kernelci-jenkins`](https://github.com/kernelci/kernelci-jenkins)
* Services: Pipeline / Jenkins, Kubernetes

### Bisections

For every test regression detected, an automated bisection is run whenever
possible.  This involves building kernels, running tests and checking their
results in a coordinated way to then send an email report when the bisection
succeeds.

* Maintainers: `gtucker`
* Components: [`kernelci-core`](https://github.com/kernelci/kernelci-core),
  [`bisect.jpl`](https://github.com/kernelci/kernelci-jenkins/blob/main/jobs/bisect.jpl)
* Services: Pipeline / Jenkins

## Instance maintainers

As there are several KernelCI instances, it's necessary to have people
dedicated to each of them.

> ToDo: Update with new API & Pipeline deployments as they become available.

## Channel Maintainers

As with any open-source project, ensuring communication between all the
contributors, users and maintainers is essential.  Several channels are
available for KernelCI and each of them requires some maintenance too.

### IRC

This is about keeping the `#kernelci` IRC channel on libera.chat updated and
managing automated notifications sent to it (monitoring services, GitHub and
Jenkins integration...)

* Maintainers: `montjoie`

### groups.io

All the KernelCI mailing lists are managed via [groups.io](https://groups.io).
Maintaining them includes moderating incoming messages and new subscriptions,
keeping settings up-to-date and dealing with changes to the schemes for each
price plan.

* Maintainers: `broonie`, `khilman`, `padovan`

### Slack

The [KernelCI Slack channel](https://kernelci.slack.com) may be used as an
alternative to IRC.  However, more people are using IRC so Slack is only there
to facilitate communication when IRC is not practical.

* Maintainers: `khilman`, `spbnick`, `gtucker`

### Twitter

The [KernelCI Twitter](https://twitter.com/kernelci) account is used to engage
with a wider public audience: events, kernel developers, other test systems...
It is also a way for the project to quickly share updates about the project's
news and, achievements.

* Maintainers: `gtucker`, `padovan`

### kernelci.org update emails (paused)

Emails are sent regularly with a summary of the changes going into production
and minutes from the various [TSC](/docs/org/tsc) and
[board](/docs/org/board) meetings.

* Maintainers: `gtucker`
