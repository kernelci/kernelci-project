---
title: "Secrets"
date: 2021-09-03
draft: false
description: "KernelCI project encrypted files"
---

The [`secrets`](https://github.com/kernelci/kernelci-project/tree/main/secrets)
directory contains encrypted files using
[`git-crypt`](https://www.agwa.name/projects/git-crypt/) with credentials used
by the KernelCI project.  It is mostly useful to project administrators such as
members of the [TSC](/docs/org/tsc), for example to have a common place where
to share passwords in a secure way.  Derivative projects based on KernelCI such
as private instances may reuse some of the tools and documentation provided
here.


## Creating a GPG key

If the user doen't already have a GPG key, they will need to create one.  It
may otherwise be a good idea to create a key dedicated to using git-crypt in
this repository, so it may be revoked later without any side-effects on other
projects or use-cases.  To generate a key:

```
gpg --generate-key
```

Answer the questions interactively, it should then show something like this:

```
gpg: key E7B3A05C40D8EDC3 marked as ultimately trusted
```

with the full public key fingerprint:

```
pub   rsa3072 2021-04-22 [SC] [expires: 2023-04-22]
    7802ED21096B2ED7B1D4D838E7B3A05C40D8EDC3
```

This can be read again with `gpg -K`.  It's then possible to [send the
  key](https://www.gnupg.org/gph/en/manual/x457.html) to a keyserver to make it
easier for others to find it and import it with just the fingerprint rather
than the full public key file.  Here's how to do it with a sample keyserver:

```
gpg --send-keys --keyserver hkps://keyserver.ubuntu.com
```

## Adding a user's GPG key

The next step is to add the user's key to the repository so they can read the
encrypted content.  First, either get the public key file for that user and
import it with `gpg --import <key-file>` or get it from a keyserver using the
fingerprint using `gpg --receive-keys <key-fingerprint>`.  Then `gpg -K` should
show the key for the user locally available.  To add the user, using the
fingerprint from the example in the previous step:

```
git-crypt add-gpg-user 7802ED21096B2ED7B1D4D838E7B3A05C40D8EDC3
```

This will create a git commit with the public GPG key of that user.  It can
then be pushed as-is, or the commit message may be edited to add the name of
the user to the subject and make the history easier to read.

If the key is not trusted, you can manually override this with the following
command:

```
gpg --edit-key <key-id>
> trust
> 5
> y
> q
```

Then run the `git-crypt add-gpg-user` again and it should work this time.


## Reading the encrypted files

Users with a GPG key added to the repository can then uncrypt the files using
this command:

```
git-crypt unlock
```

There are filters in the `.gitattributes` file to select which files to encrypt
and which ones to keep as plain text.  Essentially, all the contents of the
`secrets` directory in this repository are encrypted except some documentation
and utility scripts such as
[`dump.py`](https://github.com/kernelci/kernelci-project/blob/main/secrets/dump.py)
to dump the `passwords.toml` file.  Here's what the file typically looks like:
```toml
[service-name]
url = "https://something.com"
user = "user-name"
password = "password"
login_url = "https://something.com/login"
email = "hello@email.com"
```
