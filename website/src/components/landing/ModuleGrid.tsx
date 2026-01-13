import Link from '@docusaurus/Link';

type Module = {
  name: string;
  description: string;
  icon: string;
  link: string;
};

const modules: Module[] = [
  {
    name: 'Time',
    description: 'Julian dates, sidereal time, calendar conversions',
    icon: '⏱️',
    link: '/docs/module-guides/time',
  },
  {
    name: 'Coordinates',
    description: 'ICRS, Galactic, Horizontal transformations',
    icon: '🧭',
    link: '/docs/module-guides/coords',
  },
  {
    name: 'Angles',
    description: 'DMS/HMS parsing, angular separation',
    icon: '📐',
    link: '/docs/module-guides/angles',
  },
  {
    name: 'Sun',
    description: 'Position, rise/set, twilight times',
    icon: '☀️',
    link: '/docs/module-guides/sun',
  },
  {
    name: 'Moon',
    description: 'Phase, illumination, rise/set',
    icon: '🌙',
    link: '/docs/module-guides/moon',
  },
  {
    name: 'Planets',
    description: 'Mercury to Neptune positions and visibility',
    icon: '🪐',
    link: '/docs/module-guides/planets',
  },
  {
    name: 'Observer',
    description: 'Location management with timezone support',
    icon: '📍',
    link: '/docs/module-guides/observer',
  },
  {
    name: 'Visibility',
    description: 'Airmass, transit times, observation planning',
    icon: '🔭',
    link: '/docs/module-guides/visibility',
  },
  {
    name: 'Constants',
    description: '30+ IAU/CODATA constants with uncertainties',
    icon: '📊',
    link: '/docs/module-guides/constants',
  },
];

export default function ModuleGrid(): JSX.Element {
  return (
    <section className="modules">
      <div className="modules__container">
        <h2 className="modules__title">Nine modules for the solar system</h2>
        <p className="modules__subtitle">
          Everything you need for astronomical calculations
        </p>

        <div className="modules__grid">
          {modules.map((mod, idx) => (
            <Link key={idx} className="module-card" to={mod.link}>
              <span className="module-card__icon">{mod.icon}</span>
              <h3 className="module-card__name">{mod.name}</h3>
              <p className="module-card__description">{mod.description}</p>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
