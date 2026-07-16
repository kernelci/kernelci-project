---
title: "KCIDB"
date: 2026-07-16
description: "KCIDB - The common database for kernel test results"
weight: 3
---

KCIDB is the common results database of the KernelCI ecosystem. CI systems
that build and test the Linux kernel — including KernelCI's own
[Maestro](/components/maestro), Red Hat CKI, Google syzbot and others — send
their results here in a unified format, so the community gets one place to
look at them: the [Web Dashboard](https://dashboard.kernelci.org/).

## How it works

The current KCIDB service is implemented by
[kcidb-ng](https://github.com/kernelci/kcidb-ng) and consists of a few simple
pieces:

* **REST API** (`kcidb-restd-rs`) — receives your submissions over HTTPS,
  authenticated with JWT tokens.
* **Ingester** — validates each submission against the
  [KCIDB schema](https://github.com/kernelci/kcidb-io) and loads it into a
  PostgreSQL database.
* **LogSpec worker** — analyzes logs of failed builds and tests to
  automatically identify issues and create incidents.

Once your data is ingested, it shows up on the
[Web Dashboard](https://dashboard.kernelci.org/) and is available to tools
like [kci-dev](https://kci.dev/).

> **Note:** KCIDB used to be built on Google Cloud services (Pub/Sub and
> BigQuery) with a Grafana dashboard. That setup has been replaced by the
> kcidb-ng REST API described here.

## Submitting results

Want to contribute results from your CI system? Great, we'd love to have
them! See the [submitter guide](submitting) — it only takes a JSON file and
a `curl` command.

## Self-hosting

KCIDB-ng can also be deployed on your own infrastructure, together with the
Web Dashboard if you like. See the
[self-hosted KernelCI documentation](/components/devops/#kcidb-ng-deployment).
