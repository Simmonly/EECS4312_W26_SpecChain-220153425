# Application: [Calm] 
- Most important difference between pipelines: The manual pipeline produced
  personas and requirements directly grounded in specific review evidence,
  whereas the automated pipeline generated broader and sometimes inaccurate
  artifacts. The best example was the automated pipeline describing
  Medito as offering limited free tier when the app is entirely free
  without paywalls. This is an error that could have produced misleading
  requirements if left without corrections. The hybrid pipeline corrected those errors
  by using human judgment to these outputs, resulting in 12
  accurate requirements compared to 10 in the automated
  pipeline with an ambiguity ratio of 0.3.

- Most useful pipeline: The hybrid pipeline is surely the most useful. It combined
  the speed of LLM generation my human correction of factual errors and vague language.
  It matched the manual pipeline expectaiton in all of requirements count (12),
  tests count (24), traceability ratio (1.0), testability rate (1.0), and ambiguity ratio (0.0)
  while at the same time requiring significantly less time than building everything from scratch manually.
  
- Most surprising finding: The automated pipeline invented some requirements for
  features that were never mentioned in any user review. For example a session
  rating system and a personalized recommendations. Despite being prompted to
  derive the requirements from the provided personas, the LLM drew on its general
  knowledge of what meditation apps typically are rather than staying
  grounded in the Medito-specific review data. This is typical of LLMs
  they aren't always accurate. In my estimation this was more problematic than
  the ambiguous language issues because it introduced entirely unsupported
  functionality into the specification.
- Observed weakness in the automated pipeline: The LLM consistently used
  unmeasurable language in acceptance criteria despite being repeatedly
  instructed to avoid it. Terms such as user-friendly, easy-to-use, and
  seamless were in 3 out of the 10 automated requirements therefore,
  producing an ambiguity ratio of 0.3. These vague terms make it
  impossible to objectively verify whether a requirement was satisfied during
  testing, which undermines the core purpose of writing formal acceptance criteria.
