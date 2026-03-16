import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import type {Plugin} from '@docusaurus/types';

function devProxyPlugin(): Plugin {
  return {
    name: 'dev-proxy',
    configureWebpack(_config, isServer) {
      if (isServer) return {};
      return {
        devServer: {
          proxy: [
            {
              context: ['/api/auth'],
              target: 'http://localhost:3001',
              changeOrigin: true,
            },
            {
              context: ['/api'],
              target: 'http://localhost:8000',
              changeOrigin: true,
            },
          ],
        },
      };
    },
  };
}

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An AI-native textbook for Physical AI and Humanoid Robotics',
  favicon: 'img/favicon.ico',

  url: 'https://metachemist.github.io',
  baseUrl: '/physical-ai-textbook-with-rag-01/',
  organizationName: 'metachemist',
  projectName: 'physical-ai-textbook-with-rag-01',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [devProxyPlugin],

  themeConfig: {
    navbar: {
      title: 'Physical AI Textbook',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'textbookSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          href: 'https://github.com/metachemist/physical-ai-textbook-with-rag-01',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'markup'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
