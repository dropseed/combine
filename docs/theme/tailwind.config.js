const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  theme: {
    extend: {
      fontFamily: {
        mono: ["JetBrains Mono", ...defaultTheme.fontFamily.mono],
        sans: ["Rubik", ...defaultTheme.fontFamily.sans],
      },
    }
  },
  variants: {
    textDecoration: ['responsive', 'hover', 'focus', 'group-hover'],
  },
  purge: {
    enabled: process.env.NETLIFY == "true" || process.env.PURGE != "",
    content: ["./output/**/*.html", "./output/**/*.js"],
  },
}
