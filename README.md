# Logic Functions Analyzer

Input a logic function and get its truth table, DNF (Disjunctive Normal Form), and simplified form.

## Usage

```python main.py "<logic_function>"```

Examples:

```python main.py "A + B"```

```python main.py "/A + B"```

```python main.py "A + /B.C + C"```

```python main.py "A + B.(C @ A)"```

## Output 

Example output for `A + /B.C + C`:

```
['A', 'B', 'C']
[0, 0, 0, 0]
[0, 0, 1, 1]
[0, 1, 0, 0]
[0, 1, 1, 1]
[1, 0, 0, 1]
[1, 0, 1, 1]
[1, 1, 0, 1]
[1, 1, 1, 1]

Disjunctive Normal Form (DNF) : 
 /A./B.C + /A.B.C + A./B./C + A./B.C + A.B./C + A.B.C

Simplified form : 
 C + A
```