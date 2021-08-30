---
title: "Local (Dev setup)"
date: 2021-08-12T10:15:37Z
draft: true
description: "How to set up a local KernelCI instance"
---

This section describes how to set up a KernelCI instance which is suitable for development. It's not meant to mimic the production-like setup on your local machine, but rather give directions on how to setup a minimal set of KernelCI components to simplify the process of development and testing new features.

## Minimal set of KernelCI components

The minimal setup for KernelCI consists of:

- kernelci-backend
- storage
- kernelci-core

This is sufficient for building the kernel, running tests and pushing build and test information as well as build artifacts to the backend and storage respectively.

> **Note**
> These instructions are not suitable and should not be used to setup a production environment. They purposely neglect certain aspects of performance and security for the sake of simplicity.

## Prerequisites

Currently, the best option is to create a separate Virtual Machine that will run `kernelci-backend` and `storage`

It's assumed in this document that you're running a following setup:

- Virtual Machine running Debian Buster accessible via IP and domain name e.g. _kci-vm_. The following requirements need to be met:

   - The VM must be reachable with a domain name from the host used for installation.
   - SSH access is provided with key authorization

> You can use DNS to access the VM with its domain name or simply put an entry to the `/etc/hosts` file.

- Host machine which will be used to connect to the VM
   It needs to meet following requirements:
    - Installed apps:
      - _git_
      - _ansible_
      - _Python 2.7_
      - _Python 3.6+_

## Deploy KernelCI backend and storage

> **Note** It is assumed in this section that your kernelci VM is available from your host with the hostname `kci-vm`

- Make sure _ansible_ is installed on the host machine.
- Clone `kernelci-backend-config` repository

    ```bash
    git clone git@github.com:kernelci/kernelci-backend-config.git
    ```

### Configure ansible to be used with your VM

```bash
cd kernelci-backend-config
```

- Modify `[local]` section of the `hosts` file to match your configuration

```ini
[local]
kci-vm ansible_ssh_user=kci
```

- Create `host_vars/kci-vm`

```bash
touch host_vars/kci-vm
```

- Edit `host_vars/kci-vm` with your favorite text editor and put content there:

```ini
hostname: kci-vm 
role: production
certname: kci-vm
storage_certname: kci-vm
kci_storage_fqdn: kci-vm
become_method: su
```

- Create `dev.yml` playbook file with the following content:

```
- hosts: kci-vm
    become: yes
    become_method: su
    become_user: root
    gather_facts: yes
    roles:
        - common
        - install-deps
        - install-app
        - init-conf
        - kernelci-storage
```

### Prepare secrets

- Copy `secrets.yml` template

```
cp templates/secrets.yml dev-secrets.yml
```

- Fill out necessary values

```
master_key:
    "<random_string>"

# The url location where the backend will be running
backend_url:
    "http://kci-vm"
# The url location where the frontend will be running
base_url:
    "http://kci-vm"
# The backend token OR master key for a fresh install
# If set to the master-key this field will have to be updated
# once the tokens created
backend_token:
    "<random_string>"
# A secret key internally used by Flask
secret_key:
    "<random_string>"
# The url location of the storage server for the backend
file_server:
    "http://kci-vm"
```

```
ssl_stapling_resolver:
    "localhost"
```

> **Note** You can use UUID as your random string. You can easily generate one with
> ```
> python -c "import uuid;print(uuid.uuid4())"
> ```

### Run ansible playbook to set up your VM

```
ansible-playbook -i hosts -l kci-vm -D -b -K  -e git_head="main" -e "@./dev-secrets.yml" --key-file ~/.ssh/org/id_rsa dev.yml
```

> **Note** You may validate your ansible playbook with
> ```
> ansible-playbook dev.yml --syntax-check
> ```

> **Note** If you face unexpected behavior of ansible increasing verbosity by adding `-vvv` option may help in debugging

> **Note** The nginx configuration step may fail due to SSL issues, but that's fine for the development setup.

### Tweak your VM config

- Log in to your VM as root
- Delete backend nginx config

```
rm /etc/nginx/sites-enabled/kci-vm
```

- Replace content of the storage config (`/etc/nginx/sites-enabled/kci-vm.conf`)

```
server {
    listen *;
    listen [::];

    server_name kci-vm;
    root /var/www/images/kernel-ci;
    charset utf-8;

    access_log /var/log/nginx/kci-vm-access.log combined buffer=16k;
    error_log /var/log/nginx/kci-vm-error.log crit;

    location / {
        if (-f $document_root/maintenance.html) {
            return 503;
        }

        fancyindex on;
        fancyindex_exact_size off;
    }
}
```

- Restart nginx

```
systemctl restart nginx
```

- Start KernelCI services

```
systemctl start kernelci-backend
systemctl start kernelci-celery
```

> **Note** At this point your kernelci-backend instance should be available at `http://kci-vm:8888`

> **Note** If you want to follow your kenrelci logs use journalctl
> ```
> journalctl -f -u kernelci-celery -u kernelci-backend
> ```

## Configure KernelCI Backend

As the instance of `kernelci-backend` is up and running you can add necessary configuration to it.

### Create admin token

```
curl -XPOST -H "Content-Type: application/json" -H "Authorization: YOUR_MASTER_KEY" "http://kci-vm:8888/token" -d '{"email": "me@example.com", "username": "admin", "admin": 1}'
```

If this goes well, you should see the admin token in the output
e.g.

```
{"result":[{"token":"3f1fbc0f-4146-408c-a2da-02748f595bfe"}],"code":201}
```

## Build kernel and push results

Congratulations, your `kernelci-backend` instance is up and running.
You can now build your kernel and push the artifacts with `kci_build` and `kci_data`.
See the [`kci_build`](https://kernelci.org/docs/core/kci_build/) documentation to get you started.
