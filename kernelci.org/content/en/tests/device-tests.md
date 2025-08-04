---
title: "Device kselftests"
date: 2024-10-01
description: Overview of the process of enabling device kselftests on new platforms
---

Device kselftests provide a good starting point to validate basic kernel
functionality. There are a few of them upstream, with varying coverage and
requirements. See this documentation page for more information:
https://lore.kernel.org/all/20241001-kselftest-device-docs-v1-1-be28b70dd855@collabora.com

After deciding which test to run and satisfying its requirement (if any),
enabling the test on a new platform in KernelCI is a matter of adding the
platform to the test's scheduler entry. For example, for the DT kselftest on
ARM64, that would be adding the platform here:

https://github.com/kernelci/kernelci-pipeline/blob/08e7bce8044d04faa79028273384d9c30a1f5d9e/config/pipeline.yaml#L2495

For the other tests, just look for the entry in the ``scheduler`` that has
``collections`` set to the kselftest path as per the upstream documentation (for
example, for the error logs test, look for ``collections: devices/error_logs``).
To enable the test on a different architecture, look for the entry that has the
build corresponding to that architecture, or create it if there's none. See
https://docs.kernelci.org/maestro/pipeline/developer-documentation/#an-example-of-enabling-a-new-job
for more details on enabling tests in KernelCI.

Note: In addition to the tests described in the upstream documentation, there is
also an alternative to the DT kselftest for ACPI platforms: the ``acpi``
kselftest. It is not described there as it hasn't been merged upstream, but it
is already being run in KernelCI.
