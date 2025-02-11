SELECT r.Name, r.Role, r.Core_Technical_Expertise
FROM Resources r
WHERE r.Core_Technical_Expertise LIKE '%NLP%' AND r.Years_of_Experience > 3;









-- - SELECT p.Project_Name, d.Deliverable_Description 
-- FROM Projects p
-- JOIN Project_Deliverables d ON p.Project_ID = d.Project_ID;






-- SELECT r.Name, r.Role 
-- FROM Resources r
-- JOIN Resource_Projects rp ON r.Resource_ID = rp.Resource_ID
-- JOIN Projects p ON rp.Project_ID = p.Project_ID
-- WHERE p.Project_Name = 'AI-Powered Customer Support System';




-- -- Create the Project_Types table
-- CREATE TABLE Project_Types (
--     Project_Type_ID INT AUTO_INCREMENT PRIMARY KEY,
--     Project_Type VARCHAR(100) NOT NULL UNIQUE
-- );

-- -- Create the Projects table
-- CREATE TABLE Projects (
--     Project_ID INT AUTO_INCREMENT PRIMARY KEY,
--     Project_Name VARCHAR(255) NOT NULL,
--     Project_Type_ID INT,
--     Year_Implemented INT NOT NULL,
--     Delivery_Timeline VARCHAR(50),
--     Status ENUM('delivered', 'in support', 'in progress') NOT NULL,
--     Description TEXT,
--     FOREIGN KEY (Project_Type_ID) REFERENCES Project_Types(Project_Type_ID)
-- );

-- -- Create the Project_Deliverables table
-- CREATE TABLE Project_Deliverables (
--     Deliverable_ID INT AUTO_INCREMENT PRIMARY KEY,
--     Project_ID INT,
--     Deliverable_Description TEXT,
--     FOREIGN KEY (Project_ID) REFERENCES Projects(Project_ID)
-- );

-- -- Create the Resources table
-- CREATE TABLE Resources (
--     Resource_ID INT AUTO_INCREMENT PRIMARY KEY,
--     Name VARCHAR(255) NOT NULL,
--     Role VARCHAR(100) NOT NULL,
--     Qualification VARCHAR(255),
--     Years_of_Experience INT CHECK (Years_of_Experience >= 0),
--     Core_Technical_Expertise TEXT
-- );

-- -- Create the Resource_Projects table
-- CREATE TABLE Resource_Projects (
--     Resource_Project_ID INT AUTO_INCREMENT PRIMARY KEY,
--     Resource_ID INT,
--     Project_ID INT,
--     FOREIGN KEY (Resource_ID) REFERENCES Resources(Resource_ID),
--     FOREIGN KEY (Project_ID) REFERENCES Projects(Project_ID)
-- );


-- Insert into Project_Types
-- INSERT INTO Project_Types (Project_Type) 
-- VALUES ('AI Chatbot'), ('AI Matcher'), ('Forecasting');


