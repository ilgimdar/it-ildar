const [red, green, blue] = [30, 30, 30]
const section1 = document.querySelector('#wrapper')

window.addEventListener('scroll', () => {
  const y = 1 + (window.scrollY || window.pageYOffset) / 4;
  const [r, g, b] = [Math.min(red + y, 230), Math.min(green+y, 230), Math.min(blue+y, 230)].map(Math.round)
  section1.style.backgroundColor = `rgb(${r}, ${g}, ${b})`
})