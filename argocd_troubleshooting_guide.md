# Argo CD Troubleshooting Guide

## Table of Contents
1. [Argo CD Service Definition](#argocd-service-definition)
    1. [Summary](#summary)
    2. [Service leads](#service-leads)
        1. [Primary](#primary)
        2. [Secondary](#secondary)
    3. [Application details](#application-details)
2. [Triage Process](#triage-process)
    1. [Initial triage](#initial-triage)
    2. [OpenShift platform issue](#openshift-platform-issue)
3. [Diagnostic Steps](#diagnostic-steps)
    1. [Argo CD UI is unavailable](#argocd-ui-is-unavailable)
    2. [Argo CD UI is available, but can't log in](#ui-available-but-cant-log-in)
        1. [Cluster-level instance](#cant-log-in-cluster)
        2. [Shared instance](#cant-log-in-shared)
    3. [Argo CD UI is available](#ui-available)
        1. [Application statuses are showing as "Unknown"](#statuses-unknown)
            1. [Cluster-level Argo CD](#status-unknown-cluster)
            2. [Shared Argo CD](#status-unknown-cluster)
        2. [Application synchronizations are failing](#syncs-failing)
4. [Support Services](#support-services)
    1. [Technical contacts](#technical-contacts)
5. [Resources](#resources)
    1. [Useful links](#useful-links)
    2. [Glossary of terms](#glossary)


## Argo CD Service Definition<a name="argocd-service-definition"></a>
### Summary<a name="summary"></a>
Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes.
- third party software with custom developed components (operator and build/deploy pipelines)
- operations and maintenance (patches, upgrades, config changes, features enablement)
- user support, app integration's assistance

### Service Leads<a name="service-leads"></a>
#### Primary<a name="primary"></a>
- Name: Cailey Jones
- Email: cailey.jones@gov.bc.ca
- Cell #:
- RC Handle: cailey.jones

#### Secondary<a name="secondary"></a>
- Name: Ian Watts
- Email: ian@48thave.com
- Cell #: 250-507-7854
- RC Handle: ian.watts

### Application Details<a name="application-details"></a>
- Cluster: ALL
- Namespace: argocd, argocd-shared
- Cluster-level instance of Argo CD
    - https://github.com/bcgov-c/platform-gitops-calgary-clab/tree/master/argocd
    - https://github.com/bcgov-c/platform-gitops-kamloops-klab/tree/master/argocd
    - https://github.com/bcgov-c/platform-gitops-kamloops-silver/tree/master/argocd
    - https://github.com/bcgov-c/platform-gitops-kamloops-gold/tree/master/argocd
    - https://github.com/bcgov-c/platform-gitops-calgary-golddr/tree/master/argocd
- Shared instance of Argo CD
    - https://github.com/bcgov-c/platform-gitops-calgary-clab/tree/master/argocd-shared
    - https://github.com/bcgov-c/platform-gitops-kamloops-klab/tree/master/argocd-shared
    - https://github.com/bcgov-c/platform-gitops-kamloops-silver/tree/master/argocd-shared
    - https://github.com/bcgov-c/platform-gitops-kamloops-gold/tree/master/argocd-shared
    - https://github.com/bcgov-c/platform-gitops-calgary-golddr/tree/master/argocd-shared
- Documents
    - ArgoCD Shared Instance Overview
        - https://docs.developer.gov.bc.ca/s/bn6v0ac6f9gue7hhirbg/protected-platform-services/d/c4a1sna1tev0e75glrb0/argocd-shared-instance-overview?currentPageId=c4a1uh21tev0e75glrcg&source=argo
    - ArgoCD Shared Instance RBAC Model
        - https://docs.developer.gov.bc.ca/s/bn6v0ac6f9gue7hhirbg/protected-platform-services/d/c4apsh21tev0e75gls3g/argocd-shared-instance-rbac-model?currentPageId=c4aptbq1tev0e75gls40&source=argo
    - User document
        - https://github.com/BCDevOps/openshift-wiki/tree/master/docs/ArgoCD
- Hosting model
    - One instance of Argo CD in each cluster for both the cluster-level and shared instances

## Triage Process<a name="triage-process"></a>
### Initial Triage<a name="initial-triage"></a>
- Is this related to OpenShift platform, ArgoCD, Vault or ArgoCD?
    - No?
        - Instruct to report in RocketChat #devops-operations
        - No further action is needed by 7-7000.
- Is this a platform wide concern? I.e. major outage of the critical service
    - No?
        - Instruct to report in RocketChat #devops-operations
        - No further action is needed by 7-7000.
- What time is it? Is it within regular business hours?
    - Yes?
        - Instruct to report issue in #devops-sos in RocketChat
        - No further action needed by 7-7000.
- Check Platform Status Page for the service in question
    - Does it show as Red?
        - Yes?
            - Skip to Step 2: Capture Project Details below
- Move to specific application troubleshooting steps below
### OpenShift Platform Issue<a name="openshift-platform-issue"></a>
- Ask caller to login to cluster console
    - Is the project hosted on Silver?
        - Yes?
            - Silver: https://console.apps.silver.devops.gov.bc.ca
    - Is the project hosted on Gold/GoldDR?
        - Yes?
            - Gold: https://console.apps.gold.devops.gov.bc.ca
            - GoldDR: https://console.apps.golddr.devops.gov.bc.ca
- Were they able to access the OpenShift dashboard?
    - No?
        - Was it a username / password issue?
            - Yes?
                - Instruct to report issue to their team
                - No further action needed by 7-7000.
        - Did they observe any error codes on login?
            - Yes?
                - Record error codes observed
                - Skip to Step 2: Capture Project Details below
        - Skip to Step 2: Capture Project Details below
    - Yes?
        - Instruct to report in RocketChat #devops-operations
        - No further action is needed by 7-7000.

## Diagnostic Steps<a name="diagnostic-steps"></a>
### Argo CD UI is unavailable<a name="argocd-ui-is-unavailable"></a>
Check the following critical resources in the 'argocd' or 'argocd-shared' namespace.
1. Deployment: argocd-server
   1. Are the pods running?
   2. If they are running, check the logs for details
2. Route: 'argocd-server'
   1. It should exist and be associated with the 'argocd-server' Service.  This is necessary for access to the UI.
3. Service: 'argocd-server'
   1. The Service should have running pods associated with it, 'argocd-server-xyz...'
4. Redis
   1. Note that the Redis service is not critical to the functioning of Argo CD.  "Redis is only used as a throw-away cache and can be lost. When lost, it will be rebuilt without loss of service."
   2. https://argo-cd.readthedocs.io/en/stable/operator-manual/high_availability/

### Argo CD UI is available, but can't log in<a name="ui-available-but-cant-log-in"></a>
#### Cluster-level instance<a name="cant-log-in-cluster"></a>
Access to the cluster-level instance of Argo CD is based on membership in the Keycloak group “argo_platform_admins” in the Realm “8gyaubgq”.
- Check group membership for the given GitHub ID
- Check availability of Keycloak

#### Shared instance<a name="cant-log-in-shared"></a>
As with the cluster-level instance, access is based on the Keycloak group “argo_platform_admins”.

User access to this instance is based on membership in a Keycloak group named “argocd_shared_licenseplate”, which grants write access, and “argocd_shared_licenseplate_readers”, which grants read-only access.  Project teams have the ability to manage membership in both of these groups by way of the “GitOpsTeam” custom resource definition.  For more information, see:
https://github.com/BCDevOps/openshift-wiki/tree/master/docs/ArgoCD

A user can only see the Projects that they have access to, as well as any Applications that are in those Projects.

### Argo CD UI is available<a name="ui-available"></a>
#### Application statuses are showing as "Unknown"<a name="statuses-unknown"></a>
Argo CD cannot read from the git repository that is listed as the Source Repository in the Application.  Access to the GitHub gitops repos is managed by an SSH key.

##### Cluster-level Argo CD<a name="status-unknown-cluster"></a>
An SSH key is added as a Deploy Key in the GitHub repos (Settings --> Security --> Deploy keys).
In Argo CD, the connection with the SSH key is added as a Credentials Template (Settings --> Repositories).  It is not possible to view the SSH key in the Argo CD UI, but if necessary an existing credentials template could be deleted and recreated.  To do so:
- Click "Connect Repo Using SSH"
- Project: default
- Repository URL:
    - Use the SSH format: git@github.com:ORGNAME, such as: git@github.com:bcgov-c/
    - Because you will save this as a credentials template, do not include a specific repository name, just end the URL with "orgname/"
- SSH private key data: Enter the private key of the SSH key pair
- Click "Save as Credentials Template"


##### Shared Argo CD<a name="status-unknown-cluster"></a>
On the GitHub side, read access to the repos is configured by way of the "GitOps-Readers" team, which includes the "RoboWitness" user.
Each repo to which Argo CD requires read access is included in the repository list for the user.  For the shared Argo CD instances, the gitops repos are added to the team automatically by the Warden Operator.
On the Argo CD side, access is configured in the same way as for the cluster-level instance:
- In Argo CD, the connection with the SSH key is added as a Credentials Template (Settings --> Repositories).  It is not possible to view the
SSH key in the Argo CD UI, but if necessary an existing credentials template could be deleted and recreated.  To do so:
    - Click "Connect Repo Using SSH"
    - Project: default
    - Repository URL:
        - Use the SSH format: git@github.com:ORGNAME, such as: git@github.com:bcgov-c/
        - Because you will save this as a credentials template, do not include a specific repository name, just end the URL with "orgname/"
    - SSH private key data: Enter the private key of the SSH key pair
    - Click "Save as Credentials Template"

#### Application synchronizations are failing<a name="syncs-failing"></a>
The log messages are generally quite helpful.  Click on the app in question and click either the "Sync Status" button or the link below "Last Sync Result".

## Support Services<a name="support-services"></a>
### ArgoCD Support Contacts
Argo CD is open-source software and is used without a license or paid support.

### Hours of Availability
N/A

### Response / Resolution Times
N/A

### Technical Contacts<a name="technical-contacts"></a>
Cailey Jones
Ian Watts
Shelly Han
Steven Barre

### Severity Definitions
N/A

## Resources<a name="resources"></a>
### Useful links<a name="useful-links"></a>
- Platform Services Team's Supported Services Sheet
    - https://docs.google.com/spreadsheets/d/1pvaxCdYts1MeRv7bHP10a1yt_MGk6KpK/edit?usp=sharing&ouid=117522969697637793376&rtpof=true&sd=true
- DevSecOps Escalation Flow
    - https://app.mural.co/t/platformservices5977/m/platformservices5977/1630361745516/95ef7c6ef41a6329dd54913d14d1280fd567e2c4?sender=u1b7f725325763913e60b4808
- Platform Status Page
    - https://status.developer.gov.bc.ca
- ArgoCD Documentation
    - https://argoproj.github.io/argo-cd/
- Vault Documentation
    - https://www.vaultproject.io/docs
- OpenShift Container Platform Service Definition
    - https://developer.gov.bc.ca/BC-Gov-PaaS-OpenShift-Platform-Service-Definition

### Glossary of terms (\*Critical)<a name="glossary"></a>
- Aqua:  Container scanning for vulnerabilities and deployment security enforcement solution for Kubernetes, Docker, OpenShift, Fargate, Lambd
a, AWS & other container platforms.
- ArgoCD: a declarative, GitOps continuous delivery tool for Kubernetes that product teams use to automate deployment of their apps.
- Artifactory: Artifactory provides cached access to a number of publicly available and secure repositories held by other organizations. Access to the remote (caching) repositories is currently available by default to anyone on the Silver or Gold Clusters.
- CCM: Cluster Config Manager applies and enforces k8s objects used for managing the cluster and other core applications
- DevHub: DevHub serves as a central information portal for developers looking for any content related to developing on the BC Gov DevOps Platform such as service definitions, manuals, pro-tips and self-help docs.  It is available at  https://developer.gov.bc.ca  The DevHub itself does not store any information but instead pulls it from various sources as mentioned above and enables searching through the content. At this moment, DevHub only supports access to public content, that is why we use Documize for the content that needs to be protected.
- Documize: This open source content management tool used by the Platform Services Team for storing sensitive technical documentation that is not appropriate for the public space in GitHub. Access to the protected content in https://docs.developer.gov.bc.ca  is available to product teams using GitHub ID or IDIR after access has been manually granted to the user by the Platform Services Team.
- EnterpriseDB Operator (EDB): EDB is a product providing High Availability capability for PostgreSQL clusters. Teams are required to purchase their own EDB license before using this service. The platform services team controls and maintains a cluster-wide version of the EDB operator in the Silver cluster of Openshift Platform which licensed teams can access from their apps via CRDs.
- Mobile Signing Service (MSS): The Mobile Signing Service (MSS) allows teams developing mobile applications to sign said applications using BC Government’s signing key before publishing in Google Playstore and Apple AppStore.
- Platform Services Registry: This service provides self-serve access for product teams to request provisioning of projects on the Openshift 4 Platform.
- RocketChat: All in one communications platform: team collaboration, omnichannel engagement, DevOps and ChatOps. Access to RocketChat at https://chat.developer.gov.bc.ca is available either using GitHub ID (membership in GitHub’s BCDevOps org is required) or IDIR.
- Sysdig Monitoring Service: This service enables product teams to build monitoring dashboards for their apps hosted on the Platform.
- Vault: This secret management service is built using the Hashicorp Vault product and is used by product teams to secure, store, and tightly control access to tokens, passwords, certificates, API keys, and other secrets used in Platform apps.

