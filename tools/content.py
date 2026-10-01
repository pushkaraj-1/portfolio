# -*- coding: utf-8 -*-
"""All site content. Edit here, then run:  python3 tools/build_site.py"""

SITE = {
    "name": "Pushkaraj Baradkar",
    "role": "MS Computer Science @ USC Viterbi",
    "tagline": "I build production AI systems: search and recommendation, "
               "generative and agentic LLM applications, real-time computer vision, "
               "and decision policies learned from logged data.",
    "blurb": (
        "Final-year Master's student in Computer Science at the <strong>University of "
        "Southern California</strong>, graduating <strong>December 2026</strong>."
    ),
    "status": "Seeking full-time Software Engineering, AI/ML Engineering, and Research roles.",
    "location": "Los Angeles, CA",
    "email": "pushkarajbaradkar1@gmail.com",
    "phone": "+1 (213) 275-9348",
    "github": "https://github.com/pushkaraj-1",
    "linkedin": "https://www.linkedin.com/in/pushkarajbaradkar",
    "scholar": "https://scholar.google.com/citations?user=emGawekAAAAJ&hl=en",
    "photo": "assets/img/profile.jpeg",
    "resume_view_url": "https://drive.google.com/file/d/10jmVGDUbspW-O4RcJK-UkkevNug94hOk/view?usp=sharing",
    "resume_download_url": "assets/resume/resume.pdf",
}

QUICK_FACTS = [
    ("Focus",    "AI/ML Engineering · Retrieval &amp; RecSys · Agentic Systems"),
    ("Studying", "MS Computer Science, USC Viterbi (Dec 2026)"),
    ("Now",      "Research Assistant &amp; CSCI 585 Grader, USC"),
    ("Based",    "Los Angeles, CA"),
]

EXPERIENCE = [
    {
        "slug": "tabhi",
        "role": "AI Engineer Intern, Search &amp; Recommendation Systems",
        "org": "Tabhi", "org_url": "https://tabhi.com",
        "logo": "assets/img/logos/tabhi.avif",
        "location": "Austin, TX", "dates": "May 2026 – Aug 2026",
        "summary": "Architected an end-to-end personalized discovery feed over 450K+ items, "
                   "and cut cold-feed latency from 8 s to 500 ms.",
        "points": [
            "Architected an end-to-end personalized discovery feed for 450K+ items using hybrid "
            "retrieval and slot-based re-ranking.",
            "Designed recency-decayed personalization over Elasticsearch BM25 and pgvector retrieval "
            "using behavioral signals.",
            "Reduced cold-feed latency from 8 s to 500 ms by three-tier caching, cache pre-warming, "
            "optimized indexing, and geospatial retrieval.",
            "Built recommendation analytics using RudderStack to capture user behavior and optimize "
            "personalization through engagement metrics.",
            "Resolved Elasticsearch–MongoDB consistency issues and hardened location-aware retrieval, "
            "improving recommendation reliability.",
        ],
        "tags": ["Elasticsearch", "pgvector", "Hybrid Retrieval", "Re-ranking", "Caching",
                 "RudderStack", "MongoDB"],
    },
    {
        "slug": "usc-ra",
        "role": "Research Assistant, Real-Time AI Systems",
        "org": "University of Southern California", "org_url": "https://www.usc.edu/",
        "logo": "assets/img/logos/usc-shield.png",
        "location": "Los Angeles, CA", "dates": "Nov 2025 – Present",
        "advisor": "Prof. Laurent Itti",
        "summary": "Monocular SLAM for assistive smart glasses: a C++ GTSAM pose-graph backend cut "
                   "trajectory error from 29–58 m to 0.09–0.24 m.",
        "points": [
            "Implemented a monocular SLAM pipeline for assistive smart glasses using a 16-zone ToF "
            "sensor to recover metric scale.",
            "Built a GTSAM pose-graph backend in C++, reducing trajectory error from 29–58 m to "
            "0.09–0.24 m while optimizing 2,486 poses in 0.36 s.",
            "Designed a physics-based ToF simulator and optimized zone pooling, halving trajectory "
            "error with 2–4% scale accuracy.",
            "Extending the factor graph to fuse IMU, ultrasonic, and GPS measurements for deployment "
            "on a Jetson Orin Nano.",
        ],
        "tags": ["SLAM", "GTSAM", "C++", "ToF Sensing", "Sensor Fusion", "Jetson Orin Nano"],
    },
    {
        "slug": "usc-grader",
        "role": "Grader, CSCI 585 Database Systems",
        "org": "University of Southern California", "org_url": "https://www.usc.edu/",
        "logo": "assets/img/logos/usc-shield.png",
        "location": "Los Angeles, CA", "dates": "Aug 2026 – Present",
        "advisor": "Prof. Shahram Ghandeharizadeh",
        "summary": "Evaluating Database Systems coursework for 200+ students under "
                   "Prof. Shahram Ghandeharizadeh.",
        "points": [
            "Evaluate Database Systems coursework for 200+ students across core and distributed "
            "systems.",
            "Develop and grade technical assessments on database algorithms and architectures, "
            "evaluating correctness and performance tradeoffs.",
        ],
        "tags": ["Database Systems", "Distributed Systems", "Teaching"],
    },
    {
        "slug": "ymt-medical",
        "role": "Machine Learning Intern, Edge Computer Vision",
        "org": "YMT Medical", "org_url": "",
        "logo": "",
        "location": "India", "dates": "Jan 2024 – Aug 2024",
        "summary": "On-device clinical vision for micro-lesion detection (0.83 mAP@0.5) and "
                   "deterministic acne grading, with ~40% faster edge inference.",
        "points": [
            "Redesigned YOLOv8 with a P2 head and NWD loss for micro-lesion detection across 2,000+ "
            "patient images, achieving 0.83 mAP@0.5.",
            "Built a Laplacian/HSV image-quality pipeline to detect blur and glare in patient uploads "
            "before model inference.",
            "Optimized edge inference using INT8 quantization and operator fusion, reducing latency "
            "by approximately 40%.",
            "Mapped 468 MediaPipe facial landmarks to compute deterministic GAGS acne scores offline "
            "with an active learning loop.",
        ],
        "tags": ["YOLOv8", "INT8 Quantization", "MediaPipe", "OpenCV", "Edge ML"],
    },
    {
        "slug": "technoriya",
        "role": "Software Engineer Intern, Backend &amp; APIs",
        "org": "Technoriya ERP Solution", "org_url": "",
        "logo": "assets/img/logos/technoriya.png",
        "location": "India", "dates": "Oct 2023 – Dec 2023",
        "summary": "Built backend services and APIs supporting scalable data pipelines and "
                   "cloud-based ML workflows.",
        "points": [
            "Developed Python and Node.js backend services and APIs supporting scalable data "
            "pipelines and cloud-based ML workflows.",
            "Implemented secure authentication and access protocols via Firebase Auth and "
            "Firestore rules to ensure data integrity.",
            "Optimized RESTful APIs and Firestore queries to achieve 450 ms response times under "
            "1,000 concurrent requests for ML integration.",
        ],
        "tags": ["Python", "Node.js", "REST", "Firebase"],
    },
]

