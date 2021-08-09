---
title: "Staging"
date: 2021-07-22T08:30:00Z
draft: false
description: "How staging.kernelci.org works"
---

While the production instance is hosted on
[linux.kernelci.org](https://linux.kernelci.org), another independent instance
is hosted on [staging.kernelci.org](https://staging.kernelci.org).  This is
where all the changes to the KernelCI code and configuration get tested before
getting merged and deployed in production.  It consists of a Jenkins instance
on [bot.staging.kernelci.org](https://bot.staging.kernelci.org), a Mongo
database with a
[`kernelci-backend`](https://github.com/kernelci/kernelci-backend) instance and
a [`kernelci-frontend`](https://github.com/kernelci/kernelci-frontend) instance
for the web dashboard.

Jobs are run every 8h on staging, using all the code from open pull requests on
GitHub.  The kernel revisions being tested are rotating between mainline,
stable and linux-next.  An extra commit and a staging tag is created on top of
each branch to artifically create a new revision in the [KernelCI kernel
tree](https://github.com/kernelci/linux) even if there was no changes upstream,
to ensure that jobs are run with a separate set of results.  A reduced set of
build configurations is used to limit the resources used on staging and to get
results quicker.

There is also a plain mainline build every day, and a full linux-next build
every Friday to at least have some complete coverage and potentially catch
issues that can't be seen with the reduced number of configs in staging builds.

## GitHub pull requests

A special feature of the staging instance is the ability to test code from open
GitHub pull requests before they get merged.  This is handled by tools in the
[`kernelci-deploy`](https://github.com/kernelci/kernelci-deploy) project, to
pull all the open pull requests for a given project, apply some arbitrary
patches and push a resulting `staging.kernelci.org` branch back to the
repository with a tag.  This branch is being replaced (force-pushed) every time
the tool is run.

Things to note:

* Pull requests are only merged from users that are on a trusted list, stored
  in the `kernelci-deploy` configuration files.
* Pull requests are merged in chronological order, so older ones take
  precedence.
* Pull requests that fail to merge are ignored and will not be tested.
* Pull requests will be skipped and not merged if they have the `staging-skip`
  label set.
* If any patch from `kernelci-deploy` doesn't apply, the resulting branch is
  not pushed.  It is required that all the patches always apply since some of
  them are necessary to adjust the staging behaviour (say, to not send
  bisection email reports).  They will need to get updated if they conflict
  with pending PRs.
* A tag is created with the current date and pushed with the branch.


## Jenkins: bot.staging.kernelci.org

The staging instance is running Jenkins, just like production.  The main
difference is that the staging one is publicly visible, read-only for anonymous
users: [bot.staging.kernelci.org](https://bot.staging.kernelci.org/)

This allows for the job logs to be inspected.  Also, some developers have a
personal folder there to run modified versions of the Jenkins job but still
using the available resources (builders, API tokens to submit jobs in test
labs...).


## Run every 8h

There is a timer on the staging.kernelci.org server which starts a job every
8h, so 3 times per day.  The job does the following:

1. update [staging branch for `kernelci-jenkins`](https://github.com/kernelci/kernelci-jenkins/tree/staging.kernelci.org)
1. recreate Jenkins jobs by running the job-dsl "seed" job
1. update [staging branch for `kernelci-core`](https://github.com/kernelci/kernelci-core/tree/staging.kernelci.org)
1. update [staging branch for `kernelci-backend`](https://github.com/kernelci/kernelci-backend/tree/staging.kernelci.org)
1. update the `kernelci-backend` service using Ansible from [`kernelci-backend-config`](https://github.com/kernelci/kernelci-backend-config) with the staging branch
1. update [staging branch for `kernelci-frontend`](https://github.com/kernelci/kernelci-frontend/tree/staging.kernelci.org)
1. update the `kernelci-frontend` service using Ansible from [`kernelci-frontend-config`](https://github.com/kernelci/kernelci-frontend-config) with the staging branch
1. create and push a `staging.kernelci.org` branch with a tag to the [KernelCI
   kernel repo](https://github.com/kernelci/linux)
1. trigger a monitor job in Jenkins with the [`kernelci_staging`](https://github.com/kernelci/kernelci-core/blob/staging.kernelci.org/config/core/build-configs.yaml#L836) config

The last step should cause the monitor job to detect that the staging kernel
branch has been updated, and run a kernel build trigger job which in turn will
cause tests to be run.  Builds and test results will be sent to the staging
backend instance, and results will be available on the staging web dashboard.
Regressions will cause bisections to be run on the staging instance, and
results to be sent to the
[`kernelci-results-staging@groups.io`](https://groups.io/g/kernelci-results-staging)
mailing list.
