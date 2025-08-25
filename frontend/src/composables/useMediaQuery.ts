import { useBreakpoints, useMediaQuery as useMediaQueryCore } from '@vueuse/core'
export const useMediaQuery = () => {
  const breakpoints = useBreakpoints({
    xs: 480, // small phones to large phones
    sm: 640, // large phones
    md: 768, // tablets
    lg: 1024, // small desktops
    xl: 1280, // large desktops
    '2xl': 1536,
  })

  const isMobile = breakpoints.smaller('md')
  const isTablet = breakpoints.between('md', 'lg')
  const isDesktop = breakpoints.greaterOrEqual('lg')

  const isMobileQuery = useMediaQueryCore('(max-width: 767px)')

  return {
    isMobile,
    isTablet,
    isDesktop,
    isMobileQuery,
    breakpoints,
  }
}
