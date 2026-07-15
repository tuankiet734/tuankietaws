---
title: "Establish Service Interconnection"
date: 2024-07-07
weight: 6
chapter: false
pre: " <b> 5.2.6. </b> "
---

### 5.2.6. Establish Service Interconnection

Once the individual resources are created and configured, we connect them to establish an end-to-end flow:

* **Link CloudFront to API Gateway:** Ensure your CloudFront Distribution targets the API Gateway endpoint as its Origin, caching static assets and routing dynamic request payloads optimally.
* **Configure Load Balancer Forwarding:** Verify that both `External-ALB` and `Internal-ALB` have their port `80` Listener default action configured to `Forward` traffic to the respective Target Groups.
* **Harden Web Server Security:** In the Security Group of the EC2 instances managed by the Auto Scaling Group, only allow inbound traffic on port `80` when originating from the Load Balancer's Security Group (Source). Restricting access this way instead of exposing it to the wide internet ensures maximum network level security.
