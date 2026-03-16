---
id: 1
title: Create Project Constitution
stage: constitution
date_iso: 2026-02-13
surface: agent
model: Qwen Code
feature: none
branch: main
user: metachemist
command: /sp.constitution generate constitution.md file for this project in root directory
labels: ["constitution", "documentation", "setup"]
spec: null
ticket: null
adr: null
pr: null
files_yaml:
  - "/home/metachemist/Code/gen_ai/physical-ai-textbook-with-rag-01/constitution.md"
tests_yaml: []
prompt_text: |
  /sp.constitution generate constitution.md file for this project in root directory # Project Constitution: Physical AI & Humanoid Robotics Textbook

  ## Project Overview

  This document serves as the foundational guide for creating an AI-native textbook for teaching Physical AI & Humanoid Robotics. This project is part of Hackathon I for Panaversity, focusing on embodied intelligence and the convergence of AI systems with the physical world.

  ### Mission Statement

  To create a comprehensive, interactive, and AI-enhanced educational resource that bridges the gap between digital AI and physical robotics, enabling students to master the skills needed for the future of human-robot collaboration.

  ---

  [Rest of the detailed constitution content as provided in the original request]
response_text: |
  Created the constitution.md file in the root directory containing the complete project constitution for the Physical AI & Humanoid Robotics Textbook project. The file includes all required sections such as project overview, mission statement, core deliverables, technical architecture, content structure, guidelines, specifications, hardware requirements, authentication, localization strategy, assessment framework, development workflow, quality assurance, submission requirements, ethical guidelines, success metrics, roadmap, resources, contact information, version control, and appendix.
outcome: 
evaluation: 
---

## Project Constitution: Physical AI & Humanoid Robotics Textbook

## Project Overview

This document serves as the foundational guide for creating an AI-native textbook for teaching Physical AI & Humanoid Robotics. This project is part of Hackathon I for Panaversity, focusing on embodied intelligence and the convergence of AI systems with the physical world.

### Mission Statement

To create a comprehensive, interactive, and AI-enhanced educational resource that bridges the gap between digital AI and physical robotics, enabling students to master the skills needed for the future of human-robot collaboration.

---

## Core Deliverables

### 1. **AI-Native Textbook**
- Platform: Docusaurus
- Deployment: GitHub Pages
- Development Tools: Claude Code + Spec-Kit Plus
- Content Focus: Physical AI & Humanoid Robotics curriculum

### 2. **Integrated RAG Chatbot**
- Technology Stack:
  - OpenAI Agents/ChatKit SDKs
  - FastAPI backend
  - Neon Serverless Postgres
  - Qdrant Cloud (Free Tier)
- Features:
  - Answer questions about book content
  - Context-aware responses based on user-selected text
  - Embedded seamlessly within the published book

### 3. **Bonus Features** (Optional but Recommended)
- **Authentication System** (Better-Auth)
  - User signup/signin
  - Background profiling (software/hardware experience)
- **Content Personalization**
  - Adaptive content based on user background
  - Chapter-level personalization triggers
- **Localization**
  - Urdu translation capability
  - Per-chapter translation controls
- **Reusable Intelligence**
  - Claude Code Subagents
  - Agent Skills development

---

## Technical Architecture

### Frontend Stack
```
- Framework: Docusaurus (React-based)
- Styling: Modern, responsive design
- Interactivity: Embedded chatbot widget
- Deployment: GitHub Pages or GitHub Pages
```

### Backend Stack
```
- API Framework: FastAPI
- Database: Neon Serverless Postgres
- Vector Store: Qdrant Cloud
- Authentication: Better-Auth
- AI Integration: OpenAI SDK
```

### Development Workflow
```
1. Specification-driven development (Spec-Kit Plus)
2. AI-assisted coding (Claude Code)
3. Iterative content creation
4. Continuous deployment (GitHub Actions)
```

---

## Content Structure

### Course Modules (13 Weeks)

#### **Module 1: The Robotic Nervous System (ROS 2)** [Weeks 3-5]
- ROS 2 architecture and middleware
- Nodes, topics, services, and actions
- Python integration with rclpy
- URDF for humanoid robot description

#### **Module 2: The Digital Twin (Gazebo & Unity)** [Weeks 6-7]
- Physics simulation fundamentals
- Gazebo environment setup
- Unity for high-fidelity rendering
- Sensor simulation (LiDAR, Depth Cameras, IMUs)

#### **Module 3: The AI-Robot Brain (NVIDIA Isaac™)** [Weeks 8-10]
- NVIDIA Isaac Sim and SDK
- Hardware-accelerated VSLAM
- Isaac ROS for perception
- Nav2 for path planning

