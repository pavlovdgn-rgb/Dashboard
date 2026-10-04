import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  staticDirs: ['../src/assets'],
  "stories": [
    "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"
  ],
  "addons": [
    "@storybook/addon-a11y",
    "@storybook/addon-docs"
  ],
  "framework": { name: "@storybook/react-vite", options: { strictMode: false } },
  core: { disableTelemetry: true },
  features: { changeDetection: false, sidebarOnboardingChecklist: false, menuOnboardingChecklist: false },
  typescript: { reactDocgen: false }
};
export default config;
