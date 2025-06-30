import re

languages_frameworks = [
    # Langages
    "Python", "python3", "python 3",
    "Java", "Java SE", "Java EE",
    "JavaScript", "JS",
    "TypeScript", "TS",
    "C", "C99",
    "C++", "C plus plus", "cpp",
    "C#", "C sharp", "csharp",
    "Go", "Golang",
    "Ruby",
    "PHP",
    "Swift",
    "Kotlin",
    "Rust",
    "Scala",
    "Perl",
    "Objective-C", "Objective C",
    "R",
    "MATLAB",
    "SQL", "T-SQL", "PL/SQL", "MySQL", "PostgreSQL", "SQLite", "SQL Server",

    # Frameworks & bibliothèques
    "React", "React.js", "ReactJS",
    "Angular", "AngularJS",
    "Vue", "Vue.js", "VueJS",
    "Next.js", "NextJS",
    "Nuxt.js", "NuxtJS",
    "Node.js", "NodeJS",
    "Express", "Express.js",
    "Django",
    "Flask",
    "Spring", "Spring Boot",
    "Ruby on Rails", "Rails",
    "Laravel",
    "Symfony",
    "Bootstrap",
    "jQuery",
    "ASP.NET", "ASP.NET Core", "ASP",
    "TensorFlow", "Tensorflow",
    "PyTorch", "Pytorch",
    "Scikit-learn", "scikit learn",
    "pandas",
    "NumPy", "numpy",
    "OpenCV",
    "Keras",
    "XGBoost", "xgboost",
    "LightGBM", "lightgbm",
    "Transformers",
    "FastAPI",
    "BeautifulSoup", "Beautiful Soup",
    "Selenium",
    "Hadoop",
    "Spark", "PySpark",
    "Airflow",
    "Docker",
    "Kubernetes", "k8s",
    "Terraform",
    "Ansible",
    "Jenkins",
    "Git", "GitHub", "GitLab",
    "CI/CD",
]



def normalize_text(text, languages_frameworks):
    """Normalise le texte tout en préservant certains langages et frameworks.

    Args:
        text (str): Le texte à normaliser.
        languages_frameworks (list): Liste de langages et frameworks à préserver.

    Returns:
        str: Le texte normalisé avec les langages et frameworks préservés.
    """
    preserved_words = {}

    for word in languages_frameworks:
        # Regex pour correspondance exacte du mot
        pattern = r'\b' + re.escape(word) + r'\b'
        placeholder = f"__preserve_{len(preserved_words)}__"
        text = re.sub(pattern, placeholder, text, flags=re.IGNORECASE)
        preserved_words[placeholder] = word  # on garde la version originale

    # Nettoyage standard sans toucher aux placeholders
    text = re.sub(r'[^a-zA-Z0-9\s_.]+', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()

    # Restauration des mots préservés (en minuscule si tu veux)
    for placeholder, original_word in preserved_words.items():
        text = text.replace(placeholder, original_word.lower())  # .lower() optionnel

    return text

