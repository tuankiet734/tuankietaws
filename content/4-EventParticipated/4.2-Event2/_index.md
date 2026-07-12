---
title: "Event 2"
date: 2026-05-30
weight: 2
chapter: false
pre: " <b> 4.2. </b> "
---

# Event Report: AWS FIRST CLOUD AI JOURNEY MEET UP

### Event Information

| Field | Details |
|-------|---------|
| **Event Name** | AWS FIRST CLOUD AI JOURNEY MEET UP |
| **Date & Time** | 09:00, May 30, 2026 |
| **Location** | 26th Floor, Bitexco Tower, 02 Hai Trieu Street, Saigon Ward, Ho Chi Minh City |
| **Role** | Attendee |

---

### Speakers

| # | Speaker | Topic |
|---|---------|-------|
| 1 | **Huynh Thai Linh** | Level Up Your AWS Skills with Cloud Quest and Floci |
| 2 | **Team Khuong** *(Huynh An Khuong, Mai Quoc Anh, Nguyen Tran Minh Quan)* | Hackathon – More like "HA! A tons, of fun" |
| 3 | **Nguyen Thi Quynh Nhu** | Why We Always Need Confidence |
| 4 | **Tran Huu Nghia** | A Comprehensive Astrology Platform Combining Traditional Knowledge with Modern Technology |
| 5 | **Tran Minh Quan** | The Hidden Iceberg of a Project: DevOps Before Disaster |
| 6 | **Khac Uy Pham** | The Iceberg of Procrastination – When "Laziness" Is Just the Tip of Fear |

---

### Session Summaries

#### 1. Level Up Your AWS Skills with Cloud Quest and Floci
*Speaker: Huỳnh Thái Linh*

> *I attended this insightful session by Huỳnh Thái Linh, which focused on practical methods for acquiring hands-on cloud skills.*

This presentation was designed for cloud beginners, addressing two common concerns that hinder early learning: **unexpected AWS billing** and **forgetting to shut down active resources after practice**.

**Interactive Learning with AWS Cloud Quest:**
Cloud Quest offers an engaging, gamified 3D learning platform. Rather than reading dense technical documentation, learners solve cloud-related problems by completeing structured missions within a virtual city environment.

**Local Prototyping with Floci:**
Floci is a lightweight, open-source local emulator for AWS services. It allows developers to test their architectures on their local development machines at no cost.

**Floci vs LocalStack Comparison:**
| Metric | Floci Emulator | LocalStack (Community) |
|----------|-------|---------------------|
| Boot Time | **138x quicker** | Standard |
| Memory Footprint | **11x lower usage** | Standard |
| Available Free Services | Broad selection | Restricted in free edition |
| Key Constraints | Fewer supported services | More mature service parity |

**Recommended Study Pathway:**
1. **Understand & Architect:** Build fundamental cloud-native design patterns via AWS Cloud Quest.
2. **Local Development:** Write code and run quick tests locally using Floci with zero cost risk.
3. **Cloud Deployment:** Transition to the real AWS environment once the local architecture is verified.

> *"Do not let the fear of running up bills keep you from exploring the cloud. Build your skills in safe environments first, then launch to production with confidence."*

---

#### 2. Hackathon – More like "HA! A tons, of fun"
*Speakers: "The Ballers" - Huỳnh An Khương, Mai Quốc Anh, Nguyễn Trần Minh Quân*

The speakers shared their experiences from 36 intensive hours at LotusHacks—the largest hackathon in Vietnam—marked by sleep deprivation, high pressure, and fast-paced engineering.

**Developing the Concept:**
Following a frustrating start, the team recognized a common problem in existing generative design tools: they produce static UI mockups, and revising them breaks visual consistency while consuming excessive API tokens. To solve this, they created **UTMorpho**, an AI-powered assistant that lets users edit interface code directly on a live, interactive canvas.

**Projects Developed:**
- **SynthHunter** (Voice Authentication System): Utilizes XLS-R and Whisper to detect synthetic and deepfaked voices through pause-rhythm analysis. Results: **Top 21 overall, Top 10 AWS Track**.
- **Vortex** (Integrated Recruitment Platform): Streamlines CV parsing and simulated behavioral/technical interviews to reduce candidate anxiety. Results: **Top 25 overall, Top 10 AWS Track**.

**Real-world Challenges:**
The team had to adapt to working overnight, dealing with overcrowded study venues, eating quick meals, and navigating a busy competition floor.

**Main Takeaways:**
- The most practical ideas address frustrations you experience yourself.
- Taking a step back to re-evaluate is often more productive than working blindly.
- Strong team coordination is more valuable than individual technical skills alone.
- Treat AI tools (Claude, Bedrock) as collaborative partners rather than simple search utilities.

---

#### 3. Why We Always Need Confidence
*Speaker: Nguyễn Thị Quỳnh Như*

This presentation highlighted the role of self-confidence in career growth and explained how it can be systematically built through daily habits.

**The Problem:**
Many skilled technical developers fail to reach their full potential because they struggle with communication and presentation anxiety. This lack of confidence leads to missed career advancements and unnecessary stress.

**Rethinking Confidence:**
- Confidence is not about having an inflated ego.
- Confidence does not require knowing all the answers upfront.
- Confidence is simply the willingness to try despite feeling uncertain.

**Psychological Concepts:**
- *Impostor Syndrome*: The false belief that one's achievements are due to luck rather than skill.
- *Dunning-Kruger Effect*: The cognitive bias where beginners overestimate their abilities, followed by a sharp drop in confidence as they realize how much they have yet to learn.

