/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: [
    './pages/**/*.{ts,tsx,vue}',
    './components/**/*.{ts,tsx,vue}',
    './app/**/*.{ts,tsx,vue}',
    './src/**/*.{ts,tsx,vue}',
  ],
  prefix: '',
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  plugins: [
    require('tailwindcss-animate'),
    function ({ addBase, addComponents, theme }) {
      // Apply defaults using CSS custom properties
      addComponents({
        // Input elements - use your CSS variables
        '.input, input[type="text"], input[type="email"], input[type="password"], input[type="number"], input[type="search"], input[type="url"], input[type="tel"]':
          {
            backgroundColor: 'hsl(var(--input))',
            borderColor: 'hsl(var(--border))',
            color: 'hsl(var(--foreground))',
            '&::placeholder': {
              color: 'hsl(var(--muted-foreground))',
            },
            '&:focus': {
              borderColor: 'hsl(var(--ring))',
              outline: 'none',
              boxShadow: '0 0 0 1px hsl(var(--ring))',
            },
          },

        // Textarea
        'textarea, .textarea': {
          backgroundColor: 'hsl(var(--input))',
          borderColor: 'hsl(var(--border))',
          color: 'hsl(var(--foreground))',
          resize: 'none',
          '&::placeholder': {
            color: 'hsl(var(--muted-foreground))',
          },
          '&:focus': {
            borderColor: 'hsl(var(--ring))',
            outline: 'none',
            boxShadow: '0 0 0 1px hsl(var(--ring))',
          },
        },

        // Select elements
        'select, .select': {
          backgroundColor: 'hsl(var(--input))',
          borderColor: 'hsl(var(--border))',
          color: 'hsl(var(--foreground))',
          '&:focus': {
            borderColor: 'hsl(var(--ring))',
            outline: 'none',
            boxShadow: '0 0 0 1px hsl(var(--ring))',
          },
        },

        // Button focus styles
        'button, .button': {
          '&:focus-visible': {
            outline: 'none',
            boxShadow: '0 0 0 2px hsl(var(--ring)), 0 0 0 4px hsl(var(--ring) / 0.2)',
          },
        },
      })
    },
  ],
}
