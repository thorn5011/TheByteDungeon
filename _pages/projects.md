---
layout: default
title: Projects
permalink: /projects

---
# Projects

## :honey_pot: Cowrie Honeypot


{% assign sorted_posts = site.posts | sort: 'date' %}
{% for post in sorted_posts %}
    {% if post.tags contains 'cowrie' %}
<li><a href="{{ post.url }}">{{ post.title }}</a>,  {{ post.date | date: "%B %Y" }}</li>
    {% endif %}
{% endfor %}

---

## :flags: CTFs

{% assign sorted_posts = site.posts | sort: 'date' %}
{% for post in sorted_posts %}
    {% if post.tags contains 'ctf' %}
<li><a href="{{ post.url }}">{{ post.title }}</a>,  {{ post.date | date: "%B %Y" }}</li>
    {% endif %}
{% endfor %}
