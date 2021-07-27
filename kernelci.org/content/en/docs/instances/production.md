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

1. Flush kernel builds

   The production update uses tools in `kernelci-deploy`.  The first step is to
   update it to the latest version, which can be done with this command:

   ```sh
   ./kernelci.org checkout
   ```

   The next step is to abort any pending kernel revision to be built in
   Jenkins, and wait for all the ones currently in the pipeline to complete.
   The production update needs to be done while the pieline is empty to avoid
   glitches while multiple components are being updated.  The `kernelci.org`
   script in `kernelci-deploy` has a command to automate this part:

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
   * Rebuild the Docker images used for creating rootfs images (debos,
     buildroot) and push them to the Docker hub
   * Trigger a build for all the rootfs images in Jenkins
   * Redeploy the backend using Ansible
   * Redeploy the frontend using Ansible
   * Update the static website on kernelci.org
   * Rebuild all the other Docker images (toolchains, device tree validation,
     QEMU...) and push them to the Docker hub
   * Update the [KernelCI LAVA test-definitions
     fork](https://github.com/kernelci/test-definitions) with a rebase on top
     of upstream
   * Push a test revision to the [KernelCI linux
     tree](https://github.com/kernelci/linux) to run a "pipe cleaner" build
   * Wait for rootfs builds to complete (can take a while, like 2 or 3h)

1. Run a "pipe cleaner" build

   Once this is done, the URLs for the new rootfs images need to be updated in
   [`test-configs.yaml`](https://github.com/kernelci/kernelci-core/blob/main/config/core/test-configs.yaml).
   Then a build trigger should be run to build the test branch pushed to the
   KernelCI kernel tree:

   ```sh
   ./kernelci.org trigger
   ```

   It should take around 30min for the builds to complete, and then a while
   longer for any tests to complete in all the labs.  The results should be
   checked manually, by comparing with previous revisions on the web frontend.
   The number of builds and test results as well as their pass rates should be
   similar.  These builds can be seen here:

     https://linux.kernelci.org/job/kernelci/branch/kernelci.org/

1. Enable regular builds again

   Once the "pipe cleaner" job has completed and things look OK, the monitor
   job can be enabled again in Jenkins.  It will run every hour and start
   builds for any branch that has a different revision than the last one tested
   by KernelCI.  To avoid waiting for the next timer event, the first monitor
   after a production update may be started by hand.
