

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
|**Access Control**|||||
||[Access Control - Account Deactivation Timeliness](#access-control---account-deactivation-timeliness)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Access Control - Leavers with Disabled Accounts](#access-control---leavers-with-disabled-accounts)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
|**Asset Management**|||||
||[Asset Management - Asset Discovery Coverage](#asset-management---asset-discovery-coverage)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
|**Data Protection**|||||
||[Data Protection - Volume Encryption Coverage](#data-protection---volume-encryption-coverage)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
|**Disaster Recovery**|||||
||[Disaster Recovery - Backup Configuration Coverage](#disaster-recovery---backup-configuration-coverage)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
||[Disaster Recovery - Backup Success Rate](#disaster-recovery---backup-success-rate)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![No](https://img.shields.io/badge/NO-00F)|
|**Identity Management**|||||
||[Identity Management - Multi-Factor Authentication Coverage](#identity-management---multi-factor-authentication-coverage)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Identity Management - Password Rotation Compliance](#identity-management---password-rotation-compliance)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Identity Management - Inactive Account Detection](#identity-management---inactive-account-detection)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Identity Management - Phishing-Resistant MFA Coverage](#identity-management---phishing-resistant-mfa-coverage)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Identity Management - Privileged Account Control](#identity-management---privileged-account-control)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
|**Malware Protection**|||||
||[Malware Protection - Agent Deployment Coverage](#malware-protection---agent-deployment-coverage)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
|**Network Security**|||||
||[Network Security - DNS Domains Expiring Within the Next Month](#network-security---dns-domains-expiring-within-the-next-month)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Network Security - DNS Domains with SPF configured](#network-security---dns-domains-with-spf-configured)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Network Security - DNS Domains with DMARC Configured](#network-security---dns-domains-with-dmarc-configured)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Network Security - External endpoints with insecure ports exposed](#network-security---external-endpoints-with-insecure-ports-exposed)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
||[Network Security - External endpoints protected by a WAF](#network-security---external-endpoints-protected-by-a-waf)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
|**Software Development**|||||
||[SDLC - Repositories with SAST / DAST scanning enabled](#sdlc---repositories-with-sast-/-dast-scanning-enabled)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
||[SDLC - Repositories without exploitable vulnerabilities](#sdlc---repositories-without-exploitable-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[SDLC - Repositories without exploitable vulnerabilities remediated within SLO](#sdlc---repositories-without-exploitable-vulnerabilities-remediated-within-slo)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
|**User Security**|||||
||[User Security - Awareness Training Completion](#user-security---awareness-training-completion)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
||[User Security - Phishing Simulation Resilience](#user-security---phishing-simulation-resilience)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
|**Vulnerability Management**|||||
||[Vulnerability Management - Agent Deployment Coverage](#vulnerability-management---agent-deployment-coverage)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems with an up-to-date vulnerability database deployed](#systems-with-an-up-to-date-vulnerability-database-deployed)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
||[End-of-life - Systems running vendor-supported software](#end-of-life---systems-running-vendor-supported-software)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Vulnerability Management - Macs without actively exploited macOS vulnerabilities](#vulnerability-management---macs-without-actively-exploited-macos-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Vulnerabilities not remediated within SLO - exploitable patchable critical and high](#vulnerabilities-not-remediated-within-slo---exploitable-patchable-critical-and-high)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Application vulnerabilities not mitigated within SLO - non-patchable exploitable](#application-vulnerabilities-not-mitigated-within-slo---non-patchable-exploitable)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[OS vulnerabilities not mitigated within SLO - non-patchable exploitable](#os-vulnerabilities-not-mitigated-within-slo---non-patchable-exploitable)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Vulnerabilities not remediated within SLO - patchable](#vulnerabilities-not-remediated-within-slo---patchable)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Application vulnerabilities not remediated within SLO - patchable exploitable](#application-vulnerabilities-not-remediated-within-slo---patchable-exploitable)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[OS vulnerabilities not remediated within SLO - patchable exploitable](#os-vulnerabilities-not-remediated-within-slo---patchable-exploitable)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[OS vulnerabilities not remediated within SLO - patchable non-exploitable](#os-vulnerabilities-not-remediated-within-slo---patchable-non-exploitable)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without non-patchable exploitable application vulnerabilities](#systems-without-non-patchable-exploitable-application-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without non-patchable exploitable OS vulnerabilities](#systems-without-non-patchable-exploitable-os-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without non-patchable non-exploitable application vulnerabilities](#systems-without-non-patchable-non-exploitable-application-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without non-patchable non-exploitable OS vulnerabilities](#systems-without-non-patchable-non-exploitable-os-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without patchable exploitable application vulnerabilities](#systems-without-patchable-exploitable-application-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without patchable exploitable OS vulnerabilities](#systems-without-patchable-exploitable-os-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without patchable non-exploitable application vulnerabilities](#systems-without-patchable-non-exploitable-application-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without patchable non-exploitable OS vulnerabilities](#systems-without-patchable-non-exploitable-os-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|


## List of metrics
### Access Control - Account Deactivation Timeliness

#### Description

This metric tracks the percentage of terminated user accounts that are 
disabled within defined timeframes, ensuring that departing employees 
or contractors do not retain unauthorized access to enterprise systems 
and data.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`ac_access_revoking`|
|**Category**|Access Control|
|**SLO**|98.00% - 99.00%|
|**Weight**|0.9|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.5.17|5 Organizational controls|Authentication information|
|CIS 8.1|6.2|Access Control Management|Establish an Access Revoking Process|
|NIST CSF v2.0|PR.AA-05|Identity Management, Authentication, and Access Control (PR.AA)|PR.AA-05: Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed, and incorporate the principles of least privilege and separation of duties|




### Access Control - Leavers with Disabled Accounts

#### Description

The percentage of people who have left the organisation whose identity
account has been disabled, ensuring former staff cannot keep accessing
company systems and data after their employment ends.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`ac_leavers_disabled`|
|**Category**|Access Control|
|**SLO**|98.00% - 100.00%|
|**Weight**|0.8|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.5.18|5 Organizational controls|Access rights|
|CIS 8.1|6.2|Access Control Management|Establish an Access Revoking Process|
|NIST CSF v2.0|PR.AA-05|Identity Management, Authentication, and Access Control (PR.AA)|PR.AA-05: Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed, and incorporate the principles of least privilege and separation of duties|




### Asset Management - Asset Discovery Coverage

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




### Data Protection - Volume Encryption Coverage

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




### Disaster Recovery - Backup Configuration Coverage

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




### Disaster Recovery - Backup Success Rate

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




### Identity Management - Multi-Factor Authentication Coverage

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




### Identity Management - Password Rotation Compliance

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
|CIS 8.1|5.2|Account Management|Use Unique Passwords|




### Identity Management - Inactive Account Detection

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




### Identity Management - Phishing-Resistant MFA Coverage

#### Description

The percentage of active user accounts with a phishing-resistant
multi-factor authentication method enrolled, protecting accounts against
adversary-in-the-middle phishing and push fatigue attacks that defeat
one-time codes and push notifications.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`im_phishing_resistant_mfa`|
|**Category**|Identity Management|
|**SLO**|80.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.5|8 Technological controls|Secure authentication|
|CIS 8.1|6.3|Access Control Management|Require MFA for Externally-Exposed Applications|
|CIS 8.1|6.5|Access Control Management|Require MFA for Administrative Access|
|NIST CSF v2.0|PR.AA-03|Identity Management, Authentication, and Access Control (PR.AA)|PR.AA-03: Users, services, and hardware are authenticated|
|Essential8-ML2|ISM-1682|Multi-factor authentication|Multi-factor authentication used for authenticating users of systems is phishing-resistant.|
|Essential8-ML3|ISM-1682|Multi-factor authentication|Multi-factor authentication used for authenticating users of systems is phishing-resistant.|
|Essential8-ML2|ISM-1872|Multi-factor authentication|Multi-factor authentication used for authenticating users of online services is phishing-resistant.|
|Essential8-ML3|ISM-1872|Multi-factor authentication|Multi-factor authentication used for authenticating users of online services is phishing-resistant.|




### Identity Management - Privileged Account Control

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




### Malware Protection - Agent Deployment Coverage

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




### Network Security - External endpoints with insecure ports exposed

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




### Network Security - External endpoints protected by a WAF

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




### SDLC - Repositories with SAST / DAST scanning enabled

#### Description

The percentage of code repositories with Static Application
Security Testing (SAST) and Dynamic Application Security Testing (DAST)
scanning enabled, ensuring early detection of vulnerabilities during
development and reducing the risk of security breaches before code is
deployed.


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




### SDLC - Repositories without exploitable vulnerabilities

#### Description

The percentage of code repositories free from known security
flaws, ensuring that development efforts prioritize secure coding practices,
reduce the risk of breaches, and maintain the integrity of the software
development lifecycle. This metric is important as it directly impacts the
organization's ability to deliver secure products and protect against
potential cyber threats.


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




### SDLC - Repositories without exploitable vulnerabilities remediated within SLO

#### Description

The percentage of code repositories in the development pipeline
that have resolved critical security vulnerabilities within the established
service level objective (SLO), ensuring that potential threats are mitigated
in a timely manner to reduce exposure to security risks and maintain
compliance with security standards.


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




### User Security - Awareness Training Completion

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




### User Security - Phishing Simulation Resilience

#### Description

The percentage of users who did not fall for any simulated phishing email in
the last 12 months, showing how well staff recognise and resist social
engineering attacks.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`us_phishing_simulation`|
|**Category**|User Security|
|**SLO**|80.00% - 90.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.6.3|6 People controls|Information security awareness, education and training|
|CIS 8.1|14.2|Security Awareness and Skills Training|Train Workforce Members to Recognize Social Engineering Attacks|
|NIST CSF v2.0|PR.AT-01|Awareness and Training (PR.AT)|PR.AT-01: Personnel are provided with awareness and training so that they possess the knowledge and skills to perform general tasks with cybersecurity risks in mind|




### Vulnerability Management - Agent Deployment Coverage

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
|**Metric id**|`vm_coverage_database`|
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




### Vulnerability Management - Macs without actively exploited macOS vulnerabilities

#### Description

The percentage of Macs running a macOS version with no known actively
exploited vulnerabilities that a later release has already fixed, measuring
how quickly critical operating system updates reach the fleet.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_macos_exploited_cves`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 98.00%|
|**Weight**|0.8|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.3|Continuous Vulnerability Management|Perform Automated Operating System Patch Management|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|
|Essential8-ML1|ISM-1695|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices are applied within one month of release.|
|Essential8-ML2|ISM-1695|Patch operating systems|Patches, updates or other vendor mitigations for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices are applied within one month of release.|




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




### Application vulnerabilities not mitigated within SLO - non-patchable exploitable

#### Description

The percentage of systems that were active in the last 30 days
that have addressed non-patchable, exploitable application vulnerabilities within the agreed
Service Level Objective (SLO), providing critical insight into the
organisation's "Isolation Protocol" - Contain or remove effectiveness.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_non_patchable_exploitable_apps`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.8|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### OS vulnerabilities not mitigated within SLO - non-patchable exploitable

#### Description

The percentage of systems that were active in the last 30 days
that have addressed non-patchable, exploitable operating system vulnerabilities within the agreed
Service Level Objective (SLO), providing critical insight into the
organisation's "Emergency Mitigations" - Compensating controls NOW effectiveness.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_non_patchable_exploitable_os`|
|**Category**|Vulnerability Management|
|**SLO**|95.00% - 98.00%|
|**Weight**|0.9|
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




### Application vulnerabilities not remediated within SLO - patchable exploitable

#### Description

The percentage of systems that were active in the last 30 days
that have resolved patchable, exploitable application vulnerabilities within the agreed
Service Level Objective (SLO), providing critical insight into the
organisation's "Quick Wins" - Update the software effectiveness.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_patchable_exploitable_apps`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.8|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### OS vulnerabilities not remediated within SLO - patchable exploitable

#### Description

The percentage of systems that were active in the last 30 days
that have resolved patchable, exploitable operating system vulnerabilities within the agreed
Service Level Objective (SLO), providing critical insight into the
organisation's "Patch Tuesday Priority" - Just bloody patch it effectiveness.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_patchable_exploitable_os`|
|**Category**|Vulnerability Management|
|**SLO**|95.00% - 98.00%|
|**Weight**|0.9|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### OS vulnerabilities not remediated within SLO - patchable non-exploitable

#### Description

The percentage of systems that were active in the last 30 days
that have resolved patchable, non-exploitable operating system vulnerabilities within the agreed
Service Level Objective (SLO), providing insight into the
organisation's "Standard Cycle" - Include in regular patching effectiveness.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_patchable_non_exploitable_os`|
|**Category**|Vulnerability Management|
|**SLO**|85.00% - 90.00%|
|**Weight**|0.4|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without non-patchable exploitable application vulnerabilities

#### Description

The percentage of systems that were active in the last 30 days
that have addressed non-patchable, exploitable application vulnerabilities,
providing critical insight into the organisation's "Isolation Protocol"
capability to contain or remove vulnerable applications.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_non_patchable_exploitable_apps`|
|**Category**|Vulnerability Management|
|**SLO**|85.00% - 95.00%|
|**Weight**|0.8|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without non-patchable exploitable OS vulnerabilities

#### Description

The percentage of systems that were active in the last 30 days
that have addressed non-patchable, exploitable operating system vulnerabilities,
providing critical insight into the organisation's "Emergency Mitigations"
capability requiring compensating controls NOW.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_non_patchable_exploitable_os`|
|**Category**|Vulnerability Management|
|**SLO**|90.00% - 98.00%|
|**Weight**|0.9|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without non-patchable non-exploitable application vulnerabilities

#### Description

The percentage of systems that were active in the last 30 days
that have addressed non-patchable, non-exploitable application vulnerabilities,
providing insight into the organisation's "Backlog" management
for vulnerabilities that should be documented and reviewed periodically.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_non_patchable_non_exploitable_apps`|
|**Category**|Vulnerability Management|
|**SLO**|50.00% - 75.00%|
|**Weight**|0.1|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without non-patchable non-exploitable OS vulnerabilities

#### Description

The percentage of systems that were active in the last 30 days
that have addressed non-patchable, non-exploitable operating system vulnerabilities,
providing insight into the organisation's "Monitor & Plan" capability
to watch for exploits and plan replacement strategies.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_non_patchable_non_exploitable_os`|
|**Category**|Vulnerability Management|
|**SLO**|60.00% - 80.00%|
|**Weight**|0.2|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without patchable exploitable application vulnerabilities

#### Description

The percentage of systems that were active in the last 30 days
that have resolved patchable, exploitable application vulnerabilities,
providing critical insight into the organisation's ability to minimize
exposure to "Quick Wins" threats by updating software and effectively reduce the attack surface.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_patchable_exploitable_apps`|
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




### Systems without patchable exploitable OS vulnerabilities

#### Description

The percentage of systems that were active in the last 30 days
that have resolved patchable, exploitable operating system vulnerabilities,
providing critical insight into the organisation's ability to minimize
exposure to "Patch Tuesday Priority" threats and effectively reduce the attack surface.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_patchable_exploitable_os`|
|**Category**|Vulnerability Management|
|**SLO**|85.00% - 98.00%|
|**Weight**|0.9|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without patchable non-exploitable application vulnerabilities

#### Description

The percentage of systems that were active in the last 30 days
that have resolved patchable, non-exploitable application vulnerabilities,
providing insight into the organisation's "Maintenance Queue" effectiveness
for vulnerabilities that should be updated when convenient.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_patchable_non_exploitable_apps`|
|**Category**|Vulnerability Management|
|**SLO**|70.00% - 85.00%|
|**Weight**|0.3|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without patchable non-exploitable OS vulnerabilities

#### Description

The percentage of systems that were active in the last 30 days
that have resolved patchable, non-exploitable operating system vulnerabilities,
providing insight into the organisation's "Standard Cycle" patching effectiveness
for vulnerabilities that should be included in regular patching cycles.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_posture_patchable_non_exploitable_os`|
|**Category**|Vulnerability Management|
|**SLO**|75.00% - 90.00%|
|**Weight**|0.4|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|



