# Unella: Automatic Audit for Python Projects  
Unella is a project to automate audits exclusively on Python projects.  

## 🚧 Project Status  
Please note that Unella is currently in active development.   
While it is functional, expect regular updates and enhancements.  

## 📄 Output Formats  
With Unella, you can generate audit results in two formats:

JSON: Structured data that can be easily consumed by other applications.  
HTML Report: A comprehensive, visual report detailing the audit findings.  

## 🛠️ Tools Integrated  
Unella is powered by a suite of reputable Python tools to offer a diverse range of insights:

ruff: https://github.com/astral-sh/ruff  
mypy: https://github.com/python/mypy  
vulture: https://github.com/jendrikseipp/vulture  

...and several other tools to fetch a plethora of information.  

## 💼 Installation & Usage  

```bash
git clone https://github.com/sorasful/unella.git

cd unella
pip install -r requirements.txt
```

Use the Unella Command-Line Interface (CLI) to start your audit:

```bash
# json output to stdout 
unella --path /path_to_python_project/ --output-format json

# generate a HTML report 
unella --path /path_to_python_project/ --output-format html
```

Replace path_to_python_project with the path to your Python project.
For an HTML report, replace json with html.

