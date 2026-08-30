---
layout: page
title: Personalized Discovery Feed Engine
description: Hybrid Elasticsearch BM25 + vector search retrieval with slot-based re-ranking, recency-decayed user preference modeling & sub-500ms latency.
importance: 3
category: AI & ML
github: https://github.com/pushks18
---

Architected during my internship at **Tabhi** in Austin, TX, this system powers personalized discovery feeds (retrieve → rank → re-rank) across a 188K+ item catalog.

### Technical Achievements:
- **Hybrid Retrieval**: Combined BM25 sparse keyword retrieval with vector embeddings for semantic recall.
- **Slot-Based Re-ranking**: Applied slot constraints to ensure category diversity and fresh content delivery.
- **Sub-500ms Latency**: Reduced cold feed load time from 8s to under 500ms using three-tier caching, pre-warming, and geospatial index tuning.
- **Preference Decay Model**: Implemented a recency-weighted user preference score updating dynamically with user interactions.
