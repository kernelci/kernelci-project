---
date: 2023-09-04
title: "KernelCI API Early Access"
linkTitle: "KernelCI API Early Access"
author: Guillaume Tucker
description: >
  Early Access phase of the KernelCI API & Pipeline transition timeline
---

## Free for all

Today is the beginning of the Early Access phase for the new KernelCI API.  As
explained briefly in the [previous blog
post](https://kernelci.org/blog/posts/2023/api-timeline/), this is to give
everyone a chance to create a user account and start using the API for
beta-testing purposes.  There's now an [Early
Access](https://kernelci.org/docs/api/early-access/) documentation page with a
quick guide to get started, so please go take a look there and start taking
part.

## A work in progress

Although the fundamental principles of the API & Pipeline have now settled a
bit, it is still under active development.  In particular, we're expecting to
see a fair amount of changes in these areas:

### `kci` command line tool

It's still very new and only provides some basic features, so now it needs some
proper design.  For example, new commands should be added and it might become
more human-readable with things like `kci find node` rather than `kci node
find`.

### Build and test coverage

This can only grow as right now there's only KUnit, one x86 build and one QEMU
smoke test run for each kernel revision (and only from mainline).  Starting to
scale this up will help tackle the main bottlenecks and performance issues in
the infrastructure before reaching production quality.

### Documentation

Yes, now that things are shaping up we should also be taking good care of the
overall documentation and general ease of use of the project.  This should also
encompass things such as moderation rules to ensure continuity of the project.

## A two-way process

This system is made for you, all the members of the wider Linux kernel
ecosystem.  So while there's a small but growing team of developers still
typing away all the code needed to make it happen, we need your feedback to
help shape things up in such a way that it actually delivers on its
expectations.

Please experiment as much as you like and share your stories, thoughts and
questions via the project's usual communication channels.  Also feel free to
create issues on GitHub and send pull requests of course.

**Happy beta-testing!**
