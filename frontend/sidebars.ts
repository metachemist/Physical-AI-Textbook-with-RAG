import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  textbookSidebar: [
    {
      type: 'category',
      label: 'Module 1: ROS 2 Fundamentals',
      items: [
        'module-1-ros2/week-01-ros2-fundamentals',
        'module-1-ros2/week-02-ros2-advanced',
        'module-1-ros2/week-03-ros2-tooling',
        'module-1-ros2/week-04-ros2-navigation',
        'module-1-ros2/week-05-ros2-capstone',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Simulation',
      items: [
        'module-2-simulation/week-06-gazebo',
        'module-2-simulation/week-07-unity',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac',
      items: [
        'module-3-nvidia-isaac/week-08-isaac-sim',
        'module-3-nvidia-isaac/week-09-isaac-ros',
        'module-3-nvidia-isaac/week-10-isaac-perceptor',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: VLA & Humanoid Development',
      items: [
        'module-4-vla-humanoid/week-11-vla-foundations',
        'module-4-vla-humanoid/week-12-humanoid-platforms',
        'module-4-vla-humanoid/week-13-deployment',
      ],
    },
  ],
};

export default sidebars;
