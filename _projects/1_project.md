---
layout: page
title: AgentPay
description: Multi-agent economy where AI agents autonomously discover, hire, and pay other agents using on-chain payments and verifiable reputation — built at SCBC 2026.
img: /project_images/agentpay.png
importance: 1
category: Web3 & AI
github: https://github.com/pushks18
---

**AgentPay** is a decentralized autonomous agent economy where AI agents discover, hire, and pay other agents using on-chain payments and reputation staking — no human in the loop. Built at the **Southern California Blockchain Hackathon (SCBC 2026)**.

The smart contract layer (Rust/Anchor on Solana & Avalanche) handles agent registry, escrow payments, and a staking/slashing mechanism for verifiable reputation tracking. LangChain orchestration powers multi-agent workflows with custom x402 payment tooling, achieving under 30s end-to-end interaction cycles. A real-time Next.js + D3.js dashboard visualizes live agent interactions, network dynamics, and payment flows across the agent graph.

### Key Technical Contributions:
- **Smart Contracts (Solana/Avalanche)**: Rust/Anchor agent registry, escrow accounts, reputation staking, slashing conditions.
- **Agent Orchestration**: LangChain multi-agent workflow with x402 on-chain payment primitives.
- **Real-Time Visualizer**: Interactive network graph visualizer using D3.js and WebSockets.
