type UseCase = {
  title: string;
  description: string;
  icon: string;
};

const useCases: UseCase[] = [
  {
    title: 'Students',
    description:
      'Learn celestial mechanics with calculations that explain themselves. Verbose mode reveals the mathematics behind every result.',
    icon: '🎓',
  },
  {
    title: 'Amateur Astronomers',
    description:
      'Plan your observing sessions. Find rise/set times, optimal viewing windows, and track planets across the sky.',
    icon: '🌟',
  },
  {
    title: 'Educators',
    description:
      'Teach astronomical concepts with a tool that shows its work. Students can see exactly how calculations are performed.',
    icon: '👩‍🏫',
  },
  {
    title: 'Developers',
    description:
      'Integrate astronomy into your applications with a clean Python API. JSON output for easy parsing and automation.',
    icon: '💻',
  },
];

export default function UseCases(): JSX.Element {
  return (
    <section className="use-cases">
      <div className="use-cases__container">
        <h2 className="use-cases__title">Built for curious minds</h2>
        <p className="use-cases__subtitle">
          Whether you're learning, teaching, observing, or building
        </p>

        <div className="use-cases__grid">
          {useCases.map((useCase, idx) => (
            <div key={idx} className="use-case-card">
              <span className="use-case-card__icon">{useCase.icon}</span>
              <h3 className="use-case-card__title">{useCase.title}</h3>
              <p className="use-case-card__description">{useCase.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
