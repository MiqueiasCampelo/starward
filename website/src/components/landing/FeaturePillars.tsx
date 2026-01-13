type Pillar = {
  title: string;
  description: string;
  icon: string;
};

const pillars: Pillar[] = [
  {
    title: 'Transparent',
    description:
      'Every calculation explains itself. Use --verbose to see step-by-step mathematics, intermediate values, and algorithm references.',
    icon: '🔍',
  },
  {
    title: 'Precise',
    description:
      '500+ tests validated against authoritative sources: USNO, JPL Horizons, IAU SOFA, and Meeus algorithms.',
    icon: '🎯',
  },
  {
    title: 'Complete',
    description:
      '9 interconnected modules covering time systems, coordinates, the Sun, Moon, planets, and observation planning.',
    icon: '🌌',
  },
];

export default function FeaturePillars(): JSX.Element {
  return (
    <section className="pillars">
      <div className="pillars__container">
        {pillars.map((pillar, idx) => (
          <div key={idx} className="pillar">
            <span className="pillar__icon">{pillar.icon}</span>
            <h3 className="pillar__title">{pillar.title}</h3>
            <p className="pillar__description">{pillar.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
