---
title: "Maestro"
date: 2024-05-29
description: "Maestro API and Pipeline"
weight: 2
---

## API Overview

The Maestro API is a server-side service which provides two main features: a
database abstraction and a publisher / subscriber interface.  Another important
concept is the fact that users own the data they send to the API.  Let's have a
quick look at how this all fits together.

### Database Abstraction

All the data managed by Maestro is stored in a MongoDB database using node
objects.  These can contain data about any part of the testing hierarchy such
as a kernel revision, a build, static test results, runtime functional tests,
regressions etc.  Each node has a parent so they form a simple tree.  There is
typically one root node for each kernel revision with lots of child nodes
containing all the test data that relates to it.

Each node object also has a state which can be used when orchestrating the
pipeline.  For example, a node will be in the Running state while awaiting some
results.  There's also a result value, to tell whether the related pipeline
step that produced the node passed or failed.  Finally there's a list of
artifacts with URLs to know where to find all the related files (binaries,
logs, generated results etc.).

> **Note:** The API doesn't manage storage, the only requirement is to provide
> publicly-available HTTP(S) URLs for each artifact.

### Publisher / Subscriber Interface

Every time some data changes in the database, basically every time a node
has been added or updated, an event is sent on the Publisher / Subscriber
interface (Pub/Sub).  For example, when a new kernel revision is found and a
new node is created for it, an event will be sent to tell subscribers about it
with something like "A checkout node has been created for kernel revision
v6.2-rc4".  The actual event is a [CloudEvents](https://cloudevents.io) object
with some JSON data containing a subset of the corresponding node database
entry.

Any client code can subscribe to receive events with an API token and implement
features based on how to handle these events.  The API generates events
automatically whenever nodes are changing but clients may also use the
interface to publish their own events and coordinate other parts of the
pipeline too.

### User Ownership

Interacting with the API requires a token which is associated with a particular
user.  Whenever a user sends some data such as a new node, it is owned by that
user.  While all nodes are publicly readable, only the owner of the node can
update it.  Users can also belong to groups to share data with other users.

While the main KernelCI pipeline will be creating nodes with users from a
particular `kernelci.org` group, all the other users can create their own data
which will coexist in the database.  Then your own nodes can have parents
created by users.  For example, you may submit test results that relate to a
kernel build provided by KernelCI.

## Pipeline

The Pipeline is made up of all the client-side services that run the actual
workloads that produces data and artifacts.  It's orchestrated based on events
from the Pub/Sub interface and all the data is managed via the API.  For
example, the pipeline is responsible for detecting new kernel revision,
scheduling builds and tests, sending email reports and detecting regressions.
However, any other service which has an API token is in fact part of the
extended pipeline too.

Pipeline services are also responsible for uploading various kinds of artifacts
to some independent storage services and provide public URLs to access them.
Artifacts typically include kernel source code tarballs, build artifacts, logs
and test results in some raw format before they were submitted to the API.

## Instances

### Staging

An instance has been set up on `staging.kernelci.org` for testing all pending
changes.  The Docker logs are available in real-time via a [web
interface](https://staging.kernelci.org:9088/) for both the API and the
pipeline.  It also provides some [interactive API
documentation](https://staging.kernelci.org:9000/latest/docs).  This instance
is not stable, it's redeployed periodically with all open pull requests from
GitHub merged together on a test integration branch.
Please check [docs](/maestro/api/staging) for more details.

### Production

Production instance has been deployed in the Cloud (AKS)
on `api.kernelci.org`. This is stable instance and is being updated weekly (usually on Mondays).