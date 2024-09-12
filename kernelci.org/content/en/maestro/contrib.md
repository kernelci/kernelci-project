---
title: "Contributing Guidelines"
date: 2024-09-12T16:33:00Z
draft: false
weight: 2
---

KernelCI core project is open for contributions. Contributions may consist of
adding new builds, tests and device types as well as features and bugfixes for
KernelCI core tools.
When the PR is created, the [KernelCI staging](https://kernelci.org/docs/instances/staging)
instance takes care of updating the [staging.kernelci.org branch](https://github.com/kernelci/kernelci-core/tree/staging.kernelci.org).
In general the branch is updated every 8h and a limited set of builds and tests
are run on it.

There are several guidelines which can facilitate the PR review process:

1. Make sure the PR is well described
   1. Describe the purpose of the changes
   2. Example use cases are welcome
2. Attach staging build/test results when possible.
   1. If the PR is expected to produce build/test results
   check [staging viewer](https://staging.kernelci.org:9000/viewer) and make sure these are mentioned in the PR comment
      1. Build artifacts including logs are not kept permanently, so it's generally recommended to put them in a place that'd make them last if you want them to be part of the PR. Good way to do that seem to be:
         * Putting important information such as log fragments in the PR comments
         * Using services like [pastebin](https://pastebin.com/) to store data important for the PR (e.g. full logs) and pasting the links.
   2. If the results are not visible on staging and you think they should be, mention it in the comments, too
   3. If there is specific way to verify PR is working as expected, mention it in the comments
3. Make sure that reviewers' comments and questions are addressed
   1. When there are comments unanswered for more than 1 month the PR will be closed
4. In case there is a need to consult the PR with KernelCI maintainers join the [open hours](https://docs.kernelci.org/org/#open-hours)
5. Should you need help, you can reach KernelCI [maintainers](/org/maintainers/) or the community on the [KernelCI website](https://kernelci.org/community-contact/)
