---
layout: page
title: Real-Time Vision & SLAM Pipeline
description: Monocular VO, depth estimation, and GTSAM factor graph spatial fusion achieving 20-25 FPS with sub-meter trajectory error.
importance: 2
category: Systems & Vision
github: https://github.com/pushks18
---

Built at **USC AI Systems & Computer Vision Lab**, this project implements a real-time visual odometry (VO) and monocular depth estimation pipeline operating at 20-25 FPS on noisy indoor sequences.

### Key Highlights:
- **Feature Matching & RANSAC**: 2500 match keypoints with 2000 inliers, leveraging IMU motion priors to maintain tracking stability under sudden motion blur.
- **GTSAM Factor Graph Fusion**: Fused visual odometry with sparse depth and GPS in GTSAM, reducing overall trajectory Absolute Trajectory Error (ATE) from ~95 m to ~1.2 m.
- **Topological Semantic Memory**: Designed a scene memory representation reducing repeated scene re-identification by ~40% across long video sequences.
