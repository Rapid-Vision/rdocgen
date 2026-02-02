import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  srcDir: "docs",

  title: "rdocgen",
  description: "rdocgen documentation",
  markdown: {
    lineNumbers: false
  },
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    outline: [2, 4],
    nav: [
      { text: 'Home', link: '/getting-started' },
      { text: 'File sample', link: '/api/modules/rdocgen/example' },
      { text: 'Documentation example', link: '/api' }
    ],

    // sidebar: [
    //   {
    //     text: 'Examples',
    //     items: [
    //       { text: 'Markdown Examples', link: '/markdown-examples' },
    //       { text: 'Runtime API Examples', link: '/api-examples' }
    //     ]
    //   }
    // ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Rapid-Vision/rdocgen' }
    ]
  }
})
