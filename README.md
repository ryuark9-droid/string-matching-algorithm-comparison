# Pattern Lab — String Matching Explorer

An interactive learning project for comparing three classic string-search algorithms: Naive Search, Knuth–Morris–Pratt (KMP), and Rabin–Karp. It uses Python's standard library, so Flask and other package installations are not needed.

## Features
- Responsive, dark interface with interactive CSS states and animations
- Search your own text and pattern, or load one of four examples
- Compare selected algorithms side by side
- View match positions (zero-based), character checks, and elapsed time
- Highlight all matches in the text, including overlapping matches
- Python implementations use the same shared sample input for a fair comparison
- Python JSON API with basic input validation

## Run locally

1. Use Python 3.7 or newer.
2. Start the server: `python app.py`
3. Open `http://127.0.0.1:5000`

The browser sends the comparison request to `/api/compare`. `requirements.txt` is intentionally empty of package dependencies.

## Project structure

```text
app.py              Python standard-library web server and JSON API
algorithms.py       Naive, KMP, and Rabin–Karp implementations
templates/index.html
static/style.css    Responsive theme and interactive states
static/app.js       UI behavior and result rendering
requirements.txt
```

## Notes on the numbers
Character checks count direct text-to-pattern character comparisons in each implementation. Runtime is measured on the server with Python's high-resolution timer and will vary by machine and input. The asymptotic complexity shown is the standard worst-case bound for each algorithm (Rabin–Karp can degrade to O(n · m) with many hash collisions).
