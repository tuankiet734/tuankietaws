---
title: "Event 2"
date: 2026-06-06
weight: 3
chapter: false
pre: " <b> 4.3. </b> "
---

# Summary Report: "FCAJ Community Day 2026"

### Event Information

- **Event Name:** FCAJ Community Day 2026
- **Date & Time:** Saturday, June 6, 2026
- **Location:** Bitexco Financial Tower, Ho Chi Minh City
- **Role:** Attendee

### Event Objectives

FCAJ Community Day in June was organized to share practical knowledge and industry experience in Cloud Computing, AI, DevOps, Cyber Security, and software development on AWS. Through sessions delivered by engineers and speakers working in the technology field, participants had the opportunity to learn about new technologies, understand how systems are built on AWS, and gain clearer career orientation in IT.

Besides technical updates, the event also created a chance for students to connect with the AWS community, learn from real projects, and broaden their understanding of the skills needed in a professional working environment.

### Key Topics

#### Docker - A Containerization Technology

**Speaker:** Anh Bao Huynh

The first topic focused on the challenge of deploying applications consistently across different environments. Traditional virtual machines can consume many resources because each VM needs its own operating system, and this can make deployment and scaling more difficult when many applications are involved.

Docker was introduced as a containerization technology that packages an application together with its runtime environment into a container. This makes the application easier to run consistently across different environments with the idea of "Build once, Run anywhere." The speaker also explained Docker Image, Docker Container, Dockerfile, basic Docker commands, and common use cases in CI/CD, microservices, and cloud native development.

The practical value of Docker is that it helps teams deploy software more efficiently, reduce environment-related issues, and support modern cloud development workflows.

#### Combining AWS WAF with Machine Learning for Cyber Attack Detection

**Speaker:** Anh Le Hoang Gia Dai

This topic addressed the limitation of traditional web application firewalls. Rule-based detection can protect against known attack patterns, but it may be less effective when facing new attacks or unusual behaviors that are not covered by existing rules.

The solution presented was a Network Intrusion Detection System (NIDS) using Machine Learning to analyze network traffic and detect abnormal behavior. The model was trained with the CSE-CIC-IDS2018 dataset and deployed on AWS using services such as Amazon EC2, AWS WAF, Lambda, CloudWatch, Security Hub, and Amazon SNS.

This session helped me understand how Machine Learning can complement AWS WAF to improve real-time attack detection and alerting. For businesses, this approach can strengthen application security and reduce the risk of missing suspicious network activities.

#### Multiplayer in the Cloud: Connecting Godot Clients with AWS WebSockets

**Speaker:** Anh Nguyen Quoc Bao

The third topic discussed the challenge of building real-time communication for multiplayer games. Traditional communication methods such as HTTP polling may not be suitable for applications that need fast two-way updates between many users.

The speaker introduced a multiplayer game architecture using AWS WebSocket. The system used API Gateway WebSocket together with AWS Lambda and Amazon DynamoDB to manage player connections. Lambda handled connection logic, matchmaking, and data synchronization, while DynamoDB stored the state of each connection session.

The practical value of this architecture is that it shows how serverless AWS services can support real-time applications. It also helped me understand how WebSocket can be useful beyond games, such as chat systems, live collaboration tools, and other interactive applications.

#### The Art of Effective Teamwork

**Speaker:** Anh Truong Huy Phuoc

Besides the technical sessions, this topic focused on a problem that appears in many projects: good technology alone is not enough if the team lacks clear communication, shared goals, and responsibility.

The speaker shared four important principles for teamwork: defining a clear common goal, assigning tasks based on each member's strengths, maintaining effective communication, and emphasizing individual responsibility. He also mentioned tools such as Trello, ClickUp, Google Workspace, Slack, and Discord to support task management and collaboration.

The value of this topic was very practical for student projects. It reminded me that successful software development depends not only on coding skills, but also on coordination, ownership, and communication among team members.

