import streamlit as st
import google.generativeai as genai
import pdfplumber

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Research Paper Analyzer",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Research Paper Analyzer")
st.write("Upload a research paper and analyze it using Gemini AI.")

# ----------------------------
# API Key Input
# ----------------------------
st.subheader("🔑 Gemini Configuration")

api_key = st.text_input(
    "Enter Gemini API Key",
    type="password",
    placeholder="Paste your Gemini API Key here"
)

# ----------------------------
# PDF Upload
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload Research Paper (PDF)",
    type=["pdf"]
)

# ----------------------------
# Research Topic
# ----------------------------
research_topic = st.text_input(
    "Enter Your Research Topic",
    placeholder="Example: Machine Learning in Healthcare"
)

# ----------------------------
# Summary Length
# ----------------------------
summary_length = st.slider(
    "Summary Length (Words)",
    min_value=50,
    max_value=1000,
    value=200,
    step=50
)

# ----------------------------
# PDF Text Extraction
# ----------------------------
def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# ----------------------------
# Gemini Function
# ----------------------------
def ask_gemini(model, prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


# ----------------------------
# Analyze Button
# ----------------------------
if st.button("🚀 Analyze Paper"):

    # Validation
    if not api_key:
        st.error("Please enter your Gemini API Key.")
        st.stop()

    if uploaded_file is None:
        st.error("Please upload a PDF.")
        st.stop()

    if not research_topic:
        st.error("Please enter a research topic.")
        st.stop()

    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Read PDF
    with st.spinner("Reading PDF..."):
        paper_text = extract_text_from_pdf(uploaded_file)

    if not paper_text.strip():
        st.error("Could not extract text from PDF.")
        st.stop()

    st.success("PDF Loaded Successfully!")

    # Limit text size
    paper_content = paper_text[:20000]

    # ----------------------------
    # Relevance Analysis
    # ----------------------------
    with st.spinner("Checking relevance..."):

        relevance_prompt = f"""
        Research Topic:
        {research_topic}

        Research Paper:
        {paper_content}

        Determine whether the paper is relevant to the topic.

        Return:

        Relevance Score: XX%

        Explanation:
        Short explanation.
        """

        relevance_result = ask_gemini(model, relevance_prompt)

    st.subheader("🎯 Relevance Analysis")
    st.write(relevance_result)

    # ----------------------------
    # Summary
    # ----------------------------
    with st.spinner("Generating summary..."):

        summary_prompt = f"""
        Summarize the following research paper in
        approximately {summary_length} words.

        Research Paper:
        {paper_content}
        """

        summary_result = ask_gemini(model, summary_prompt)

    st.subheader("📝 Summary")
    st.write(summary_result)

    # ----------------------------
    # Keywords
    # ----------------------------
    with st.spinner("Extracting keywords..."):

        keywords_prompt = f"""
        Extract the top 15 keywords from this
        research paper.

        Return only bullet points.

        Research Paper:
        {paper_content}
        """

        keywords_result = ask_gemini(model, keywords_prompt)

    st.subheader("🔑 Keywords")
    st.write(keywords_result)

    # ----------------------------
    # Mind Map
    # ----------------------------
    with st.spinner("Generating mind map..."):

        mindmap_prompt = f"""
        Analyze the research paper and create
        a Mermaid mind map.

        Format:

        mindmap
          root((Research Paper))
            Main Topic
              Sub Topic

        Return ONLY Mermaid code.
        
        Research Paper:
        {paper_content}
        """

        mindmap_result = ask_gemini(model, mindmap_prompt)

    st.subheader("🧠 Mind Map (Mermaid Code)")
    st.code(mindmap_result, language="text")

    st.info(
        "You can paste this Mermaid code into Mermaid Live Editor "
        "or use a Streamlit Mermaid component to render it visually."
    )
