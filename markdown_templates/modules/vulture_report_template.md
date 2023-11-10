## Vulture Report

| File path | Line | Message | Confidence |
|-----------|------|---------|------------|
{% for item in data -%}
| {{ item.file_path }} | {{ item.line }} | {{ item.msg }} | {{ item.confidence }} |
{% endfor -%}
