import CodeBlock from '@theme/CodeBlock';

const normalOutput = `$ astr0 time jd

2460676.50000`;

const verboseOutput = `$ astr0 time jd --verbose

# Julian Date Calculation
# Algorithm: Meeus, Astronomical Algorithms (2nd ed.)

Input date: 2025-01-12 00:00:00 UTC

Step 1: Adjust for January/February
  Year (Y): 2025
  Month (M): 1 → adjusted to 13
  Adjusted year: 2024

Step 2: Calculate intermediate values
  A = floor(Y / 100) = 20
  B = 2 - A + floor(A / 4) = -13

Step 3: Compute Julian Date
  JD = floor(365.25 × (Y + 4716))
     + floor(30.6001 × (M + 1))
     + D + B - 1524.5
  JD = 2460676.50000

Result: 2460676.50000`;

export default function VerboseSpotlight(): JSX.Element {
  return (
    <section className="verbose-spotlight">
      <div className="verbose-spotlight__container">
        <div className="verbose-spotlight__text">
          <h2 className="verbose-spotlight__title">
            See the astronomy, not just the answer
          </h2>
          <p className="verbose-spotlight__description">
            Traditional astronomy tools are black boxes. astr0 is different.
            Every calculation can show its work with <code>--verbose</code> mode.
          </p>
          <ul className="verbose-spotlight__features">
            <li>Step-by-step mathematics</li>
            <li>Intermediate values at each stage</li>
            <li>Algorithm references and sources</li>
            <li>Perfect for learning and verification</li>
          </ul>
        </div>

        <div className="verbose-spotlight__comparison">
          <div className="verbose-spotlight__panel">
            <h4 className="verbose-spotlight__panel-title">Standard output</h4>
            <div className="verbose-spotlight__code-wrapper">
              <CodeBlock language="bash">{normalOutput}</CodeBlock>
            </div>
          </div>
          <div className="verbose-spotlight__panel verbose-spotlight__panel--verbose">
            <h4 className="verbose-spotlight__panel-title">With --verbose</h4>
            <div className="verbose-spotlight__code-wrapper">
              <CodeBlock language="bash">{verboseOutput}</CodeBlock>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
