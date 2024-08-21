---
name: API Staging Access
about: Request to get a staging account for the new API
title: Request API account for USER
labels: ''
assignees:
  - nuclearcat
  - JenySadadia
---

Maestro has a staging instance running for development purposes.
It allows users to request an account on the new KernelCI API to give it a try. You can also enable your trees, builds, and tests on it. Here is the [developer documentation](https://docs.kernelci.org/maestro/pipeline/developer-documentation/) for the same.

[Staging deployment](https://github.com/kernelci/kernelci-api/tree/main/kube/aks) can already run a pipeline with KUnit, kselftest, kernel builds and boot tests. So please give it a go and create issues on GitHub and ask  questions on the [mailing list](mailto:kernelci@lists.linux.dev), IRC `#kernelci` on libera.chat or [Slack](https://kernelci.slack.com) with whatever you may find.

Once the account request is accepted, a user account will be created by an admin and a random password will be sent to your email address.  You can then use `kci user password update` to set your own password, `kci user verify` to verify your email address, and `kci user token` to get an API token.  We'll also provide you with an AzureFiles share to use alongside the API, even though you may use any other storage as long as artifacts can be reached with a public HTTP URL.

Please provide the required information below and also replace `USER` with your name or username in the issue title:

* User name:
* Email address:
