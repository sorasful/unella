## Mypy Report

### Files with the most messages

| File path | Number of messages |
|-----------|--------------------|
{% for file_path, count in data.files_most_messages -%}
| {{ file_path }} | {{ count }} |
{% endfor -%}

### Most frequent message

| Message | Number of messages |
|---------|--------------------|
{% for msg, count in data.most_messages -%}
| {{ msg }} | {{ count }} |
{% endfor -%}

### Categories with most messages

| Category | Number of messages |
|----------|--------------------|
{% for category, count in data.most_messages_categories -%}
| {{ category }} | {{ count }} |
{% endfor -%}
