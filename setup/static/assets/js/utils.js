/* ================================================
   Utils — Visual/UI helpers only
================================================ */

/* --- TOAST --- */
function toast(msg, type = 'success') {
  const container = document.getElementById('toasts')
  if (!container) return
  const icons = { success: '✓', error: '✕', info: 'i' }
  const t = document.createElement('div')
  t.className = `toast ${type}`
  t.innerHTML = `<span class="toast-icon">${icons[type] || '•'}</span><span style="font-size:.85rem">${msg}</span>`
  container.appendChild(t)
  setTimeout(() => { t.classList.add('toast-out'); setTimeout(() => t.remove(), 350) }, 3200)
}

/* --- MODAL --- */
function openModal(id) {
  const el = document.getElementById(id)
  if (el) { el.classList.add('open'); document.body.style.overflow = 'hidden' }
}
function closeModal(id) {
  const el = document.getElementById(id)
  if (el) { el.classList.remove('open'); document.body.style.overflow = '' }
}
document.addEventListener('click', e => {
  if (e.target.classList.contains('overlay')) {
    e.target.classList.remove('open')
    document.body.style.overflow = ''
  }
})

/* --- SCROLL FADE-UP ANIMATIONS --- */
function initFadeUps() {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); obs.unobserve(e.target) } })
  }, { threshold: .12, rootMargin: '0px 0px -40px 0px' })
  document.querySelectorAll('.fade-up').forEach(el => obs.observe(el))
}

/* --- NAV SCROLL EFFECT --- */
function initNavScroll(navId = 'nav') {
  const nav = document.getElementById(navId)
  if (!nav) return
  const toggle = () => nav.classList.toggle('solid', window.scrollY > 40)
  toggle()
  window.addEventListener('scroll', toggle, { passive: true })
}
