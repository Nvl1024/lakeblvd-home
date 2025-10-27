module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/**/*.py",
    "./app/static/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography")],
}