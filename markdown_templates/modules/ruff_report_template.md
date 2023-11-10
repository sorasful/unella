## Ruff Report

| Code | Message | Fixable | Count |
|------|---------|---------|-------|
{% for item in data -%}
| {{ item.code }} | {{ item.message }} | {{ item.fixable }} | {{ item.count }} |
{% endfor -%}
