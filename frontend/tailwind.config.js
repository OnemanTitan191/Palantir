export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: { cinzel: ["Cinzel", "serif"] },
      colors: {
        stone: {
          bg: "#0d0d0d",
          surface: "#1a1a2e",
          text: "#e8e8f0",
          accent: "#c4963e"
        },
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
}
