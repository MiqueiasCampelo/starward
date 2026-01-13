import Layout from '@theme/Layout';
import {
  Hero,
  FeaturePillars,
  CodeExamples,
  ModuleGrid,
  VerboseSpotlight,
  UseCases,
  QuickInstall,
} from '../components/landing';

export default function Home(): JSX.Element {
  return (
    <Layout
      title="Astronomy that shows its work"
      description="Educational Python toolkit for astronomical calculations with CLI and API"
    >
      <main className="landing">
        <Hero />
        <FeaturePillars />
        <CodeExamples />
        <ModuleGrid />
        <VerboseSpotlight />
        <UseCases />
        <QuickInstall />
      </main>
    </Layout>
  );
}