#### Build GraphRAG Applications using Amazon Bedrock and Amazon Neptune

**Speaker:** Anh Viet Phat

This topic introduced GraphRAG as a way to improve Retrieval-Augmented Generation when questions require multi-step reasoning. Traditional RAG can be limited when it only retrieves text chunks without understanding the relationships between entities.

The speaker explained how GraphRAG combines Amazon Bedrock with Amazon Neptune. Amazon Neptune can store relationships between entities as graph data, while Amazon Bedrock provides foundation models for AI reasoning and response generation. This allows the AI system to use connected information instead of relying only on plain text retrieval.

The practical value is better answer quality for AI applications that need relationship-based reasoning. This is useful for knowledge systems, enterprise search, and applications where understanding connections between data points is important.

#### From IT Helpdesk to Senior Sysadmin

**Speaker:** Anh Tran Trung Vinh

The final sharing session focused on career development, especially the journey from IT Helpdesk to Senior System Administrator. The main problem discussed was that many learners want to move quickly into Cloud or DevOps, but may not yet have a strong foundation in Linux, networking, and system administration.

The speaker emphasized the importance of building technical fundamentals before approaching cloud and DevOps technologies. He also shared experience about interviews, personal projects, and hands-on practice. One message that stood out to me was that certifications are valuable, but real experience and personal projects help candidates create stronger advantages when applying for jobs.

The practical value of this topic was career guidance. It helped me see that long-term growth in cloud and DevOps requires continuous learning, practice, and a solid technical foundation.

### What I Learned

- I understood the difference between virtual machines and Docker containers, as well as the role of Docker in cloud native application deployment.
- I learned how AWS WAF can be combined with Machine Learning to improve cyber attack detection and system security.
- I understood how API Gateway WebSocket, AWS Lambda, and Amazon DynamoDB can work together to build real-time applications.
- I realized the importance of communication, task division, and personal responsibility in teamwork.
- I gained more knowledge about GraphRAG, Amazon Bedrock, and Amazon Neptune for building modern AI applications.
- I learned that continuous learning, hands-on projects, and strong fundamentals are important for developing a career in Cloud Computing and DevOps.

### Application

The knowledge from this event is useful for my AWS Serverless Event Portal project because several topics connect directly with backend services, AWS architecture, and project collaboration. The WebSocket session helped me better understand how API Gateway, Lambda, and DynamoDB can support real-time communication, even though my current project does not implement multiplayer or live messaging features.

The Docker session also helped me understand why consistent environments are important when developing and deploying applications. For future improvements, this knowledge can support cleaner development workflows and make it easier to prepare backend services for deployment.

The security topic reminded me that web applications need protection and monitoring after deployment. Although I did not implement a Machine Learning security system in my project, the session helped me think more seriously about AWS WAF, monitoring, alerts, and secure architecture.

GraphRAG also gave me ideas for future AI integration. If the Event Portal later needs AI features such as event knowledge search or smarter support, Amazon Bedrock and graph-based data relationships could be useful areas to explore without claiming that these features are already implemented.

### Event Experience

What impressed me most about this event was the variety of topics. The sessions moved from containerization and security to real-time applications, teamwork, AI architecture, and career growth. This made the event feel balanced because it covered both technical skills and professional development.

I especially found the WebSocket and GraphRAG sessions useful because they connected AWS services with real application scenarios. They helped me see how services such as API Gateway, Lambda, DynamoDB, Bedrock, and Neptune can be combined depending on the problem being solved.

The career sharing session also gave me motivation to keep strengthening my fundamentals. After the event, I felt that learning AWS should go together with practicing Linux, networking, system administration, teamwork, and project-building skills.

#### Some event photos

![Photo from FCAJ Community Day 2026](/images/4-EventParticipated/4.3-Event3/fcaj-community-day-2026-event3.jpg)

> Overall, this event helped me connect AWS cloud services, AI, security, teamwork, and career development in a more practical way.