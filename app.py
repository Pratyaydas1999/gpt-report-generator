import streamlit as st
import pandas as pd
import openai

st.title("📊 Marketing Metrics Summary Generator")

# Set up OpenAI API key (using your working API key)
api_key = st.secrets["OPENAI_API_KEY"]

# Create OpenAI client (NEW API syntax - same as your Colab code)
client = openai.OpenAI(api_key=api_key)

# File upload section
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
    
    # Convert data to text format for AI (same as your Colab code)
    metrics_text = "\n".join([f"{row['Metric']}: {row['Value']}" for index, row in df.iterrows()])
    
    # Create the prompt for AI (same as your Colab code)
    prompt = f"""
You are a marketing analyst. Given the following performance metrics, write a short client report summary.
Mention what went well, what needs improvement, and suggest next steps.

Metrics:
{metrics_text}
"""
    
    # Generate report using OpenAI (NEW API syntax - same as your Colab code)
    with st.spinner("Generating Report with GPT-4..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using same model as your Colab code
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        report = response.choices[0].message.content
    
    # Display the report
    st.success("Here's your summary:")
    st.write(report)
    
    # Optional: Download as PDF
    try:
        from fpdf import FPDF
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        
        for line in report.split("\n"):
            if line.strip():  # Only add non-empty lines
                try:
                    pdf.multi_cell(0, 10, line)
                except:
                    # Handle special characters
                    pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))
        
        pdf.output("report.pdf")
        
        with open("report.pdf", "rb") as f:
            st.download_button("Download Report as PDF", f, file_name="Marketing_Report.pdf")
    except ImportError:
        st.info("PDF download feature requires fpdf library. Report displayed above.")
    except Exception as e:
        st.warning(f"PDF generation failed: {e}. Report is displayed above.")