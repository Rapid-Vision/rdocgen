import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  srcDir: "docs",

  title: "rdocgen",
  description: "rdocgen documentation",

  base: "/rdocgen",

  markdown: {
    lineNumbers: false
  },
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    outline: [2, 4],
    nav: [
      { text: 'Getting started', link: '/getting-started' },
      { text: 'File example', link: '/api/modules/rdocgen/example' },
      { text: 'Project example', link: '/api' }
    ],

    search: {
      provider: 'local'
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Rapid-Vision/rdocgen' }
    ]
  }
})
