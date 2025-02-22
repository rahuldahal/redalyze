from google import genai

class GenaiService:
  def __init__(self, api_key: str):
    self.client = genai.Client(api_key=api_key)
    self.cache = {}

  def generate_content(self, model: str, contents: list):
    response = self.client.models.generate_content(
      model=model,
      contents=contents
    )
    return response.text

  def interpret_data(self, numerical_data: list, visualization_type: str):
    cache_key = f"{visualization_type}"
    
    if cache_key in self.cache:
      return self.cache[cache_key]
    
    content = [f"Analyze the following numerical data: {numerical_data}. The user is visualizing this data as a {visualization_type}. Focus on summarizing the main trends and actionable insights that a user would see. For example, highlight key peaks and dips, the best times for engagement, and the differences between data points. Provide concise recommendations for when to post based on the trends. Avoid unnecessary explanations and keep it suitable for displaying directly within a web visualization (e.g., Dash), where clarity and actionable insights are the priority."]
    
    interpretation = self.generate_content(
      model="gemini-2.0-flash",
      contents=content
    )
    
    self.cache[cache_key] = interpretation

    return interpretation
