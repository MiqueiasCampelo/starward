# Verbose Mode: Show Your Work

One of astr0's most distinctive features is its **verbose mode**—the ability to see every step of every calculation. This makes astr0 not just a calculator, but a **learning tool**.

---

## Why "Show Your Work"?

In school, teachers say "show your work" because the process matters as much as the answer. The same is true in science:

- **Learning**: See how formulas are applied
- **Verification**: Check that calculations are correct
- **Debugging**: Find where your own code differs
- **Teaching**: Generate worked examples instantly
- **Documentation**: Create explanatory materials

---

## Using Verbose Mode

### From the CLI

Add `--verbose` (or `-v`) **before** the command:

```bash
astr0 --verbose time now
astr0 -v angles sep "10h +30d" "11h +31d"
astr0 --verbose coords transform "12h +45d" --to galactic
```

⚠️ **Important**: The `--verbose` flag must come before the subcommand, not after!

```bash
# ✓ Correct
astr0 --verbose angles sep "10h +30d" "11h +31d"

# ✗ Wrong (won't work)
astr0 angles sep "10h +30d" "11h +31d" --verbose
```

### Output Format

Verbose output appears after the main result, formatted with box-drawing characters for clarity:

```
┌─ Section Title
│  Step 1: description
│  Calculation...
│  Result = value
└────────────────────────────────────────
```

---

## Example: Angular Separation

```bash
astr0 --verbose angles sep "10h +30d" "11h +31d"
```

```
Point 1: 10ʰ 00ᵐ 00.00ˢ 30° 00′ 00.00″
Point 2: 11ʰ 00ᵐ 00.00ˢ 31° 00′ 00.00″
─────────────────────────────────────────────

Angular Separation:
  12° 57′ 11.54″
  = 12.9532059786°

┌─ Input coordinates
│  Point 1: RA = 10ʰ 00ᵐ 00.00ˢ, Dec = 30° 00′ 00.00″
│  Point 2: RA = 11ʰ 00ᵐ 00.00ˢ, Dec = 31° 00′ 00.00″
└────────────────────────────────────────
┌─ RA difference
│  Δλ = 15.000000°
└────────────────────────────────────────
┌─ Trigonometric values
│  sin(φ₁) = 0.5000000000, cos(φ₁) = 0.8660254038
│  sin(φ₂) = 0.5150380749, cos(φ₂) = 0.8571673007
│  sin(Δλ) = 0.2588190451, cos(Δλ) = 0.9659258263
└────────────────────────────────────────
┌─ Vincenty formula
│  numerator = √[(cos φ₂ sin Δλ)² + (cos φ₁ sin φ₂ − sin φ₁ cos φ₂ cos Δλ)²]
│            = √[0.2218512223² + 0.0320560402²]
│            = 0.2241552019
│  
│  denominator = sin φ₁ sin φ₂ + cos φ₁ cos φ₂ cos Δλ
│              = 0.9745534595
└────────────────────────────────────────
┌─ Result
│  σ = atan2(0.2241552019, 0.9745534595)
│    = 12.9532059786°
│    = 12° 57′ 11.54″
└────────────────────────────────────────
```

You can trace through every step of the Vincenty formula!

---

## Example: GMST Calculation

```bash
astr0 --verbose time now
```

```
┌─ Calculate GMST
│  T = (JD - 2451545.0) / 36525 = 0.26005504109...
│  
│  GMST (degrees) = 280.46061837 
│                 + 360.98564736629 × D
│                 + 0.000387933 × T²
│                 − T³/38710000
│  where D = JD - 2451545.0 = 9498.5104...
│  
│  GMST = 280.46061837 + 3429876.234... + 0.0262... - 0.0000...
│       = ... (normalized to 0-360)
│       = 106.458...° = 7.097h
└────────────────────────────────────────
```

---

## Example: Coordinate Transformation

```bash
astr0 --verbose coords transform "12h30m +45d" --to galactic
```

Shows the full spherical trigonometry transformation including:
- Reference frame constants (NGP position)
- Intermediate angle calculations
- Final coordinate values

---

## Verbose Mode with JSON Output

