---
date: 2023-07-28
title: "API Transition Timeline"
linkTitle: "API Transition Timeline"
author: Guillaume Tucker
description: >
  Timeline for transitioning to the new KernelCI API & Pipeline
---

Once upon a time, on a Thursday afternoon somewhere in Italy, a KernelCI
backend API was created:

```
commit 08c9b0879ebe81463e124308192670c0e7447e0b
Author: Milo Casagrande <milo@ubuntu.com>
Date:   Thu Feb 20 16:10:41 2014 +0100

    First commit.
```

As you can see, it was nearly 10 years ago.  How much does that represent in
the modern software world?  Of course, it depends.  The Linux kernel is much
older, still written in C and still going strong.  But in most cases, including
this particular one, it means a whole new world.  The old API was written in
Python 2.7 which stopped being maintained as a language on 1st January 2020.
We could have just rewritten it in Python 3, which was the initial thought.
But in the meantime, KernelCI was also growing as a project.  It wasn't just
about building ARM kernels and doing boot testing on embedded dev boards any
more.  It had become a Linux Foundation project aiming to test the whole
upstream kernel.

## What is this new API?

Following this move, an increasing number of people became interested as it got
under the spotlight.  That is when we started to realise that the architecture
needed to fundamentally evolve in order to match the scale of the new mission
it had been assigned.  The Linux kernel is a vast and complex open-source
project with a unique ecosystem.  As such, it requires some unique tooling too.
We all know that [Git](https://git-scm.com/) was initially created out of a
need to manage all the kernel patches.  Now KernelCI needs an automated testing
tool tailor-made to its unique requirements - and that's why we're finally
launching the new API & Pipeline.

It comes with lots of improvements and it's still a work-in-progress.  We'll
keep publishing blog posts and update the documentation as things evolve over
the next few months.  Right now we have a pipeline that can monitor Git
repositories for new revisions, take a snapshot of the kernel source tree in a
tarball, run KUnit with it as well as an x86 kernel build and smoke test it in
QEMU.  It can then also send a summary email and detect regressions.  That's
basically enough to prove we have a workable system.  Nothing too
groundbreaking there, you might think.  So, what's all the fuss about?

In a nutshell: a Pub/Sub interface to orchestrate distributed client-side
services that can be run anywhere.  You could have your own too at home.  Also:
user accounts so you can keep your own personal test data there, an abstraction
for runtime environments so jobs can be run seamlessly in Docker, Kubernetes, a
local shell, LAVA, [insert your own system here]... a new `kci` command line
tool to rule them all and a unified Node schema to contain all the test data
(revision, build, runtime test, regression...) in a tree.  But again, we'll go
through all that later in more detail.  It's all based on requirements gathered
from the community over the past few years.

## Timeline

The main message in this blog post is the timeline for retiring the old system
and getting the new API in production.  Here's the proposal:

Early Access
: Monday 4th September 2023

Production Deployment
: Monday 4th December 2023

Legacy System Deprecation
: Monday 4th March 2024

Legacy System Sunset
: Monday 4th November 2024

It only takes four Monday-the-Forth milestones to get through all this.  Here's
what they mean:

### Early Access

This is when a new API & Pipeline instance becomes available to let the public
experiment with it.  It can be seen as some form of beta-testing.  It will be
deployed in the Cloud to evaluate how a real production instance would behave,
but it's only kept online as a best effort.  There should be frequent updates
as the code evolves, probably at least weekly and at most daily.  Only changes
that made it through early testing on the staging instance should be deployed
so it's meant to be reasonably stable.

### Production Deployment

The plan is to build upon the experience learned from the Early Access
deployment to prepare a persistent instance that would eventually become the
production one.  Data should be carefully kept and backed up, changes in the
database schema should go through managed migrations and the API code should be
deployed from tagged releases.  As soon as this has become reliable enough we
might shut down the Early Access instance since it should have become redundant
by then.

### Legacy System Deprecation

In other words, this is when the new API & Pipeline production instance becomes
the official main KernelCI instance.  We'll first be going through a transition
phase to ramp up the build and test coverage on the new API while equally
reducing the load on the legacy system to avoid overloading the shared
infrastructure.  Ideally, coverage should have reached 80% on the new API and
20% on the old one by this date.

### Legacy System Sunset

After being deprecated, the legacy system will keep running with a bare minimal
amount of coverage just to facilitate the transition for users who depended the
most on it.  It will be definitely shut down and the data will be archived when
finally reaching the Sunset milestone.

## Stay tuned

These dates have been identified as realistic targets for having the new API
rolled out and retiring the old one with a transition in between.  We'll be
aiming to have the new API in place _by_ these dates and conversely retire the
legacy system _no sooner than_ announced here.

In the meantime, we'll be posting updates as these milestones get reached or if
any alterations need to be managed.  We'll also clarify how to use the API and
exactly what features become available alongside the main
[documentation](/api).  Please share with us any feedback you may have, if
you need some clarifications or to raise any concerns.  The best way to do this
is via the [mailing list](mailto:kernelci@lists.linux.dev) as always.  Stay
tuned!
