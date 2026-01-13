import Link from '@docusaurus/Link';
import VantaBackground from './VantaBackground';

export default function QuickInstall(): JSX.Element {
  return (
    <section className="quick-install">
      <VantaBackground
        className="vanta-background"
        color={0x0e3a40}
        points={8.0}
        maxDistance={25.0}
        spacing={20.0}
      />
      <div className="quick-install__container">
        <h2 className="quick-install__title">Ready to explore?</h2>
        <p className="quick-install__subtitle">
          Install astr0 with pip and start calculating
        </p>

        <div className="quick-install__command">
          <code>pip install astr0</code>
        </div>

        <p className="quick-install__requirements">
          Requires Python 3.9+
        </p>

        <div className="quick-install__buttons">
          <Link className="button button--primary button--lg" to="/docs/getting-started/installation">
            Installation Guide
          </Link>
          <Link className="button button--secondary button--lg" to="/docs/getting-started/quickstart">
            Quick Start
          </Link>
        </div>
      </div>
    </section>
  );
}
