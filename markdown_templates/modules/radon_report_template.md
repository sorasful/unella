## Radon Complexity Report

### Average Complexity
Average Complexity of the Project: {{ data.average_complexity }}

### Code Constructs Complexity
{% for file_path, complexities in data.complexity.items() %}
#### File: {{ file_path }}

| Name | Type | Complexity | Rank | Line Number | End Line | Column Offset |
|------|------|------------|------|-------------|----------|---------------|
{% for item in complexities -%}
| {{ item.name }} | {{ item.type }} | {{ item.complexity }} | {{ item.rank }} | {{ item.lineno }} | {{ item.endline }} | {{ item.col_offset }} |
{% endfor -%}
{% endfor %}
