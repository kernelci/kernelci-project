---
title: "Submitter guide"
date: 2026-07-16
description: "How to submit build and test results to KCIDB"
weight: 20
---

Any CI system that builds or tests the Linux kernel can contribute results
to KCIDB. You only share what you want to make public — there is no
requirement to submit private test results.

Submitting is a simple HTTPS POST. No daemons, no cloud accounts, no special
client tools needed.

## 1. Get in touch

Write to us using any of the [contact channels](/contacts). We will:

* agree on an **origin** — a short string identifying your CI system
  (e.g. `myci`), used as a prefix in all your object IDs;
* hand you **JWT tokens** and endpoint URLs for the staging and production
  instances.

You start on staging, where you can experiment freely, and move to
production once you are happy with your data.

## 2. Prepare your data

Reports are JSON documents following the
[KCIDB schema](https://github.com/kernelci/kcidb-io). They can contain five
kinds of objects: **checkouts**, **builds**, **tests**, **issues** and
**incidents**. You can submit any of them, in any combination — for example
only tests, referring to builds submitted by someone else.

All object IDs must start with your origin followed by a colon. Here is a
minimal but useful report:

```json
{
    "version": {"major": 5, "minor": 3},
    "checkouts": [
        {
            "id": "myci:c9c9735c46f5",
            "origin": "myci",
            "git_repository_url": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
            "git_commit_hash": "c9c9735c46f589b9877b7fc00c89ef1b61a31e18",
            "patchset_hash": ""
        }
    ],
    "builds": [
        {
            "id": "myci:build-1",
            "origin": "myci",
            "checkout_id": "myci:c9c9735c46f5",
            "architecture": "x86_64",
            "config_name": "defconfig",
            "status": "PASS"
        }
    ],
    "tests": [
        {
            "id": "myci:test-1",
            "origin": "myci",
            "build_id": "myci:build-1",
            "path": "ltp.sem01",
            "status": "PASS"
        }
    ]
}
```

For builds we want at least the kernel configuration, build environment
details and logs; for tests, the results, logs and information about the
test environment (device type, configuration, etc.). Anything that doesn't
fit the schema can go into the free-form `misc` field of any object.

### Artifact hosting

KCIDB stores metadata and links, not files. Logs, kernel images and other
artifacts you reference in your submissions (`log_url`, `config_url`,
`output_files`...) need to be hosted by you and **publicly available** over
HTTP(S) — they are linked from the dashboard and downloaded for automatic
log analysis.

If you are a member of the KernelCI foundation, we will gladly assist and
can provide file hosting for these materials on our
[kernelci-storage](/components/kernelci-storage) infrastructure. If not,
[reach out](/contacts) anyway — whether we can help with hosting is
something to discuss and decide together.

### Hybrid submissions

You don't have to build kernels yourself. A common setup is a lab that takes
kernels built by [Maestro](/components/maestro), runs its own tests on its
own hardware and submits only the test results, with `build_id` pointing at
the existing Maestro build:

```json
{
    "version": {"major": 5, "minor": 3},
    "tests": [
        {
            "id": "myci:test-42",
            "origin": "myci",
            "build_id": "maestro:67d409f9f378f0c5986dc7df",
            "path": "ltp.sem01",
            "status": "PASS"
        }
    ]
}
```

Your results then show up on the dashboard right next to the build they were
run against. The same works the other way around: you can submit builds for
others to test.

If this describes your lab, also consider connecting it to
[Maestro](/components/maestro) directly instead of submitting to KCIDB
yourself. Maestro supports
[pull labs](/components/maestro/pipeline/connecting-pull-lab): your lab
polls Maestro for jobs over outbound HTTPS, so it doesn't need to be
publicly reachable and works fine behind a firewall. For labs testing
Maestro kernels this is the recommended path — results submitted through
Maestro keep its node hierarchy consistent, and Maestro takes care of
forwarding them to KCIDB for you.

## 3. Submit it

Send your report to the `/submit` endpoint with your token in the
`Authorization` header:

```bash
curl -X POST \
  -H "Authorization: Bearer $KCIDB_TOKEN" \
  -H "Content-Type: application/json" \
  -d @report.json \
  https://staging.db.kernelci.org/submit
```

The response contains a submission ID which you can use to track progress:

```bash
curl -H "Authorization: Bearer $KCIDB_TOKEN" \
  "https://staging.db.kernelci.org/status?id=<submission_id>"
```

The status will go from `ready` to `processed` once the data is in the
database, or `failed` if it didn't pass schema validation.

> **Note:** the staging instance is occasionally taken down for maintenance.
> If your submissions fail unexpectedly or nothing shows up, don't spend
> hours debugging your side — just [contact the sysadmins](/contacts) and
> we'll sort it out.

Alternatively, [kci-dev](https://kci.dev/) can build the payload and submit
it for you — handy for scripting or trying things out from a git checkout:

```bash
kci-dev submit build --origin myci \
  --kcidb-rest-url https://staging.db.kernelci.org \
  --kcidb-token $KCIDB_TOKEN \
  --arch x86_64 --config-name defconfig --status PASS \
  --log-url https://myci.example.com/logs/build-1.log
```

It also accepts a complete payload with `--from-json report.json`, and
`--dry-run` shows what would be submitted without sending anything.

## 4. Watch your results arrive

Staging submissions appear on the
[staging dashboard](https://staging-dashboard.kernelci.org/), production
ones on the [main dashboard](https://dashboard.kernelci.org/) — look for
your origin. You can also monitor arrival from the command line with
[kci-dev](https://kci.dev/):

```bash
kci-dev results summary --origin myci \
  --giturl 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git' \
  --branch master
```

Start submitting early: seeing your real data is the fastest way to spot
what needs tweaking, and we are happy to help along the way.

Once everything looks good, switch your submissions to the production
endpoint at `https://db.kernelci.org/` and you're done.

For more details see the
[kcidb-ng submitter documentation](https://github.com/kernelci/kcidb-ng/blob/main/SUBMITTERS.md).
