---
layout: default
permalink: /
---

# Welcome to the TheByteDungeon

{{ site.description }}

## :pencil2: [Posts](Posts)
  
## :hammer: [Projects](projects)

---

### Latest entries

{% assign sorted_posts = site.posts | sort: 'date' | reverse %}
{% for post in sorted_posts %}
<li><a href="{{ post.url }}">{{ post.title }}</a> |  {{ post.date | date: "%Y-%m-%d" }}</li>
{% endfor %}
