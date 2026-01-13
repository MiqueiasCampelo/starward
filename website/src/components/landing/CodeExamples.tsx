import { useState } from 'react';
import CodeBlock from '@theme/CodeBlock';

type Tab = 'cli' | 'python';

const cliExample = `$ starward sun position --observer "New York"

Sun Position for New York
─────────────────────────
Right Ascension:  19h 42m 15.3s
Declination:      -21° 58' 42"
Altitude:         32.4°
Azimuth:          215.7°
Distance:         0.9838 AU`;

const pythonExample = `from starward import sun, observer

# Set your location
obs = observer.Observer("New York", lat=40.7128, lon=-74.0060)

# Get current sun position
pos = sun.position(observer=obs)

print(f"Altitude: {pos.altitude:.1f}°")
print(f"Azimuth: {pos.azimuth:.1f}°")
# Altitude: 32.4°
# Azimuth: 215.7°`;

export default function CodeExamples(): JSX.Element {
  const [activeTab, setActiveTab] = useState<Tab>('cli');

  return (
    <section className="code-examples">
      <div className="code-examples__container">
        <h2 className="code-examples__title">Two ways to explore the cosmos</h2>
        <p className="code-examples__subtitle">
          Use the CLI for quick calculations or the Python API for integration
        </p>

        <div className="code-examples__tabs">
          <button
            className={`code-examples__tab ${activeTab === 'cli' ? 'code-examples__tab--active' : ''}`}
            onClick={() => setActiveTab('cli')}
          >
            Command Line
          </button>
          <button
            className={`code-examples__tab ${activeTab === 'python' ? 'code-examples__tab--active' : ''}`}
            onClick={() => setActiveTab('python')}
          >
            Python API
          </button>
        </div>

        <div className="code-examples__content">
          {activeTab === 'cli' ? (
            <CodeBlock language="bash">{cliExample}</CodeBlock>
          ) : (
            <CodeBlock language="python">{pythonExample}</CodeBlock>
          )}
        </div>
      </div>
    </section>
  );
}