-- INSERT INTO Projects (Project_Name, Project_Type_ID, Year_Implemented, Delivery_Timeline, Status, Description)
-- VALUES 
--     ('AI-Powered Customer Support System', 1, 2022, '2022-06 to 2022-12', 'delivered', 'Designed and developed a chatbot system leveraging large language models (LLMs) to handle customer queries, automate responses, and escalate complex issues to human agents when needed. Integrated NLP for understanding customer intent and entity extraction.
-- -- Technology Stack:
-- Frontend: React.js for the user interface
-- Backend: Node.js for server-side logic, Express.js for APIs
-- LLM Integration: OpenAI GPT APIs via LangChain for conversational flow management
-- Database: PostgreSQL for structured data, Redis for caching frequently accessed data
-- NLP: SpaCy for intent recognition, entity extraction, and tokenization
-- Graph-based Querying: LangGraph for managing conversation states and knowledge graph queries
-- Message Queue: RabbitMQ for managing chatbot and human escalation processes
-- Deployment: Dockerized microservices architecture, deployed on AWS (ECS, Lambda, or EC2)
-- Authentication and Security: OAuth 2.0, JWT tokens for user authentication, and SSL encryption
-- Monitoring & Logging: Prometheus for performance monitoring, ELK Stack for logging
-- Libraries & Tools:
-- LangChain: To handle conversation context, memory management, and LLM chaining
-- LangGraph: For querying graphs and mapping conversation states dynamically
-- Hugging Face Transformers: For fallback tasks like intent classification or summarization
-- openpyxl (Optional): For handling data exchanges between the system and external Excel sheets
-- Languages:
-- JavaScript (Node.js, React.js)
-- Python (for LLM integration and NLP tasks)
-- SQL (PostgreSQL)
-- '),

--     ('Employee Skill-Matching System', 2, 2023, '2023-01 to 2023-09', 'delivered', 'Developed an AI-powered system designed to analyze employee skills, availability, and project requirements to optimize task allocation. The system leveraged natural language processing (NLP) to extract relevant skills from CVs, automated project assignments, and improved employee productivity by reducing time spent on manual task assignments.
-- Technology Stack:
-- Frontend: React.js for the user dashboard and project management interface
-- Backend: Python (Flask/FastAPI) for server-side logic and API endpoints
-- Database: PostgreSQL for structured employee and project data storage
-- NLP & AI: Hugging Face Transformers and SpaCy for extracting skills and entities from CVs and job descriptions
-- Machine Learning Algorithms:
-- TF-IDF Vectorization for encoding skill and job requirement text
-- Cosine Similarity to measure the closeness between employee skills and project requirements
-- K-Nearest Neighbors (KNN) for recommendation of the most suitable employees for each project
-- Decision Trees (Optional) for task prioritization and skill-gap analysis
-- Graph-based Matching: LangGraph for knowledge graph querying and mapping relationships between skills, employees, and tasks
-- Recommendation Engine: Scikit-learn for skill-matching and project recommendations
-- Data Processing: Pandas and NumPy for data transformation and analysis
-- Scheduling & Availability Check: Integration with project-tracking Excel sheets using openpyxl
-- Cloud Deployment: AWS (EC2, S3, RDS) or Google Cloud Platform (GKE, Cloud Functions)
-- Authentication and Security: JWT for session management and role-based access control
-- Version Control & CI/CD: GitHub Actions for automated deployment and testing
-- Libraries & Tools:
-- LangChain: To handle dynamic querying and task assignment logic
-- LangGraph: For knowledge graph construction and query mapping
-- Scikit-learn: For implementing recommendation and classification models
-- Hugging Face Transformers & SpaCy: For advanced NLP tasks
-- openpyxl: For tracking project assignments and updating availability in Excel
-- Languages:
-- Python (NLP, backend logic, data processing)
-- JavaScript (React.js for frontend)
-- SQL (PostgreSQL for database queries)
-- Specific Algorithms/Techniques Used:
-- TF-IDF and Cosine Similarity: Matching skill vectors with job requirement vectors
-- KNN-based Employee Recommendation: Selecting the top candidates for each project
-- LangGraph Querying: Capturing dynamic relationships between employees, skills, and projects
-- Skill-Gap Analysis: Using Decision Trees or rule-based logic to identify missing skills
-- '),

--     ('Retail Sales Forecasting', 3, 2023, '2023-03 to 2023-12', 'in support', 'Developed an AI-driven demand prediction system to help retail businesses optimize inventory management and reduce stock shortages or overages. The system used time-series forecasting techniques and machine learning models to predict sales, enabling better planning and efficient resource allocation.

-- Technology Stack:

-- Data Collection: Apache Airflow for ETL pipeline automation
-- Database: MySQL for storing sales data, product information, and historical records
-- Data Processing: Pandas and NumPy for data cleaning and transformation
-- Modeling & Forecasting:
-- Time-series models (ARIMA, SARIMA)
-- Machine learning models (XGBoost, Random Forest)
-- Deep learning models (LSTMs for long-term forecasting)
-- NLP (Optional): SpaCy or Hugging Face for incorporating external data sources such as news or market trends affecting demand
-- Model Evaluation & Optimization: Hyperparameter tuning with GridSearchCV
-- Visualization: Matplotlib and Plotly for performance tracking and trend analysis
-- Deployment: Flask API to serve predictions, containerized using Docker, deployed on AWS (EC2, S3) or GCP
-- Monitoring & Maintenance: Prometheus and Grafana for monitoring model performance and retraining triggers
-- Languages:

-- Python (data preprocessing, model development, backend logic)
-- SQL (for data querying and analysis)
-- Bash (for ETL pipeline automation)
-- Tools & Libraries:

-- Scikit-learn, TensorFlow/Keras, Statsmodels
-- AWS Lambda for scheduled prediction updates');


-- Insert into Resources
-- INSERT INTO Resources (Name, Role, Qualification, Years_of_Experience, Core_Technical_Expertise)
-- VALUES 
--     ('John Smith', 'AI Engineer', 'Master’s in CS', 5, 'John has extensive experience in designing, developing, and optimizing large language models (LLMs) for various applications, including conversational AI, text generation, and semantic search. His expertise includes fine-tuning models such as GPT, BERT, and T5 for task-specific purposes, leveraging transfer learning to maximize performance across multiple domains.He has a deep understanding of supervised and unsupervised machine learning techniques, such as classification, clustering, and recommendation systems. His work often involves applying algorithms like Random Forest, XGBoost, and deep neural networks to solve business-critical problems.John also has hands-on experience with key tools and libraries, including LangChain (for LLM chaining and task orchestration) and Hugging Face Transformers (for NLP-based tasks). His proficiency in data engineering includes building scalable data pipelines using Pandas, NumPy, and SQL for pre-processing large datasets.Additionally, John has led the deployment of AI models using containerized microservices (Docker) and cloud platforms (AWS, GCP), ensuring low-latency performance and efficient resource allocation. He is well-versed in model monitoring, evaluation, and retraining strategies, utilizing tools such as LangGraph for knowledge-based insights and model state tracking. His ability to bridge the gap between cutting-edge AI research and real-world applications makes him a valuable contributor to enterprise AI projects.'),
--     ('Emma Johnson', 'Data Scientist', 'Bachelor’s in Data Science', 3, 'Emma has developed a strong foundation in data-driven problem-solving through her work on various machine learning and data analysis projects. Her expertise in data preprocessing includes handling missing data, feature engineering, data transformation, and cleaning large datasets to ensure model accuracy and reliability.She has experience working with machine learning models for both supervised and unsupervised learning tasks, including regression, classification, and clustering algorithms. Emma is proficient in key libraries and tools such as Scikit-learn, XGBoost, and TensorFlow/Keras for model development and evaluation. She also specializes in hyperparameter tuning using techniques like GridSearchCV and random search to improve model performance.Emma is skilled in building data pipelines using Pandas, NumPy, and SQL, ensuring that data flows efficiently from source systems to model deployment. Her work often involves integrating external data sources such as APIs and real-time feeds to enhance model predictions.Additionally, she is adept at visualization using tools like Matplotlib and Seaborn to communicate insights effectively to stakeholders. Her deployment experience includes Dockerized machine learning models and cloud-based solutions on AWS and GCP.Emma has shown proficiency in identifying data patterns and anomalies through exploratory data analysis (EDA) and has successfully deployed models for tasks like customer segmentation, demand forecasting, and recommendation systems. Her ability to translate business objectives into actionable machine learning solutions makes her a valuable asset to data-driven teams.'),
--     ('Ayesha Khan', 'NLP Specialist', 'Ph.D. in NLP', 4, 'Ayesha has a deep specialization in developing domain-specific NLP models, particularly for low-resource languages and industry-specific jargon. Her Ph.D. research explored context-aware embeddings and semantic similarity, where she developed novel approaches to handling ambiguous text using attention-based models and hybrid techniques combining symbolic and statistical methods.Her expertise includes low-resource language processing, where she created custom tokenizers and trained word embeddings from scratch using GloVe and FastText. She has also contributed to knowledge extraction in legal and healthcare texts by applying advanced named entity recognition (NER) techniques using CRFs and transformers.In text analytics, Ayesha is proficient in sentiment extraction from unstructured sources, employing advanced linguistic heuristics for fine-grained sentiment detection beyond standard binary classification. She has worked on aspect-based sentiment analysis, integrating syntactic dependency parsing to improve accuracy in reviews and feedback systems.Her practical experience spans working with tools such as Hugging Face Transformers (BERT, RoBERTa) for fine-tuning models, SpaCy for custom pipelines, and LangGraph for integrating knowledge graphs, enhancing fact-checking and document search systems. She’s also skilled in contrastive learning techniques, applied in creating document representations for similarity searches.Additionally, she has contributed to real-time chatbot systems by integrating multilingual NLP capabilities using zero-shot classification and language-specific fine-tuning. Her deployment strategies prioritize optimizing NLP workloads through cloud services like AWS SageMaker and GCP Vertex AI, leveraging model compression techniques like pruning and quantization to reduce latency in production.Her ability to innovate through research-driven, domain-specific NLP applications while meeting real-world scalability demands highlights her core strength as an NLP expert.'),
--     ('Carlos Martinez', 'Software Engineer', 'Bachelor’s in Software Engineering', 4, 'Carlos is a skilled software engineer with extensive experience designing, developing, and integrating scalable software systems. His primary expertise lies in building robust, RESTful and GraphQL APIs, ensuring high availability and performance for enterprise applications. He has developed secure, scalable backend systems using frameworks like Express.js, Django, and FastAPI.Carlos has a strong focus on microservices architecture, leveraging containerization tools such as Docker and orchestration tools like Kubernetes for deploying distributed systems. He is proficient in developing APIs that facilitate seamless communication between distributed services using message queues such as RabbitMQ and Apache Kafka.His system integration expertise includes connecting disparate enterprise systems through middleware and custom APIs. He has led projects involving integration of third-party services, such as payment gateways (Stripe, PayPal) and cloud storage (AWS S3, Google Cloud Storage), using OAuth and token-based authentication.Carlos is proficient in building scalable backend data pipelines, performing ETL operations to integrate structured and unstructured data using Pandas and SQLAlchemy. His deep understanding of error-handling, caching strategies (Redis), and API versioning has enabled him to create reliable systems with minimal downtime.He has optimized API performance using techniques like load balancing, rate-limiting, and caching to reduce latency and ensure smooth scaling under high workloads. Carlos also follows DevOps best practices, using CI/CD pipelines (Jenkins, GitHub Actions) to automate deployments and ensure continuous delivery.He actively contributes to improving system security by implementing JWT-based authentication, API gateway protection, and conducting security audits to prevent common vulnerabilities like SQL injection and XSS attacks. His collaborative approach and problem-solving mindset allow him to efficiently work with cross-functional teams, making him a valuable asset in complex, distributed system environments.'),
--     ('Sofia Patel', 'AI Product Manager', 'MBA in Technology Management', 6, 'Sofia is a results-driven AI Product Manager with a unique combination of technical understanding and business acumen, making her adept at bridging the gap between technical teams and stakeholders. Her expertise lies in overseeing end-to-end development of AI products, from concept and requirements gathering to deployment and maintenance. She excels in resource allocation, sprint planning, and optimizing development cycles to meet project deadlines while ensuring product quality.Sofia has led cross-functional teams consisting of AI engineers, data scientists, designers, and marketing professionals to successfully deliver AI-driven applications in industries such as healthcare, retail, and finance. She is experienced in using Agile methodologies (Scrum, Kanban) and project management tools such as JIRA, Trello, and Asana to maintain project transparency and efficiency.Her strong understanding of AI systems and technical concepts enables her to communicate effectively with engineering teams and stakeholders. She is familiar with core machine learning concepts, LLM-based systems, and NLP models and can guide decision-making on topics like model selection, deployment strategies, and performance monitoring.Sofia’s resource allocation skills involve managing budgets, negotiating project scope, and maximizing the productivity of team members by aligning resources with key project priorities. She has optimized resource allocation using project analytics dashboards and performance-tracking systems, ensuring minimal resource wastage.She is also adept at conducting market research and competitive analysis to identify key opportunities for AI innovation. Her ability to gather user feedback and translate it into actionable product enhancements has significantly contributed to successful product iterations. Sofia’s data-driven approach to risk assessment and mitigation has proven valuable in maintaining project timelines and reducing unexpected delays.With experience in cloud-based AI deployments (AWS, GCP) and product lifecycle management, she has successfully overseen the release of AI models embedded in SaaS applications. Sofia’s focus on aligning business objectives with AI product goals ensures that the solutions delivered provide measurable business impact and user satisfaction.'),
--     ('Liam Davis', 'UI/UX Designer', 'Bachelor’s in Design', 5, 'Liam is a creative and user-focused UI/UX designer with five years of experience crafting intuitive, accessible, and visually appealing user interfaces for web and mobile applications. His expertise lies in user-centered design (UCD), where he applies human-computer interaction principles to create products that enhance usability and customer satisfaction.Liam has led the end-to-end design process, including user research, wireframing, prototyping, usability testing, and final design implementation. His designs balance functionality and aesthetics by leveraging tools such as Figma, Adobe XD, Sketch, and InVision. His wireframes and interactive prototypes help align stakeholders and development teams before implementation, reducing costly design revisions.He excels in design systems development, creating scalable and reusable components to maintain design consistency across large applications. His knowledge of color theory, typography, and responsive design ensures that the interfaces he designs are accessible across different devices and meet WCAG accessibility standards.Liam’s proficiency extends to conducting usability studies and A/B testing to evaluate design effectiveness and iteratively improve products based on user feedback. He works closely with developers to ensure seamless handoff and accurate design implementation using tools like Zeplin.He has collaborated on AI and data-driven UI designs, creating interfaces for dashboards, analytics tools, and recommendation engines where large data visualization was key. His experience includes using D3.js and Plotly to visualize data interactively.Liam’s ability to balance user needs with business requirements has enabled him to contribute to successful product launches across industries, including e-commerce, SaaS platforms, and fintech applications. His excellent communication skills and collaborative approach with cross-functional teams make him an essential part of any product development lifecycle.'),
--     ('Ahmed Ali', 'DevOps Engineer', 'Bachelor’s in IT', 4, 'Ahmed is a highly skilled DevOps engineer with expertise in building and managing scalable, automated infrastructure to support continuous delivery and deployment of applications. His proficiency in CI/CD pipelines has enabled teams to reduce deployment times and improve the reliability of releases through tools like Jenkins, GitLab CI/CD, and GitHub Actions.He has extensive experience with containerization technologies, including Docker and orchestration tools like Kubernetes, ensuring smooth deployment of distributed microservices. Ahmed’s work often involves optimizing the scalability of cloud-native applications using AWS (ECS, Lambda) and Google Cloud (GKE), incorporating autoscaling strategies for cost-effective resource allocation.His infrastructure-as-code (IaC) expertise includes writing maintainable and scalable scripts using Terraform and Ansible, enabling automated provisioning and configuration of infrastructure. He has also implemented monitoring and logging solutions using Prometheus, Grafana, and ELK Stack, ensuring high system reliability and quick incident response.Ahmed is proficient in load balancing, horizontal scaling, and system resilience techniques, ensuring high availability even under heavy workloads. He also has hands-on experience in security best practices, including setting up network policies, identity access management (IAM), and automated vulnerability scans using tools like SonarQube and OWASP ZAP.With strong collaboration skills, Ahmed works closely with developers and QA teams to resolve deployment issues and improve development pipelines, making him a key contributor to any DevOps-driven organization.'),
--     ('Maya Chen', 'AI Researcher', 'Ph.D. in AI', 7, 'Maya is an accomplished AI researcher with a deep understanding of cutting-edge machine learning models and techniques, having worked extensively in both academia and industry. Her expertise spans LLMs, reinforcement learning, computer vision, and multi-modal models, making her a key contributor to projects involving novel AI architectures.She has published numerous research papers on emerging AI trends, including meta-learning, transfer learning, and zero-shot learning. Maya’s research focuses on solving complex, real-world problems through innovative model development, such as adversarial robustness and explainable AI.Maya is proficient in fine-tuning large language models (e.g., BERT, GPT, T5) and applying them to tasks like sentiment analysis, knowledge extraction, and conversational agents. Her computer vision work includes convolutional neural networks (CNNs) and transformer-based architectures for image classification, object detection, and image captioning.Her expertise in AI safety and ethics ensures that the systems she designs align with responsible AI practices. She has experience implementing AI fairness frameworks and bias mitigation techniques in model training pipelines.Maya collaborates with engineering teams to deploy models efficiently using TensorFlow, PyTorch, and Hugging Face Transformers. She also integrates LangChain and LangGraph for building dynamic LLM-based applications, including knowledge retrieval systems and conversational agents.Her proficiency in staying ahead of emerging trends has enabled her to contribute to research-backed AI innovation, making her a key player in bridging academic research with practical AI applications.');


-- -- Insert into Resource_Projects
-- INSERT INTO Resource_Projects (Resource_ID, Project_ID)
-- VALUES 
--     (1, 1), -- John Smith worked on the chatbot project
--     (3, 1), -- Ayesha Khan worked on the chatbot project
--     (2, 2), -- Emma Johnson worked on the skill-matching system
--     (4, 2), -- Carlos Martinez worked on the skill-matching system
--     (1, 3), -- John Smith worked on the forecasting project
--     (2, 3), -- Emma Johnson worked on the forecasting project
--     (6, 1), -- Liam Davis worked on UI design for the chatbot project
--     (5, 2), -- Sofia Patel managed the skill-matching project
--     (7, 3), -- Ahmed Ali handled DevOps for the forecasting project
--     (8, 3); -- Maya Chen contributed research for the forecasting project



-- Insert into Project_Deliverables
-- INSERT INTO Project_Deliverables (Project_ID, Deliverable_Description)
-- VALUES 
--     (1, 'Reduce customer wait times by 40% through LLM-powered automation'),
--     (2, 'Boost task allocation efficiency and employee productivity through AI matching'),
--     (3, 'Optimize inventory management and improve overall sales forecasting accuracy');

-- SET FOREIGN_KEY_CHECKS = 0;
-- TRUNCATE TABLE Project_Deliverables;
-- TRUNCATE TABLE Project_Types;
-- TRUNCATE TABLE Projects;
-- TRUNCATE TABLE Resource_Projects;
-- TRUNCATE TABLE Resources;
-- SET FOREIGN_KEY_CHECKS = 1;




-- Insert into Project_Types
-- INSERT INTO Project_Types (Project_Type) 
-- VALUES ('AI Chatbot'), ('AI Matcher'), ('Forecasting');

-- -- Insert into Projects
-- INSERT INTO Projects (Project_Name, Project_Type_ID, Year_Implemented, Delivery_Timeline, Status, Description)
-- VALUES 
--     ('AI-Powered Customer Support System', 1, 2022, '2022-06 to 2022-12', 'delivered', 'Implemented a chatbot system integrated with LLM capabilities to automate responses.'),
--     ('Employee Skill-Matching System', 2, 2023, '2023-01 to 2023-09', 'delivered', 'Built an AI-based platform to match employees’ skills to ongoing projects.'),
--     ('Retail Sales Forecasting', 3, 2023, '2023-03 to 2023-12', 'in support', 'Delivered an AI model for demand prediction and optimized inventory management.');

-- -- Insert into Resources
-- INSERT INTO Resources (Name, Role, Qualification, Years_of_Experience, Core_Technical_Expertise)
-- VALUES 
--     ('John Smith', 'AI Engineer', 'Master’s in CS', 5, 'LLMs, ML Models'),
--     ('Emma Johnson', 'Data Scientist', 'Bachelor’s in Data Science', 3, 'Data Preprocessing, Modeling'),
--     ('Ayesha Khan', 'NLP Specialist', 'Ph.D. in NLP', 4, 'NLP, Text Analytics'),
--     ('Carlos Martinez', 'Software Engineer', 'Bachelor’s in Software Engineering', 4, 'API Development, System Integration'),
--     ('Sofia Patel', 'AI Product Manager', 'MBA in Technology Management', 6, 'Project Management, Resource Allocation'),
--     ('Liam Davis', 'UI/UX Designer', 'Bachelor’s in Design', 5, 'UI/UX Design'),
--     ('Ahmed Ali', 'DevOps Engineer', 'Bachelor’s in IT', 4, 'CI/CD, Scalability'),
--     ('Maya Chen', 'AI Researcher', 'Ph.D. in AI', 7, 'AI Research, Emerging AI Trends');

-- -- Insert into Project_Deliverables
-- INSERT INTO Project_Deliverables (Project_ID, Deliverable_Description)
-- VALUES 
--     (1, 'Reduce customer wait times by 40% through LLM-powered automation'),
--     (2, 'Boost task allocation efficiency and employee productivity through AI matching'),
--     (3, 'Optimize inventory management and improve overall sales forecasting accuracy');

-- -- Insert into Resource_Projects
-- INSERT INTO Resource_Projects (Resource_ID, Project_ID)
-- VALUES 
--     (1, 1), -- John Smith worked on the chatbot project
--     (3, 1), -- Ayesha Khan worked on the chatbot project
--     (2, 2), -- Emma Johnson worked on the skill-matching system
--     (4, 2), -- Carlos Martinez worked on the skill-matching system
--     (1, 3), -- John Smith worked on the forecasting project
--     (2, 3), -- Emma Johnson worked on the forecasting project
--     (6, 1), -- Liam Davis worked on UI design for the chatbot project
--     (5, 2), -- Sofia Patel managed the skill-matching project
--     (7, 3), -- Ahmed Ali handled DevOps for the forecasting project
--     (8, 3); -- Maya Chen contributed research for the forecasting project



-- SELECT Project_Name, Status 
-- FROM Projects 
-- WHERE Year_Implemented = 2023;