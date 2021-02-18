KernelCI project
================

KernelCI is a Linux Foundation project dedicated to testing the upstream [Linux
kernel](https://kernel.org).

Mission statement:

> To ensure the quality, stability and long-term maintenance of the Linux
> kernel by maintaining an open ecosystem around test automation practices and
> principles.

This repository contains general documentation about the project.


kernelci.org static website
===========================

The source code of the [kernelci.org](https://kernelci.org) static website is
contained in the [`kernelci.org`](kernelci.org) directory.  It uses the
[Hugo](https://gohugo.io) framework.

To set up a local development server with Docker:

```sh
$ git clone https://github.com/kernelci/kernelci-project.git
$ cd kernelci.org
$ sudo apt install -y git-lfs
$ git-lfs checkout
$ git submodule update --init --recursive
$ docker run -v $PWD:/src -p 1313:1313 klakegg/hugo:0.80.0-ext-debian server -D
```

Then open http://localhost:1313 in your browser.
