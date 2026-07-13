---
title: "Event 3"
date: 2026-06-13
weight: 3
chapter: false
pre: " <b> 4.3. </b> "
---

# Event Report: AWS FIRST CLOUD AI JOURNEY MEET UP

### Event Information

| Field | Details |
|-------|---------|
| **Event Name** | AWS FIRST CLOUD AI JOURNEY MEET UP |
| **Date & Time** | 09:00, June 13, 2026 |
| **Location** | 26th Floor, Bitexco Tower, 02 Hai Trieu Street, Saigon Ward, Ho Chi Minh City |
| **Role** | Attendee |

---

### Speakers

| # | Speaker | Topic |
|---|---------|-------|
| 1 | **Huỳnh Thái Linh** | Level Up Your AWS Skills with Cloud Quest and Floci |
| 2 | **Team Khương** *(Huỳnh An Khương, Mai Quốc Anh, Nguyễn Trần Minh Quân)* | Hackathon – More like "HA! A tons, of fun" |
| 3 | **Nguyễn Thị Quỳnh Như** | Why We Always Need Confidence |
| 4 | **Trần Hữu Nghĩa** | A Comprehensive Astrology Platform Combining Traditional Knowledge with Modern Technology |
| 5 | **Trần Minh Quân** | The Hidden Iceberg of a Project: DevOps Before Disaster |
| 6 | **Khắc Uy Phạm** | The Iceberg of Procrastination – When "Laziness" Is Just the Tip of Fear |

---

### Session Summaries

#### 1. Level Up Your AWS Skills with Cloud Quest and Floci
*Speaker: Huỳnh Thái Linh*

> *This was my own presentation at the event, delivered in the role of Speaker.*

This session targeted beginners in AWS - people blocked by the two biggest fears: **AWS billing** and **forgetting to delete resources after practice**.

**AWS Cloud Quest - Learn AWS like a game:**
Cloud Quest is a free 3D practice environment with game-style quests. Instead of dry documentation, learners engage with core cloud concepts through hands-on missions inside a virtual city.

**Floci - Free, open-source AWS emulator:**
Floci is a local AWS service emulator that lets you test cloud architectures on your own machine with zero cost.

**Floci vs LocalStack comparison:**
| Criteria | Floci | LocalStack Community |
|----------|-------|---------------------|
| Startup speed | **138x faster** | Slower |
| Memory usage | **11x more efficient** | Higher memory usage |
| Free services | More | Limited in Community edition |
| Limitations | Fewer services, some return mock data | More stable across services |

**Recommended learning roadmap:**
1. **Phase 1 - Mindset & Architecture:** Learn through AWS Cloud Quest, build cloud-native thinking.
2. **Phase 2 - Code & Test Locally:** Write and test fast with Floci - no billing concerns.
3. **Phase 3 - Real Deployment:** Once confident, deploy to real AWS.

> *"Don't let the fear of billing stop you from learning cloud. Practice enough first - build your confidence before going live."*

---

#### 2. Hackathon – More like "HA! A tons, of fun"
*Speakers: "The Ballers" - Huỳnh An Khương, Mai Quốc Anh, Nguyễn Trần Minh Quân*

The real stories from 36 hours at LotusHacks - Vietnam's largest hackathon - filled with back pain, sleep deprivation, and last-minute bug fixes.

**How the ideas were born:**
After a completely stuck first day, the team realized the problem came from their own daily frustration: existing AI UI tools only generate static models, continuous re-prompting breaks design consistency and burns tokens. That's how **UTMorpho** was born - an AI Agent enabling direct UI creation and editing on a WYSIWYG canvas.

**Two projects built during the competition:**
- **SynthHunter** - AI Voice Authentication System: Uses XLS-R, Whisper, and pause-rhythm analysis to detect AI-generated voices and combat fraud. Result: **Top 21 overall, Top 10 AWS Track**.
- **Vortex** - Connected Hiring Workflow: CV screening, behavioral and technical interviews to help candidates overcome job-application anxiety. Result: **Top 25 overall, Top 10 AWS Track**.

**The real struggles:**
Staying up all night, no 24/7 air-conditioned cafes, dirty floors, fast food, and all the beanbags taken over by kids playing Minecraft.

**Key lessons:**
- The best ideas come from your own everyday frustrations.
- Stepping back sometimes unlocks better thinking than pushing forward.
- Team chemistry beats individual skill every time.
- Treat AI (Claude, Bedrock) as a teammate, not just a tool.

---

#### 3. Why We Always Need Confidence
*Speaker: Nguyễn Thị Quỳnh Như*

A session on why confidence matters - and how it's not something you're born with, but something **built through small actions every day**.

**The real problem:**
Many technically skilled people are underrated simply because they freeze when presenting. A lack of confidence causes students to miss opportunities, carry invisible pressure, and hide their actual potential.

**Redefining confidence:**
- Confidence is **not** ego.
- Confidence is **not** having all the answers before you start.
- Confidence **is** daring to try, even when you feel nervous.

**The science behind it:**
- *Impostor Syndrome*: "I don't deserve to be here."
- *Dunning-Kruger Effect*: The "valley of despair" when first learning a new field.

**How to build confidence:**
- **Thorough preparation**: Clarity reduces fear before interviews and presentations.
- **Celebrate small wins**: Asking one question, fixing one bug - small actions accumulate into real confidence.
- **The 5-Second Rule**: Count down 5-4-3-2-1 and act immediately - silence self-doubt before it wins.

> *"Technical skill is the foundation; confidence is the bridge. Without that bridge, you'll always be watching opportunities from the wrong side of the river."*

