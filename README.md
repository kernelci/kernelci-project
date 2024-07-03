<img src="https://kernelci.org/image/kernelci-horizontal-color.png"
     alt="KernelCI project logo"
     width="40%" />

KernelCI project
================

KernelCI is a Linux Foundation project dedicated to testing the upstream [Linux
kernel](https://kernel.org).

Mission statement:

> To ensure the quality, stability and long-term maintenance of the Linux
> kernel by maintaining an open ecosystem around test automation practices and
> principles.

This repository contains general documentation about the project.


Documentation website
=====================

The source code of [docs.kernelci.org](https://docs.kernelci.org) static pages is
contained in the [`kernelci.org`](kernelci.org) directory.  It uses the
[Hugo](https://gohugo.io) framework.

To set up a local development server with Docker:

```sh
$ git clone https://github.com/kernelci/kernelci-project.git
$ cd kernelci-project
$ sudo apt install -y git-lfs
$ git-lfs fetch
$ git-lfs checkout
$ git submodule update --init --recursive
$ cd kernelci.org
```

Then to start the server:
```sh
$ docker run -v $PWD:/src -p 1313:1313 klakegg/hugo:0.97.3-ext-debian server -D
```

Alternatively, this can be started with `docker-compose`:

```sh
docker-compose up
```

Then open http://localhost:1313 in your browser.

Secrets and git-crypt
=====================

The [`secrets`](https://github.com/kernelci/kernelci-project/tree/main/secrets)
directory contains encrypted files with credentials used by the KernelCI
project.  See the [Secrets](https://kernelci.org/docs/admin/secrets/) page for
more details about how it is used.
