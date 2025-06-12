import pandas as pd
import os
import json
import google.generativeai as genai



def perform_basic_analysis(df):
    results = {}
    if 'Product' in df.columns and 'Sales' in df.columns:
        sales_by_product = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(10)
        results['bar_chart_data'] = {
            "labels": sales_by_product.index.tolist(),
            "data": sales_by_product.values.tolist(),
            "title": "Top 10 Products by Sales"
        }
    
    if 'Category' in df.columns and 'Sales' in df.columns:
        sales_by_category = df.groupby('Category')['Sales'].sum()
        results['pie_chart_data'] = {
            "labels": sales_by_category.index.tolist(),
            "data": sales_by_category.values.tolist(),
            "title": "Sales Distribution by Category"
        }
    
    if not results:
        return {"error": "Could not generate charts. Ensure your data has columns like 'Product', 'Sales', or 'Category'."}
        
    return results

# NEW FUNCTION - USE THIS


def get_ai_insights(df_head_str):
    # Configure the API key from the .env file
    try:
        genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    except Exception as e:
        print(f"Error configuring Google AI: {e}")
        return "Could not configure the Google AI Service. Please check the API key."

    # The prompt remains the same!
    prompt = f"""
    You are a friendly and insightful business data analyst for small businesses.
    A user has uploaded their sales data. Here are the first 5 rows:
    ---
    {df_head_str}
    ---
    Based ONLY on this sample data, provide:
    1.  **Key Observation:** A simple, one-sentence observation about the data.
    2.  **Potential Trend:** A potential trend you are noticing.
    3.  **Actionable Advice:** One clear, simple recommendation the business owner can take.

    Format your response in simple, easy-to-read bullet points. Be concise.
    """
    
    # Initialize the model
    # NEW, CORRECTED LINE
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    try:
        # Generate the content
        response = model.generate_content(prompt)
        
        # Check for safety ratings and get the text
        if response.parts:
            return response.text
        else:
            # This handles cases where the response might be blocked for safety reasons
            return "The AI could not generate a response for this data. It may have been blocked for safety reasons."
            
    except Exception as e:
        print(f"Google Gemini API Error: {e}")
        return f"An error occurred while contacting the Google AI service: {e}"