EDUCATION = [
    {
        "school": "University of Southern California, Viterbi School of Engineering",
        "url": "https://viterbischool.usc.edu/", "logo": "assets/img/logos/usc-shield.png",
        "degree": "Master of Science in Computer Science",
        "dates": "Jan 2025 – Dec 2026", "location": "Los Angeles, CA",
        "score": "GPA 3.73 / 4.00",
        "courses": ["Machine Learning for Data Science", "Analysis of Algorithms",
                    "Web Technologies", "Database Systems"],
    },
    {
        "school": "University of Mumbai",
        "url": "", "logo": "assets/img/logos/universityofmumbai.svg",
        "degree": "Bachelor of Engineering in Computer Engineering",
        "dates": "Jul 2020 – May 2024", "location": "Mumbai, India",
        "score": "GPA 9.13 / 10",
        "courses": ["Data Structures", "Analysis of Algorithms", "Operating Systems",
                    "Computer Networks", "Machine Learning", "Natural Language Processing"],
    },
]

SKILLS = [
    ("Programming Languages", ["Python", "C++", "Java", "JavaScript", "TypeScript"]),
    ("AI / ML & Deep Learning", ["Deep Learning", "PyTorch", "TensorFlow", "Transformers",
                                 "Computer Vision", "NLP", "Reinforcement Learning", "Offline RL",
                                 "scikit-learn", "Pandas", "NumPy"]),
    ("Generative AI & Agents", ["LLMs", "RAG", "Agentic AI Systems", "Prompt Engineering",
                                "LangChain", "LangGraph", "MCP", "Google ADK", "A2A", "Langfuse"]),
    ("Retrieval & Recommendation", ["Elasticsearch BM25", "Hybrid Search", "Vector Retrieval",
                                    "FAISS", "pgvector", "Two-Tower / SASRec",
                                    "Off-policy Evaluation"]),
    ("Computer Vision & Edge", ["Visual Odometry / SLAM", "GTSAM", "OpenCV", "YOLOv8",
                                "FastSAM / SAM", "MediaPipe", "INT8 Quantization", "CoreML",
                                "ONNX Runtime"]),
    ("Privacy & Trustworthy ML", ["Differential Privacy", "diffprivlib", "Membership Inference",
                                  "Off-policy Evaluation"]),
    ("Frameworks & Development", ["FastAPI", "Flask", "Django", "Node.js", "Express.js",
                                  "React.js", "Next.js", "Streamlit", "OAuth"]),
    ("Databases & Cloud", ["PostgreSQL", "MongoDB", "SQL", "Redis", "Supabase", "AWS", "GCP",
                           "Azure", "Docker", "Kubernetes", "Git", "CI/CD", "Linux"]),
]

