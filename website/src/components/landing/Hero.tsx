import Link from '@docusaurus/Link';
import VantaBackground from './VantaBackground';

const easterEgg = `

    ✦  ·  ˚  ✧  ·  ˚  ✦  ·  ˚  ✧  ·  ˚  ✦

              Per aspera ad astra
           Through hardships to the stars

    ✧  ·  ˚  ✦  ·  ˚  ✧  ·  ˚  ✦  ·  ˚  ✧

`;

export default function Hero(): JSX.Element {
  return (
    <>
      <div dangerouslySetInnerHTML={{ __html: `<!--${easterEgg}-->` }} style={{ display: 'none' }} />
      <section className="hero">
        <VantaBackground />
        <div className="hero__container">
          <h1 className="hero__title">
            Astronomy that shows its work
          </h1>
          <p className="hero__description">
            An educational Python toolkit for astronomical calculations.
            <br />
            CLI and Python API with transparent, step-by-step mathematics.
          </p>
          <div className="hero__buttons">
            <Link className="button button--primary button--lg" to="/docs/intro">
              Get Started
            </Link>
            <Link
              className="button button--secondary button--lg"
              to="https://github.com/oddurs/astr0"
            >
              View on GitHub
            </Link>
          </div>
        </div>
        <div className="hero__terminal">
          <div className="terminal">
            <div className="terminal__header">
              <span className="terminal__dot terminal__dot--red"></span>
              <span className="terminal__dot terminal__dot--yellow"></span>
              <span className="terminal__dot terminal__dot--green"></span>
            </div>
            <pre className="terminal__content">
              <code>
                <span className="terminal__prompt">$</span> astr0 moon phase --verbose{'\n'}
                {'\n'}
                <span className="terminal__comment"># Moon Phase Calculation</span>{'\n'}
                <span className="terminal__label">Julian Date:</span> 2460676.5{'\n'}
                <span className="terminal__label">Days since new moon:</span> 12.4{'\n'}
                <span className="terminal__label">Phase angle:</span> 151.2°{'\n'}
                <span className="terminal__label">Illumination:</span> 93.2%{'\n'}
                {'\n'}
                <span className="terminal__result">Waxing Gibbous</span>
              </code>
            </pre>
          </div>
        </div>
      </section>
    </>
  );
}
