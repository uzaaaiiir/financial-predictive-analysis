# Predictive Analysis
This project is an tool aimed at automating the process of collecting, extracting, and analyzing financial data for SMBs to perform a predictive analysis (PA). 

## Features
- **Industry Classification**: Uses Natural Language Processing (NLP) to determine the industry based on company website content.
- **Competitor Discovery**: Automatically identifies competitors in the target industry and fetches their financial data.
- **Predictive Analysis**: Leverages historical financial data to project future revenue and growth.
- **Report Generation**: Compiles predictive analysis results into downloadable reports for internal use. 

---
## Getting Started
### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/uzaaaiiir/financial-predictive-analysis.git
    ```

2. Navigate to the project directory
    ```bash
    cd financial-predictive-analysis
    ```

3. Create a virtual environment in this top-level directory:
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
  - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```
  - On Windows:
    ```bash
    venv\Scripts\activate
    ```

5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Set up your environment variables: Create a `.env` file in the top-level project folder and add your environment variables, including your OpenAI API key API Key. Your `.env` file should look like this:
    ```makefile
    OPENAI_API_KEY=your_openai_api_key
    ```

### Usage
1. Run the FastAPI Server:
    ```bash
    cd app
    fastapi dev main.py
    ```
2. Go to `localhost:8000/docs` to view the API docs and access the APIs. Currently, we have the following APIs (these will change in the near future):
  - `/upload`: Upload financial documents for data extraction.
  - `/comp_revenue`: Get financial revenue data for competitors. 

### Contribution Guidelines 
- Clone the repository.
- Create a feature branch (`git checkout -b feature-name`).
- Commit your changes (`git commit -m 'Useful message').
- Push to the branch (`git push origin feature-name`).
- Open a pull request.