You can combine verbose mode with JSON output:

```bash
astr0 --verbose --output json angles sep "10h +30d" "11h +31d"
```

The JSON will include a `"steps"` array with the calculation steps:

```json
{
  "separation_degrees": 12.9532059786,
  "separation_dms": "12° 57′ 11.54″",
  "steps": [
    {
      "title": "Input coordinates",
      "content": "Point 1: RA = 10h, Dec = 30°\nPoint 2: RA = 11h, Dec = 31°"
    },
    {
      "title": "RA difference",
      "content": "Δλ = 15.000000°"
    },
    ...
  ]
}
```

This is useful for:
- Programmatic processing of explanations
- Building educational tools on top of astr0
- Automated documentation generation

---

## The VerboseContext System

### How It Works

Under the hood, astr0 uses a `VerboseContext` object to collect calculation steps:

1. When `--verbose` is passed, a `VerboseContext` is created
2. It's passed to calculation functions
3. Functions call `step(ctx, title, content)` to record their work
4. After calculation, the steps are formatted and displayed

### Design Philosophy

The verbose system follows these principles:

**Opt-in**: Functions only record steps if a context is provided. This means:
- No performance penalty when verbose mode is off
- Functions remain usable as a library without CLI overhead

**Hierarchical**: Steps can be nested using context managers for complex multi-stage calculations.

**Output-agnostic**: Steps are collected as data, then formatted. This allows different output formats (plain text, JSON, eventually LaTeX).

---

## Python API

```python
from astr0.core.angles import angular_separation, Angle
from astr0.verbose import VerboseContext

# Create a verbose context
ctx = VerboseContext()

# Pass it to calculations
ra1, dec1 = Angle(hours=10), Angle(degrees=30)
ra2, dec2 = Angle(hours=11), Angle(degrees=31)

sep = angular_separation(ra1, dec1, ra2, dec2, verbose=ctx)

# Print the steps
ctx.print_steps()

# Or get as string
output = ctx.format_steps()

# Or get as data (for JSON, etc.)
steps_data = ctx.to_dict()
```

### Adding Steps in Your Own Code

If you're extending astr0 or writing your own calculations:

```python
from astr0.verbose import VerboseContext, step

def my_calculation(x, y, verbose=None):
    """A calculation that shows its work."""
    
    step(verbose, "Input values", f"x = {x}, y = {y}")
    
    intermediate = x * y
    step(verbose, "Multiply", f"x × y = {x} × {y} = {intermediate}")
    
    result = intermediate ** 2
    step(verbose, "Square", f"({intermediate})² = {result}")
    
    return result
```

The `step()` function is a no-op if `verbose` is None, so there's no need to check.

### Nested Sections

For complex calculations with multiple stages:

```python
ctx = VerboseContext()

with ctx.section("Stage 1"):
    step(ctx, "Step 1.1", "...")
    step(ctx, "Step 1.2", "...")

with ctx.section("Stage 2"):
    step(ctx, "Step 2.1", "...")
```

---

## Educational Uses

### Generating Homework Solutions

Need a worked example of angular separation?

```bash
astr0 --verbose angles sep "Vega" "Deneb"  # (once catalog lookups are added!)
```

### Comparing Implementations

Writing your own coordinate transformation? Use astr0's verbose output to check each step against your implementation.

### Textbook Illustrations

The verbose output follows the same structure as textbook derivations, making it easy to create educational materials.

---

## Tips for Using Verbose Mode

1. **Start without verbose** to get the answer
2. **Add verbose** when you want to understand the calculation
3. **Pipe to a file** for long outputs: `astr0 --verbose ... > output.txt`
4. **Use JSON** for programmatic processing
5. **Compare with textbooks** to verify understanding

---

## Future Plans

The verbose system will be extended with:

- **LaTeX output**: Generate publication-ready equations
- **Step-by-step mode**: Interactive walkthrough of calculations
- **Diagram generation**: Visualize coordinate systems and transformations
- **Configurable detail levels**: Control verbosity depth

---

*Next: [CLI Reference](cli-reference.md) — Complete command-line reference*