#### **Module 4: Vision-Language-Action (VLA)** [Weeks 11-13]
- Voice-to-Action pipelines (OpenAI Whisper)
- LLM-based cognitive planning
- Multi-modal interaction design
- Capstone project integration

#### **Foundation: Introduction to Physical AI** [Weeks 1-2]
- Principles of embodied intelligence
- Physical AI vs. traditional AI
- Humanoid robotics landscape
- Sensor systems overview

---

## Content Guidelines

### Writing Standards

1. **Clarity and Accessibility**
   - Write for students with AI fundamentals but new to robotics
   - Define technical terms on first use
   - Use progressive disclosure (simple → complex)

2. **Practical Focus**
   - Include hands-on examples for every concept
   - Provide code snippets with explanations
   - Link theory to real-world applications

3. **Visual Learning**
   - Diagrams for architecture and workflows
   - Screenshots for software setup
   - Videos for demonstrations (where applicable)
   - Interactive simulations (where possible)

4. **AI-Native Approach**
   - Embed chatbot assistance throughout
   - Provide alternative explanations via AI
   - Enable "explain like I'm 5" mode
   - Support code debugging through chat

### Chapter Structure Template

```markdown
# Chapter Title

## Learning Objectives
- Clear, measurable outcomes

## Prerequisites
- Required knowledge/setup

## Introduction
- Context and motivation
- Real-world relevance

## Core Concepts
- Detailed explanations
- Code examples
- Diagrams/visuals

## Hands-On Practice
- Step-by-step tutorials
- Common pitfalls and solutions

## Assessment
- Knowledge check questions
- Practical exercises
- Project ideas

## Further Resources
- Official documentation links
- Research papers
- Community resources

## Summary
- Key takeaways
- Connection to next chapter
```

---

## RAG Chatbot Specifications

### Functional Requirements

1. **Context-Aware Q&A**
   - Answer questions about any book content
   - Cite specific chapters/sections
   - Handle multi-turn conversations

2. **Text Selection Mode**
   - Process user-highlighted text
   - Provide targeted explanations
   - Suggest related content

3. **Personalization**
   - Adapt responses to user background
   - Track learning progress
   - Suggest next steps

### Data Pipeline

```
Content → Chunking → Embedding → Qdrant Storage
                                        ↓
User Query → Embedding → Similarity Search → Context Retrieval
                                                    ↓
                                        LLM Processing → Response
```

### Performance Targets
- Response time: < 3 seconds
- Relevance accuracy: > 85%
- Context window: 4000+ tokens
- Concurrent users: 100+

---

## Hardware Requirements Documentation

### Student Workstation Specifications

#### Minimum Requirements
- **GPU**: NVIDIA RTX 4070 Ti (12GB VRAM)
- **CPU**: Intel i7 13th Gen / AMD Ryzen 9
- **RAM**: 32GB DDR5 (64GB recommended)
- **Storage**: 500GB NVMe SSD
- **OS**: Ubuntu 22.04 LTS

#### Recommended Setup
- **GPU**: NVIDIA RTX 3090/4090 (24GB VRAM)
- **RAM**: 64GB DDR5
- **Storage**: 1TB NVMe SSD

### Edge Computing Kit ($700)
- NVIDIA Jetson Orin Nano Super (8GB): $249
- Intel RealSense D435i: $349
- ReSpeaker USB Mic Array v2.0: $69
- SD Card + Accessories: $30

### Robot Options
- **Budget**: Unitree Go2 (~$1,800-$3,000)
- **Mid-Range**: Unitree G1 (~$16,000)
- **Premium**: Unitree H1 (~$90,000)

---

## Authentication & Personalization

### User Profile Schema

```javascript
{
  userId: string,
  email: string,
  profile: {
    softwareBackground: {
      pythonLevel: "beginner" | "intermediate" | "advanced",
      rosExperience: boolean,
      aiKnowledge: "none" | "basic" | "intermediate" | "advanced"
    },
    hardwareBackground: {
      roboticsExperience: boolean,
      electronicsTinkering: boolean,
      hasAccessToGPU: boolean,
      hasAccessToRobot: boolean
    },
    learningPreferences: {
      preferredLanguage: "en" | "ur",
      learningPace: "slow" | "moderate" | "fast",
      preferredExamples: "theoretical" | "practical" | "mixed"
    }
  },
  progress: {
    chaptersCompleted: number[],
    lastVisited: date,
    quizScores: object
  }
}
```

### Personalization Logic

1. **Beginner Software Background**
   - More detailed code explanations
   - Additional Python refreshers
   - Step-by-step installation guides

2. **Advanced Software Background**
   - Condensed basics
   - Advanced optimization techniques
   - Research paper references

3. **Limited Hardware Access**
   - Emphasis on simulation
   - Cloud computing alternatives
   - Budget-friendly options

