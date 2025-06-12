### Elasticsearch: A Full Search Engine Built on Lucene

`Elasticsearch` is:

- A complete `search engine` application.

- written in `Java`.

- It uses `Lucene` under the hood for the actual searching and indexing.

- But it hides all the complexity and gives you a simple way to use it — through a RESTful API (you send HTTP requests like you would to a website).

### Lucene: A Search Engine Library
 
- `Lucene` is a `Java library`, not a full program. That means:

- It gives you the tools to build a search engine.

- But you have to write your own code (in Java) to use it.

- It’s very powerful, but also complex — you need to know a lot about how search engines work.

> `Lucene` = Java library for building search engines (powerful but complex).

> `Elasticsearch` = Full search engine application that uses Lucene, but is much easier to use.

---


### Elasticsearch can be described as:

- A distributed real-time document store where every field is indexed and searchable
- A distributed search engine with real-time analytics
- Capable of scaling to hundreds of servers and petabytes of structured and unstructured data

> `distributed` simply means: The work or data is split across multiple machines that work together as one system.




##### 1. A distributed real-time document store where every field is indexed and searchable

✅ Simple Breakdown:

`Document store:`

Elasticsearch stores data as JSON documents, not rows like a traditional database.

→ Think: a product, blog post, or log entry is a document.

`Real-time:`
As soon as you store a document, it’s quickly searchable — usually within a second.
→ You don’t have to wait for indexing jobs like in some older systems.

Every field is indexed and searchable:
If your document has:

``` json
{
  "name": "MacBook",
  "price": 1200,
  "in_stock": true
}
```
Then you can search by name, filter by price, or check availability — without doing anything special. Elasticsearch automatically prepares fields for fast searching.

`Distributed`:
This storing and searching is done across many machines that works together.


##### 2. A distributed search engine with real-time analytics

`Search engine:`

It’s like Google, but for your own data — you can do powerful full-text search, filtering, fuzzy matches, and more.

`Real-time analytics:`

- You can analyze your data as it streams in — for example:

- Count logins per hour

- Average order value today

- Top search terms this week

`Distributed:`
These searches and analytics are performed by multiple machines working together, giving you fast results even with huge datasets.

##### 3. Capable of scaling to hundreds of servers and petabytes of structured and unstructured data"

Scaling to hundreds of servers:

You can start small (maybe 1 or 3 machines) and grow to hundreds of machines, and Elasticsearch will still work as a single system.

Petabytes of data:

- It can handle enormous volumes — logs, documents, metrics — in the scale of millions or billions of records.

Structured and unstructured data:

- Structured: Data with a clear schema (e.g., numbers, dates, categories).

- Unstructured: Text-heavy data like emails, support tickets, chat logs.

Elasticsearch can search and analyze both kinds of data effectively.

---
</br>

> Elasticsearch packages up all this functionality into a standalone server that your application can talk to via a simple RESTful API, using a web client from your favorite programming language, or even from the command line.


Exampel of a simple diagram that show a python program that uses elasticsearch

> Python Script  <───>  Port 9200  <───>  Elasticsearch Server

What happens step by step:

- Your Python script sends an HTTP request (like: index a document, search for a keyword).

- The request goes to localhost:9200 — the port where Elasticsearch is listening.

- The Elasticsearch server processes the request and prepares a response.

- The response goes back through port 9200 to your Python script.