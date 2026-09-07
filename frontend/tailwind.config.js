/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        hospital: {
          primary: '#1e40af',   // deep blue
          secondary: '#0f766e', // teal
          danger: '#dc2626',    // red
          warning: '#d97706',   // amber
          success: '#16a34a',   // green
          info: '#2563eb',      // blue
          gray: '#6b7280',
        }
      }
    }
  },
  plugins: [require('@tailwindcss/forms')],
}