RESEARCH = [
    {
        "title": "Blockchain Based Music Streaming Platform Using NFTs",
        "authors": "P. Baradkar et al.",
        "venue": "IEEE ICSCSS 2023",
        "note": "Cited by 7",
        "image": "assets/img/diagrams/publication-ieee.svg",
        "abstract": "A blockchain-based music streaming platform leveraging NFTs for rights "
                    "management and royalty distribution, enabling transparent and automated "
                    "compensation for artists.",
        "links": [("Paper", "https://ieeexplore.ieee.org/abstract/document/10169304"),
                  ("Code", "https://github.com/pushkaraj-1/Music-streaming-platform-using-blockchain"),
                  ("Google Scholar", "https://scholar.google.com/citations?user=emGawekAAAAJ&hl=en")],
    },
]

# TODO: add the rest of your activities here, same shape as the entries below.
ACTIVITIES = [
    {"title": "Rotaract Club of Thane Greenspans", "role": "Community Engagement Volunteer",
     "logo": "", "dates": "Jul 2023 – Jun 2024",
     "desc": "Coordinated 10+ volunteers on coastal cleanups and sustainability campaigns that removed "
             "over 100 kg of waste, and led logistics for donation drives reaching 30+ people from "
             "underserved communities."},
    {"title": "USC Mentorship Programme", "role": "Mentor",
     "logo": "assets/img/logos/usc-shield.png", "dates": "",
     "desc": "Mentoring incoming graduate students on coursework, research direction, and internship search."},
]

AWARDS = [
    ("1st Place, Syrus 2023 Hackathon", "2023"),
    ("Second round, Smart India Hackathon (SIH) 2023", "2023"),
    ("Finalist, IndeHub Hackathon 2025", "2025"),
    ("CodeShastra 9.0 &amp; X, DJ Sanghvi College of Engineering", "2023–2024"),
    ("Presented at IEEE ICSCSS 2023 · SWE Conference 2025", "2023–2025"),
]

