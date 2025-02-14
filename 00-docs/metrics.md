

# Metrics

The Cyber Metric Library is a list of security metrics that can be used as a baseline for any executive reporting platform.  The list is not exhaustive, and is focussed primarily on technical controls that can be measured easily with available tooling.

## How to use this guide

### Types of Metrics

* ![control](https://img.shields.io/badge/CONTROL-0000F0) A measure that tracks the implementation of actions, processes, or technologies designed to reduce or mitigate risks within the organization.
* ![risk](https://img.shields.io/badge/RISK-c00000) A measure that provides visibility into existing or potential risks within the organization, helping to assess areas of vulnerability.
* ![performance](https://img.shields.io/badge/PERFORMANCE-0F00) A measure that evaluates the efficiency and speed with which a team is executing and delivering on control implementations and operational tasks.

### Framework references

The following frameworks are used in the mapping of metrics

* [ISO 27001:2022](https://www.iso.org/standard/27001)
* [CIS 8.1](https://www.cisecurity.org/controls/v8-1)
* [NIST CSF v.2.0](https://csf.tools/reference/nist-cybersecurity-framework/v2-0/)
* [Essential 8](https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight)

|**Category**|**Title**|**Type**|**Query**|
|--|--|--|--|
|**Asset Management**|||||
||[Assets known to Asset Management](#assets-known-to-asset-management)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
|**Data Protection**|||||
||[Systems with their volumes encrypted](#systems-with-their-volumes-encrypted)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
|**Disaster Recovery**|||||
||[Systems with backups configured per their SLO](#systems-with-backups-configured-per-their-slo)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
||[Systems that has had a successful backup per their SLO](#systems-that-has-had-a-successful-backup-per-their-slo)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![No](https://img.shields.io/badge/NO-00F)|
|**Identity Management**|||||
||[Identities with MFA](#identities-with-mfa)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
||[Identity - Credentials - Regular Password Rotation](#identity---credentials---regular-password-rotation)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Identity - Inactive Identities](#identity---inactive-identities)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Accounts without Admin privileges](#accounts-without-admin-privileges)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
|**Malware Protection**|||||
||[Systems with an up-to-date agent deployed](#systems-with-an-up-to-date-agent-deployed)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
|**Network Security**|||||
||[Network Security - DNS Domains Expiring Within the Next Month](#network-security---dns-domains-expiring-within-the-next-month)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Network Security - DNS Domains with SPF configured](#network-security---dns-domains-with-spf-configured)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Network Security - DNS Domains with DMARC Configured](#network-security---dns-domains-with-dmarc-configured)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[External endpoints with insecure ports exposed](#external-endpoints-with-insecure-ports-exposed)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
||[External endpoints protected by a WAF](#external-endpoints-protected-by-a-waf)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
|**Software Development**|||||
||[Repositories with SAST / DAST scanning enabled](#repositories-with-sast-/-dast-scanning-enabled)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
||[Repositories without exploitable vulnerabilities](#repositories-without-exploitable-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Repositories without exploitable vulnerabilities remediated within SLO](#repositories-without-exploitable-vulnerabilities-remediated-within-slo)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![No](https://img.shields.io/badge/NO-00F)|
|**User Security**|||||
||[Users completed awareness training in the last 12 months](#users-completed-awareness-training-in-the-last-12-months)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
|**Vulnerability Management**|||||
||[Systems with an up-to-date agent deployed](#systems-with-an-up-to-date-agent-deployed)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
||[Systems with an up-to-date vulnerability database deployed](#systems-with-an-up-to-date-vulnerability-database-deployed)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
||[End-of-life - Systems running vendor-supported software](#end-of-life---systems-running-vendor-supported-software)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
||[Vulnerabilities not remediated within SLO - critical and high](#vulnerabilities-not-remediated-within-slo---critical-and-high)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Vulnerabilities not remediated within SLO - exploitable](#vulnerabilities-not-remediated-within-slo---exploitable)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Vulnerabilities not remediated within SLO - exploitable patchable](#vulnerabilities-not-remediated-within-slo---exploitable-patchable)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Vulnerabilities not remediated within SLO - exploitable patchable critical and high](#vulnerabilities-not-remediated-within-slo---exploitable-patchable-critical-and-high)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Vulnerabilities not remediated within SLO - patchable](#vulnerabilities-not-remediated-within-slo---patchable)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without vulnerabilities - exploitable and patchable critical and high](#systems-without-vulnerabilities---exploitable-and-patchable-critical-and-high)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without vulnerabilities - exploitable and patchable critical and high](#systems-without-vulnerabilities---exploitable-and-patchable-critical-and-high)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without vulnerabilities in 48 hours - exploitable or critical and high](#systems-without-vulnerabilities-in-48-hours---exploitable-or-critical-and-high)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without vulnerabilities - exploitable and patchable critical and high](#systems-without-vulnerabilities---exploitable-and-patchable-critical-and-high)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without vulnerabilities - exploitable and patchable critical and high](#systems-without-vulnerabilities---exploitable-and-patchable-critical-and-high)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without vulnerabilities - non critical patched in 2 weeks](#systems-without-vulnerabilities---non-critical-patched-in-2-weeks)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without vulnerabilities - non critical patched in a month](#systems-without-vulnerabilities---non-critical-patched-in-a-month)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without vulnerabilities - exploitable and patchable critical and high](#systems-without-vulnerabilities---exploitable-and-patchable-critical-and-high)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|


## List of metrics
### Assets known to Asset Management

#### Description

Using our scanning tools, we identify systems that may exist in the environment that may not have been recorded in the asset management system.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`am_known_assets`|
|**Category**|Asset Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.5.9|5 Organizational controls|Inventory of information and other associated assets|
|CIS 8.1|1.1|Inventory and Control of Enterprise Assets|Establish and Maintain Detailed Enterprise Asset Inventory|
|NIST CSF v2.0|ID.AM-01|Asset Management (ID.AM)|ID.AM-01: Inventories of hardware managed by the organization are maintained|
|Essential8-ML1|ISM-1807|Patch applications|An automated method of asset discovery is used at least fortnightly to support the detection of assets for subsequent vulnerability scanning activities.|
|Essential8-ML2|ISM-1807|Patch applications|An automated method of asset discovery is used at least fortnightly to support the detection of assets for subsequent vulnerability scanning activities.|
|Essential8-ML3|ISM-1807|Patch applications|An automated method of asset discovery is used at least fortnightly to support the detection of assets for subsequent vulnerability scanning activities.|
|Essential8-ML1|ISM-1807|Patch operating systems|An automated method of asset discovery is used at least fortnightly to support the detection of assets for subsequent vulnerability scanning activities.|
|Essential8-ML2|ISM-1807|Patch operating systems|An automated method of asset discovery is used at least fortnightly to support the detection of assets for subsequent vulnerability scanning activities.|
|Essential8-ML3|ISM-1807|Patch operating systems|An automated method of asset discovery is used at least fortnightly to support the detection of assets for subsequent vulnerability scanning activities.|




### Systems with their volumes encrypted

#### Description

The percentage of systems with their volumes fully encrypted, ensuring that sensitive data is protected from unauthorized access in the event of a device loss or breach, which is crucial for safeguarding company assets and complying with data protection regulations.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`dp_volume_encrypted`|
|**Category**|Data Protection|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|3.11|Data Protection|Encrypt Sensitive Data at Rest|
|ISO 27001:2022|A.8.24|8 Technological controls|Use of cryptography|
|NIST CSF v2.0|PR.DS-01|Data Security (PR.DS)|PR.DS-01: The confidentiality, integrity, and availability of data-at-rest are protected|




### Systems with backups configured per their SLO

#### Description

The percentage of systems with backups configured in accordance with their Service Level Objectives (SLO), ensuring critical data can be restored in the event of a failure, which is essential for maintaining business continuity and mitigating the impact of data loss.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`dr_backup_coverage`|
|**Category**|Disaster Recovery|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|11.2|Data Recovery|Perform Automated Backups|
|ISO 27001:2022|A.8.13|8 Technological controls|Information backup|
|NIST CSF v2.0|PR.DS-11|Data Security (PR.DS)|PR.DS-11: Backups of data are created, protected, maintained, and tested|




### Systems that has had a successful backup per their SLO

#### Description

The percentage of systems that successfully complete backups within their defined Service Level Objectives (SLO), ensuring data integrity and availability, which is critical for minimizing downtime, protecting against data loss, and maintaining business continuity in the event of an incident.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`dr_backup_performance`|
|**Category**|Disaster Recovery|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|11.2|Data Recovery|Perform Automated Backups|
|ISO 27001:2022|A.8.13|8 Technological controls|Information backup|
|NIST CSF v2.0|PR.DS-11|Data Security (PR.DS)|PR.DS-11: Backups of data are created, protected, maintained, and tested|




### Identities with MFA

#### Description

The percentage of user accounts secured with multi-factor authentication, a critical metric that quantifies the effectiveness of identity protection by reducing the risk of unauthorized access and safeguarding sensitive assets, making it vital for minimizing the impact of credential-based attacks.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`im_authentication_mfa`|
|**Category**|Identity Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|6.3|Access Control Management|Require MFA for Externally-Exposed Applications|
|CIS 8.1|6.4|Access Control Management|Require MFA for Remote Network Access|
|CIS 8.1|6.5|Access Control Management|Require MFA for Administrative Access|
|ISO 27001:2022|A.5.17|5 Organizational controls|Authentication information|
|NIST CSF v2.0|PR.AA-03|Identity Management, Authentication, and Access Control (PR.AA)|PR.AA-03: Users, services, and hardware are authenticated|




### Identity - Credentials - Regular Password Rotation

#### Description

Regular password rotation ensures that credentials are periodically updated,
reducing the risk of unauthorized access from compromised or stale
passwords, which is critical to maintaining the security of your
organization's systems and data.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`im_credentials`|
|**Category**|Identity Management|
|**SLO**|98.00% - 99.00%|
|**Weight**|0.8|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.5|8 Technological controls|Secure authentication|
|NIST CSF v2.0|PR.AA-02|Identity Management, Authentication, and Access Control (PR.AA)|PR.AA-02: Identities are proofed and bound to credentials based on the context of interactions|




### Identity - Inactive Identities

#### Description

Dormant Identities tracks the number of unused or inactive accounts within
the organization, providing critical insight into potential security risks
as dormant accounts are prime targets for unauthorized access and
exploitation, making their identification and timely deactivation essential
for reducing the attack surface and maintaining robust access controls.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`im_dormant`|
|**Category**|Identity Management|
|**SLO**|98.00% - 99.00%|
|**Weight**|0.8|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.5.16|5 Organizational controls|Identity management|
|CIS 8.1|5.3|Account Management|Disable Dormant Accounts|
|NIST CSF v2.0|PR.AA-01|Identity Management, Authentication, and Access Control (PR.AA)|PR.AA-01: Identities and credentials for authorized users, services, and hardware are managed by the organization|




### Accounts without Admin privileges

#### Description

The percentage of user accounts configured without administrative rights, which is critical for reducing the attack surface, limiting the potential impact of compromised credentials, and aligning with least-privilege security principles to protect organizational systems and data.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`im_privileges`|
|**Category**|Identity Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|5.4|Account Management|Restrict Administrator Privileges to Dedicated Administrator Accounts|
|ISO 27001:2022|A.8.2|8 Technological controls|Privileged access rights|
|NIST CSF v2.0|PR.AA-05|Identity Management, Authentication, and Access Control (PR.AA)|PR.AA-05: Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed, and incorporate the principles of least privilege and separation of duties|




### Systems with an up-to-date agent deployed

#### Description

The percentage of systems with an up-to-date malware detection agent deployed, ensuring the organization\u2019s defenses are robust against the latest threats, and is critical for minimizing vulnerability to malware attacks.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`mp_coverage`|
|**Category**|Malware Protection|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|10.1|Malware Defenses|Deploy and Maintain Anti-Malware Software|
|ISO 27001:2022|A.8.7|8 Technological controls|Protection against malware|
|NIST CSF v2.0|PR.PS-05|Platform Security (PR.PS)|PR.PS-05: Installation and execution of unauthorized software are prevented|




### Network Security - DNS Domains Expiring Within the Next Month

#### Description

The percentage of DNS domains that are set to expire within the next month, which could lead to service disruptions if not renewed in time.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`ns_domains_expiring`|
|**Category**|Network Security|
|**SLO**|99.00% - 100.00%|
|**Weight**|0.2|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.20|8 Technological controls|Networks security|
|CIS 8.1|9.3|Email and Web Browser Protections|Maintain and Enforce Network-Based URL Filters|
|NIST CSF v2.0|ID.AM-04|Asset Management (ID.AM)|ID.AM-04: Inventories of services provided by suppliers are maintained|




### Network Security - DNS Domains with SPF configured

#### Description

The percentage of DNS domains with email configured that has an SPF record
created in the DNS zone.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`ns_domains_with_spf`|
|**Category**|Network Security|
|**SLO**|95.00% - 99.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.20|8 Technological controls|Networks security|
|CIS 8.1|9.2|Email and Web Browser Protections|Use DNS Filtering Services|
|CIS 8.1|9.3|Email and Web Browser Protections|Maintain and Enforce Network-Based URL Filters|
|CIS 8.1|12.6|Network Infrastructure Management|Use of Secure Network Management and Communication Protocols|
|NIST CSF v2.0|PR.DS-01|Data Security (PR.DS)|PR.DS-01: The confidentiality, integrity, and availability of data-at-rest are protected|




### Network Security - DNS Domains with DMARC Configured

#### Description

The percentage of DNS domains with email configured that have a DMARC record
created in the DNS zone.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`ns_domains_with_dmarc`|
|**Category**|Network Security|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.6|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.20|8 Technological controls|Networks security|
|CIS 8.1|9.4|Email and Web Browser Protections|Restrict Unnecessary or Unauthorized Browser and Email Client Extensions|
|CIS 8.1|12.6|Network Infrastructure Management|Use of Secure Network Management and Communication Protocols|
|NIST CSF v2.0|PR.DS-02|Data Security (PR.DS)|PR.DS-02: The confidentiality, integrity, and availability of data-in-transit are protected|




### External endpoints with insecure ports exposed

#### Description

The "Insecure Ports" metric tracks external endpoints with open ports that are improperly configured or vulnerable, highlighting potential entry points for cyberattacks, which is critical for reducing the organization's exposure to exploitation and ensuring the security of its network infrastructure.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`ns_insecure_ports`|
|**Category**|Network Security|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|12.2|Network Infrastructure Management|Establish and Maintain a Secure Network Architecture|
|ISO 27001:2022|A.8.20|8 Technological controls|Networks security|
|NIST CSF v2.0|PR.DS-02|Data Security (PR.DS)|PR.DS-02: The confidentiality, integrity, and availability of data-in-transit are protected|




### External endpoints protected by a WAF

#### Description

The metric measures the proportion of external-facing endpoints shielded by a Web Application Firewall (WAF), highlighting an organization's ability to prevent unauthorized access, mitigate threats like SQL injection and cross-site scripting, and safeguard critical systems from cyberattacks, making it a key indicator of external-facing application security.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`ns_waf`|
|**Category**|Network Security|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|13.3|Network Monitoring and Defense|Deploy a Network Intrusion Detection Solution|
|ISO 27001:2022|A.8.20|8 Technological controls|Networks security|
|NIST CSF v2.0|PR.IR-01|Technology Infrastructure Resilience (PR.IR)|PR.IR-01: Networks and environments are protected from unauthorized logical access and usage|




### Repositories with SAST / DAST scanning enabled

#### Description

The percentage of code repositories with Static Application Security Testing (SAST) and Dynamic Application Security Testing (DAST) scanning enabled, ensuring early detection of vulnerabilities during development and reducing the risk of security breaches before code is deployed.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`sd_repository_coverage`|
|**Category**|Software Development|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|16.12|Application Software Security|Implement Code-Level Security Checks|
|ISO 27001:2022|A.8.25|8 Technological controls|Secure development life cycle|
|NIST CSF v2.0|PR.PS-06|Platform Security (PR.PS)|PR.PS-06: Secure software development practices are integrated, and their performance is monitored throughout the software development life cycle|




### Repositories without exploitable vulnerabilities

#### Description

The percentage of code repositories free from known security flaws, ensuring that development efforts prioritize secure coding practices, reduce the risk of breaches, and maintain the integrity of the software development lifecycle. This metric is important as it directly impacts the organization's ability to deliver secure products and protect against potential cyber threats.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`sd_vulnerabilities`|
|**Category**|Software Development|
|**SLO**|98.00% - 99.00%|
|**Weight**|0.8|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.25|8 Technological controls|Secure development life cycle|
|CIS 8.1|16.12|Application Software Security|Implement Code-Level Security Checks|
|NIST CSF v2.0|PR.PS-06|Platform Security (PR.PS)|PR.PS-06: Secure software development practices are integrated, and their performance is monitored throughout the software development life cycle|




### Repositories without exploitable vulnerabilities remediated within SLO

#### Description

The percentage of code repositories in the development pipeline that have resolved critical security vulnerabilities within the established service level objective (SLO), ensuring that potential threats are mitigated in a timely manner to reduce exposure to security risks and maintain compliance with security standards.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`sd_vulnerabilities_performance`|
|**Category**|Software Development|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|16.12|Application Software Security|Implement Code-Level Security Checks|
|ISO 27001:2022|A.8.25|8 Technological controls|Secure development life cycle|
|NIST CSF v2.0|PR.PS-06|Platform Security (PR.PS)|PR.PS-06: Secure software development practices are integrated, and their performance is monitored throughout the software development life cycle|




### Users completed awareness training in the last 12 months

#### Description

The percentage of users who have completed security awareness training in the last 12 months, ensuring that employees are equipped with the latest knowledge to identify and mitigate cyber threats, which is critical for reducing organizational vulnerabilities and enhancing overall security posture.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`us_awareness`|
|**Category**|User Security|
|**SLO**|80.00% - 90.00%|
|**Weight**|0.4|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.6.3|6 People controls|Information security awareness, education and training|
|CIS 8.1|14.2|Security Awareness and Skills Training|Train Workforce Members to Recognize Social Engineering Attacks|
|CIS 8.1|14.3|Security Awareness and Skills Training|Train Workforce Members on Authentication Best Practices|
|CIS 8.1|14.4|Security Awareness and Skills Training|Train Workforce on Data Handling Best Practices|
|CIS 8.1|14.5|Security Awareness and Skills Training|Train Workforce Members on Causes of Unintentional Data Exposure|
|CIS 8.1|14.6|Security Awareness and Skills Training|Train Workforce Members on Recognizing and Reporting Security Incidents|
|CIS 8.1|14.7|Security Awareness and Skills Training|Train Workforce on How to Identify and Report if Their Enterprise Assets are Missing Security Updates|
|CIS 8.1|14.8|Security Awareness and Skills Training|Train Workforce on the Dangers of Connecting to and Transmitting Enterprise Data Over Insecure Networks|
|NIST CSF v2.0|PR.AT-01|Awareness and Training (PR.AT)|PR.AT-01: Personnel are provided with awareness and training so that they possess the knowledge and skills to perform general tasks with cybersecurity risks in mind|




### Systems with an up-to-date agent deployed

#### Description

The percentage of systems with up-to-date vulnerability management agents
deployed, providing critical visibility into security gaps and enabling swift
action to protect the organization from exploitable weaknesses.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_coverage`|
|**Category**|Vulnerability Management|
|**SLO**|80.00% - 95.00%|
|**Weight**|0.4|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|
|Essential8-ML1|ISM-1698|Patch applications|A vulnerability scanner is used at least daily to identify missing patches or updates for vulnerabilities in online services.|
|Essential8-ML2|ISM-1698|Patch applications|A vulnerability scanner is used at least daily to identify missing patches or updates for vulnerabilities in online services.|
|Essential8-ML3|ISM-1698|Patch applications|A vulnerability scanner is used at least daily to identify missing patches or updates for vulnerabilities in online services.|
|Essential8-ML1|ISM-1699|Patch applications|A vulnerability scanner is used at least weekly to identify missing patches or updates for vulnerabilities in office productivity suites, web browsers and their extensions, email clients, PDF software, and security products.|
|Essential8-ML2|ISM-1699|Patch applications|A vulnerability scanner is used at least weekly to identify missing patches or updates for vulnerabilities in office productivity suites, web browsers and their extensions, email clients, PDF software, and security products.|
|Essential8-ML3|ISM-1699|Patch applications|A vulnerability scanner is used at least weekly to identify missing patches or updates for vulnerabilities in office productivity suites, web browsers and their extensions, email clients, PDF software, and security products.|
|Essential8-ML1|ISM-1701|Patch operating systems|A vulnerability scanner is used at least daily to identify missing patches or updates for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices.|
|Essential8-ML2|ISM-1701|Patch operating systems|A vulnerability scanner is used at least daily to identify missing patches or updates for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices.|
|Essential8-ML3|ISM-1701|Patch operating systems|A vulnerability scanner is used at least daily to identify missing patches or updates for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices.|
|Essential8-ML1|ISM-1702|Patch operating systems|A vulnerability scanner is used at least fortnightly to identify missing patches or updates for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices.|
|Essential8-ML2|ISM-1702|Patch operating systems|A vulnerability scanner is used at least fortnightly to identify missing patches or updates for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices.|
|Essential8-ML3|ISM-1702|Patch operating systems|A vulnerability scanner is used at least fortnightly to identify missing patches or updates for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices.|
|Essential8-ML3|ISM-1703|Patch operating systems|A vulnerability scanner is used at least fortnightly to identify missing patches or updates for vulnerabilities in drivers.|
|Essential8-ML3|ISM-1900|Patch operating systems|A vulnerability scanner is used at least fortnightly to identify missing patches or updates for vulnerabilities in firmware.|




### Systems with an up-to-date vulnerability database deployed

#### Description

The percentage of systems with up-to-date vulnerability management agents
deployed with an up-to-date database, providing critical visibility into
security gaps and enabling swift action to protect the organization from
exploitable weaknesses.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_coverage`|
|**Category**|Vulnerability Management|
|**SLO**|80.00% - 95.00%|
|**Weight**|0.4|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|
|Essential8-ML1|ISM-1808|Patch applications|A vulnerability scanner with an up-to-date vulnerability database is used for vulnerability scanning activities.|
|Essential8-ML2|ISM-1808|Patch applications|A vulnerability scanner with an up-to-date vulnerability database is used for vulnerability scanning activities.|
|Essential8-ML3|ISM-1808|Patch applications|A vulnerability scanner with an up-to-date vulnerability database is used for vulnerability scanning activities.|
|Essential8-ML1|ISM-1808|Patch operating systems|A vulnerability scanner with an up-to-date vulnerability database is used for vulnerability scanning activities.|
|Essential8-ML2|ISM-1808|Patch operating systems|A vulnerability scanner with an up-to-date vulnerability database is used for vulnerability scanning activities.|
|Essential8-ML3|ISM-1808|Patch operating systems|A vulnerability scanner with an up-to-date vulnerability database is used for vulnerability scanning activities.|




### End-of-life - Systems running vendor-supported software

#### Description

Ensure that systems are not running end-of-life, unsuported or unpatchable
software.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_eol_software`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.8|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|2.2|Inventory and Control of Software Assets|Ensure Authorized Software is Currently Supported|
|NIST CSF v2.0|ID.AM-08|Asset Management (ID.AM)|ID.AM-08: Systems, hardware, software, services, and data are managed throughout their life cycles|
|Essential8-ML3|ISM-0304|Patch applications|Applications other than office productivity suites, web browsers and their extensions, email clients, PDF software, Adobe Flash Player, and security products that are no longer supported by vendors are removed.|
|Essential8-ML1|ISM-1704|Patch applications|Office productivity suites, web browsers and their extensions, email clients, PDF software, Adobe Flash Player, and security products that are no longer supported by vendors are removed.|
|Essential8-ML2|ISM-1704|Patch applications|Office productivity suites, web browsers and their extensions, email clients, PDF software, Adobe Flash Player, and security products that are no longer supported by vendors are removed.|
|Essential8-ML3|ISM-1704|Patch applications|Office productivity suites, web browsers and their extensions, email clients, PDF software, Adobe Flash Player, and security products that are no longer supported by vendors are removed.|
|Essential8-ML1|ISM-1905|Patch applications|Online services that are no longer supported by vendors are removed.|
|Essential8-ML2|ISM-1905|Patch applications|Online services that are no longer supported by vendors are removed.|
|Essential8-ML3|ISM-1905|Patch applications|Online services that are no longer supported by vendors are removed.|
|Essential8-ML3|ISM-1407|Patch operating systems|The latest release, or the previous release, of operating systems are used.|
|Essential8-ML1|ISM-1501|Patch operating systems|Operating systems that are no longer supported by vendors are replaced.|
|Essential8-ML2|ISM-1501|Patch operating systems|Operating systems that are no longer supported by vendors are replaced.|
|Essential8-ML3|ISM-1501|Patch operating systems|Operating systems that are no longer supported by vendors are replaced.|




### Vulnerabilities not remediated within SLO - critical and high

#### Description

The percentage of systems that were active in the last 30 days
that have resolved critical and high vulnerabilities within the agreed
Service Level Objective (SLO), providing critical insight into the
organisation's ability to minimize exposure to known threats and reduce
the attack surface effectively.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_critical`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Vulnerabilities not remediated within SLO - exploitable

#### Description

The percentage of systems that were active in the last 30 days
that have resolved exploitable vulnerabilities within the agreed
Service Level Objective (SLO), providing critical insight into the
organisation's ability to minimize exposure to known threats and reduce the
attack surface effectively.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_exploitable`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Vulnerabilities not remediated within SLO - exploitable patchable

#### Description

The percentage of systems that were active in the last 30 days
that have resolved exploitable, patchable vulnerabilities within the agreed
Service Level Objective (SLO), providing critical insight into the
organisation's ability to minimize exposure to known threats and reduce the
attack surface effectively.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_exploitable_patchable`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Vulnerabilities not remediated within SLO - exploitable patchable critical and high

#### Description

The percentage of systems that were active in the last 30 days
that have resolved exploitable, patchable, critical and high vulnerabilities
within the agreed Service Level Objective (SLO), providing critical insight
into the organisation's ability to minimize exposure to known threats and
reduce the attack surface effectively.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_exploitable_patchable_critical`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Vulnerabilities not remediated within SLO - patchable

#### Description

The percentage of systems that were active in the last 30 days
that have resolved patchable vulnerabilities within the agreed
Service Level Objective (SLO), providing critical insight into the
organisation's ability to minimize exposure to known threats and reduce the
attack surface effectively.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_patchable`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without vulnerabilities - exploitable and patchable critical and high

#### Description

The percentage of systems that were active in the last 30 days
that have vulnerabilities classified as critical or high priority, providing
critical insight into the organisation's ability to minimize exposure to
known threats and effectively reduce the attack surface.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_critical`|
|**Category**|Vulnerability Management|
|**SLO**|80.00% - 95.00%|
|**Weight**|0.2|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without vulnerabilities - exploitable and patchable critical and high

#### Description

The percentage of systems that have been active in the last 30
days and that have resolved exploitable vulnerabilities, providing
critical insight into the organisation's ability to minimize exposure to
known threats and effectively reduce the attack surface.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_exploitable`|
|**Category**|Vulnerability Management|
|**SLO**|80.00% - 95.00%|
|**Weight**|0.2|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without vulnerabilities in 48 hours - exploitable or critical and high

#### Description

The percentage of systems that have been active in the last 30
days and that have resolved exploitable or critical and high vulnerabilities published in the last 48 hours,
providing critical insight into the organisation's ability to minimize
exposure to known threats and effectively reduce the attack surface.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_exploitable_critical_48_hours`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.8|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|
|Essential8-ML3|ISM-1692|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in office productivity suites, web browsers and their extensions, email clients, PDF software, and security products are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist.|
|Essential8-ML1|ISM-1876|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in online services are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist.|
|Essential8-ML2|ISM-1876|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in online services are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist.|
|Essential8-ML3|ISM-1876|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in online services are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist.|
|Essential8-ML3|ISM-1696|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist.|
|Essential8-ML1|ISM-1877|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist.|
|Essential8-ML2|ISM-1877|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist.|
|Essential8-ML3|ISM-1877|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist.|
|Essential8-ML3|ISM-1879|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in drivers are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist.|
|Essential8-ML3|ISM-1903|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in firmware are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist.|




### Systems without vulnerabilities - exploitable and patchable critical and high

#### Description

The percentage of systems that were active in the last 30 days
that have resolved exploitable, patchable vulnerabilities, providing
critical insight into the organisation's ability to minimize exposure to
known threats and effectively reduce the attack surface.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_exploitable_patchable`|
|**Category**|Vulnerability Management|
|**SLO**|80.00% - 95.00%|
|**Weight**|0.8|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without vulnerabilities - exploitable and patchable critical and high

#### Description

The percentage of systems that were active in the last 30 days
taht have resolved exploitable, patchable vulnerabilities classified as
critical or high priority, providing critical insight into the
organisation's ability to minimize exposure to known threats and
effectively reduce the attack surface.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_exploitable_patchable_critical`|
|**Category**|Vulnerability Management|
|**SLO**|80.00% - 95.00%|
|**Weight**|0.8|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without vulnerabilities - non critical patched in 2 weeks

#### Description

The percentage of systems that have been active in the last 30
days and that have resolved non critical vulnerabilities published in the 2 weeks,
providing critical insight into the organisation's ability to minimize
exposure to known threats and effectively reduce the attack surface.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_non_critical_month`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.8|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|
|Essential8-ML1|ISM-1690|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in online services are applied within two weeks of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist.|
|Essential8-ML2|ISM-1690|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in online services are applied within two weeks of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist.|
|Essential8-ML3|ISM-1690|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in online services are applied within two weeks of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist.|
|Essential8-ML1|ISM-1691|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in office productivity suites, web browsers and their extensions, email clients, PDF software, and security products are applied within two weeks of release.|
|Essential8-ML2|ISM-1691|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in office productivity suites, web browsers and their extensions, email clients, PDF software, and security products are applied within two weeks of release.|
|Essential8-ML2|ISM-1700|Patch applications|A vulnerability scanner is used at least fortnightly to identify missing patches or updates for vulnerabilities in applications other than office productivity suites, web browsers and their extensions, email clients, PDF software, and security products.|
|Essential8-ML3|ISM-1700|Patch applications|A vulnerability scanner is used at least fortnightly to identify missing patches or updates for vulnerabilities in applications other than office productivity suites, web browsers and their extensions, email clients, PDF software, and security products.|
|Essential8-ML3|ISM-1901|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in office productivity suites, web browsers and their extensions, email clients, PDF software, and security products are applied within two weeks of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist.|
|Essential8-ML1|ISM-1694|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices are applied within two weeks of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist.|
|Essential8-ML2|ISM-1694|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices are applied within two weeks of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist.|
|Essential8-ML3|ISM-1694|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices are applied within two weeks of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist.|




### Systems without vulnerabilities - non critical patched in a month

#### Description

The percentage of systems that have been active in the last 30
days and that have resolved non critical vulnerabilities published in the last month,
providing critical insight into the organisation's ability to minimize
exposure to known threats and effectively reduce the attack surface.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_non_critical_month`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.8|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|
|Essential8-ML2|ISM-1693|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in applications other than office productivity suites, web browsers and their extensions, email clients, PDF software, and security products are applied within one month of release.|
|Essential8-ML3|ISM-1693|Patch applications|Patches, updates or other vendor mitigations for vulnerabilities in applications other than office productivity suites, web browsers and their extensions, email clients, PDF software, and security products are applied within one month of release.|
|Essential8-ML1|ISM-1695|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices are applied within one month of release.|
|Essential8-ML2|ISM-1695|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices are applied within one month of release.|
|Essential8-ML3|ISM-1697|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in drivers are applied within one month of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist.|
|Essential8-ML3|ISM-1902|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices are applied within one month of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist.|
|Essential8-ML3|ISM-1904|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in firmware are applied within one month of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist.|




### Systems without vulnerabilities - exploitable and patchable critical and high

#### Description

The percentage of systems that have been active in the last 30
days and that have patchable vulnerabilities providing critical insight
into the organisation's ability to minimize exposure to known threats and
effectively reduce the attack surface.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_patchable`|
|**Category**|Vulnerability Management|
|**SLO**|80.00% - 95.00%|
|**Weight**|0.8|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|



