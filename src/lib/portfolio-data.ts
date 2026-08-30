import { JobEntry, EducationEntry } from "./types";

export const EDUCATION: EducationEntry[] = [
  {
    school: "University of Southern California, Viterbi School of Engineering",
    degree: "Master's",
    fieldOfStudy: "Computer Science",
    startDate: "2025-01",
    currentlyAttending: false,
    endDate: "2026-12",
    gpa: "3.73 / 4.00",
  },
  {
    school: "University of Mumbai",
    degree: "Bachelor's",
    fieldOfStudy: "Computer Engineering",
    startDate: "2020-07",
    currentlyAttending: false,
    endDate: "2024-05",
    gpa: "9.13 / 10",
  },
];

export const EXPERIENCE: JobEntry[] = [
  {
    jobTitle: "AI Engineer Intern",
    company: "Tabhi",
    location: "Austin, TX",
    startDate: "2026-05",
    currentlyWorkHere: true,
    description: "- Architected an end-to-end personalized discovery feed (retrieve → rank → re-rank) for a 188K-item catalog using hybrid Elasticsearch BM25 and vector retrieval with slot-based re-ranking\n- Designed a recency-decayed user preference model to personalize retrieval and support future Two-Tower and SASRec ranking\n- Reduced cold-feed latency from 8s to <500 ms via three-tier caching, cache pre-warming, optimized indexing, and geospatial retrieval\n- Built recommendation analytics using RudderStack to capture user behavior and optimize personalization through engagement metrics\n- Resolved ES-MongoDB data consistency issues and hardened location-aware retrieval, improving feed and recommendation reliability\n- Engineered the recommendation architecture to support future Two-Tower and SASRec models",
  },
  {
    jobTitle: "Software Engineer Intern – Real-Time AI Systems",
    company: "USC",
    location: "Los Angeles, CA",
    startDate: "2025-11",
    currentlyWorkHere: false,
    endDate: "2026-05",
    description: "- Built a real-time SLAM pipeline combining monocular VO and depth estimation, achieving ~20–25 FPS on noisy indoor data\n- Implemented RANSAC-based feature matching (2500 matches, 2000 inliers), leveraging IMU to improve motion consistency under noise\n- Resolved scale ambiguity using sparse depth and fused VO with GPS in GTSAM, reducing trajectory error from ~95 m to ~1.2 m ATE\n- Debugged sensor noise, calibration drift, and VO failures, improving tracking stability and reducing dropouts by ~30%",
  },
  {
    jobTitle: "Software Engineer Intern – Backend & APIs",
    company: "Technoriya ERP Solution",
    location: "India",
    startDate: "2023-10",
    currentlyWorkHere: false,
    endDate: "2023-12",
    description: "- Developed Python and Node.js backend services and APIs supporting scalable data pipelines and cloud-based ML workflows\n- Implemented secure authentication and access protocols via Firebase Auth and Firestore rules to ensure data integrity\n- Optimized RESTful APIs and Firestore queries to achieve 450 ms response times under 1,000 concurrent requests for ML integration\n- Streamlined deployment workflows using Vercel and GitHub Actions to improve delivery consistency and reliability",
  },
];

export const SKILLS: string[] = [
  // AI/ML
  "Deep Learning", "Generative AI", "NLP", "LLMs", "Transformers",
  "RAGs", "Data Mining", "Data Science", "PyTorch", "TensorFlow", "LangChain",
  // Languages
  "Python", "Java", "C++", "JavaScript", "TypeScript", "R",
  // Frameworks
  "React.js", "Next.js", "Node.js", "Django", "Flask", "Express.js",
  "FastAPI", "NestJS", "Angular.js", "GraphQL", "Flutter", "Kotlin", "Swift",
  "OAuth", "Microservices",
  // Databases & Cloud
  "MongoDB", "SQL", "MySQL", "PostgreSQL", "Supabase", "Redis",
  "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Git", "CI/CD",
];

export const LINKS = {
  github: "https://github.com/pushks18",
  linkedin: "https://www.linkedin.com/in/pushks18/",
  email: "pushkarajbaradkar1@gmail.com",
  scholar: "https://scholar.google.com/citations?user=pushkaraj",
  resume: "/resume.pdf",
};

