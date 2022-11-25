---
title: "Technical Steering Committee"
date: 2021-11-10
description: "KernelCI core developers and maintainers"
weight: 3
aliases:
  - "/docs/team/tsc"
---

The Technical Steering Committee (TSC) is a team of people who are responsible
for keeping the KernelCI project in a good shape and driving its development.
The [rules](#rules) are based on the LF [project
charter](/files/KernelCI_Project_Technical_Charter_20181107.pdf).  Typically,
major contributors eventually become members and those who have stopped
contributing for an extended period of time may be removed.

## Members

As of today, the committee is composed of the members listed below with their
respective email address and IRC nicknames:

* [Kevin Hilman](mailto:<khilman@baylibre.com>) - `khilman`
* [Mark Brown](mailto:<broonie@kernel.org>) - `broonie`
* [Guillaume Tucker](mailto:<guillaume.tucker@collabora.com>) - `gtucker`
* [Corentin Labbe](mailto:<clabbe@baylibre.com>) - `montjoie`
* [Nikolai Kondrashov](mailto:<spbnick@gmail.com>) - `spbnick`
* [Michał Gałka](mailto:<michal.galka@collabora.com>) - `mgalka`
* [Alexandra Pereira](mailto:<alexandra.pereira@collabora.com>) - `apereira`
* [Alice Ferrazzi](mailto:<alice.ferrazzi@miraclelinux.com>) - `alicef`
* [Denys Fedoryshchenko](mailto:<denys.f@collabora.com>) - `nuclearcat`

## Communication

For general discussions, the usual IRC channel `#kernelci` on libera.chat and
the [`kernelci@lists.linux.dev`](mailto:<kernelci@lists.linux.dev>) mailing
list can be used.  To contact only the TSC members directly, the
[`kernelci-tsc@groups.io`](mailto:<kernelci-tsc@groups.io>) private list may be
used instead.

The TSC also meet monthly online to discuss current topics and make decisions
including votes when necessary.

## Rules

### Votes

As per paragraph *3.a TSC Voting* of the [project
charter](/files/KernelCI_Project_Technical_Charter_20181107.pdf):

> While the Project aims to operate as a consensus based community, if any TSC
> decision requires a vote to move the Project forward, the voting members of
> the TSC will vote on a one vote per voting member basis.

Decisions that always require a vote are:
* adding or removing TSC members
* making changes to the TSC rules
* granting or removing any kind of admin rights to individuals
* making proposals to the LF project board

The result of each vote should be shared on the mailing list and kept in an
archive.  It should also include the date when any related changes were
enacted.  As such they provide a way to keep a formal trace of decisions being
made.

> *Note* The archiving process for TSC votes hasn't been formalised yet.  Past
> votes should be retroactively archived when this has been put in place.  They
> should appear in a sub-section of this documentation section.

Votes done during a live meeting require 50% of the TSC members to be voting
and a majority among these voting members.  Votes done by email or any other
deferred channel require a majority among all of the TSC members.

### Members

Current members of the TSC may propose to vote for new people to be added or
removed.  This should prevent a single organisation from taking over the TSC.
People to be considered as new TSC members should have typically played an
important role for a significant amount of time in the project.  There is
however no strict requirement, the only condition is the outcome of the TSC
vote.

Likewise, members of the TSC may propose that a member be removed which should
result in a vote.  Members who have not been active for over a year should be
notified and considered for removal from TSC in order to keep the list
up-to-date with the reality of the project.  Active members are typically
expected to:

* attend TSC meetings (monthly)
* participate in votes
* make sustained contributions to the project, such as:
  * contributing to the code
  * doing code reviews
  * sharing experience and contributing ideas for solving technical issues
  * helping keep the services working
  * writing documentation or creating any content that promotes the project

This list is not exhaustive, in the end it's up to the TSC to vote and judge
whether a member should be removed due to inactivity.  Members who commit acts
that pose a threat to the stability of the project may also be removed
following a TSC vote.