# Paper presentations. Each gets its own write-up page under talks/.
TALKS = [
    {
        "slug": "mlm-membership-inference",
        "title": "Quantifying Privacy Risks of Masked Language Models Using Membership Inference Attacks",
        "paper_authors": "Mireshghallah, Goyal, Uniyal, Berg-Kirkpatrick &amp; Shokri",
        "paper_venue": "EMNLP 2022",
        "context": "CSCI 699 · Side-Channel Threats in Cloud &amp; LLM Systems · USC · Fall 2026",
        "image": "assets/img/talks/mlm-mia-figure1.png",
        "abstract": "Paper presentation. Loss-threshold attacks made masked LMs look safe; a likelihood-ratio "
                    "test against a reference model, scored as an energy gap, lifts attack AUC on "
                    "ClinicalBERT from 0.66 to 0.90, and to 0.99 per patient.",
        "links": [("arXiv", "https://arxiv.org/abs/2203.03929")],
        "body": """
<p>A paper presentation for CSCI 699 at USC. The paper is by Mireshghallah, Goyal, Uniyal,
Berg-Kirkpatrick and Shokri (EMNLP 2022). This page is my summary and my reading of it.</p>

<h2>The question</h2>
<p>BERT-style models are fine-tuned on data nobody would publish: hospital notes, legal filings,
internal email. The weights get shared; the notes do not. <strong>Can someone holding the model
tell whose records it was trained on?</strong> Membership alone is a breach: confirming that a
sentence from one patient's record trained a model built on an HIV clinic's notes reveals that the
person was a patient there. The case study is <strong>ClinicalBERT</strong>, trained on MIMIC-III
(about 1.25M health records from 46,520 patients).</p>

<h2>Why earlier work said MLMs were safe</h2>
<p>Prior attacks thresholded the model's loss: a low loss means "the model has seen this". On
ClinicalBERT-Base that gives <strong>AUC 0.66</strong> and only 15.6% recall at a 10% false-positive
rate, so the field concluded masked LMs memorize little. The paper argues this was a weak attack,
not a safe model. Loss measures <em>difficulty</em>, not memory: "The patient is stable." looks
familiar to every medical model, and "Pt c/o SOB x3d, Hx CHF" looks strange even to one that
trained on it.</p>

<h2>The idea: compare against a reference model</h2>
<p>Score the sentence under the target model <em>and</em> under a reference model that never saw
the training data (PubMed-BERT), and look at the gap. If both find it easy, it is just an easy
sentence. If only the target does, the target memorized it. Formally this is a likelihood ratio
test, the optimal test for this kind of hypothesis.</p>

<figure class="fig"><a href="assets/img/talks/mlm-mia-figure1.png" target="_blank" rel="noopener" title="Open full size"><img src="assets/img/talks/mlm-mia-figure1.png" alt="Attack pipeline: a target sample is scored by energy-based versions of the target model and a PubMed reference model, and the log ratio of the two likelihoods is compared with a threshold to decide member or non-member" loading="lazy"></a><figcaption>Figure 1 from Mireshghallah et al., EMNLP 2022: the likelihood-ratio attack with a reference model.</figcaption></figure>

<p>The obstacle is that a masked LM has no sentence probability; it only fills in blanks. The fix
is to treat the MLM as an <strong>energy-based model</strong>, with p(s) = exp(−E(s)) / Z. The
normalizer Z cannot be computed, but it depends only on the model, so in the ratio it becomes one
global constant and cancels. The score reduces to
<code>L(s) = E(s; target) − E(s; reference)</code>, where energy is the average fill-in-the-blank
loss over K = 10 random 15% masks. No shadow models are trained; scoring takes about 18 GPU-hours.</p>

<h2>Results</h2>
<ul>
<li>Sample level: <strong>AUC 0.66 → 0.90</strong>, recall at 10% FPR from 15.6% to 79.2%, at
88.9% precision.</li>
<li>At 1% FPR, the regime a real attacker works in, the attack is <strong>51× stronger</strong>
than prior work.</li>
<li>Patient level, aggregating all of one patient's notes: <strong>AUC 0.992</strong>. "Was this
person a patient here?" is answered almost perfectly.</li>
<li>Leakage grows with sentence length and model size, and inserting patient names raises AUC to
0.96 while <em>lowering</em> the loss baseline to 0.56. An in-domain reference model matters:
plain BERT drops recall from 79.2% to 71.5%.</li>
</ul>

<h2>Defenses</h2>
<p>Differential-privacy training is the only defense with a worst-case guarantee, at a cost in
accuracy. Scrubbing identifiers, deduplication, regularization and hiding scores all help without
guaranteeing anything.</p>

<h2>My take</h2>
<p>The strongest contribution is reframing a negative result: the models were never safe, the
attack was weak. It is principled and cheap, and it reports low-FPR numbers rather than just AUC.
The limits are that it needs a good same-domain reference model, it is tested only on clinical
BERT, the sensitivity to K is not explored in the main text, and licensed data with gated code
makes it hard to reproduce.</p>

<p>Why it belongs in a side-channel course: strictly, it is not a side channel, because the signal
is the model's own output. But the pattern is the same one used all semester. A raw measurement is
confounded by noise (sentence difficulty here, clock frequency or system load there), and
calibrating against a baseline makes the real signal appear, just like setting a hit/miss
threshold in Flush+Reload. The natural next step is membership or prompt inference on an LLM
through a timing or hardware channel instead of scores.</p>
""",
    },
]

