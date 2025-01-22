

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

|**Category**|**Title**|**Type**|**Query**|
|--|--|--|--|
|**Data Protection**|||||
||[Systems with their volumes encrypted](#systems-with-their-volumes-encrypted)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
||[Systems with backups configured per their SLO](#systems-with-backups-configured-per-their-slo)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
||[Systems that has had a successful backup per their SLO](#systems-that-has-had-a-successful-backup-per-their-slo)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![No](https://img.shields.io/badge/NO-00F)|
|**Identity**|||||
||[Identities with MFA](#identities-with-mfa)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
||[Accounts without Admin privileges](#accounts-without-admin-privileges)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
|**Identity Management**|||||
||[Identity - Credentials - Regular Password Rotation](#identity---credentials---regular-password-rotation)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Identity - Inactive Identities](#identity---inactive-identities)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
|**Malware**|||||
||[Systems with an up-to-date agent deployed](#systems-with-an-up-to-date-agent-deployed)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
|**Network**|||||
||[External endpoints with insecure ports exposed](#external-endpoints-with-insecure-ports-exposed)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|
||[External endpoints protected by a WAF](#external-endpoints-protected-by-a-waf)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
|**Development**|||||
||[Repositories with SAST / DAST scanning enabled](#repositories-with-sast-/-dast-scanning-enabled)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
||[Repositories without exploitable vulnerabilities remediated within SLO](#repositories-without-exploitable-vulnerabilities-remediated-within-slo)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![No](https://img.shields.io/badge/NO-00F)|
|**Software Development**|||||
||[Repositories without exploitable vulnerabilities](#repositories-without-exploitable-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
|**User Security**|||||
||[Users completed awareness training in the last 12 months](#users-completed-awareness-training-in-the-last-12-months)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![yes](https://img.shields.io/badge/YES-00F0)|
|**Vulnerability Management**|||||
||[Systems with an up-to-date agent deployed](#systems-with-an-up-to-date-agent-deployed)|![control](https://img.shields.io/badge/CONTROL-0000F0)|![No](https://img.shields.io/badge/NO-00F)|
||[Systems without Critical and High vulnerabilities](#systems-without-critical-and-high-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Critical vulnerabilities patched within SLO](#critical-vulnerabilities-patched-within-slo)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![yes](https://img.shields.io/badge/YES-00F0)|
||[Systems without exploitable vulnerabilities](#systems-without-exploitable-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![yes](https://img.shields.io/badge/YES-00F0)|
|**Vulnerability**|||||
||[Systems without exploitable patchable vulnerabilities remediated within SLO](#systems-without-exploitable-patchable-vulnerabilities-remediated-within-slo)|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)|![No](https://img.shields.io/badge/NO-00F)|
||[Systems without exploitable patchable vulnerabilities](#systems-without-exploitable-patchable-vulnerabilities)|![risk](https://img.shields.io/badge/RISK-c00000)|![No](https://img.shields.io/badge/NO-00F)|


## List of metrics
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
|ISO 27001:2022|A.8.24|8 Technological controls|Use of cryptography|
|CIS 8.1|3.11|Data Protection|Encrypt Sensitive Data at Rest|
|NIST CSF v2.0|PR.DS-01|Data Security (PR.DS)|PR.DS-01: The confidentiality, integrity, and availability of data-at-rest are protected|




### Systems with backups configured per their SLO

#### Description

The percentage of systems with backups configured in accordance with their Service Level Objectives (SLO), ensuring critical data can be restored in the event of a failure, which is essential for maintaining business continuity and mitigating the impact of data loss.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`dr_backup_coverage`|
|**Category**|Data Protection|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.13|8 Technological controls|Information backup|
|CIS 8.1|11.2|Data Recovery|Perform Automated Backups|
|NIST CSF v2.0|PR.DS-11|Data Security (PR.DS)|PR.DS-11: Backups of data are created, protected, maintained, and tested|




### Systems that has had a successful backup per their SLO

#### Description

The percentage of systems that successfully complete backups within their defined Service Level Objectives (SLO), ensuring data integrity and availability, which is critical for minimizing downtime, protecting against data loss, and maintaining business continuity in the event of an incident.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`dr_backup_performance`|
|**Category**|Data Protection|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.13|8 Technological controls|Information backup|
|CIS 8.1|11.2|Data Recovery|Perform Automated Backups|
|NIST CSF v2.0|PR.DS-11|Data Security (PR.DS)|PR.DS-11: Backups of data are created, protected, maintained, and tested|




### Identities with MFA

#### Description

The percentage of user accounts secured with multi-factor authentication, a critical metric that quantifies the effectiveness of identity protection by reducing the risk of unauthorized access and safeguarding sensitive assets, making it vital for minimizing the impact of credential-based attacks.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`im_authentication_mfa`|
|**Category**|Identity|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.5.17|5 Organizational controls|Authentication information|
|CIS 8.1|6.3|Access Control Management|Require MFA for Externally-Exposed Applications|
|CIS 8.1|6.4|Access Control Management|Require MFA for Remote Network Access|
|CIS 8.1|6.5|Access Control Management|Require MFA for Administrative Access|
|NIST CSF v2.0|PR.AA-03|Identity Management, Authentication, and Access Control (PR.AA)|PR.AA-03: Users, services, and hardware are authenticated|




### Identity - Credentials - Regular Password Rotation

#### Description

Regular password rotation ensures that credentials are periodically updated, reducing the risk of unauthorized access from compromised or stale passwords, which is critical to maintaining the security of your organization's systems and data.


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

Dormant Identities tracks the number of unused or inactive accounts within the organization, providing critical insight into potential security risks as dormant accounts are prime targets for unauthorized access and exploitation, making their identification and timely deactivation essential for reducing the attack surface and maintaining robust access controls.


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
|**Category**|Identity|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.2|8 Technological controls|Privileged access rights|
|CIS 8.1|5.4|Account Management|Restrict Administrator Privileges to Dedicated Administrator Accounts|
|NIST CSF v2.0|PR.AA-05|Identity Management, Authentication, and Access Control (PR.AA)|PR.AA-05: Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed, and incorporate the principles of least privilege and separation of duties|




### Systems with an up-to-date agent deployed

#### Description

The percentage of systems with an up-to-date malware detection agent deployed, ensuring the organization’s defenses are robust against the latest threats, and is critical for minimizing vulnerability to malware attacks.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`mp_coverage`|
|**Category**|Malware|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.7|8 Technological controls|Protection against malware|
|CIS 8.1|10.1|Malware Defenses|Deploy and Maintain Anti-Malware Software|
|NIST CSF v2.0|PR.PS-05|Platform Security (PR.PS)|PR.PS-05: Installation and execution of unauthorized software are prevented|




### External endpoints with insecure ports exposed

#### Description

The "Insecure Ports" metric tracks external endpoints with open ports that are improperly configured or vulnerable, highlighting potential entry points for cyberattacks, which is critical for reducing the organization's exposure to exploitation and ensuring the security of its network infrastructure.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`ne_insecure_ports`|
|**Category**|Network|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.20|8 Technological controls|Networks security|
|CIS 8.1|12.2|Network Infrastructure Management|Establish and Maintain a Secure Network Architecture|
|NIST CSF v2.0|PR.DS-02|Data Security (PR.DS)|PR.DS-02: The confidentiality, integrity, and availability of data-in-transit are protected|




### External endpoints protected by a WAF

#### Description

The "Network Application Firewall: External Endpoints Protected by a WAF" metric measures the proportion of external-facing endpoints shielded by a Web Application Firewall (WAF), highlighting an organization's ability to prevent unauthorized access, mitigate threats like SQL injection and cross-site scripting, and safeguard critical systems from cyberattacks, making it a key indicator of external-facing application security.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`ne_waf`|
|**Category**|Network|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.20|8 Technological controls|Networks security|
|CIS 8.1|13.3|Network Monitoring and Defense|Deploy a Network Intrusion Detection Solution|
|NIST CSF v2.0|PR.IR-01|Technology Infrastructure Resilience (PR.IR)|PR.IR-01: Networks and environments are protected from unauthorized logical access and usage|




### Repositories with SAST / DAST scanning enabled

#### Description

The percentage of code repositories with Static Application Security Testing (SAST) and Dynamic Application Security Testing (DAST) scanning enabled, ensuring early detection of vulnerabilities during development and reducing the risk of security breaches before code is deployed.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`sd_repository_coverage`|
|**Category**|Development|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![control](https://img.shields.io/badge/CONTROL-0000F0)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.25|8 Technological controls|Secure development life cycle|
|CIS 8.1|16.12|Application Software Security|Implement Code-Level Security Checks|
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
|**Category**|Development|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.25|8 Technological controls|Secure development life cycle|
|CIS 8.1|16.12|Application Software Security|Implement Code-Level Security Checks|
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

The percentage of systems with up-to-date vulnerability management agents deployed, providing critical visibility into security gaps and enabling swift action to protect the organization from exploitable weaknesses.


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




### Systems without Critical and High vulnerabilities

#### Description

Ensure that all systems do not have any urgent vulnerabilities that can impact the risk.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_critical`|
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




### Critical vulnerabilities patched within SLO

#### Description

Ensure that all systems do not have any urgent vulnerabilities that can impact the risk.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_critical_patching`|
|**Category**|Vulnerability Management|
|**SLO**|80.00% - 95.00%|
|**Weight**|0.2|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.5|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Internal Enterprise Assets|
|CIS 8.1|7.6|Continuous Vulnerability Management|Perform Automated Vulnerability Scans of Externally-Exposed Enterprise Assets|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without exploitable vulnerabilities

#### Description

Ensure that all systems do not have any explotable vulnerabilities that can be patched.


#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_explot_patchable`|
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




### Systems without exploitable patchable vulnerabilities remediated within SLO

#### Description

The percentage of systems that have resolved exploitable, patchable vulnerabilities within the agreed Service Level Objective (SLO), providing critical insight into the organization's ability to minimize exposure to known threats and reduce the attack surface effectively.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_performance_patchable`|
|**Category**|Vulnerability|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![performance](https://img.shields.io/badge/PERFORMANCE-0F00)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.7|Continuous Vulnerability Management|Remediate Detected Vulnerabilities|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|




### Systems without exploitable patchable vulnerabilities

#### Description

The percentage of systems within the organization that are free of known exploitable vulnerabilities with available patches, highlighting the organization's ability to reduce risk through timely patch management and ensuring a secure operational environment.

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`vm_risk_patchable`|
|**Category**|Vulnerability|
|**SLO**|90.00% - 95.00%|
|**Weight**|0.5|
|**Type**|![risk](https://img.shields.io/badge/RISK-c00000)

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
|ISO 27001:2022|A.8.8|8 Technological controls|Management of technical vulnerabilities|
|CIS 8.1|7.3|Continuous Vulnerability Management|Perform Automated Operating System Patch Management|
|CIS 8.1|7.4|Continuous Vulnerability Management|Perform Automated Application Patch Management|
|NIST CSF v2.0|ID.RA-01|Risk Assessment (ID.RA)|ID.RA-01: Vulnerabilities in assets are identified, validated, and recorded|