**Strategies to Build Confidence:**
- **Thorough Preparation**: Structuring presentations and interviews beforehand reduces nervousness.
- **Recognize Minor Successes**: Fixing a difficult bug or raising a question in a meeting builds confidence incrementally.
- **The 5-Second Rule**: Count down from 5 to 1 and take action immediately to bypass hesitation.

> *"Technical skill is the engine; confidence is the transmission that translates that power into movement. Without it, your knowledge remains static."*

---

#### 4. A Comprehensive Astrology Platform Combining Traditional Knowledge with Modern Technology
*Speaker: Trần Hữu Nghĩa*

This session introduced **Tử Vi Đại Việt**, a modern astrology application that digitizes traditional Vietnamese astrological charts by utilizing AWS serverless infrastructure and AI.

**Product Features:**
Tử Vi Đại Việt addresses the constraints of traditional consulting (which is manual and hard to scale) by converting historical astrological rules into a scalable AI system capable of generating personalized charts.

**AWS System Architecture:**
The platform leverages: Amazon Bedrock (for natural language synthesis), AWS Lambda (for serverless business logic), API Gateway (API management), DynamoDB (user records and chart storage), S3 (static media), and CloudFront (global CDN).

**AI Agent Workflow:**
The application takes birth data → calculates the astrological chart via deterministic logic → forwards the chart data to Amazon Bedrock/LLM to generate a personalized, conversational analysis → delivers the final report through a web portal.

**Key Insight:**
This project illustrates that modern AI and cloud services are not confined to traditional tech fields; they can be applied to preserve and scale ancient cultural knowledge when structured rules are digitized.

---

#### 5. The Hidden Iceberg of a Project: DevOps Before Disaster
*Speaker: Trần Minh Quân*

The presenter used an iceberg metaphor to show how hidden operational issues beneath the surface of a software project lead to delivery failures.

**The Project Iceberg Model:**
- **The Visible Tip (Symptoms):** Missed delivery dates, frequent bugs in production, deployment failures, and team exhaustion.
- **The Submerged Mass (Root Causes):** Unclear project specifications, communication silos, manual delivery pipelines, and slow feedback loops.

**Core DevOps Values:**
DevOps is not defined by tooling alone (Docker, Kubernetes, Terraform). The true value of DevOps lies in the alignment of **People, Processes, and Technology**, with communication being the most critical element.

**Mapping Operational Problems to DevOps Solutions:**
| Operational Issue | DevOps Approach |
|---|---|
| Siloed teams & misaligned communication | Collaborative culture & shared goals |
| Slow manual provisioning & deployments | Automation (CI/CD pipelines, Infrastructure as Code) |
| Delayed bug discovery | Continuous monitoring & automated integration testing |
| Recurrent deployment failures | Post-mortems & iterative improvement practices |

> *"Do not just resolve the visible symptoms on the surface. Focus on fixing the underlying delivery pipeline—that is where real reliability is built."*

---

#### 6. The Iceberg of Procrastination – When "Laziness" Is Just the Tip of Fear
*Speaker: Khắc Uy Phạm*

The speaker reframed procrastination, showing that it is primarily an emotional regulation challenge rather than a time management failure or simple laziness.

**The Procrastination Iceberg Model:**
- **The Tip (Visible Actions):** Distracting activities like checking social media and delaying work.
- **The Base (Hidden Emotions):**
  - **Inadequacy**: Avoiding a task out of fear that the output won't be good enough.
  - **Exposure**: Hesitation to share code or publish a repository due to fear of criticism.
  - **Self-protection**: Intentionally delaying preparation so that a failure can be blamed on lack of time rather than lack of ability.

**The Procrastination Cycle:**
A challenging task leads to anxiety → the mind seeks immediate relief through distraction → this results in guilt and stress → which increases anxiety and triggers further avoidance.

**Actionable Solutions:**
- **Acknowledge the Emotion**: Reframe "I am being lazy" to "I am feeling overwhelmed by this task."
- **The 5-Minute Rule**: Commit to working on a task for just five minutes (e.g., writing a few lines of code or reading a page) to break the initial resistance.

> *"Action is what builds confidence, not the other way around. Start small, iterate quickly, and learn from the process."*

---

### Key Takeaways

#### On technical skills
- **Cost-effective Learning**: Tools like AWS Cloud Quest and Floci allow developers to learn cloud engineering without incurring high sandbox costs.
- **DevOps Culture**: Successful operations rely on team culture and clear processes, not just software tools.
- **Domain Integration**: The astrology platform shows how custom AI agents can convert domain-specific rules into scalable software products.

#### On mindset and attitude
- **Managing Procrastination**: Recognizing that procrastination is driven by fear allows developers to address the root emotional cause rather than forcing productivity.
- **Incremental Confidence**: Confidence is developed through consistent, small actions rather than waiting to feel fully prepared.
- **Practical Experience**: Hackathons offer hands-on experience in collaboration, rapid prototyping, and engineering under constraints.

#### On a personal level
- Listening to these diverse topics—ranging from serverless architectures and DevOps metrics to cognitive psychology—highlighted how technical proficiency and personal mindset are interconnected in software engineering.

---

### Personal Reflection

Attending this Meet Up was a very motivating experience. It gave me a broader perspective on how cloud technologies are applied in diverse domains and highlighted the human factors—like communication, confidence, and emotional management—that determine the success of technical projects.

The sessions reminded me that every engineer is constantly learning and refining their skills. Waiting to feel fully prepared is a common trap; the most effective approach is to start building and iterate along the way.

---

### Event Photos

![AWS First Cloud AI Journey Workshop](/images/event2.JPG)
