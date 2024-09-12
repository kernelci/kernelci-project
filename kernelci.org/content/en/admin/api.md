---
title: "API"
date: 2023-09-08
description: "KernelCI API"
---

## Getting an admin token

Some operations such as creating user accounts requires an admin user, so you
need to be in the `admin` group.  Then you need to get an API token to perform
queries restricted to admins.  Here are some sample commands to do that:

```
$ kci user whoami --indent=1
{
  "id": "64f5ff9e8326c545a780c2a0",
  "email": "<your-email-address>",
  "is_active": true,
  "is_superuser": true,
  "is_verified": true,
  "username": "<your-username>",
  "groups": [
    {
      "id": "6499aa9da02fef8143c1feb0",
      "name": "admin"
    }
  ]
}
$ kci user token <your-username>
Password:
"<your-admin-token>"
```

Then you can store this token in `kernelci.toml` when running the commands
that require admin permissions.  Please don't use your admin token as the
default one when using the regular parts of the API to avoid breaking things
by mistake.

## Creating user accounts

> **Note**: This is how things are done as part of the [Early
> Access](/api/early-access) phase.  The procedure once in production
> might change if users can just sign up by themselves.

First, create a random password and then use it with `kci user add` to create
the account:

```
$ pwgen -y 16 -1
Aeh3jah:t'ieshah
$ kci user add <username> <email>
Password: <paste password here>
```

If all goes well there aren't any errors and the user has been created.  To
double check that is the case, or to see if a user already exists or anything:

```
$ kci user find username=<username> --indent=1
[
 {
  "id": "6526448e7d140ee220971a0e",
  "email": "<email>",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "username": "<username>",
  "groups": []
 }
]
```

Then this is a template email to send a private confirmation to the new user
with the random password:

```
Subject: KernelCI API Early Access account
---
Hello USERNAME,

Your KernelCI API account has been created, here's your randomly
generated password:

  PASSWORD

Your personal Azure Files token is:

  ?sv=2022-11-02&ss=bfq&srt=sco&sp=<signature>

and the associated share name is:

  <share name>

Please take a look at the Early Access documentation page to update your API
account with your own password and get started:

  https://docs.kernelci.org/api/early-access/

Happy beta-testing!
```

The Azure Files token is common for all the Early Access users.
