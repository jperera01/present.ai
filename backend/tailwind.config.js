/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.{html,j2}"],
  theme: {
    extend: {
      animation: {
        "text-gradient": "text-gradient 2.5s linear infinite",
        "slide-down": "slide-down 0.7s ease-out forwards",
      },
      keyframes: {
        "text-gradient": {
          "0%": { backgroundPosition: "0% center" },
          "100%": { backgroundPosition: "200% center" },
        },
        "slide-down": {
          from: { transform: "translateY(-100%)" },
          to: { transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
