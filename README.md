<div align="center">
    <a href="https://erpnexus.com">
        <img src="https://raw.githubusercontent.com/saashq/erpnexus/develop/erpnexus/public/images/erpnexus-logo.png" height="128">
    </a>
    <h2>ERPNexus</h2>
    <p align="center">
        <p>ERP made simple</p>
    </p>

[![CI](https://github.com/saashqdev/erpnexus/actions/workflows/server-tests-mariadb.yml/badge.svg?event=schedule)](https://github.com/saashqdev/erpnexus/actions/workflows/server-tests-mariadb.yml)
[![Open Source Helpers](https://www.codetriage.com/saashq/erpnexus/badges/users.svg)](https://www.codetriage.com/saashq/erpnexus)
[![codecov](https://codecov.io/gh/saashq/erpnexus/branch/develop/graph/badge.svg?token=0TwvyUg3I5)](https://codecov.io/gh/saashq/erpnexus)
[![docker pulls](https://img.shields.io/docker/pulls/saashq/erpnexus-worker.svg)](https://hub.docker.com/r/saashq/erpnexus-worker)

[https://erpnexus.com](https://erpnexus.com)

</div>

ERPNexus as a monolith includes the following areas for managing businesses:

1. [Accounting](https://erpnexus.com/open-source-accounting)
1. [Warehouse Management](https://erpnexus.com/distribution/warehouse-management-system)
1. [CRM](https://erpnexus.com/open-source-crm)
1. [Sales](https://erpnexus.com/open-source-sales-purchase)
1. [Purchase](https://erpnexus.com/open-source-sales-purchase)
1. [HRMS](https://erpnexus.com/open-source-hrms)
1. [Project Management](https://erpnexus.com/open-source-projects)
1. [Support](https://erpnexus.com/open-source-help-desk-software)
1. [Asset Management](https://erpnexus.com/open-source-asset-management-software)
1. [Quality Management](https://erpnexus.com/docs/user/manual/en/quality-management)
1. [Manufacturing](https://erpnexus.com/open-source-manufacturing-erp-software)
1. [Website Management](https://erpnexus.com/open-source-website-builder-software)
1. [Customize ERPNexus](https://erpnexus.com/docs/user/manual/en/customize-erpnexus)
1. [And More](https://erpnexus.com/docs/user/manual/en/)

ERPNexus is built on the [Saashq Framework](https://github.com/saashqdev/saashq), a full-stack web app framework built with Python & JavaScript.

## Installation

<div align="center" style="max-height: 40px;">
    <a href="https://saashqcloud.com/erpnexus/signup">
        <img src=".github/try-on-f-cloud-button.svg" height="40">
    </a>
    <a href="https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/saashq/saashq_docker/main/pwd.yml">
      <img src="https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png" alt="Try in PWD" height="37"/>
    </a>
</div>

> Login for the PWD site: (username: Administrator, password: admin)

### Containerized Installation

Use docker to deploy ERPNexus in production or for development of [Saashq](https://github.com/saashqdev/saashq) apps. See https://github.com/saashqdev/saashq_docker for more details.

### Manual Install

The Easy Way: our install script for wrench will install all dependencies (e.g. MariaDB). See https://github.com/saashqdev/wrench for more details.

New passwords will be created for the ERPNexus "Administrator" user, the MariaDB root user, and the saashq user (the script displays the passwords and saves them to ~/saashq_passwords.txt).


## Learning and community

1. [Saashq School](https://saashq.school) - Learn Saashq Framework and ERPNexus from the various courses by the maintainers or from the community.
2. [Official documentation](https://docs.erpnexus.com/) - Extensive documentation for ERPNexus.
3. [Discussion Forum](https://discuss.erpnexus.com/) - Engage with community of ERPNexus users and service providers.
4. [Telegram Group](https://erpnexus_public.t.me) - Get instant help from huge community of users.


## Contributing

1. [Issue Guidelines](https://github.com/saashqdev/erpnexus/wiki/Issue-Guidelines)
1. [Report Security Vulnerabilities](https://erpnexus.com/security)
1. [Pull Request Requirements](https://github.com/saashqdev/erpnexus/wiki/Contribution-Guidelines)

## License

GNU/General Public License (see [license.txt](license.txt))

The ERPNexus code is licensed as GNU General Public License (v3) and the Documentation is licensed as Creative Commons (CC-BY-SA-3.0) and the copyright is owned by Saashq Technologies Pvt Ltd (Saashq) and Contributors.

By contributing to ERPNexus, you agree that your contributions will be licensed under its GNU General Public License (v3).

## Logo and Trademark Policy

Please read our [Logo and Trademark Policy](TRADEMARK_POLICY.md).