4. **Full Hardware Setup**
   - Sim-to-real transfer focus
   - Physical deployment guides
   - Troubleshooting hardware issues

---

## Localization Strategy

### Urdu Translation Implementation

1. **Technical Terms**
   - Maintain English for technical terms (ROS, URDF, etc.)
   - Provide Urdu explanations for concepts
   - Glossary with Urdu translations

2. **Content Translation**
   - AI-assisted translation with human review
   - Preserve code blocks in English
   - Maintain technical accuracy

3. **UI Elements**
   - Bilingual navigation
   - Toggle button at chapter start
   - Persistent language preference

---

## Assessment Framework

### Project Deliverables

1. **ROS 2 Package Development**
   - Custom node implementation
   - Service and topic integration
   - Launch file configuration

2. **Gazebo Simulation**
   - Environment creation
   - Sensor integration
   - Physics tuning

3. **Isaac Perception Pipeline**
   - VSLAM implementation
   - Object detection
   - Navigation stack

4. **Capstone Project: Autonomous Humanoid**
   - Voice command processing
   - Path planning
   - Object manipulation
   - Full system integration

### Evaluation Criteria

- **Base Score**: 100 points
  - Content completeness: 40 points
  - RAG chatbot functionality: 30 points
  - Documentation quality: 15 points
  - Deployment success: 15 points

- **Bonus Points**: Up to 200 additional points
  - Reusable intelligence: 50 points
  - Authentication system: 50 points
  - Content personalization: 50 points
  - Urdu translation: 50 points

---

## Development Workflow

### Phase 1: Planning & Setup (Days 1-2)
- [ ] Repository initialization
- [ ] Docusaurus configuration
- [ ] Database schema design
- [ ] Project structure setup

### Phase 2: Content Creation (Days 3-10)
- [ ] Write foundational chapters (Weeks 1-2)
- [ ] Develop Module 1 content (ROS 2)
- [ ] Develop Module 2 content (Gazebo/Unity)
- [ ] Develop Module 3 content (NVIDIA Isaac)
- [ ] Develop Module 4 content (VLA)
- [ ] Create code examples and tutorials

### Phase 3: RAG Integration (Days 11-15)
- [ ] Content chunking and embedding
- [ ] Qdrant setup and indexing
- [ ] FastAPI backend development
- [ ] ChatKit integration
- [ ] UI embedding

### Phase 4: Enhancement Features (Days 16-20)
- [ ] Better-Auth implementation
- [ ] User profiling system
- [ ] Content personalization engine
- [ ] Urdu translation system

### Phase 5: Testing & Refinement (Days 21-25)
- [ ] Content review and editing
- [ ] Chatbot accuracy testing
- [ ] Performance optimization
- [ ] Bug fixes and improvements

### Phase 6: Deployment & Documentation (Days 26-28)
- [ ] GitHub Pages deployment
- [ ] Demo video creation (< 90 seconds)
- [ ] README and documentation
- [ ] Final submission

---

## Quality Assurance

### Content Review Checklist

- [ ] Technical accuracy verified
- [ ] Code examples tested
- [ ] Links and references validated
- [ ] Grammar and spelling checked
- [ ] Consistent formatting
- [ ] Progressive difficulty maintained
- [ ] Learning objectives met

### Chatbot Testing

- [ ] Factual accuracy: > 90%
- [ ] Response relevance: > 85%
- [ ] Hallucination rate: < 5%
- [ ] Response time: < 3 seconds
- [ ] Context retention across turns
- [ ] Graceful error handling

### Accessibility Standards

- [ ] WCAG 2.1 AA compliance
- [ ] Keyboard navigation support
- [ ] Screen reader compatibility
- [ ] Color contrast ratios met
- [ ] Alternative text for images
- [ ] Responsive design (mobile-first)

---

## Submission Requirements

### Deliverables Checklist

1. **GitHub Repository**
   - [ ] Public repository
   - [ ] Clean commit history
   - [ ] Comprehensive README
   - [ ] MIT or Apache 2.0 license

2. **Published Book**
   - [ ] Live on GitHub Pages/GitHub Pages
   - [ ] All chapters accessible
   - [ ] Chatbot functional
   - [ ] Fast load times (< 2s)

3. **Demo Video**
   - [ ] Under 90 seconds
   - [ ] Shows key features
   - [ ] Clear narration/captions
   - [ ] High-quality recording

4. **Contact Information**
   - [ ] WhatsApp number provided
   - [ ] Email for follow-up
   - [ ] GitHub profile linked

### Submission Form Data

```
- Public GitHub Repo Link
- Published Book URL
- Demo Video Link (YouTube/Vimeo/Drive)
- WhatsApp Number
- Team Members (if applicable)
- Bonus Features Implemented
```

---

## Ethical Guidelines

### AI Usage

