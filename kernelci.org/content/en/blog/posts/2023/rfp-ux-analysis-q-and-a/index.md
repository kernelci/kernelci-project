---
date: 2023-07-20
title: "Request for Proposals: UX Analysis 2023 - Q&A"
linkTitle: "RFP: UX Analysis 2023 Q&A"
author: Guillaume Tucker
description: >
  Questions and Answers collected for the UX Analysis RFP
---

Following the [UX Analysis RFP](/blog/posts/2023/rfp-ux-analysis/), we've
received a number of questions which seem worth sharing publicly in order to
equally benefit all the proposals we receive.

## Big Picture

### What are your organization's most important broader goals with this new dashboard?

We've identified a requirement to have a web dashboard in a [community
survey](/blog/posts/2020/07/09/) we did a couple of years ago.  It's mostly
about providing Linux kernel developers with the information they need to
facilitate their daily workflows, and also other types of users for example if
they're basing their products on the upstream kernel and need to monitor its
quality.

### What are biggest issues or problems you're having with your current system that prompted this UX Analysis RFP?

We currently have a very [old web dashboard](https://linux.kernelci.org/job/)
with an associated backend that can't be maintained any more.  On top of that,
the project has been growing and we're now redesigning the whole approach to be
able to better scale with a new API which doesn't have any actual web dashboard
right now.

### What factors made your team decide to release an RFP for this project?

None of the KernelCI LF project members had enough in-house expertise.  Also,
looking for an independent external supplier appeared as an appropriate choice
in this case.

### Is there an incumbent bidder on this project?

No, this is the first RFP we do about UX Analysis and web development in
general.

### How will vendors be evaluated and scored?

We will come up with some criteria as a basic comparison method, then each
member of the advisory board will look at all the proposals and we'll discuss
it and eventually hold a vote.  We may also inquire further with some vendors
if needed.

### How many rounds of revisions and how many UX flows are you expecting as part of this project?

This is very hard to predict as we're still in the early design stages.  There
should probably be a small number both of revisions and flows (e.g. 2 or 3),
maybe later we would be dealing with incremental changes resulting in more
revisions as part of the full implementation efforts.

### Do you have a preference regarding the vendor's location?

No, there is no preference over the country where the vendor is located.  The
KernelCI project's team is remotely distributed around the world.


## Content

### Would you need any copywriting or content migration services?

None that we're currently aware of.

### Would you need any original or stock videography or photography?

Not with the UX Analysis phase.  We might need some original content for a
final website in production.

### How much content do you currently have on your website?

Our static websites have tens of pages.  Our current dynamic web dashboard has
millions of entries, and this is what we're expecting to see covered by the UX
Analysis.  Some static content may be part of the interactive web dashboard but
it's not the primary goal.

### Is there a CMS that you have a preference for over the other?

No, however we do have an API for storing our data.  How this is turned into a
UX and web dashboard is up to the vendor to decide as part of the proposal.

### What CMS platform do you use currently?

For some static websites we use WordPress and Hugo, but this UX Analysis work
is for an interactive web dashboard.  We don't have any particular CMS
requirements for it.


## Requirements

### Would you require hosting, dns or ssl services?

No, the KernelCI project can take care of this.

### How much initial research has been done as part of this RFP?

A lot of research has been done in the past few years to try and understand
what the public and users need.  What's missing is how this may translate into
an actual UX.  We now have some ideas about "what" we need but not "how" users
can have it.

### Are there any factors driving the timeline for the completion of the work?

We're developing a new API which will be used hand-in-hand with the web
dashboard.  The timeline isn't set in stone but having a prototype dashboard or
basic demo around the end of September would be great.  We're thinking of
having the new API in production in the first half of 2024 so it would be good
to see the web dashboard getting finalised around that time too.

### Can you give us a high-level overview of the demographics of each persona from the user stories?

* "Someone who cares about the kernel" can be literally anyone, from a student
  to a high-profile maintainer or developer.  The only real criteria is that
  they need to know about the upstream kernel code quality.  There may be a
  million people in this category.
* "Kernel / subsystem maintainer" are a relatively small set of people in
  charge of accepting changes into the kernel.  They form some sort of pyramid
  of trust with several maintainers sending their collected changes to a common
  maintainer etc.  Like any kernel contributors, they are located around the
  world and have various levels of experience.  There's maybe about 100
  subsystem maintainers and 1000 maintainers responsible for smaller areas of
  the code.

### Do you have examples of the email reports that are sent with summaries of test results?

* Here's a particular one about a bisection result which found a commit that
  caused some test to fail:<br />
  https://lore.kernel.org/all/Y%2Fi1tX6th2I8hY0o@sirena.org.uk/
* Here's the full archive with all the email reports we're currently
  sending:<br /> https://groups.io/g/kernelci-results/topics
* Here's also a KCIDB email report, which collects results from other test
  systems into a single report:<br />
  https://groups.io/g/kernelci-results-staging/message/48385

### Are the test results currently stored in a database that the new web dashboard will visualize?

Yes, the new API has an [auto-generated
documentation](https://staging.kernelci.org:9000/latest/docs) with OpenAPI
description.  This is still a staging instance for experiments, we're planning
to roll out a production-like instance in the coming weeks and start refining
the schema.  Basically, all the test data is contained in a tree of Node
objects.  The underlying engine is MongoDB, and we're looking into using Atlas
for this.  The API also features a Pub/Sub interface for events that trigger
different stages of the testing pipeline on the client side.

The [KCIDB](https://kernelci.org/docs/kcidb/) database has a different schema,
but the web dashboard wouldn't necessarily need to read data from both sources.
That's something we still need to define, there are several ways to solve this.
It's also something which might depend on the outcome of the UX Analysis.
There's already an interim web dashboard for KCIDB based on
[Grafana](https://kcidb.kernelci.org/).