---

#### 4. A Comprehensive Astrology Platform Combining Traditional Knowledge with Modern Technology
*Speaker: Trần Hữu Nghĩa*

An introduction to **Tử Vi Đại Việt** - a next-generation Vietnamese astrology platform that combines centuries-old traditional knowledge with AWS infrastructure and AI Agents.

**Product overview:**
Tử Vi Đại Việt addresses the limitations of traditional astrology services - dependency on human experts, inability to scale, and lack of personalization - by encoding astrological knowledge into an AI system capable of serving thousands of users simultaneously.

**AWS architecture:**
The system is built on AWS with core services including: Amazon Bedrock (AI model layer), Lambda (serverless compute), API Gateway, DynamoDB (user data and chart storage), S3 (static assets), and CloudFront (global CDN).

**AI Agent flow:**
The AI Agent receives the user's birth date and time → computes the astrological chart according to encoded traditional rules → combines with a large language model (LLM) to generate personalized, context-aware, and easy-to-understand analysis → returns results to the user through a web interface.

**Demo highlights:**
The system interprets destiny, personality traits, career prospects, and relationships based on the astrological chart - presented in natural language instead of technical terminology.

> *Interesting insight: Combining traditional knowledge that spans thousands of years with modern AI demonstrates that AI is not limited to tech domains - it can be applied anywhere rules and data can be encoded.*

---

#### 5. The Hidden Iceberg of a Project: DevOps Before Disaster
*Speaker: Trần Minh Quân*

Using the iceberg model to expose the hidden DevOps problems beneath a project's surface - the real causes of failure, not just the visible symptoms.

**The project iceberg:**

*Above the surface - Visible symptoms:*
Missed deadlines, production bugs, failed deployments, customer complaints, team burnout.

*Below the surface - Root causes:*
Ambiguous requirements, communication gaps, siloed teams, lack of accountability, manual processes, slow feedback loops.

**The right DevOps mindset:**
DevOps is not a toolset (Docker, CI/CD, Terraform...). The core of DevOps lies in **People - Process - Technology**. Communication and trust are things that cannot be automated.

**DevOps principles mapped to hidden problems:**

| Hidden problem | DevOps solution |
|---------------|----------------|
| Poor communication / Siloed teams | Collaboration & shared ownership |
| Manual processes | Automation (CI/CD, Infrastructure as Code) |
| Slow feedback / Late bug detection | Fast feedback (Monitoring, Continuous Integration) |
| Repeated failures | Continuous improvement (Retrospectives, learning from failure) |

> *"Don't just treat the symptoms floating on the surface. Dive down and fix the root cause - that's what DevOps is really about."*

---

#### 6. The Iceberg of Procrastination – When "Laziness" Is Just the Tip of Fear
*Speaker: Khắc Uy Phạm - 3rd Year Student, Vietnamese-German University (VGU)*

A reframing of procrastination: it's not about laziness or poor time management - it's fundamentally about **emotional management**.

**The procrastination iceberg:**

*Above the surface (20-30%) - Visible behaviors:*
Scrolling TikTok and Facebook, snoozing alarms, telling yourself "I'll do it tomorrow."

*Below the surface (70-80%) - Hidden fears:*
- **Fear of not being good enough**: The brain escapes to TikTok to relieve the feeling of being overwhelmed.
- **Fear of judgment**: Keeping code on a hard drive, never pushing to GitHub.
- **Fear of failure**: "If I don't try my hardest, I can tell myself I failed because I didn't try."

**The guilt loop:**
Face a hard task → Avoid it → Temporary relief → Guilt & self-blame → Exhaustion & stress → Continue procrastinating.

**Practical solutions:**
- **Step 1 - Name the fear**: Instead of "I'm lazy," say "I'm afraid I'm not good enough." Naming it correctly means solving it correctly.
- **Step 2 - The 5-Minute Rule**: Don't try to force yourself to finish the whole project. Start with the smallest possible action in 5 minutes - write 3 lines of code, read 1 page - to build momentum.

> *"Action creates confidence - not the other way around. GO BUILD. Fail fast, learn faster."*

---

### Key Takeaways

#### On technical skills
- **Learning doesn't have to cost money**: Cloud Quest + Floci is a complete, free pathway to AWS proficiency - no billing anxiety required.
- **DevOps is about people**: The best tools are meaningless if communication and processes aren't addressed first.
- **AI + domain knowledge**: Tử Vi Đại Việt proves AI can be applied anywhere - what matters is encoding the right rules and data.

#### On mindset and attitude
- **Procrastination isn't laziness** - it's an unnamed fear. The solution isn't forcing yourself harder, it's acknowledging and starting small.
- **Confidence is a trainable skill** - built through small actions, not waiting until you feel "ready."
- **Hackathons teach what textbooks can't**: Real-world pressure, fast decisions, and the compounding power of team chemistry.

#### On a personal level
- Presenting as a speaker for the first time was an entirely different experience from sitting in the audience. Preparing to explain technical content to a live audience forces deeper understanding. Receiving direct feedback from the crowd is something no book can teach.

---

### Personal Reflection

This Meet Up was special compared to previous events for one reason: instead of just listening, I was also speaking. Preparing a technical presentation for the community required me to understand deeply - not just know superficially. That pressure was a gift.

Hearing the other speakers - from the hidden DevOps layer beneath every project, to the psychology of procrastination, to the hackathon journey - I noticed one common thread: **everyone is learning as they go. Nobody waits until they're fully ready before they start**.

---

### Event Photos

![AWS First Cloud AI Journey Workshop](/images/event3.JPG)