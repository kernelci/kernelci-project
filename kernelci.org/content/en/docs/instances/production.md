---
title: "Production"
date: 2021-07-27T19:30:00Z
draft: false
description: "How linux.kernelci.org works"
---

The main dashboard on [linux.kernelci.org](https://linux.kernelci.org) shows
all the results for the [native tests](../../tests) run by KernelCI with
upstream kernels.  It is updated typically once a week with all the changes
that have been merged in the various components: [core tools](https://github.com/kernelci/kernelci-core), [YAML configuration](https://github.com/kernelci/kernelci-core/tree/main/config/core), [backend](https://github.com/kernelci/kernelci-backend), [frontend](https://github.com/kernelci/kernelci-frontend), [Jenkins](https://github.com/kernelci/kernelci-jenkins)
...

Each project has a `main` branch used for development, this is where all the
PRs are normally merged.  Then there is also a `kernelci.org` branch in each
project for production deployment.  These branches are updated every time the
production instance is updated.  All the changes should be tested on
[staging](../staging) before being merged into the `main` branches and later on
deployed in production.

The [kernelci-deploy](https://github.com/kernelci/kernelci-deploy) project
contains some tools to automate parts of the production update.  This is
gradually getting more automated but a few steps still require manual
intervention.  Updating the production instance requires having SSH access to
the main kernelci.org server.

## Update procedure

1. Release new versions

   Each component which has some changes ready to be deployed needs a new
   version tag.  This is something that respective maintainers normally do.
   They should also look if there are any PRs ready to be merged before
   creating the new version.

1. Update the kernelci-deploy checkout

   The production update uses tools in `kernelci-deploy`.  The first step is to
   update it to the latest version, which can be done with this command:

   ```sh
   ./kernelci.org checkout
   ```

1. Build new rootfs images

   Root file system (rootfs) images should be built ahead of the production
   update, so they can be tested on staging.  It can take several hours to
   build all of them, so ideally this should be a couple of days before the
   production update.  For example, with production updates usually occurring
   every Monday, the root file system images can be built every Friday to get
   tested on staging over the weekend.

   To build a new set of rootfs images:

   ```sh
   ./kernelci.org rootfs
   ```

   This will first rebuild the Docker images used to build the rootfs images,
   then trigger the rootfs image builds, and wait for them to complete.  You
   may abort while waiting for the builds to complete and resume later with
   this command:

   ```sh
   ./kernelci.org rootfs_flush
   ```

1. Flush kernel builds

   Once rootfs images have been tested and the new URLs have been merged in
   `test-configs.yaml`, the next step is to abort any pending kernel revision
   to be built in Jenkins and wait for all the ones currently in the pipeline
   to complete.  The production update needs to be done while the pipeline is
   empty to avoid glitches while multiple components are being updated.  The
   `kernelci.org` script in `kernelci-deploy` has a command to automate this
   part:

    ```sh
    ./kernelci.org pause
    ```

   This may take a while, typically 1h or so, depending on the number of kernel
   builds still pending.  The script will be monitoring the status and exit
   once completed.  It will also cancel all bisections as they can take a very
   long time to run.  Regressions that persist will cause other bisections to
   be run after the production update.

1. Restart jenkins

   Once there are no more kernel builds running in Jenkins, it should be
   restarted with the latest changes from `kernelci-jenkins` and the encrypted
   data in `kernelci-jenkins-data` (labs API tokens etc.).  This is also a good
   time for rebooting all the nodes VMs and pruning Docker resources.  Doing
   this requires SSH access to all the nodes.  There is a
   [`reboot.sh`](https://github.com/kernelci/kernelci-jenkins-data/blob/main/bot.kernelci.org/reboot.sh)
   helper script in `kernelci-jenkins-data`:

   ```sh
   ./bot.kernelci.org/reboot.sh
   ```

   There is currently no automated way to detect that Jenkins as fully
   restarted.  This is a gap to be filled in the `kernelci.org` helper script
   before the production update can be fully automated.

1. Update everything

   Once Jenkins has restarted, the `kernelci.org` script provides another
   command to automatically updated everything:

   ```sh
   ./kernelci.org update
   ```

   This does the following:

   * Checkout the `kernelci-core` repository locally with the head of the
     `kernelci.org` branch
   * Run the Jenkins DSL job to recreate all the job definitions
   * Redeploy the backend using Ansible
   * Redeploy the frontend using Ansible
   * Update the static website on kernelci.org
   * Update the [KernelCI LAVA test-definitions
     fork](https://github.com/kernelci/test-definitions) with a rebase on top
     of upstream
   * Rebuild all the kernel Docker images (toolchains, device tree validation,
     QEMU...) and push them to the Docker hub
   * Push a test revision to the [KernelCI linux
     tree](https://github.com/kernelci/linux) to run a "pipe cleaner" build
   * Start a "pipe cleaner" build trigger job in Jenkins to build the test
     kernel revision

   It should take around 30min for the test kernel builds to complete, and then
   a while longer for any tests to complete in all the labs.  The results
   should be checked manually, by comparing with previous revisions on the web
   frontend.  The number of builds and test results as well as their pass rates
   should be similar.  These builds can be seen here:

     https://linux.kernelci.org/job/kernelci/branch/kernelci.org/

   If there appear to be some issues with the results, the monitor job should
   be stopped so no new revisions will be automatically built.  Some changes
   may be reverted or a fix applied depending on the root cause of the issues.
   If the results look fine, then the monitor job will start discovering new
   kernel revisions periodically and the production update is complete.