# (date, label, html), sorted newest first below, so entries can be added in any order
NEWS = [
    ("2026-09", "Sep, 2026",
     'Presented <a href="talks/mlm-membership-inference.html"><em>"Quantifying Privacy Risks of Masked '
     'Language Models Using Membership Inference Attacks"</em></a> (EMNLP 2022) in <strong>CSCI 699</strong> '
     'at USC.'),
    ("2026-08", "Aug, 2026",
     'Started as a <strong>Grader</strong> for <strong>CSCI 585 Database Systems</strong> at USC, under '
     'Prof. Shahram Ghandeharizadeh.'),
    ("2026-08", "Aug, 2026",
     'Built a <a href="projects/warp-tote.html"><strong>warehouse tote perception</strong></a> pipeline: '
     '0.958 pick score on 120 ARMBench images, 619 ms median on a laptop CPU.'),
    ("2026-05", "May, 2026",
     'Joined <a href="https://tabhi.com" target="_blank" rel="noopener"><strong>Tabhi</strong></a> as an '
     '<strong>AI Engineer Intern</strong> (Search &amp; Recommendation Systems) in Austin, TX, building hybrid '
     'Elasticsearch and vector retrieval over a 450K-item catalog.'),
    ("2026-04", "Apr, 2026",
     'Contributed an <strong>RPC reliability &amp; failover redesign</strong> to the '
     '<a href="https://github.com/DefiLlama/defillama-sdk" target="_blank" rel="noopener">DefiLlama SDK</a>, '
     'fixing endpoint override precedence and adding runtime quarantine.'),
    ("2026-02", "Feb, 2026",
     'Built <a href="https://agent-pay-lake.vercel.app/" target="_blank" rel="noopener"><strong>AgentPay</strong></a> '
     'at the <strong>Southern California Blockchain Hackathon</strong>: an autonomous multi-agent '
     'micro-economy with on-chain payments and staked reputation.'),
    ("2025-07", "Jul, 2025",
     'Reached the <strong>final round</strong> of the <strong>IndeHub Hackathon 2025</strong>, a '
     'post-WWDC hybrid hackathon for building on Apple platforms, with '
     '<a href="https://github.com/pushkaraj-1/Voxel-Strides" target="_blank" rel="noopener"><strong>Voxel '
     'Strides</strong></a>: an iOS app that turns daily tasks into a gamified adventure, with an ARKit '
     'companion and an on-device Core ML agent that breaks goals into steps.'),
    ("2025-10", "Oct, 2025",
     'Attended <strong>WE25</strong>, the Society of Women Engineers annual conference, in '
     '<strong>New Orleans, Louisiana</strong>.'),
    ("2025-11", "Nov, 2025",
     'Started as a <strong>Research Assistant</strong> (Real-Time AI Systems) at <strong>USC</strong> under '
     '<strong>Prof. Laurent Itti</strong>, building real-time monocular visual odometry and SLAM with a GTSAM '
     'factor-graph backend.'),
    ("2025-01", "Jan, 2025",
     'Started a <strong>Master of Science in Computer Science</strong> at the <strong>USC Viterbi '
     'School of Engineering</strong> in Los Angeles.'),
    ("2024-05", "May, 2024",
     'Graduated with a <strong>Bachelor of Engineering in Computer Engineering</strong> from the '
     '<strong>University of Mumbai</strong>, GPA 9.13 / 10.'),
    ("2024-03", "Mar, 2024",
     'Returned for <strong>CodeShastra X</strong>, the 10th-anniversary edition of the 24-hour national '
     'hackathon at DJ Sanghvi College of Engineering, Mumbai.'),
    ("2023-04", "Apr, 2023",
     'Competed at <strong>CodeShastra 9.0</strong>, a 24-hour offline hackathon organised by the DJ-CSI '
     'Student Chapter at DJ Sanghvi College of Engineering, Mumbai.'),
    ("2024-01", "Jan, 2024",
     'Joined <strong>YMT Medical</strong> as a <strong>Machine Learning Intern</strong>, building on-device clinical '
     'computer vision for micro-lesion detection and deterministic acne grading.'),
    ("2023-09", "Sep, 2023",
     'Reached the <strong>second round</strong> of the <strong>Smart India Hackathon (SIH) 2023</strong>.'),
    ("2023-07", "Jul, 2023",
     'Joined the <strong>Rotaract Club of Thane Greenspans</strong> as a Community Engagement Volunteer, '
     'running coastal cleanups that removed over 100 kg of waste and donation drives for underserved '
     'communities.'),
    ("2023-10", "Oct, 2023",
     'Presented <em>"Blockchain-based Music Streaming Platform using NFTs"</em> at '
     '<a href="https://ieeexplore.ieee.org/abstract/document/10169304" target="_blank" rel="noopener">'
     '<strong>IEEE ICSCSS 2023</strong></a>. Published in IEEE Xplore.'),
    ("2023-05", "May, 2023",
     'Won <strong>1st place</strong> out of 50+ teams at <strong>Syrus 2023</strong>, a 24-hour Web3 '
     'hackathon organised by CodeCell, VESIT.'),
    ("2020-07", "Jul, 2020",
     'Began a <strong>Bachelor of Engineering in Computer Engineering</strong> at the '
     '<strong>University of Mumbai</strong>.'),
]

NEWS.sort(key=lambda n: n[0], reverse=True)
