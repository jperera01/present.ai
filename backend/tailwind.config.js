/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.{html,j2}"],
  theme: {
    extend: {
      animation: {
        "text-gradient": "text-gradient 2.5s linear infinite",
      },
      keyframes: {
        "text-gradient": {
          "0%": { backgroundPosition: "0% center" },
          "100%": { backgroundPosition: "200% center" },
        },
      },
    },
  },
  plugins: [],
};
