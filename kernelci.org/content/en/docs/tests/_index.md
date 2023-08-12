---
title: "Tests"
date: 2021-08-04
description: KernelCI Tests
weight: 3
---

## Native tests

KernelCI native tests are orchestrated by KernelCI.  They are initiated in test
labs directly connected to KernelCI and results are visible on the [web
frontend](https://linux.kernelci.org/job/).

Tests run natively by KernelCI such as [kselftest](kselftest) and [LTP](ltp)
but also some KernelCI specific ones are all described with dedicated pages
under this current section.

It's possible for anyone to add new native tests.  See the [How-To
guide](howto) to get started.

## External tests and KCIDB

Non-native tests are run in fully autonomous systems, such as syzbot or CKI.
Their results are shared alongside KernelCI native test results via
[KCIDB](https://kcidb.kernelci.org).

See the [Tests Catalog](https://github.com/kernelci/kcidb/blob/main/tests.yaml)
file with the list of test identifiers used by KCIDB.

The fastest way to add the test is to use existing test suites:

## LTP

* LTP Test source lives at the [Linux Test Project](https://linux-test-project.github.io/)
* Contact: Send questions to the mailing list **ltp@lists.linux.it**. For full [contact information](https://github.com/linux-test-project/ltp/wiki/Contact-Info), including IRC, see the [LTP wiki](https://github.com/linux-test-project/ltp/wiki/Developers)
* Proposing patches: You can submit Pull Requests to the [LTP project on GitHub](https://github.com/linux-test-project/ltp).
* Documentation: The [LTP wiki](https://github.com/linux-test-project/ltp/wiki/Developers) has plenty of documentation to get you started.  You have a [step-by-step tutorial](https://github.com/linux-test-project/ltp/blob/master/doc/c-test-tutorial-simple.txt) to create a new C test, [Guidelines](https://github.com/linux-test-project/ltp/blob/master/doc/test-writing-guidelines.txt), and other documentation.

## kselftests

* The kernel contains a set of “self tests” under the tools/testing/selftests/
directory
* See [Contributing to kselftests](https://www.kernel.org/doc/html/latest/dev-tools/kselftest.html#contributing-new-tests) for instructions to add tests
* You can find more details at the [kselftests wiki](https://kselftest.wiki.kernel.org)
* Contact: Send questions to the mailing list **linux-kselftest@vger.kernel.org** or join **#linux-kselftest** IRC Channel on freenode
