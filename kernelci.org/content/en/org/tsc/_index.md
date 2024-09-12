---
title: "Technical Steering Committee"
date: 2024-03-18
description: "KernelCI core developers and maintainers"
weight: 3
aliases:
  - "/team/tsc"
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
* [Guillaume Tucker](mailto:<gtucker@gtucker.io>) - `gtucker`
* [Nikolai Kondrashov](mailto:<spbnick@gmail.com>) - `spbnick`
* [Michał Gałka](mailto:<galka.michal@gmail.com>) - `mgalka`
* [Arisu Tachibana](mailto:<arisu.tachibana@miraclelinux.com>) - `arisut`
* [Denys Fedoryshchenko](mailto:<denys.f@collabora.com>) - `nuclearcat`
* [Jeny Sadadia](mailto:jeny.sadadia@collabora.com) - `jenysadadia`
* [Paweł Wieczorek](mailto:pawiecz@collabora.com) - `pawiecz`
* [Shuah Khan](mailto:skhan@linuxfoundation.org) - `shuah`

## Communication

For general discussions, the usual IRC channel `#kernelci` on libera.chat and
the [`kernelci@lists.linux.dev`](mailto:<kernelci@lists.linux.dev>) mailing
list can be used.  To contact only the TSC members directly, the
[`kernelci-tsc@groups.io`](mailto:<kernelci-tsc@groups.io>) private list may be
used instead.

The TSC also meet monthly online to discuss current topics and make decisions
including votes when necessary.  See the [Meetings
section](/org/#technical-steering-committee) for more details.

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

Votes are made on motions with a yes/no choice and have to be proposed by a TSC
member.  The result of each vote should be shared on the mailing list and added
to the [voting records](votes).  It should also include the date when any
related changes are enacted.  As such they provide a way to keep a formal trace
of decisions being made.

**Votes done during a live meeting** require a quorum of 50% of the TSC members
to be present in the meeting and a majority of "yes" votes among these voting
members to move the motion. However, to make sure that everyone has a say,
voting in a meeting should preferably be done only when at least 90% of the
members are in attendance.

**Votes done by email** or any other deferred channel require a majority among
all of the TSC members as everyone is expected to be able to take part.  Votes
by email expire after a period of two weeks: the motion will be rejected if a
majority of "yes" votes from the whole TSC hasn't been reached by then.

Because our members are spread across the world, and normally cannot attend a
meeting all at once, the preferred approach is to vote by email.

Abstentions are not counted as votes.  Effectively, they are the same as not
attending a meeting or not replying to an email.  For example, with 7 TSC
members in a meeting, if 3 are abstaining, 3 vote "yes" and 1 votes "no", we
have quorum as 4/7 are voting and a majority as 3/4 voted "yes" - and the
motion is moved.

### Members

Current members of the TSC may propose to vote for new people to be added or
removed.  This should prevent a single organisation from taking over the TSC.
People to be considered as new TSC members should have typically played an
important role for a significant amount of time in the project.  There is
however no strict requirement, the only condition is the outcome of the TSC
vote.

Likewise, members of the TSC may propose that a member be removed which should
result in a motion and a vote.  Members who have not been active for over a
year should be notified and considered for removal from TSC in order to keep
the list up-to-date with the reality of the project.

The criteria for removing a member aren't strictly defined either, in the end
it's up to the TSC to vote and judge whether a member should be removed due to
inactivity.  Members who commit acts that pose a threat to the stability of the
project may also be removed following a TSC vote.

### Duties

Each TSC member is responsible for taking part in making important technical
decisions.  As members are ideally also maintainers or active developers, it
makes sense to have a committee to discuss the general roadmap or design
principles to ensure cohesion within the project.  It should become a natural
progression when new members join the TSC to facilitate coordination with
others who have been involved for a long time.

In practice, active members are typically expected to:

* attend TSC meetings (monthly)
* participate in votes
* make sustained contributions to the project, such as:
  * contributing to the code
  * doing code reviews
  * sharing experience and contributing ideas for solving technical issues
  * helping keep the services working
  * writing documentation or creating any content that promotes the project
