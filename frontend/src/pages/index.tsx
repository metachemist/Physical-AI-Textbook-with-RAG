import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header
      className={clsx('hero hero--primary')}
      style={{textAlign: 'center', padding: '4rem 0'}}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div>
          <Link
            className="button button--secondary button--lg"
            to="/docs/module-1-ros2/week-01-ros2-fundamentals">
            Start Learning
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): React.JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="An AI-native textbook for Physical AI and Humanoid Robotics">
      <HomepageHeader />
      <main style={{padding: '2rem 0', textAlign: 'center'}}>
        <div className="container">
          <h2>Course Modules</h2>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '1.5rem',
              marginTop: '2rem',
            }}>
            <ModuleCard
              title="Module 1: ROS 2 Fundamentals"
              description="Weeks 1-5. Core robotics middleware, Python development, URDF, and integration capstone."
              link="/docs/module-1-ros2/week-01-ros2-fundamentals"
            />
            <ModuleCard
              title="Module 2: Simulation"
              description="Weeks 6-7. Gazebo and Unity simulation environments for robotics development."
              link="/docs/module-2-simulation/week-06-gazebo"
            />
            <ModuleCard
              title="Module 3: NVIDIA Isaac"
              description="Weeks 8-10. Isaac Sim, Isaac ROS, Nav2, and perception pipelines."
              link="/docs/module-3-nvidia-isaac/week-08-isaac-sim"
            />
            <ModuleCard
              title="Module 4: VLA & Humanoid"
              description="Weeks 11-13. Vision-Language-Action models, humanoid platforms, and deployment capstone."
              link="/docs/module-4-vla-humanoid/week-11-vla-foundations"
            />
          </div>
        </div>
      </main>
    </Layout>
  );
}

function ModuleCard({
  title,
  description,
  link,
}: {
  title: string;
  description: string;
  link: string;
}) {
  return (
    <div
      style={{
        border: '1px solid var(--ifm-color-emphasis-300)',
        borderRadius: '8px',
        padding: '1.5rem',
        textAlign: 'left',
      }}>
      <h3>{title}</h3>
      <p>{description}</p>
      <Link to={link}>View module &rarr;</Link>
    </div>
  );
}