1. **Transparency**
   - Disclose AI-generated content
   - Cite AI assistance appropriately
   - Verify AI outputs for accuracy

2. **Originality**
   - No plagiarism from existing textbooks
   - Original explanations and examples
   - Proper attribution of external resources

3. **Accessibility**
   - Inclusive language
   - Multiple learning pathways
   - Support for diverse backgrounds

### Safety Considerations

1. **Hardware Safety**
   - Clear warnings for electrical work
   - Safe robot handling procedures
   - Emergency stop protocols

2. **Software Security**
   - Secure authentication implementation
   - Data privacy protection
   - No hardcoded credentials

3. **Responsible AI**
   - Ethical implications discussions
   - Bias awareness in robotics
   - Safety-first design principles

---

## Success Metrics

### Quantitative Metrics

- Book completeness: 100% of required content
- Chatbot accuracy: > 85% relevant responses
- Page load time: < 2 seconds
- Mobile responsiveness: 100%
- Accessibility score: > 90
- Code example success rate: > 95%

### Qualitative Metrics

- Content clarity and coherence
- Practical applicability
- Engaging presentation
- Innovation in AI integration
- User experience quality

---

## Post-Hackathon Roadmap

### Immediate Next Steps (If Selected)

1. **Integration with Panaversity Platform**
   - Migrate to official platform
   - Integrate with user management
   - Connect to payment systems

2. **Content Expansion**
   - Add advanced topics
   - Create video tutorials
   - Develop interactive simulations

3. **Community Building**
   - Discussion forums
   - Student project showcase
   - Mentor matching

### Long-Term Vision

1. **Curriculum Evolution**
   - Update with latest technologies
   - Add certification programs
   - Partner with industry

2. **Ecosystem Growth**
   - O/A Level AI books
   - Medical AI textbooks
   - Engineering AI series

3. **Global Impact**
   - Multi-language support
   - Regional partnerships
   - Open educational resources

---

## Resources & References

### Essential Documentation

- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Gazebo Documentation](https://gazebosim.org/docs)
- [NVIDIA Isaac Documentation](https://docs.omniverse.nvidia.com/isaacsim/)
- [Docusaurus Documentation](https://docusaurus.io/docs)
- [Spec-Kit Plus Repository](https://github.com/panaversity/spec-kit-plus/)
- [Claude Code Documentation](https://www.claude.com/product/claude-code)

### Supporting Tools

- [Better-Auth Documentation](https://www.better-auth.com/)
- [OpenAI ChatKit SDK](https://platform.openai.com/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Neon Postgres](https://neon.tech/docs)
- [Qdrant Cloud](https://qdrant.tech/documentation/)

### Learning Resources

- NVIDIA Deep Learning Institute
- ROS 2 Tutorials by The Construct
- PyTorch Robotics Framework
- OpenAI Robotics Research

---

## Contact & Support

### Hackathon Coordinators

- **Panaversity Founders**: Zia, Rehan, Junaid, Wania
- **Submission Form**: https://forms.gle/CQsSEGM3GeCrL43c8
- **Live Presentation**: Nov 30, 2025, 6:00 PM on Zoom
- **Meeting ID**: 849 7684 7088
- **Passcode**: 305850

### Community Channels

- PIAIC Community
- GIAIC Network
- Panaversity Discord/Slack (if available)

---

## Document Version Control

- **Version**: 1.0
- **Last Updated**: November 2025
- **Status**: Active
- **Review Cycle**: Updated as project progresses

---

## Appendix

### A. Technical Terms Glossary

**Physical AI**: AI systems that function in and understand the physical world, beyond digital environments.

**Embodied Intelligence**: Intelligence that emerges from the interaction between an agent's body, its environment, and its cognitive processes.

**ROS 2**: Robot Operating System 2, a middleware framework for robot software development.

**URDF**: Unified Robot Description Format, an XML format for representing robot models.

**VSLAM**: Visual Simultaneous Localization and Mapping, using camera data to build maps and track position.

**VLA**: Vision-Language-Action models that connect visual perception, natural language, and physical actions.

**Sim-to-Real**: The process of training models in simulation and deploying them to real-world robots.

### B. Code Style Guide

- Follow PEP 8 for Python code
- Use meaningful variable names
- Comment complex algorithms
- Include docstrings for functions
- Consistent indentation (4 spaces)
- Maximum line length: 88 characters

### C. Contribution Guidelines

If this project becomes open-source:
- Fork and create feature branches
- Write descriptive commit messages
- Update documentation with code changes
- Add tests for new features
- Submit pull requests with clear descriptions

---

**This constitution serves as the living document for the Physical AI & Humanoid Robotics Textbook project. It will be updated as the project evolves and new requirements emerge.**

---

*Created for Panaversity Hackathon I*  
*Building the future of AI education, one textbook at a time.*