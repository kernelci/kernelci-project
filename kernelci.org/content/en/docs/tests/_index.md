---
title: "Tests"
date: 2021-08-04
description: KernelCI Tests
---

The fastest and preferred way to add a test and get it run by CI systems is to
contribute to existing test suites:

## kselftest

* The kernel source tree contains a set of “self tests” under the
  `tools/testing/selftests/` directory
* See [Contributing to
  kselftests](https://www.kernel.org/doc/html/latest/dev-tools/kselftest.html#contributing-new-tests)
  for instructions to add tests
* You can find more details at the [kselftests
  wiki](https://kselftest.wiki.kernel.org)
* Contact: Send questions to the mailing list
  [linux-kselftest@vger.kernel.org](mailto:linux-kselftest@vger.kernel.org) or
  join the `#linux-kselftest` IRC Channel on freenode

## LTP

* LTP Test source lives at the [Linux Test Project](https://linux-test-project.github.io/)
* Contact: Send questions to the mailing list **ltp@lists.linux.it**. For full [contact information](https://github.com/linux-test-project/ltp/wiki/Contact-Info), including IRC, see the [LTP wiki](https://github.com/linux-test-project/ltp/wiki/Developers)
* Proposing patches: You can submit Pull Requests to the [LTP project on GitHub](https://github.com/linux-test-project/ltp).
* Documentation: The [LTP wiki](https://github.com/linux-test-project/ltp/wiki/Developers) has plenty of documentation to get you started.  You have a [step-by-step tutorial](https://github.com/linux-test-project/ltp/blob/master/doc/c-test-tutorial-simple.txt) to create a new C test, [Guidelines](https://github.com/linux-test-project/ltp/blob/master/doc/test-writing-guidelines.txt), and other documentation.
