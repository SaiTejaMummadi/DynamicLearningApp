from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random
import json
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Predefined list of temporary keywords
TEMP_KEYWORDS = [
    "Culture",
    "Health",
    "Fashion",
    "Technology",
    "Sustainability",
    "Genetics",
    "Nutrition",
    "Urbanization",
    "Robotics",
    "Psychology",
    "Ecology",
    "Education",
    "Innovation",
    "Sociology",
    "Anthropology",
    "Biochemistry",
    "Mindfulness",
    "ArtificialIntelligence",
    "RenewableEnergy",
    "Archaeology",
    "Fitness",
    "DataScience",
    "HumanBehavior",
    "ClimateChange",
    "Biotechnology",
    "Meditation",
    "VirtualReality",
    "SocialMedia",
    "Astronomy",
    "MentalHealth",
    "Engineering",
    "Design",
    "Neuroscience",
    "InternetOfThings",
    "Photography",
    "MachineLearning",
    "EnvironmentalScience",
    "Travel",
    "QuantumPhysics",
    "Wellness",
    "MobileTechnology",
    "CulturalDiversity",
    "BigData",
    "PersonalDevelopment",
    "Astrophysics",
    "SustainableLiving",
    "Bioinformatics",
    "SoftwareDevelopment",
    "CulturalHeritage",
    "Nanotechnology",
    "Mindset",
    "GraphicDesign",
    "CognitiveScience",
    "E-commerce",
    "Evolution",
    "HealthCare",
    "Blockchain",
    "Ethnography",
    "DataAnalytics",
    "HumanRights",
    "3DPrinting",
    "Yoga",
    "Paleontology",
    "CyberSecurity",
    "BehavioralScience",
    "WearableTech",
    "Linguistics",
    "Fintech",
    "Migration",
    "RenewableResources",
    "UserExperience",
    "MarineBiology",
    "DigitalMarketing",
    "Demography",
    "ArtificialLife",
    "LifestyleDesign",
    "ComputationalBiology",
    "Globalization",
    "SmartCities",
    "Archeogenetics",
    "FitnessTraining",
    "InformationTechnology",
    "CulturalStudies",
    "SpaceExploration",
    "OrganicNutrition",
    "VirtualCommunities",
    "StructuralEngineering",
    "PublicHealth",
    "GeneticEngineering",
    "SustainableArchitecture",
    "BehavioralEconomics",
    "HumanEvolution",
    "DataVisualization",
    "QuantumComputing",
    "BiotechnologyApplications",
    "RenewableMaterials",
    "SustainableTransportation",
    "GeneticResearch",
    "ClimateAction",
    "HealthInnovation"
]

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            keywords TEXT
        )
    ''')
    
    # Create generated_content table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            FOREIGN KEY (entry_id) REFERENCES entries(id)
        )
    ''')

    # Create addresses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address_line TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zipcode TEXT NOT NULL,
            country TEXT NOT NULL,
            current_address BOOLEAN NOT NULL DEFAULT 1
        )
    ''')

    # Removed the 'additional_info' table

    conn.commit()
    conn.close()

# Example of a simple caching mechanism
cache = {}

def generate_tile(text, keywords):
    current_model = "OpenAI"  # Set default model to OpenAI, can be updated in the future

    # Define the prompt template with escaped curly braces
    template = """
    You are a helpful assistant specialized in content creation.
    Based on the provided information, generate a captivating title and a well-structured body for the given context.
    The response should be clear, engaging, and relevant to the input provided.

    Text: {text}
    Keywords: {keywords}

    Provide the response in JSON format with the following structure:
    {{
        "title": "Generated Title Here",
        "body": "Generated Body Content Here"
    }}
    """

    prompt = ChatPromptTemplate.from_template(template)

    # Select the model based on current_model
    if current_model == "OpenAI":
        llm = ChatOpenAI()
    elif current_model == "Anthropic":
        llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    elif current_model == "LLaMA - with Groq":
        llm = ChatGroq(model="llama3-8b-8192")
    elif current_model == "Mistral":
        llm = ChatMistralAI(model="mistral-medium")
    else:
        # Default to OpenAI if no match
        llm = ChatOpenAI()

    # Create the chain
    chain = prompt | llm | StrOutputParser()

    # Invoke the chain to get the response
    response = chain.invoke({
        "text": text,
        "keywords": keywords
    })

    # Parse the JSON string into a Python dictionary
    try:
        response = json.loads(response)
    except json.JSONDecodeError:
        # Handle parsing error
        response = {}
        print("Error: Failed to parse JSON response.")

    # Return both title and body
    title = response.get('title')
    body = response.get('body')
    return title, body

# Route for the home page with the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        keywords = request.form['keywords']
        
        # Save the text and keywords to the entries table
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO entries (text, keywords) VALUES (?, ?)', (text, keywords))
        conn.commit()
        entry_id = cursor.lastrowid
        
        # Generate title and body
        title, body = generate_tile(text, keywords)
        
        # Save generated title and body to generated_content table
        cursor.execute('INSERT INTO generated_content (entry_id, title, body) VALUES (?, ?, ?)', (entry_id, title, body))
        conn.commit()
        conn.close()
        
        return redirect(url_for('display_entry', id=entry_id))
    
    # Generate 6 random temporary keywords
    temp_keywords = random.sample(TEMP_KEYWORDS, 6)
    
    return render_template('index.html', temp_keywords=temp_keywords)

# Route to handle address submission
@app.route('/submit_address', methods=['POST'])
def submit_address():
    address_line = request.form['address_line']
    city = request.form['city']
    state = request.form['state']
    zipcode = request.form['zipcode']
    country = request.form['country']

    # Save the address to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Set all existing addresses to not current
    cursor.execute('UPDATE addresses SET current_address = 0')

    # Insert the new address as the current address
    cursor.execute('''
        INSERT INTO addresses (address_line, city, state, zipcode, country, current_address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (address_line, city, state, zipcode, country, 1))

    conn.commit()
    conn.close()

    # Stay on the same page by redirecting back to the index
    return redirect(url_for('index'))

# Route to display all entries
@app.route('/entries')
def entries():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries')
    entries = cursor.fetchall()
    conn.close()
    return render_template('entries.html', entries=entries)

# Route to display individual entry with title and body
@app.route('/entry/<int:id>')
def display_entry(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Retrieve the entry
    cursor.execute('SELECT text, keywords FROM entries WHERE id = ?', (id,))
    entry = cursor.fetchone()
    
    # Retrieve the generated content
    cursor.execute('SELECT title, body FROM generated_content WHERE entry_id = ?', (id,))
    generated = cursor.fetchone()
    
    conn.close()
    
    if entry and generated:
        text, keywords = entry
        title, body = generated
        # Removed additional_info references
        return render_template('entry.html', title=title, body=body)
    else:
        return "Entry or Generated Content not found", 404

# Removed the route to handle additional info submission

if __name__ == '__main__':
    init_db()
    app.run(debug=True)