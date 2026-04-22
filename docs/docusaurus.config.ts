import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "Indian Payroll",
  tagline: "Full-stack Indian statutory payroll for ERPNext & HRMS",
  favicon: "img/favicon.ico",

  future: { v4: true },

  url: "https://hybrowlabs.github.io",
  baseUrl: "/ERPNext-India-Payroll/",
  organizationName: "hybrowlabs",
  projectName: "ERPNext-India-Payroll",
  trailingSlash: false,

  onBrokenLinks: "warn",
  onBrokenMarkdownLinks: "warn",

  i18n: { defaultLocale: "en", locales: ["en"] },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          editUrl:
            "https://github.com/hybrowlabs/ERPNext-India-Payroll/edit/main/docs/",
          routeBasePath: "/",
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: "img/social-card.png",
    colorMode: {
      defaultMode: "light",
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: "Indian Payroll",
      logo: {
        alt: "Indian Payroll",
        src: "img/logo.svg",
      },
      hideOnScroll: false,
      items: [
        {
          type: "docSidebar",
          sidebarId: "mainSidebar",
          position: "left",
          label: "Documentation",
        },
        {
          href: "https://github.com/hybrowlabs/ERPNext-India-Payroll",
          position: "right",
          className: "header-github-link",
          "aria-label": "GitHub",
        },
      ],
    },
    footer: {
      style: "light",
      links: [
        {
          title: "Learn",
          items: [
            { label: "Introduction", to: "/" },
            { label: "Installation", to: "/installation" },
            { label: "Payroll Processing", to: "/payroll/processing" },
          ],
        },
        {
          title: "Compliance",
          items: [
            { label: "EPF / EPS / EDLI", to: "/compliance/epf" },
            { label: "ESIC", to: "/compliance/esic" },
            { label: "Income Tax (TDS)", to: "/compliance/tds" },
          ],
        },
        {
          title: "Ecosystem",
          items: [
            { label: "Frappe", href: "https://frappeframework.com/docs" },
            { label: "ERPNext", href: "https://docs.erpnext.com" },
            { label: "HRMS", href: "https://github.com/frappe/hrms" },
          ],
        },
        {
          title: "Project",
          items: [
            {
              label: "GitHub",
              href: "https://github.com/hybrowlabs/ERPNext-India-Payroll",
            },
            {
              label: "Issues",
              href: "https://github.com/hybrowlabs/ERPNext-India-Payroll/issues",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Hybrowlabs Technologies. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.oneLight,
      darkTheme: prismThemes.oneDark,
      additionalLanguages: ["bash", "python", "json"],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
