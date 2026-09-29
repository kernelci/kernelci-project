---
title: "Staging"
date: 2026-09-29
description: "How the staging.kernelci.org instance is deployed and maintained"
weight: 3
---

[staging.kernelci.org](https://staging.kernelci.org/) is a Maestro instance
used to test pending changes before they reach production. It is redeployed
periodically with all eligible open pull requests merged together, and it
builds and tests a small set of kernel trees mirrored into
[kernelci/linux](https://github.com/kernelci/linux).

This page describes how staging works and how to maintain it. For requesting
a user account and using the staging API, see the
[Staging API](/components/maestro/api/staging) page.

## Components

* **staging-web** ([kernelci/staging-web](https://github.com/kernelci/staging-web)):
  the staging control panel at
  [staging.kernelci.org](https://staging.kernelci.org/). It schedules and
  runs deployments ("staging runs") and shows their progress, the pull
  requests included in each run and the resulting nodes.
* **kernelci-deploy** ([kernelci/kernelci-deploy](https://github.com/kernelci/kernelci-deploy)):
  helper scripts used by staging-web, in particular `tools/kci-pending.py`
  (merges pull requests), `kernel.py` (pushes kernel branches) and
  `data/staging.ini` (list of contributors whose pull requests are deployed).
* **Staging deploy workflow** (`.github/workflows/staging.yml` in
  [kernelci/kernelci-core](https://github.com/kernelci/kernelci-core)):
  prepares the integration branches and builds the Docker images.
* **API and pipeline**: `kernelci-api` and `kernelci-pipeline` running with
  docker-compose on the staging host, deployed from their
  `staging.kernelci.org` branches.
* **Viewer**: [staging.kernelci.org:9000/viewer](https://staging.kernelci.org:9000/viewer)
  to browse the nodes produced by staging.

## Staging runs

A staging run is triggered either:

* **automatically**, at 00:00, 08:00 and 16:00 UTC. A scheduled run is
  skipped if another run is in progress or if a user triggered a run in the
  last hour;
* **manually**, from the control panel, by users with the `admin` or
  `maintainer` role.

Only one staging run can be active at a time. Each run goes through these
steps; if a step fails, the remaining steps are skipped:

1. **GitHub workflow**: triggers the staging deploy workflow in
   kernelci-core and waits for it to finish. The workflow:
   * runs `kci-pending.py` for `kernelci-core`, `kernelci-api` and
     `kernelci-pipeline`. It applies the open pull requests as patches on
     top of `main`, one after the other, and force-pushes the result to the
     `staging.kernelci.org` branch of each repository. A pull request is left out if:
     * its author is not listed in `data/staging.ini` in kernelci-deploy,
     * it has the `staging-skip` label,
     * it has not been updated for more than two weeks,
     * it doesn't apply cleanly on top of the pull requests already merged;
   * builds the Docker images from the `staging.kernelci.org` branches
     (optionally skipping the compiler images).
2. **Self update** (optional, disabled by default): updates the
   kernelci-deploy checkout on the staging host.
3. **API/pipeline update**: checks out the new `staging.kernelci.org`
   branches of kernelci-api and kernelci-pipeline, pulls the new images and
   restarts the containers.
4. **Kernel tree update**: pushes one kernel tree to kernelci/linux (see
   below).
5. **Trigger restart**: restarts the pipeline `trigger` service so the new
   kernel branch is picked up.
6. **Checkout wait**: waits up to 5 minutes for a new checkout node to
   appear in the staging API.

The control panel lists, for each run, which pull requests were applied or
skipped (and why), so it is the first place to look when a pull request is
not being tested.

## Kernel trees

Staging builds and tests three branches of
[kernelci/linux](https://github.com/kernelci/linux), each one a mirror of an
upstream tree:

| Staging branch     | Upstream tree | Upstream branch |
|--------------------|---------------|-----------------|
| `staging-next`     | [linux-next](https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git) | `master` |
| `staging-mainline` | [mainline](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git) | `master` |
| `staging-stable`   | [linux-stable](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git) | `linux-6.18.y` |

Each staging run updates one tree. When a run is triggered, the kernel tree
can be chosen:

* `auto` (used by scheduled runs): rotates through `next`, `mainline` and
  `stable`, one per run;
* `next`, `mainline` or `stable`: updates that tree only;
* `none`: does not update any kernel tree, only redeploys the API and
  pipeline.

The kernel tree update runs `kernel.py` from kernelci-deploy, which fetches
the upstream branch, adds a commit and a date-based tag (for example
`staging-stable-20260929.1`) and force-pushes the branch and tag to
kernelci/linux. The pipeline then detects the new revision and creates a
checkout node. These branches are defined as the `kernelci` tree build
configurations in
[`config/trees/kernelci.yaml`](https://github.com/kernelci/kernelci-pipeline/blob/main/config/trees/kernelci.yaml)
in kernelci-pipeline.

### Updating the stable tree

The stable tree should follow a maintained stable or longterm branch
(see [kernel.org](https://www.kernel.org/)). When the tracked branch reaches
end of life, or no longer builds with the current toolchains, move it to a
newer one:

1. On the staging host, edit the `[kernel_trees.stable]` section of
   staging-web's `config/staging.toml`:

   ```toml
   [kernel_trees.stable]
   url = "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git"
   branch = "linux-6.18.y"
   staging_branch = "staging-stable"
   tag_prefix = "staging-stable-"
   ```

2. Restart staging-web, as the configuration is only read at startup.
3. Trigger a staging run with the `stable` kernel tree from the control
   panel, or wait for the rotation to reach it.
4. Update `config/staging.toml.example` in
   [kernelci/staging-web](https://github.com/kernelci/staging-web) and the
   table above so they match the deployed configuration.

The `next` and `mainline` trees are updated in the same way, through their
`[kernel_trees.next]` and `[kernel_trees.mainline]` sections.

## Getting your pull requests on staging

* Make sure your GitHub username is listed in `data/staging.ini` in
  [kernelci-deploy](https://github.com/kernelci/kernelci-deploy); if not,
  open a pull request adding it.
* Open your pull request against `main` in kernelci-core, kernelci-api or
  kernelci-pipeline. It will be included in the next staging run.
* Add the `staging-skip` label if your pull request is not ready and might
  break staging.
* Check the control panel and the
  [viewer](https://staging.kernelci.org:9000/viewer) for results, and
  mention them in the pull request as described in the
  [contributing guidelines](/components/maestro/contrib).