export const RESEARCH_STATEMENT = {
  title: "Pushkaraj Baradkar",
  role: "Master's Student in Computer Science",
  institution: "University of Southern California (USC Viterbi)",
  advisor: "USC AI Systems & Computer Vision Lab",
  location: "Los Angeles, CA & Austin, TX",
  status: "I am actively seeking full-time AI Engineer & Research roles for 2026 / 2027!",
  bio: [
    "I am a Master's student in Computer Science at the University of Southern California (USC), Viterbi School of Engineering, graduating in December 2026. Previously, I completed my Bachelor's in Computer Engineering at the University of Mumbai with distinction.",
    "My research and engineering focus centers on building real-time AI systems, computer vision & SLAM pipelines, and scalable personalization engines. I study data-driven systems that combine multi-modal perception, factor-graph optimization, and high-throughput vector retrieval.",
    "During my graduate studies, I've pursued two complementary research and engineering directions:"
  ],
  topics: [
    {
      title: "Real-Time AI & Spatial Vision Systems",
      description: "I build real-time visual odometry (VO), monocular depth estimation, and SLAM pipelines achieving 20-25 FPS. My work fuses sparse depth with GPS/IMU in GTSAM factor graphs, reducing trajectory errors to sub-meter precision (~1.2m ATE) and creating topological semantic memory for open-vocabulary scene understanding."
    },
    {
      title: "Personalization & Recommendation Infrastructure",
      description: "I design end-to-end personalized discovery architectures (retrieve → rank → re-rank). At Tabhi, I engineered hybrid vector + BM25 retrieval over 188K+ items with slot-based re-ranking, recency-decayed user preference modeling, and sub-500ms multi-tier caching."
    }
  ]
};

export const NEWS = [
  {
    id: "tabhi-intern",
    date: "May 2026",
    content: "Joined **Tabhi** as an **AI Engineer Intern** in Austin, TX! Working on hybrid vector search, cold-start mitigation, and real-time personalized discovery feeds for a 188K+ item catalog.",
    highlight: true,
  },
  {
    id: "scbc-agentpay",
    date: "Feb 2026",
    content: "Built **AgentPay** at the **Southern California Blockchain Hackathon (SCBC 2026)** — an autonomous multi-agent micro-economy powered by on-chain payments & verifiable reputation!",
    link: "https://agent-pay-lake.vercel.app/",
    linkText: "Live Demo",
    highlight: true,
  },
  {
    id: "usc-ra",
    date: "Nov 2025",
    content: "Started as **Software Engineer Intern / RA (Real-Time AI Systems)** at **USC**, building real-time monocular visual odometry & topological SLAM pipelines.",
    highlight: false,
  },
  {
    id: "swe-conf",
    date: "Feb 2025",
    content: "Participated in the **Society of Women Engineers (SWE) Conference 2025** showcasing AI/ML applications and spatial computing.",
    highlight: false,
  },
  {
    id: "ieee-paper",
    date: "Oct 2023",
    content: "Presented paper *'Blockchain-based Music Streaming Platform using NFTs'* at **IEEE ICSCSS 2023**! Published in IEEE Xplore.",
    link: "https://ieeexplore.ieee.org/abstract/document/10169304",
    linkText: "IEEE Paper",
    highlight: true,
  },
  {
    id: "syrus-win",
    date: "May 2023",
    content: "Won **1st Place** at the **Syrus 2023 Hackathon** for building an innovative decentralized platform!",
    highlight: false,
  }
];

export const CONFERENCES = [
  "Southern California Blockchain Conference (SCBC) 2026",
  "Participated in SWE (Society of Women Engineers) Conference 2025",
  "Presented blockchain paper at ICSCSS 2023",
];

export const ACHIEVEMENTS = [
  "Built AgentPay at Southern California Blockchain Hackathon (SCBC) 2026",
  "Won Syrus 2023 Hackathon",
  "Shortlisted for SIH 2023 Hackathon",
  "Shortlisted for IndeHub 2025 Hackathon",
  "Shortlisted for CodeShashtra 2023 & 2024",
];

